"""Supervisor agent that parses the user request into a structured request."""

from __future__ import annotations

import re

from models.schemas import TravelRequest


def parse_currency(value: str | None) -> str:
    """Normalize a currency string from the user request."""
    if not value:
        return "INR"
    up = value.upper().strip()
    if "USD" in up:
        return "USD"
    if "EUR" in up:
        return "EUR"
    if "SGD" in up:
        return "SGD"
    return "INR"


def extract_travel_request(user_request: str, **kwargs) -> TravelRequest:
    """Parse a natural-language request into a validated TravelRequest."""
    text = user_request.strip()
    lower_text = text.lower()

    origin = kwargs.get("origin") or re.search(r"from\s+([A-Za-z][A-Za-z\s]+?)(?=\s+to\s+)", text, flags=re.IGNORECASE)
    origin_value = origin.group(1).strip() if isinstance(origin, re.Match) else kwargs.get("origin", "Chennai")

    destination_match = re.search(r"to\s+([A-Za-z][A-Za-z\s]+?)(?=\s+for\s|\s+for\s*\d|$)", text, flags=re.IGNORECASE)
    destination = kwargs.get("destination") or (destination_match.group(1).strip() if destination_match else "Singapore")

    duration_match = re.search(r"for\s+(\d+)\s+days?", text, flags=re.IGNORECASE)
    duration_days = int(duration_match.group(1)) if duration_match else int(kwargs.get("duration_days", 4))

    travelers_match = re.search(r"for\s+(\d+)\s+people?", text, flags=re.IGNORECASE)
    travelers = int(travelers_match.group(1)) if travelers_match else int(kwargs.get("travelers", 2))

    budget_match = re.search(r"(?:budget|under|within)\s*(?:of\s*)?(?:₹|INR|rs\.?\s*)?(\d[\d,]*)", text, flags=re.IGNORECASE)
    budget = float(budget_match.group(1).replace(",", "")) if budget_match else float(kwargs.get("budget", 100000))

    interests = kwargs.get("interests") or [
        "sightseeing",
        "food",
        "shopping",
    ]
    if isinstance(interests, str):
        interests = [item.strip().lower() for item in interests.split(",") if item.strip()]

    hotel_preference = kwargs.get("hotel_preference") or ("mid-range" if "mid-range" in lower_text or "mid range" in lower_text else "budget")
    activity_preferences = kwargs.get("activity_preferences") or interests

    return TravelRequest(
        origin=origin_value,
        destination=destination,
        duration_days=duration_days,
        travelers=travelers,
        budget=budget,
        currency=parse_currency(kwargs.get("currency") or ("INR" if "₹" in text or "inr" in lower_text else None)),
        interests=[str(item).strip().lower() for item in interests],
        hotel_preference=str(hotel_preference).lower(),
        activity_preferences=[str(item).strip().lower() for item in activity_preferences],
        travel_dates=kwargs.get("travel_dates") or "Flexible dates",
    )


def supervise(user_request: str) -> str:
    """Compatibility wrapper for a simple textual supervisor response."""
    request = extract_travel_request(user_request)
    return (
        f"Supervisor parsed request: {request.origin} -> {request.destination}, "
        f"{request.duration_days} days, {request.travelers} travelers, budget {request.currency} {request.budget}."
    )


__all__ = ["extract_travel_request", "supervise"]
