# ============================================================================
# market_report_agent/sub_agents/sector_performance_agent/agent.py
# ============================================================================
"""
SectorPerformanceAgent - Analyzes GICS 11 sector performance using sector ETFs
"""
import yfinance as yf
from datetime import datetime, timedelta
from google.adk.agents import Agent
from utils.constants import GICS_SECTORS

def get_sector_performance() -> dict:
    """
    Fetch performance data for all GICS 11 sectors using sector ETFs.
    
    Returns:
        Dictionary with sector performance data, leaders, and laggards
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)  # Today's performance
    
    sector_data = {}
    
    for sector_name, etf_ticker in GICS_SECTORS.items():
        try:
            etf = yf.Ticker(etf_ticker)
            hist = etf.history(start=start_date, end=end_date)
            
            if hist.empty or len(hist) < 2:
                sector_data[sector_name] = {"error": "Insufficient data"}
                continue
            
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            
            day_change = current_price - prev_close
            day_change_pct = (day_change / prev_close) * 100
            
            sector_data[sector_name] = {
                "etf": etf_ticker,
                "current_price": round(current_price, 2),
                "day_change": round(day_change, 2),
                "day_change_pct": round(day_change_pct, 2),
                "volume": int(hist['Volume'].iloc[-1])
            }
            
        except Exception as e:
            sector_data[sector_name] = {"error": str(e)}
    
    # Sort sectors by performance
    valid_sectors = {k: v for k, v in sector_data.items() if "error" not in v}
    sorted_sectors = sorted(
        valid_sectors.items(),
        key=lambda x: x[1]['day_change_pct'],
        reverse=True
    )
    
    # Get top 2 leaders and bottom 2 laggards
    leaders = sorted_sectors[:2] if len(sorted_sectors) >= 2 else sorted_sectors
    laggards = sorted_sectors[-2:] if len(sorted_sectors) >= 2 else []
    
    return {
        "all_sectors": sector_data,
        "leaders": dict(leaders),
        "laggards": dict(laggards),
        "analysis_date": end_date.strftime("%Y-%m-%d")
    }

# Create the SectorPerformanceAgent
sector_performance_agent = Agent(
    model="gemini-2.0-flash-exp",
    system_instruction="""You are a Sector Performance Agent specializing in market sector analysis.

Your role:
- Analyze the GICS 11 sectors using sector ETF performance
- Identify the top 2 performing sectors (leaders)
- Identify the bottom 2 performing sectors (laggards)
- Provide market context and rotation insights

When presenting sector analysis:
- Clearly highlight the leaders and laggards
- Explain what's driving sector movements (if patterns are evident)
- Note any sector rotation trends
- Keep analysis focused on actionable insights

Format your response as a concise sector performance report with clear sections for leaders and laggards.""",
    functions=[get_sector_performance]
)