# ============================================================================
# market_report_agent/tools/report_tools.py
# ============================================================================
"""Report generation tool that orchestrates sub-agents"""

from typing import Dict, Any


async def generate_report(
    session_state: dict
) -> Dict[str, Any]:
    """
    Generate a comprehensive market report.
    
    This is a simplified version that returns the structure.
    The actual orchestration of sub-agents happens via the main agent's LLM
    using the AgentTools we've provided.
    
    Args:
        session_state: Current session state containing portfolio
        
    Returns:
        Dictionary with report structure
    """
    portfolio = session_state.get("portfolio", [])
    
    if not portfolio:
        return {
            "success": False,
            "message": "Cannot generate report: Portfolio is empty. Please add tickers first.",
            "report": None
        }
    
    # The agent's LLM will handle calling the sub-agents through AgentTools
    # This function just validates and structures the request
    return {
        "success": True,
        "portfolio": portfolio,
        "message": f"Ready to generate report for {len(portfolio)} ticker(s). The agent will now call the price_update_agent, sector_performance_agent, and market_news_agent to gather data.",
        "instructions": "Call the three sub-agents (price_update_agent, sector_performance_agent, market_news_agent) and synthesize their outputs into a comprehensive market report."
    }