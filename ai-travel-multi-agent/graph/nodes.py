"""Workflow node implementations for the LangGraph travel planner."""

from __future__ import annotations

from typing import Any

from agents.activity_agent import generate_activity_plan
from agents.budget_agent import calculate_budget
from agents.flight_agent import generate_flight_options
from agents.hotel_agent import generate_hotel_options
from agents.itinerary_agent import generate_itinerary
from agents.rag_agent import retrieve_travel_context
from agents.reviewer_agent import review_plan
from agents.supervisor import extract_travel_request
from models.schemas import BudgetBreakdown, DailyItinerary, FinalTravelPlan, TravelReview


def supervisor_node(state: dict[str, Any]) -> dict[str, Any]:
    """Parse and normalize the user request into a structured travel request."""
    request = extract_travel_request(state["user_request"])
    state["origin"] = request.origin
    state["destination"] = request.destination
    state["travel_dates"] = request.travel_dates or "Flexible dates"
    state["duration"] = request.duration_days
    state["travelers"] = request.travelers
    state["budget"] = request.budget
    state["currency"] = request.currency
    state["interests"] = request.interests
    state["hotel_preference"] = request.hotel_preference
    state["activity_preference"] = ", ".join(request.activity_preferences or request.interests)
    state["optimization_count"] = state.get("optimization_count", 0)
    state["errors"] = []
    state["workflow_status"] = "supervised"
    return state


def flight_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    """Generate flight recommendation options using the mock provider."""
    state["flight_options"] = [option.model_dump() for option in generate_flight_options(state["origin"], state["destination"], state["travelers"], state["duration"])]
    return state


def hotel_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    """Generate hotel suggestions using the mock hotel provider."""
    state["hotel_options"] = [option.model_dump() for option in generate_hotel_options(state["destination"], state["hotel_preference"], state["travelers"], state["duration"])]
    return state


def activity_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    """Generate activities based on the destination and user interests."""
    state["activities"] = [activity.model_dump() for activity in generate_activity_plan(state["destination"], state["interests"], state["duration"], state["budget"])]
    return state


def budget_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    """Compute a full travel budget estimate and compare it against the user's budget."""
    flight_options = [option for option in state.get("flight_options", [])]
    hotel_options = [option for option in state.get("hotel_options", [])]
    activities = [activity for activity in state.get("activities", [])]
    breakdown = calculate_budget(
        origin=state["origin"],
        destination=state["destination"],
        travelers=state["travelers"],
        duration_days=state["duration"],
        budget=state["budget"],
        flight_options=flight_options,
        hotel_options=hotel_options,
        activities=activities,
    )
    state["budget_analysis"] = breakdown.model_dump()
    return state


def budget_check_node(state: dict[str, Any]) -> dict[str, Any]:
    """Check whether the total estimate exceeds the user budget."""
    total = float(state.get("budget_analysis", {}).get("total_estimated_cost", 0.0))
    budget = float(state.get("budget", 0.0))
    state["workflow_status"] = "within_budget" if total <= budget else "over_budget"
    return state


def optimization_node(state: dict[str, Any]) -> dict[str, Any]:
    """Return the workflow to an optimization path when the budget is exceeded."""
    state["optimization_count"] = state.get("optimization_count", 0) + 1
    breakdown = state.get("budget_analysis", {})
    if breakdown:
        breakdown["contingency"] = max(0.0, float(breakdown.get("contingency", 0.0)) * 0.7)
        breakdown["miscellaneous"] = max(0.0, float(breakdown.get("miscellaneous", 0.0)) * 0.8)
        breakdown["total_estimated_cost"] = max(0.0, float(breakdown.get("total_estimated_cost", 0.0)) * 0.9)
        breakdown["remaining_budget"] = float(state.get("budget", 0.0)) - float(breakdown.get("total_estimated_cost", 0.0))
    state["workflow_status"] = "optimized"
    return state


def rag_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    """Populates relevant travel information from the local knowledge base."""
    destination = state.get("destination", "")
    query = f"Travel tips for {destination} with interests {state.get('interests', [])}"
    state["retrieved_information"] = retrieve_travel_context(destination, query)
    return state


def itinerary_agent_node(state: dict[str, Any]) -> dict[str, Any]:
    """Build a decision-friendly day-by-day itinerary."""
    itinerary = generate_itinerary(
        destination=state["destination"],
        duration_days=state["duration"],
        interests=state["interests"],
        activities=state.get("activities", []),
        budget=state["budget"],
    )
    state["itinerary"] = [item.model_dump() for item in itinerary]
    return state


def grok_reviewer_node(state: dict[str, Any]) -> dict[str, Any]:
    """Give the itinerary an independent review using the Grok reviewer logic."""
    review = review_plan(state)
    state["review"] = review.model_dump()
    return state


def review_decision_node(state: dict[str, Any]) -> dict[str, Any]:
    """Decide whether the final plan is approved or needs another loop."""
    review = state.get("review", {})
    if review.get("approved") is True:
        state["workflow_status"] = "approved"
        return state
    if state.get("optimization_count", 0) >= 3:
        state["workflow_status"] = "finalized_with_warnings"
        return state
    state["workflow_status"] = "needs_revision"
    return state


def final_response_node(state: dict[str, Any]) -> dict[str, Any]:
    """Package the final result into a clear final-plan object."""
    review = state.get("review", {})
    final_plan = FinalTravelPlan(
        destination=state["destination"],
        duration_days=state["duration"],
        flight_recommendation=state.get("flight_options", [{}])[0],
        hotel_recommendation=state.get("hotel_options", [{}])[0],
        activities=[activity["name"] for activity in state.get("activities", [])],
        budget=BudgetBreakdown(**state.get("budget_analysis", {})),
        itinerary=[DailyItinerary(**item) for item in state.get("itinerary", [])],
        travel_tips=state.get("retrieved_information", []),
        risks=["Review limitations: demo/mock data used; verify live pricing and restrictions before booking."],
        assumptions=["Trip details are based on a demo scenario.", "Real booking data should be verified from official sources."],
        review_summary="; ".join(review.get("issues", [])) or "Plan accepted by the review step.",
    )
    state["final_plan"] = final_plan.model_dump()
    state["workflow_status"] = "complete"
    return state


__all__ = [
    "supervisor_node",
    "flight_agent_node",
    "hotel_agent_node",
    "activity_agent_node",
    "budget_agent_node",
    "budget_check_node",
    "optimization_node",
    "rag_agent_node",
    "itinerary_agent_node",
    "grok_reviewer_node",
    "review_decision_node",
    "final_response_node",
]
