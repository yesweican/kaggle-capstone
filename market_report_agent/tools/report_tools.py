# ============================================================================
# market_report_agent/tools/report_tools.py
# ============================================================================
"""Report generation tool that orchestrates sub-agents"""

from typing import Dict, Any


async def generate_report(
    session_state: dict,
    price_agent,
    sector_agent,
    news_agent
) -> Dict[str, Any]:
    """
    Generate a comprehensive market report by orchestrating sub-agents.
    
    Args:
        session_state: Current session state containing portfolio
        price_agent: PriceUpdateAgent instance
        sector_agent: SectorPerformanceAgent instance
        news_agent: MarketNewsAgent instance
        
    Returns:
        Dictionary containing aggregated report data
    """
    portfolio = session_state.get("portfolio", [])
    
    if not portfolio:
        return {
            "success": False,
            "message": "Cannot generate report: Portfolio is empty. Please add tickers first.",
            "report": None
        }
    
    report_sections = {}
    
    # 1. Get price updates for portfolio
    try:
        price_response = await price_agent.run(
            message=f"Analyze price updates for these tickers: {', '.join(portfolio)}"
        )
        report_sections["price_updates"] = price_response
    except Exception as e:
        report_sections["price_updates"] = f"Error fetching price updates: {str(e)}"
    
    # 2. Get sector performance (independent of portfolio)
    try:
        sector_response = await sector_agent.run(
            message="Analyze current sector performance and identify leaders and laggards"
        )
        report_sections["sector_performance"] = sector_response
    except Exception as e:
        report_sections["sector_performance"] = f"Error fetching sector performance: {str(e)}"
    
    # 3. Get market news (portfolio-specific + general)
    try:
        news_response = await news_agent.run(
            message=f"Search for news related to these tickers: {', '.join(portfolio)}, and also gather general market news"
        )
        report_sections["market_news"] = news_response
    except Exception as e:
        report_sections["market_news"] = f"Error fetching market news: {str(e)}"
    
    return {
        "success": True,
        "portfolio": portfolio,
        "report_sections": report_sections,
        "message": "Market report generated successfully"
    }