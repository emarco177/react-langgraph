from dotenv import load_dotenv

load_dotenv()

from langgraph.prebuilt.tool_executor import ToolExecutor

from react.chains.reasoning_chain import react_reasoning_runnable, tools
from react.state import AgentState


def run_agent_reasoning_engine(state: AgentState):
    agent_outcome = react_reasoning_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}


tool_executor = ToolExecutor(tools)


def execute_tools(state: AgentState):
    agent_action = state["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}
