from dotenv import load_dotenv

from react.nodes.nodes import execute_tools, run_agent_reasoning_engine

load_dotenv()

from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph

from react.consts import ACT, AGENT_REASON
from react.state import AgentState


def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT


flow = StateGraph(AgentState)

flow.add_node(AGENT_REASON, run_agent_reasoning_engine)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, execute_tools)


flow.add_conditional_edges(
    AGENT_REASON,
    should_continue,
)
flow.add_edge(ACT, AGENT_REASON)
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":checkpoints.sqlite:")

app = flow.compile(checkpointer=memory)
# app.get_graph().draw_mermaid_png(output_file_path="../static/graph.png")
