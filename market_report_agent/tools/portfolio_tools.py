# ============================================================================
# market_report_agent/tools/portfolio_tools.py
# ============================================================================
"""Portfolio management tools for adding, deleting, and listing tickers"""

from typing import List

def add_ticker(session_state: dict, ticker: str) -> dict:
    """
    Add a ticker to the portfolio.
    
    Args:
        session_state: Current session state containing portfolio
        ticker: Stock ticker symbol to add
        
    Returns:
        Dictionary with operation result
    """
    ticker = ticker.upper().strip()
    
    # Initialize portfolio if it doesn't exist
    if "portfolio" not in session_state:
        session_state["portfolio"] = []
    
    portfolio = session_state["portfolio"]
    
    # Check if ticker already exists
    if ticker in portfolio:
        return {
            "success": False,
            "message": f"{ticker} is already in your portfolio",
            "portfolio": portfolio
        }
    
    # Add ticker
    portfolio.append(ticker)
    session_state["portfolio"] = portfolio
    
    return {
        "success": True,
        "message": f"Added {ticker} to your portfolio",
        "portfolio": portfolio
    }


def delete_ticker(session_state: dict, ticker: str) -> dict:
    """
    Remove a ticker from the portfolio.
    
    Args:
        session_state: Current session state containing portfolio
        ticker: Stock ticker symbol to remove
        
    Returns:
        Dictionary with operation result
    """
    ticker = ticker.upper().strip()
    
    # Check if portfolio exists
    if "portfolio" not in session_state or not session_state["portfolio"]:
        return {
            "success": False,
            "message": "Your portfolio is empty",
            "portfolio": []
        }
    
    portfolio = session_state["portfolio"]
    
    # Check if ticker exists in portfolio
    if ticker not in portfolio:
        return {
            "success": False,
            "message": f"{ticker} is not in your portfolio",
            "portfolio": portfolio
        }
    
    # Remove ticker
    portfolio.remove(ticker)
    session_state["portfolio"] = portfolio
    
    return {
        "success": True,
        "message": f"Removed {ticker} from your portfolio",
        "portfolio": portfolio
    }


def list_tickers(session_state: dict) -> dict:
    """
    List all tickers in the portfolio.
    
    Args:
        session_state: Current session state containing portfolio
        
    Returns:
        Dictionary with portfolio tickers
    """
    portfolio = session_state.get("portfolio", [])
    
    if not portfolio:
        return {
            "success": True,
            "message": "Your portfolio is empty",
            "portfolio": [],
            "count": 0
        }
    
    return {
        "success": True,
        "message": f"You have {len(portfolio)} ticker(s) in your portfolio",
        "portfolio": portfolio,
        "count": len(portfolio)
    }