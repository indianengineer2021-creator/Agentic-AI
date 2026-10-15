"""TypedDict state used by the LangGraph workflow."""

from __future__ import annotations

from typing import Any, TypedDict


class TravelState(TypedDict, total=False):
    """Shared state object for the travel-planning workflow."""

    user_request: str
    origin: str
    destination: str
    travel_dates: str
    duration: int
    travelers: int
    budget: float
    currency: str
    interests: list[str]
    hotel_preference: str
    activity_preference: str
    flight_options: list[dict[str, Any]]
    hotel_options: list[dict[str, Any]]
    activities: list[dict[str, Any]]
    retrieved_information: list[str]
    budget_analysis: dict[str, Any]
    itinerary: list[dict[str, Any]]
    review: dict[str, Any]
    optimization_count: int
    errors: list[str]
    final_plan: dict[str, Any]
    workflow_status: str


__all__ = ["TravelState"]
