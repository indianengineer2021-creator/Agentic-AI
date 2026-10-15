"""Tests for the budget logic."""

from __future__ import annotations

from agents.budget_agent import calculate_budget


def test_budget_calculation() -> None:
    """Calculate a representative trip budget and confirm major cost fields exist."""
    breakdown = calculate_budget(
        origin="Chennai",
        destination="Singapore",
        travelers=2,
        duration_days=4,
        budget=100000,
        flight_options=[{"estimated_cost": 20000}],
        hotel_options=[{"estimated_cost_per_night": 5200}],
        activities=[{"estimated_cost": 4000}, {"estimated_cost": 2500}],
    )
    assert breakdown.total_estimated_cost > 0
    assert breakdown.remaining_budget < 100000
    assert "utilization_percent" in breakdown.model_dump()
