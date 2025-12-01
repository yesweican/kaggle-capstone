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
    # Fetch more days to ensure we have enough trading days
    start_date = end_date - timedelta(days=7)
    
    sector_data = {}
    
    for sector_name, etf_ticker in GICS_SECTORS.items():
        try:
            etf = yf.Ticker(etf_ticker)
            hist = etf.history(start=start_date, end=end_date)
            
            # Drop any NaN values
            hist = hist.dropna()
            
            if hist.empty or len(hist) < 2:
                sector_data[sector_name] = {"error": "Insufficient data"}
                continue
            
            # Most recent trading day
            current_price = hist['Close'].iloc[-1]
            current_date = hist.index[-1]
            
            # Previous trading day (handles weekends and holidays)
            prev_close = hist['Close'].iloc[-2]
            prev_date = hist.index[-2]
            
            day_change = current_price - prev_close
            day_change_pct = (day_change / prev_close) * 100
            
            sector_data[sector_name] = {
                "etf": etf_ticker,
                "current_price": round(current_price, 2),
                "current_date": current_date.strftime("%Y-%m-%d"),
                "day_change": round(day_change, 2),
                "day_change_pct": round(day_change_pct, 2),
                "prev_close_date": prev_date.strftime("%Y-%m-%d"),
                "volume": int(hist['Volume'].iloc[-1])
            }
            
        except Exception as e:
            sector_data[sector_name] = {"error": str(e)}
    
    # Sort sectors by performance
    valid_sectors = {k: v for k, v in sector_data.items() if "error" not in v}
    
    if not valid_sectors:
        return {
            "all_sectors": sector_data,
            "leaders": {},
            "laggards": {},
            "error": "No valid sector data available",
            "analysis_date": end_date.strftime("%Y-%m-%d")
        }
    
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
        "analysis_date": end_date.strftime("%Y-%m-%d"),
        "trading_date": valid_sectors[list(valid_sectors.keys())[0]]["current_date"]
    }

# Create the SectorPerformanceAgent
sector_performance_agent = Agent(
    name="sector_performance_agent",
    model="gemini-2.0-flash",
    tools=[get_sector_performance],
    instruction="""You are a Sector Performance Agent specializing in market sector analysis.

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
)