"""Activity agent planning recommendations based on interests and trip length."""

from __future__ import annotations

from tools.activity_tools import MockActivityProvider


def generate_activity_plan(destination: str, interests: list[str], duration_days: int, budget: float):
    """Return a list of demo activities for the requested trip profile."""
    provider = MockActivityProvider()
    return provider.get_activities(destination, interests, duration_days, budget)


def generate_activity_plan_summary() -> str:
    """Compatibility helper for the earlier scaffold."""
    return "Activity agent initialized with demo recommendations."


__all__ = ["generate_activity_plan", "generate_activity_plan_summary"]
