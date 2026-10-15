"""Budget agent that computes total trip cost and compares it to the user's budget."""

from __future__ import annotations

from models.schemas import BudgetBreakdown


def calculate_budget(
    origin: str,
    destination: str,
    travelers: int,
    duration_days: int,
    budget: float,
    flight_options: list[dict],
    hotel_options: list[dict],
    activities: list[dict],
) -> BudgetBreakdown:
    """Compute all major trip cost components for the requested trip."""
    flight_cost = sum(float(option.get("estimated_cost", 0.0)) for option in flight_options)
    hotel_cost = sum(
        float(option.get("estimated_cost_per_night", 0.0)) * max(1, duration_days) for option in hotel_options
    ) * max(1, travelers)
    food = 2500 * travelers * max(1, duration_days)
    local_transport = 1000 * travelers * max(1, duration_days)
    activity_cost = sum(float(item.get("estimated_cost", 0.0)) for item in activities)
    miscellaneous = 0.08 * budget
    contingency = 0.1 * budget
    total_estimated_cost = flight_cost + hotel_cost + food + local_transport + activity_cost + miscellaneous + contingency
    remaining_budget = budget - total_estimated_cost
    utilization_percent = (total_estimated_cost / budget) * 100 if budget else 0.0
    categories_exceeding_budget = []
    if total_estimated_cost > budget:
        categories_exceeding_budget = ["flight_cost", "hotel_cost", "activities", "food", "local_transport"]

    return BudgetBreakdown(
        flight_cost=flight_cost,
        hotel_cost=hotel_cost,
        food=food,
        local_transport=local_transport,
        activities=activity_cost,
        miscellaneous=miscellaneous,
        contingency=contingency,
        total_estimated_cost=total_estimated_cost,
        remaining_budget=remaining_budget,
        utilization_percent=utilization_percent,
        categories_exceeding_budget=categories_exceeding_budget,
    )


def calculate_budget_summary() -> str:
    """Compatibility helper for the earlier scaffold."""
    return "Budget agent initialized."


__all__ = ["calculate_budget", "calculate_budget_summary"]
