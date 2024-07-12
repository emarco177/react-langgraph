from typing import Literal

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

tools = [TavilySearchResults()]
tool_node = ToolNode(tools)
model = ChatMistralAI(model="mistral-large-latest", temperature=0).bind_tools(tools)


def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

graphh = workflow.compile()

# graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


# user_input = "what is the current weather in London? In Celsuis"
# events = graph.stream({"messages": [("user", user_input)]}, stream_mode="values")
# for event in events:
#     if "messages" in event:
#         event["messages"][-1].pretty_print()
