# ============================================================================
# market_report_agent/sub_agents/price_update_agent/agent.py
# ============================================================================
"""
PriceUpdateAgent - Analyzes price movements for portfolio tickers using yfinance
"""
import yfinance as yf
from datetime import datetime, timedelta
from google.adk.agents import Agent

def get_price_updates(tickers: list[str]) -> dict:
    """
    Fetch price data for given tickers and analyze their performance.
    
    Args:
        tickers: List of stock ticker symbols
        
    Returns:
        Dictionary with price data and performance metrics
    """
    if not tickers:
        return {"error": "No tickers provided"}
    
    results = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # Last 7 days for context
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            
            if hist.empty:
                results[ticker] = {"error": "No data available"}
                continue
            
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            week_open = hist['Close'].iloc[0]
            
            # Calculate metrics
            day_change = current_price - prev_close
            day_change_pct = (day_change / prev_close) * 100
            week_change = current_price - week_open
            week_change_pct = (week_change / week_open) * 100
            
            results[ticker] = {
                "symbol": ticker,
                "current_price": round(current_price, 2),
                "day_change": round(day_change, 2),
                "day_change_pct": round(day_change_pct, 2),
                "week_change": round(week_change, 2),
                "week_change_pct": round(week_change_pct, 2),
                "volume": int(hist['Volume'].iloc[-1]),
                "high_52w": round(stock.info.get('fiftyTwoWeekHigh', 0), 2),
                "low_52w": round(stock.info.get('fiftyTwoWeekLow', 0), 2),
            }
            
        except Exception as e:
            results[ticker] = {"error": str(e)}
    
    return results

# Create the PriceUpdateAgent
price_update_agent = Agent(
    model="gemini-2.0-flash-exp",
    system_instruction="""You are a Price Update Agent specializing in stock price analysis.

Your role:
- Analyze current price data for provided stock tickers
- Calculate daily and weekly performance metrics
- Highlight significant price movements
- Provide context with 52-week highs/lows

When presenting price updates:
- Lead with the most significant movers (biggest % changes)
- Mention both gains and losses
- Include volume context if unusual
- Keep analysis concise and data-driven

Format your response as a clear, structured price update report.""",
    functions=[get_price_updates]
)