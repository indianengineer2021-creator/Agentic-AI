"""Agent-level tests using mock providers."""

from __future__ import annotations

from agents.flight_agent import generate_flight_options
from agents.hotel_agent import generate_hotel_options
from agents.activity_agent import generate_activity_plan


def test_mock_agent_outputs() -> None:
    """Confirm the demo agents produce valid structured travel recommendations."""
    flights = generate_flight_options("Chennai", "Singapore", 2, 4)
    hotels = generate_hotel_options("Singapore", "mid-range", 2, 4)
    activities = generate_activity_plan("Singapore", ["sightseeing", "food", "shopping"], 4, 100000)

    assert len(flights) >= 1
    assert len(hotels) >= 1
    assert len(activities) >= 1
    assert flights[0].destination == "Singapore"
    assert hotels[0].category == "mid-range"
    assert activities[0].name
