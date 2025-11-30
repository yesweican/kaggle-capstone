# ============================================================================
# market_report_agent/agent.py
# ============================================================================
"""Root MarketReportAgent that manages portfolio and generates reports"""

from google.adk.agents import Agent, AgentTool
from .tools.portfolio_tools import add_ticker, delete_ticker, list_tickers
from .tools.report_tools import generate_report
from .sub_agents import (
    price_update_agent,
    sector_performance_agent,
    market_news_agent
)

# Wrap sub-agents as AgentTools
price_agent_tool = AgentTool(
    agent=price_update_agent,
    name="price_update_agent",
    description="Analyzes current price data and performance metrics for portfolio tickers using yfinance"
)

sector_agent_tool = AgentTool(
    agent=sector_performance_agent,
    name="sector_performance_agent",
    description="Analyzes GICS 11 sector performance and identifies market leaders and laggards"
)

news_agent_tool = AgentTool(
    agent=market_news_agent,
    name="market_news_agent",
    description="Searches for portfolio-specific and general market news"
)

# Portfolio management functions with session state access
def add_ticker_wrapper(ticker: str) -> dict:
    """Add a ticker to the portfolio."""
    # Note: Session state access will be handled at runtime through agent context
    session_state = market_report_agent.get_session_state()
    result = add_ticker(session_state, ticker)
    market_report_agent.save_session_state(session_state)
    return result

def delete_ticker_wrapper(ticker: str) -> dict:
    """Remove a ticker from the portfolio."""
    session_state = market_report_agent.get_session_state()
    result = delete_ticker(session_state, ticker)
    market_report_agent.save_session_state(session_state)
    return result

def list_tickers_wrapper() -> dict:
    """List all tickers in the portfolio."""
    session_state = market_report_agent.get_session_state()
    return list_tickers(session_state)

async def generate_report_wrapper() -> dict:
    """Generate a comprehensive market report."""
    session_state = market_report_agent.get_session_state()
    return await generate_report(
        session_state,
        price_update_agent,
        sector_performance_agent,
        market_news_agent
    )

# Create the root agent
market_report_agent = Agent(
    model="gemini-2.0-flash-exp",
    tools=[price_agent_tool, sector_agent_tool, news_agent_tool],
    functions=[
        add_ticker_wrapper,
        delete_ticker_wrapper,
        list_tickers_wrapper,
        generate_report_wrapper
    ],
    system_instruction="""You are the MarketReportAgent, a sophisticated portfolio management and market analysis assistant.

Your capabilities:
1. Portfolio Management:
   - Add tickers to the user's portfolio
   - Remove tickers from the portfolio
   - List current portfolio holdings

2. Market Report Generation:
   - Generate comprehensive market reports by coordinating with three specialized sub-agents:
     * PriceUpdateAgent: Provides price analysis for portfolio tickers
     * SectorPerformanceAgent: Analyzes GICS 11 sectors (leaders/laggards)
     * MarketNewsAgent: Gathers portfolio-specific and general market news
   - Synthesize insights from all sub-agents into a cohesive narrative

Your communication style:
- Professional yet approachable
- Data-driven with clear insights
- Concise but comprehensive
- Highlight key takeaways and actionable information

When generating reports:
1. First ensure the portfolio is not empty
2. Coordinate with all three sub-agents
3. Synthesize their outputs into a unified market report with:
   - Executive summary of key findings
   - Portfolio performance highlights
   - Sector trends and market context
   - Relevant news and its potential impact
4. Provide clear, actionable insights

Always confirm successful operations and provide helpful feedback to users."""
)