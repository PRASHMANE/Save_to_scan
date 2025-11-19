# The core logic of a LangGraph agent implemented in Python.
# This structure defines the state, nodes, and conditional edges
# for the ReAct (Reasoning and Acting) loop.

from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END, START

# --- 1. Define the Agent State (The data passed through the graph) ---

class AgentState(TypedDict):
    """
    Represents the state of the graph. This is the 'memory' that gets passed
    between nodes in the graph flow.
    """
    user_query: str                  # The original user request (e.g., "Find hospitals near me")
    tool_input: str                  # Input arguments for the next tool call (e.g., location data)
    tool_name: str                   # Name of the tool to be executed (e.g., "HospitalFinder")
    tool_output: List[dict]          # Output from the executed tool (e.g., list of hospital dicts)
    final_answer: str                # The final, formatted response to the user
    run_history: Annotated[List[str], operator.add] # Log of steps taken for debugging/tracing

# --- 2. Define the Agent Tools (Functions the agent can execute) ---

# In a real application, these would use external libraries (e.g., Google Maps Places API).
# Here, they are simulated for logic demonstration.

def get_user_location_tool(query: str) -> dict:
    """
    Simulated tool to determine the user's location based on context or request.
    In a real app, this would use the browser's geolocation or a lookup service.
    """
    print("--- Tool Called: get_user_location_tool ---")
    # Simulation: Assume we successfully found a location.
    if "near me" in query.lower():
        location_data = {"lat": 34.0522, "lon": -118.2437, "city": "Los Angeles"}
        return location_data
    return {"error": "Location could not be determined."}

def search_hospitals_tool(location_data: dict) -> List[dict]:
    """
    Simulated tool to search for hospitals near the provided location.
    """
    print("--- Tool Called: search_hospitals_tool ---")
    if location_data.get("lat"):
        # Simulation: Return mock hospital data
        results = [
            {"name": "General Medical Center", "distance": "1.2km"},
            {"name": "Urgent Care Clinic", "distance": "2.5km"},
            {"name": "City Emergency Hospital", "distance": "4.1km"},
        ]
        return results
    return []

# Tool Mapping for the Agent
AVAILABLE_TOOLS = {
    "get_user_location": get_user_location_tool,
    "search_hospitals": search_hospitals_tool,
}

# --- 3. Define the Graph Nodes (The steps in the state machine) ---

def call_llm(state: AgentState) -> AgentState:
    """
    Simulates the LLM's Reasoning step.
    The LLM inspects the state and decides:
    1. Which tool to call next (Action), OR
    2. If the process is complete (Final Answer).
    """
    print("\n[LLM REASONING] Analyzing current state...")
    history = state.get("run_history", [])

    if not state["tool_output"]:
        # Initial step or previous step was not a tool execution
        if "location" not in str(history):
            print("Decision: Need to find user location first.")
            return {
                "tool_name": "get_user_location",
                "tool_input": state["user_query"],
                "run_history": ["Thought: Deciding on initial action.", "Action: Call get_user_location."],
            }
        else:
            # Location has been found, now search for hospitals
            location_data = next((h for h in history if isinstance(h, dict) and h.get('city')), None)
            if location_data:
                 print("Decision: Location found, now search for hospitals.")
                 return {
                    "tool_name": "search_hospitals",
                    "tool_input": location_data,
                    "run_history": ["Thought: Location found, next step is to search.", "Action: Call search_hospitals."],
                }
            else:
                # Fallback error
                return {
                    "final_answer": "Error: Location information missing or invalid.",
                    "run_history": ["Thought: Fatal error, cannot proceed without location."],
                }

    elif state["tool_name"] == "search_hospitals":
        # Final step: Tool has run and returned hospital results
        print("Decision: Tool execution complete. Generating final answer.")
        hospital_list = state["tool_output"]
        answer = f"Found {len(hospital_list)} healthcare facilities nearby:\n"
        for i, h in enumerate(hospital_list):
            answer += f"{i+1}. {h['name']} ({h['distance']})\n"

        return {
            "final_answer": answer,
            "run_history": ["Observation: Search results received.", "Thought: Formatting final response."],
        }

    # If the logic is fully defined, this should not be reached
    return {"final_answer": "Agent finished without a proper conclusion."}


def execute_tool(state: AgentState) -> AgentState:
    """
    Simulates the tool execution step.
    Calls the function corresponding to the tool_name specified by the LLM.
    """
    print("\n[TOOL EXECUTION] Executing tool...")
    tool_name = state["tool_name"]
    tool_input = state["tool_input"]

    if tool_name not in AVAILABLE_TOOLS:
        print(f"Error: Tool '{tool_name}' not recognized.")
        return {"final_answer": f"Tool '{tool_name}' not found."}

    tool_func = AVAILABLE_TOOLS[tool_name]

    # Execute the tool
    if tool_name == "get_user_location":
        output = tool_func(tool_input)
        if output.get("error"):
            return {"final_answer": output["error"]}
        # Update history with the result
        return {"tool_output": [output], "run_history": [f"Observation: Location found: {output['city']}."]}
    elif tool_name == "search_hospitals":
        output = tool_func(tool_input)
        # Update history with the result
        return {"tool_output": output, "run_history": [f"Observation: Found {len(output)} hospital results."]}

    return {}


# --- 4. Define the Router (Conditional Edges) ---

def should_continue(state: AgentState) -> str:
    """
    Router: Determines the next node based on the current state.
    """
    if state.get("final_answer"):
        return "end" # Process is complete
    elif state.get("tool_name"):
        return "continue" # An action/tool needs to be executed
    return "end" # Should not happen in a well-formed graph


# --- 5. Build and Run the Graph ---

# 1. Create a StateGraph instance
workflow = StateGraph(AgentState)

# 2. Add nodes (the steps)
workflow.add_node("llm", call_llm)           # Node A: Reasoning/Decision
workflow.add_node("tool_execution", execute_tool) # Node B: Action

# 3. Set the starting point
workflow.set_entry_point("llm")

# 4. Define edges (the flow)
# From the LLM, use the router to decide the next step
workflow.add_conditional_edges(
    "llm", # Start from the LLM node
    should_continue, # The function that determines the next step
    {
        "continue": "tool_execution", # If tool_name is set, go execute the tool
        "end": END,                   # If final_answer is set, stop
    }
)

# After executing a tool, always return to the LLM for the next decision/step
workflow.add_edge("tool_execution", "llm")

# 5. Compile the graph
app = workflow.compile()

# --- Run the Agent Flow ---
initial_state = {"user_query": "Find hospitals near me", "tool_output": []}

print("==========================================")
print(f"STARTING AGENT RUN with Query: '{initial_state['user_query']}'")
print("==========================================")

# This runs the flow until the graph reaches the END node
final_state = app.invoke(initial_state)

print("\n==========================================")
print("AGENT RUN COMPLETE")
print("==========================================")
print(final_state["final_answer"])