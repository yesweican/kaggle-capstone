# ============================================================================
# main.py - Runner Setup
# ============================================================================
import os
import asyncio
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from market_report_agent import market_report_agent

# Load environment variables
load_dotenv()

async def main():
    """Main entry point for MarketReportAgent runner."""

    # Load environment variables
    load_dotenv()
    
    # Database URL for SQLite with async driver (aiosqlite)
    db_url = "sqlite+aiosqlite:///./data/sessions.db"

    # Initialize session service with SQLite database
    session_service = DatabaseSessionService(
        db_url=db_url,
        # The session service will create the database if it doesn't exist
    )

    user_id="user_001"
    session_id = "user_portfolio_session_001"
    
    # Define app name for the runner
    APP_NAME = market_report_agent.name
    
    # Create Runner to orchestrate agent and session service
    runner = Runner(
        agent=market_report_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Note: No Client parameter needed! 
    # Authentication is handled through environment variables (GOOGLE_API_KEY)
    # or through the agent's model configuration
    
    print("🚀 MarketReportAgent Starting...")
    print("=" * 60)
    
    # Example: Start a new session ????
    session = await session_service.create_session(
       app_name=APP_NAME,
       user_id=user_id,
       session_id=session_id
    )
    
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

        # Create a types.Content object, specifying the role and including the part
        content_object = types.Content(
            role='user',  # Or 'model' if it's an AI response
            parts=[types.Part(text=query)]
        )
        
        try:

            # Run the agent with the query using Runner
            events = runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=content_object
            )

            Response = None
            # Process events to get the final response
            for event in events:
                if event.is_final_response():
                    response = event.content.parts[0].text
                    print(f"🤖 Agent: {response}")
                    break
            print("-" * 60)
            
            print(f"🤖 Agent: {response}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("-" * 60)
            traceback.print_exc()
    
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
    
    # Setup
    load_dotenv()
    db_url = "sqlite+aiosqlite:///./data/sessions.db"
    session_service = DatabaseSessionService(db_url=db_url)
    
    APP_NAME = market_report_agent.name
    
    # Create Runner
    runner = Runner(
        agent=market_report_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    session_id = "interactive_session"
    user_id = "user_interactive"

    # Example: Start a new session ????
    session = await session_service.create_session(
       app_name=APP_NAME,
       user_id=user_id,
       session_id=session_id
    )
    
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

            # Create a types.Content object, specifying the role and including the part
            content_object = types.Content(
                role='user',  # Or 'model' if it's an AI response
                parts=[types.Part(text=user_input)]
            )

            # Run the agent
            events = runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=content_object
            )
            
            Response = None
            # Process events to get the final response
            for event in events:
                if event.is_final_response():
                    response = event.content.parts[0].text
                    print(f"\n🤖 Agent: {response}")
                    break
            
            print(f"\n🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            traceback.print_exc()

# To run interactive mode:
# asyncio.run(interactive_runner())