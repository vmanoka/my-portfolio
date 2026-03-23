# Import the pandas library for data manipulation, especially for reading CSV files.
import pandas as pd

# Import typing for type hints to improve code readability and maintainability.
from typing import Dict, Any

# Import ToolContext from the ADK to access the agent's state.
from google.adk.tools import ToolContext

def get_inventory_data(tool_context: ToolContext, filepath: str = "inventory.csv") -> Dict[str, Any]:
    """
    Reads inventory data from a CSV file.

    Args:
        tool_context: The context object for the tool, providing access to agent state.
        filepath: The path to the inventory CSV file. Defaults to "inventory.csv".

    Returns:
        A dictionary containing the status of the operation and the inventory data
        as a JSON string if successful. In case of an error, it returns an error message.
    """
    try:
        # Read the specified CSV file into a pandas DataFrame.
        df = pd.read_csv(filepath)
        # Return a dictionary indicating success and the inventory data.
        # The DataFrame is converted to a JSON string with records orientation
        # (a list of dictionaries, where each dictionary represents a row).
        return {
            "status": "SUCCESS",
            "inventory_data": df.to_json(orient="records"),
        }
        
    except Exception as e:
        # If an error occurs during file reading (e.g., file not found),
        # return a string with an error message.
        return f"Error reading database: {str(e)}"

def execute_markdown(tool_context: ToolContext, sku: str, new_price: float, markdown_cost: float) -> Dict[str, Any]:
    """
    {inventory_data?}
    Modifies the price of a specific SKU by applying a markdown.
    It checks if the markdown cost is within the available budget before applying it.

    Args:
        tool_context: The context object for the tool, used to access and update the markdown budget.
        sku: The Stock Keeping Unit (SKU) of the item to be marked down.
        new_price: The new price after applying the markdown.
        markdown_cost: The cost of the markdown for this item.

    Returns:
        A dictionary containing the status of the operation. If successful, it includes
        a confirmation action message and the updated remaining markdown budget.
        If it fails (due to budget constraints), it includes a reason for the failure.
    """
    # Retrieve the current markdown budget from the agent's state.
    current_budget = tool_context.state.get("remaining_markdown_budget")

    # Check if the cost of the proposed markdown exceeds the current budget.
    if markdown_cost > current_budget:
        # If the budget is insufficient, return a failure status and reason.
        return {"status": "FAILED", "reason": "Markdown exceeds remaining daily budget."}
        
    # If the budget is sufficient, subtract the markdown cost to update the budget.
    tool_context.state["remaining_markdown_budget"] = current_budget - markdown_cost
    
    # Return a success status, a log of the action taken, and the new remaining budget.
    return {
        "status": "SUCCESS", 
        "action": f"Price updated to ${new_price} for {sku}",
        "remaining_markdown_budget": tool_context.state["remaining_markdown_budget"]
    }
