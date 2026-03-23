# Import necessary libraries
import os
import asyncio
from agent import root_agent  # Import the main agent from the 'agent.py' file
from google.adk.agents import Agent
from google.genai import types as genai_types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# --- Configure Vertex AI Environment Variables ---
# This section sets up the connection to Google Cloud's Vertex AI.
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"  # Instructs the SDK to use Vertex AI
os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project" # <-- Replace with your GCP Project ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"    # <-- Replace with your desired GCP Region

# Define the main asynchronous function that will run the agent application.
async def main():
    # --- 2. Setup Application Variables & Services ---
    # These variables define the context for the agent's run.
    app_name = "margin_app"
    user_id = "user_123"
    session_id = "conversation_123"

    # Create a dedicated session manager that stores conversation history in memory.
    # This is useful for development and testing but is not persistent.
    session_service = InMemorySessionService()

    # --- 3. Create the Runner ---
    # The Runner is responsible for executing the agent with the user's input.
    # We attach our session service to it to manage the conversation state.
    runner = Runner(
        agent=root_agent,  # The main agent to be executed
        app_name=app_name,
        session_service=session_service
    )
    print("Created standard Runner with InMemorySessionService.")

    # --- 4. EXPLICITLY CREATE THE SESSION ---
    # This step is crucial for pre-populating the agent's state before it runs.
    # Define the initial state of the session with necessary variables.
    initiate_state = {"inventory_data": '', "flagged_inventory": '', "remaining_markdown_budget": 10000}

    # Create a new session with the specified app name, user, session ID, and initial state.
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state=initiate_state
    )
    print(f"Successfully created session: {session.id}")

    # --- 5. Create the user's message ---
    # This is the initial prompt or question from the user that kicks off the agent's task.
    user_message = genai_types.Content(
        role="user", parts=[genai_types.Part(text="current markdown budget is $10000")]
    )
    print(f"Prepared user message: {user_message.parts[0].text}")

    # --- 6. Run the agent ---
    print("\nRunning the agent...")
    # Use the async runner method to execute the agent with the user's message.
    # This returns an asynchronous stream of events.
    event_stream = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    )

    # Process the asynchronous results (Events) as they come in.
    async for event in event_stream:
        # Get the author of the event (e.g., 'user', 'agent', 'tool').
        author = getattr(event, 'author', 'System')

        # We only want to print the final responses from the agent to the user,
        # not the internal thoughts or tool calls.
        if event.is_final_response() and event.content and event.content.parts:
             print(f"  -> {author} says: {event.content.parts[0].text}")

# This is the standard entry point for a Python script.
if __name__ == "__main__":
    print("🚀 Starting the script...")
    # Run the main asynchronous function.
    asyncio.run(main())
    print("🏁 Script has finished.")
