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
    # Fetch more days to ensure we have enough trading days
    start_date = end_date - timedelta(days=14)  # 14 days to cover weekends/holidays
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            
            # Drop any NaN values (shouldn't happen with yfinance, but just in case)
            hist = hist.dropna()
            
            if hist.empty:
                results[ticker] = {"error": "No data available"}
                continue
            
            # Ensure we have at least 2 trading days
            if len(hist) < 2:
                results[ticker] = {"error": "Insufficient trading data"}
                continue
            
            # Most recent trading day (could be today or last Friday if weekend)
            current_price = hist['Close'].iloc[-1]
            current_date = hist.index[-1]
            
            # Previous trading day (handles weekends and holidays automatically)
            prev_close = hist['Close'].iloc[-2]
            prev_date = hist.index[-2]
            
            # Week ago data (or closest trading day)
            week_ago_idx = max(0, len(hist) - 6)  # Approximate 5 trading days
            week_open = hist['Close'].iloc[week_ago_idx]
            
            # Calculate metrics
            day_change = current_price - prev_close
            day_change_pct = (day_change / prev_close) * 100
            week_change = current_price - week_open
            week_change_pct = (week_change / week_open) * 100
            
            results[ticker] = {
                "symbol": ticker,
                "current_price": round(current_price, 2),
                "current_date": current_date.strftime("%Y-%m-%d"),
                "day_change": round(day_change, 2),
                "day_change_pct": round(day_change_pct, 2),
                "prev_close_date": prev_date.strftime("%Y-%m-%d"),
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
    name="price_update_agent",
    model="gemini-2.0-flash",
    tools=[get_price_updates],
    instruction="""You are a Price Update Agent specializing in stock price analysis.

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

Format your response as a clear, structured price update report."""
)