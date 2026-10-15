"""Independent Grok-style reviewer that checks budget, logic, and itinerary quality."""

from __future__ import annotations

from models.schemas import TravelReview


def review_plan(plan_state: dict) -> TravelReview:
    """Return a structured review with issues, warnings, and suggestions."""
    budget = plan_state.get("budget_analysis", {})
    total = float(budget.get("total_estimated_cost", 0.0))
    allowed = float(plan_state.get("budget", 0.0))
    issues: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    if total > allowed:
        issues.append("Total estimate exceeds the requested budget.")
        suggestions.append("Reduce activity or hotel cost to bring the plan within budget.")
    if not plan_state.get("itinerary"):
        warnings.append("Itinerary is missing or incomplete.")
    if plan_state.get("optimization_count", 0) >= 2:
        warnings.append("Workflow has already been optimized multiple times; verify the final plan carefully.")
    if not plan_state.get("retrieved_information"):
        warnings.append("Travel knowledge is not yet populated from the RAG store.")

    approved = not issues
    return TravelReview(
        approved=approved,
        issues=issues,
        warnings=warnings,
        suggestions=suggestions,
    )


def review_plan_text() -> str:
    """Compatibility helper for older code paths."""
    return "Reviewer agent initialized."


__all__ = ["review_plan", "review_plan_text"]
