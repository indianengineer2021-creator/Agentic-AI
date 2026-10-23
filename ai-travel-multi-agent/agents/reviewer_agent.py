"""Reviewer that checks consistency across travel-planning agent outputs."""

from __future__ import annotations

import json

from llm.groq import GroqClient
from models.schemas import TravelReview


def review_plan(plan_state: dict, groq_client: GroqClient | None = None) -> TravelReview:
    """Review agent outputs with deterministic checks and optional Groq analysis."""
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

    rule_review = TravelReview(
        approved=not issues,
        issues=issues,
        warnings=warnings,
        suggestions=suggestions,
    )
    client = groq_client if groq_client is not None else GroqClient()
    if not client.is_configured():
        return rule_review

    agent_outputs = {
        "trip_request": {
            "origin": plan_state.get("origin"),
            "destination": plan_state.get("destination"),
            "duration_days": plan_state.get("duration"),
            "travelers": plan_state.get("travelers"),
            "budget": allowed,
            "currency": plan_state.get("currency"),
        },
        "flight_agent": plan_state.get("flight_options", []),
        "hotel_agent": plan_state.get("hotel_options", []),
        "activity_agent": plan_state.get("activities", []),
        "budget_agent": budget,
        "rag_agent": plan_state.get("retrieved_information", []),
        "itinerary_agent": plan_state.get("itinerary", []),
    }
    prompt = (
        "Independently analyze these travel-planning multi-agent outputs. Check that the "
        "flight, hotel, activities, budget, retrieved travel information, and itinerary "
        "are consistent with the request and with each other. Identify concrete issues, "
        "warnings, and actionable suggestions. Do not invent facts not present in the data. "
        "Return a structured review; approve only if there are no blocking issues.\n\n"
        f"Agent outputs:\n{json.dumps(agent_outputs, ensure_ascii=True, default=str)}"
    )
    model_review = client.review(prompt)
    return TravelReview(
        approved=rule_review.approved and model_review.approved and not model_review.issues,
        issues=list(dict.fromkeys(rule_review.issues + model_review.issues)),
        warnings=list(dict.fromkeys(rule_review.warnings + model_review.warnings)),
        suggestions=list(dict.fromkeys(rule_review.suggestions + model_review.suggestions)),
        provider=model_review.provider,
        model=model_review.model,
    )


def review_plan_text() -> str:
    """Compatibility helper for older code paths."""
    return "Reviewer agent initialized."


__all__ = ["review_plan", "review_plan_text"]
