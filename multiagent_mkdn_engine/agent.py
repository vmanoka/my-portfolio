# Import necessary classes and functions from the ADK and other libraries.
from google.adk.agents import Agent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from tools import get_inventory_data, execute_markdown

# Define the Analyst Agent
# This agent is responsible for identifying slow-moving inventory.
analyst_agent = Agent(
    model='gemini-1.5-flash',  # Specifies the language model to be used by the agent.
    name='analyst_agent',  # A unique name for the agent.
    instruction="""
    # Role
    You are a data analyst with a knack for identifying slow moving inventory.

    # Instructions
    1. Use the get_inventory_data tool to load the current inventory.
    2. Identify slow moving inventory.
    """,
    tools=[get_inventory_data],  # The list of tools available to this agent.
)

# Define the Pricing Strategist Agent
# This agent determines the markdown strategy for inventory flagged by the Analyst Agent.
pricing_strategist = Agent(
    name="Pricing_Strategist",  # A unique name for the agent.
    model='gemini-1.5-flash',  # Specifies the language model.
    instruction="""
    remaining_markdown_budget={current_markdown_budget?} # Accesses the markdown budget from the state.

    1. Review the 'flagged_inventory' in the State variables provided by the Analyst agent.
    2. For each flagged item, read the `recent_reviews` column.
    3. NORMAL MARKDOWN: If the reviews are positive or neutral but the item is just selling slowly, calculate a standard 20% markdown on the current `price`.
    4. DEFECT MARKDOWN: If the `recent_reviews` indicate a persistent issue (like poor sizing, bad quality, or defects), a standard markdown won't work. Apply a deep 40% clearance markdown to aggressively get rid of the bad stock.
    5. CRITICAL RULE: The new price must NEVER be lower than the `cost`. If a 40% markdown drops it below cost, price it exactly at cost.
    6. Check the 'remaining_markdown_budget' in the State. If the total markdown cost exceeds this budget, you must stop.
    7. Use the `execute_markdown` tool to apply the price change and log the exact reasoning (including the review sentiment) to the 'actions_log' State variable.
    """,
    tools=[execute_markdown],  # The list of tools available to this agent.
)

# Define the Root Orchestrator using a SequentialAgent
# This agent orchestrates the workflow by running the sub-agents in a specific order.
markdown_engine = SequentialAgent(
    name="Markdown_Engine",  # A unique name for the orchestrator agent.
    description='A sequential execution agent that runs analyst agent first and strategist agent next',
    sub_agents=[analyst_agent, pricing_strategist],  # Defines the order of execution for the sub-agents.
)

# Set the markdown_engine as the root agent for execution.
root_agent = markdown_engine
