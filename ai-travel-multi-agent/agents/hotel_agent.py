"""Hotel agent returns a mock hotel recommendation. """

from __future__ import annotations

from tools.hotel_tools import MockHotelProvider


def generate_hotel_options(destination: str, hotel_preference: str, travelers: int, duration_days: int):
    """Return hotel options based on destination and travel preferences."""
    provider = MockHotelProvider()
    return provider.get_hotel_options(destination, hotel_preference, travelers, duration_days)


def generate_hotel_plan() -> str:
    """Compatibility helper for early project scaffolding."""
    return "Hotel agent initialized with mock provider."


__all__ = ["generate_hotel_options", "generate_hotel_plan"]
