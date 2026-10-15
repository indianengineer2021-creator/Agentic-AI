"""LangGraph workflow for the travel-planning application."""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from graph.nodes import (
    activity_agent_node,
    budget_agent_node,
    budget_check_node,
    final_response_node,
    flight_agent_node,
    grok_reviewer_node,
    hotel_agent_node,
    itinerary_agent_node,
    optimization_node,
    rag_agent_node,
    review_decision_node,
    supervisor_node,
)
from graph.state import TravelState


def build_workflow() -> StateGraph:
    """Create and compile a reusable LangGraph workflow."""
    workflow = StateGraph(TravelState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("flight_agent", flight_agent_node)
    workflow.add_node("hotel_agent", hotel_agent_node)
    workflow.add_node("activity_agent", activity_agent_node)
    workflow.add_node("budget_agent", budget_agent_node)
    workflow.add_node("budget_check", budget_check_node)
    workflow.add_node("optimization", optimization_node)
    workflow.add_node("rag_agent", rag_agent_node)
    workflow.add_node("itinerary_agent", itinerary_agent_node)
    workflow.add_node("grok_reviewer", grok_reviewer_node)
    workflow.add_node("review_decision", review_decision_node)
    workflow.add_node("final_response", final_response_node)

    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", "flight_agent")
    workflow.add_edge("flight_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "activity_agent")
    workflow.add_edge("activity_agent", "budget_agent")
    workflow.add_edge("budget_agent", "budget_check")

    def budget_routing(state: dict[str, Any]) -> str:
        over_budget = state.get("workflow_status") == "over_budget"
        retries_remaining = state.get("optimization_count", 0) < 3
        return "over_budget" if over_budget and retries_remaining else "within_budget"

    workflow.add_conditional_edges(
        "budget_check",
        budget_routing,
        {
            "over_budget": "optimization",
            "within_budget": "rag_agent",
        },
    )
    workflow.add_edge("optimization", "budget_agent")
    workflow.add_edge("rag_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "grok_reviewer")
    workflow.add_edge("grok_reviewer", "review_decision")

    def review_routing(state: dict[str, Any]) -> str:
        if state.get("workflow_status") == "approved":
            return "final_response"
        if state.get("workflow_status") in {"finalized_with_warnings", "needs_revision"}:
            if state.get("optimization_count", 0) >= 3:
                return "final_response"
            return "optimization"
        return "final_response"

    workflow.add_conditional_edges(
        "review_decision",
        review_routing,
        {
            "final_response": "final_response",
            "optimization": "optimization",
        },
    )
    workflow.add_edge("final_response", END)

    return workflow.compile()


def run_workflow(user_request: str) -> dict[str, Any]:
    """Run the fully assembled planning workflow for a natural-language trip request."""
    workflow = build_workflow()
    initial_state: TravelState = {"user_request": user_request}
    return workflow.invoke(initial_state)


__all__ = ["build_workflow", "run_workflow"]
