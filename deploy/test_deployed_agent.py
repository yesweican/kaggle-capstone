# ============================================================================
# deploy/test_deployed_agent.py (optional)
# ============================================================================
"""
Test script for deployed MarketReportAgent on Vertex AI Agent Engine
"""

import os
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from market_report_agent import market_report_agent

async def test_deployed_agent():
    """Test the deployed agent with sample queries."""
    
    # Configuration for deployed agent
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    agent_id = "market-report-agent"
    
    if not project_id:
        print("❌ Error: GOOGLE_CLOUD_PROJECT environment variable not set")
        return
    
    print(f"🧪 Testing deployed agent...")
    print(f"   Project: {project_id}")
    print(f"   Location: {location}")
    print(f"   Agent: {agent_id}")
    print("=" * 70)
    
    # Create session service (using in-memory for testing)
    session_service = DatabaseSessionService(db_path=":memory:")
    
    # Create runner
    runner = Runner(
        agent=market_report_agent,
        app_name=agent_id,
        session_service=session_service
    )
    
    # Test queries
    test_queries = [
        "Add AAPL to my portfolio",
        "Add GOOGL and MSFT to my portfolio",
        "List my portfolio",
        "Generate a market report"
    ]
    
    session_id = "test_session_001"
    user_id = "test_user"
    
    for query in test_queries:
        print(f"\n💬 Query: {query}")
        print("-" * 70)
        
        try:
            response = await runner.run(
                user_id=user_id,
                session_id=session_id,
                message=query
            )
            
            print(f"✅ Response: {response}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 70)
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    asyncio.run(test_deployed_agent())

