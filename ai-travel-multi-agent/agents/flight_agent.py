"""Flight agent using a mock provider with an extensible provider interface."""

from __future__ import annotations

from tools.flight_tools import MockFlightProvider


def generate_flight_options(origin: str, destination: str, travelers: int, duration_days: int):
    """Return a list of mocked flight options for the destination."""
    provider = MockFlightProvider()
    return provider.get_flight_options(origin, destination, travelers, duration_days)


def generate_flight_plan() -> str:
    """Compatibility helper for the initial project scaffolding."""
    return "Flight agent initialized with mock provider."


__all__ = ["generate_flight_options", "generate_flight_plan"]
