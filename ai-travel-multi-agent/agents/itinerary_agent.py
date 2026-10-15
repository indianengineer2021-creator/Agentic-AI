"""Itinerary agent that builds a realistic multi-day trip plan."""

from __future__ import annotations

from models.schemas import DailyItinerary


def generate_itinerary(destination: str, duration_days: int, interests: list[str], activities: list[dict], budget: float) -> list[DailyItinerary]:
    """Build a realistic itinerary from the chosen activities and destination."""
    activity_names = [item.get("name", "Exploration") for item in activities[:3]]
    itinerary: list[DailyItinerary] = []
    for day in range(1, duration_days + 1):
        if day == 1:
            day_activities = [
                "Arrival and hotel check-in",
                "Short neighborhood walk",
                "Dinner near hotel",
            ]
        elif day == duration_days:
            day_activities = [
                "Breakfast and last-minute shopping",
                "Final attraction visit",
                "Departure preparation",
            ]
        else:
            day_activities = [
                f"Morning: {activity_names[0] if activity_names else 'city sightseeing'}",
                f"Afternoon: {activity_names[1] if len(activity_names) > 1 else 'local market walk'}",
                f"Evening: {activity_names[2] if len(activity_names) > 2 else 'local food experience'}",
            ]
        itinerary.append(DailyItinerary(day=day, title=f"Day {day}: {destination} plan", activities=day_activities))
    return itinerary


def build_itinerary_summary() -> str:
    """Compatibility helper for the earlier scaffold."""
    return "Itinerary agent initialized."


__all__ = ["generate_itinerary", "build_itinerary_summary"]
