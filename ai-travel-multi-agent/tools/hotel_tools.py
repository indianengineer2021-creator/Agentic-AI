"""Mock hotel provider and interface for future real hotel integrations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.schemas import HotelOption


class BaseHotelProvider(ABC):
    """Interface for future hotel APIs."""

    @abstractmethod
    def get_hotel_options(self, destination: str, hotel_preference: str, travelers: int, duration_days: int) -> list[HotelOption]:
        """Return hotel recommendation objects."""


class MockHotelProvider(BaseHotelProvider):
    """Demo hotel provider with labelled mock pricing."""

    def get_hotel_options(self, destination: str, hotel_preference: str, travelers: int, duration_days: int) -> list[HotelOption]:
        preference = (hotel_preference or "mid-range").lower()
        nightly_cost = {
            "budget": 2800,
            "mid-range": 5200,
            "premium": 8200,
            "luxury": 12000,
        }.get(preference, 5200)
        nights = max(1, duration_days)
        return [
            HotelOption(
                destination=destination,
                category=preference,
                estimated_cost_per_night=float(nightly_cost),
                notes="DEMO DATA ONLY: not a live hotel availability check or booking quote.",
            )
        ]


def get_mock_hotel_options(destination: str, hotel_preference: str = "mid-range", travelers: int = 2) -> list[dict]:
    """Compatibility helper for the early UI and tests."""
    provider = MockHotelProvider()
    hotel_options = provider.get_hotel_options(destination, hotel_preference, travelers, 4)
    return [option.model_dump() for option in hotel_options]
