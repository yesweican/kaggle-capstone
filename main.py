# ============================================================================
# main.py - Runner Setup
# ============================================================================
import os
import asyncio
from dotenv import load_dotenv
from google.genai import Client
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from market_report_agent.agent import market_report_agent

# Load environment variables
load_dotenv()

async def main():
    """Main entry point for MarketReportAgent runner."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize session service with SQLite database
    session_service = DatabaseSessionService(
        db_path="data/sessions.db",
        # The session service will create the database if it doesn't exist
    )

    # Define app name for the runner
    APP_NAME = "market_report_agent"
    
    # Create Runner to orchestrate agent and session service
    runner = Runner(
        agent=market_report_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    # Authentication is handled through environment variables (GOOGLE_API_KEY)
    # or GOOGLE_CLOUD_PROJECT + GOOGLE_CLOUD_LOCATION
    # or through the agent's model configuration
    
    print("🚀 MarketReportAgent Starting...")
    print("=" * 60)
    
       
    # Example: Start a new session
    session_id = "user_portfolio_session_001"
    
    print(f"📊 Session ID: {session_id}")
    print("=" * 60)
    
    # Example interactions
    queries = [
        "Add AAPL to my portfolio",
        "Add MSFT and GOOGL to my portfolio",
        "List my current portfolio",
        "Generate a market report for my portfolio",
    ]
    
    for query in queries:
        print(f"\n💬 User: {query}")
        print("-" * 60)
        
        try:
            # Run the agent with the query
            response = await root_agent.run(
                user_id="user_001",
                session_id=session_id,
                message=query
            )
            
            print(f"🤖 Agent: {response}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("-" * 60)
    
    print("\n✅ MarketReportAgent Session Complete")

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Run the async main function
    asyncio.run(main())


# ============================================================================
# Alternative: Interactive Runner
# ============================================================================
async def interactive_runner():
    """Interactive CLI for MarketReportAgent."""
    
    # Setup (same as main)
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    client = Client(api_key=api_key)
    session_service = DatabaseSessionService(db_path="data/sessions.db")
    
    root_agent = create_market_report_agent(client, session_service)
    
    session_id = "interactive_session"
    user_id = "user_interactive"
    
    print("🚀 MarketReportAgent Interactive Mode")
    print("=" * 60)
    print("Commands:")
    print("  - Add tickers: 'Add AAPL to my portfolio'")
    print("  - Remove tickers: 'Delete MSFT from my portfolio'")
    print("  - List portfolio: 'List my tickers'")
    print("  - Generate report: 'Generate a market report'")
    print("  - Exit: 'quit' or 'exit'")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = await root_agent.run(
                user_id=user_id,
                session_id=session_id,
                message=user_input
            )
            
            print(f"\n🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")