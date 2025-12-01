# ============================================================================
# deploy/test_deployed_agent.py
# ============================================================================
"""
Test script for deployed MarketReportAgent
"""

import os
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from market_report_agent import market_report_agent

async def test_deployed_agent():
    """Test the deployed agent with sample queries."""
    
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
    
    # Create session service
    db_url = "sqlite+aiosqlite:///:memory:"
    session_service = DatabaseSessionService(db_url=db_url)
    
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
            # Create Content object
            content = types.Content(role='user', parts=[types.Part(text=query)])
            
            # Run the agent
            events = runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            )
            
            # Get final response
            final_response = None
            for event in events:
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    break
            
            if final_response:
                print(f"✅ Response: {final_response}")
            else:
                print("⚠️ No final response received")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 70)
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    asyncio.run(test_deployed_agent())

