"""
LangGraph Graph — route ve compile
"""

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END

from agent.state import HotelState
from agent.nodes import agent_node, tool_node, response_node


def _should_continue(state: HotelState) -> str:
    last: AIMessage = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return "respond"


def build_graph():
    g = StateGraph(HotelState)

    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)
    g.add_node("respond", response_node)

    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", _should_continue, {"tools": "tools", "respond": "respond"})
    g.add_edge("tools", "agent")
    g.add_edge("respond", END)

    return g.compile()


hotel_agent = build_graph()
