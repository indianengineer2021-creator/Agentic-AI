"""Mock activity provider and future activity integrations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.schemas import Activity


class BaseActivityProvider(ABC):
    """Interface for future activity/data providers."""

    @abstractmethod
    def get_activities(self, destination: str, interests: list[str], duration_days: int, budget: float) -> list[Activity]:
        """Return activities for the trip."""


class MockActivityProvider(BaseActivityProvider):
    """Demo activity generator built around simple destination interests."""

    def get_activities(self, destination: str, interests: list[str], duration_days: int, budget: float) -> list[Activity]:
        default = [
            Activity(name="City walking tour", category="Sightseeing", estimated_cost=1200, notes="Group walking tour for key landmarks."),
            Activity(name="Local food trail", category="Food", estimated_cost=1800, notes="Popular food streets and local tasting route."),
            Activity(name="Shopping district visit", category="Shopping", estimated_cost=1500, notes="Market exploration and souvenir shopping."),
        ]
        if "food" not in [item.lower() for item in interests]:
            default[1] = Activity(name="Scenic evening cruise", category="Leisure", estimated_cost=2200, notes="Relaxed evening activity with city views.")
        if "shopping" not in [item.lower() for item in interests]:
            default[2] = Activity(name="Museum visit", category="Culture", estimated_cost=1400, notes="Cultural and heritage stop.")
        return default[: min(3, max(1, duration_days))]


def get_mock_activity_recommendations(destination: str, interests: list[str] | None = None, budget: float = 0.0) -> list[dict]:
    """Compatibility helper used by tests and the UI."""
    provider = MockActivityProvider()
    activities = provider.get_activities(destination, interests or ["sightseeing", "food", "shopping"], 4, budget)
    return [activity.model_dump() for activity in activities]
