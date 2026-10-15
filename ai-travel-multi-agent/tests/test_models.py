"""Tests for the Pydantic model layer."""

from __future__ import annotations

from models.schemas import BudgetBreakdown, FlightOption, HotelOption, TravelRequest


def test_travel_request_model() -> None:
    """Validate the travel request schema."""
    request = TravelRequest(
        origin="Chennai",
        destination="Singapore",
        duration_days=4,
        travelers=2,
        budget=100000,
        interests=["sightseeing", "food", "shopping"],
        hotel_preference="mid-range",
    )
    assert request.origin == "Chennai"
    assert request.destination == "Singapore"


def test_flight_hotel_models() -> None:
    """Ensure core models can be constructed with valid values."""
    flight = FlightOption(origin="Chennai", destination="Singapore", airline="Mock Air", estimated_cost=18000)
    hotel = HotelOption(destination="Singapore", category="mid-range", estimated_cost_per_night=5200)
    budget = BudgetBreakdown(total_estimated_cost=85000, remaining_budget=15000, utilization_percent=85.0)
    assert flight.origin == "Chennai"
    assert hotel.category == "mid-range"
    assert budget.total_estimated_cost == 85000
