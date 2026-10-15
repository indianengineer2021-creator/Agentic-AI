"""Mock flight provider and reusable provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.schemas import FlightOption


class BaseFlightProvider(ABC):
    """Interface for future real flight APIs."""

    @abstractmethod
    def get_flight_options(self, origin: str, destination: str, travelers: int, duration_days: int) -> list[FlightOption]:
        """Return flight recommendation objects."""


class MockFlightProvider(BaseFlightProvider):
    """Demo provider with clearly labeled mock flight estimates."""

    def get_flight_options(self, origin: str, destination: str, travelers: int, duration_days: int) -> list[FlightOption]:
        base_cost = 18000 if destination.lower() == "singapore" else 21000
        multiplier = max(1, travelers)
        return [
            FlightOption(
                origin=origin,
                destination=destination,
                airline="Mock Air India",
                estimated_cost=float(base_cost * multiplier),
                notes="DEMO DATA ONLY: flight estimate is illustrative and not a live booking quote.",
            ),
            FlightOption(
                origin=origin,
                destination=destination,
                airline="Mock Singapore Express",
                estimated_cost=float((base_cost + 3500) * multiplier),
                notes="DEMO DATA ONLY: this is a mock comparison option for planning purposes.",
            ),
        ]


def get_mock_flight_options(destination: str, origin: str = "Chennai", travelers: int = 2) -> list[dict]:
    """Compatibility helper used by early tests and demo UI code."""
    provider = MockFlightProvider()
    flight_options = provider.get_flight_options(origin, destination, travelers, 4)
    return [option.model_dump() for option in flight_options]
