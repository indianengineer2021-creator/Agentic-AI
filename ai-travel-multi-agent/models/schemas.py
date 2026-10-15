"""Pydantic models used across the travel-planning workflow."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TravelRequest(BaseModel):
    """User travel request model."""

    origin: str = Field(..., description="Origin city")
    destination: str = Field(..., description="Destination city")
    duration_days: int = Field(..., ge=1, description="Trip duration in days")
    travelers: int = Field(..., ge=1, description="Number of travelers")
    budget: float = Field(..., gt=0, description="Total trip budget")
    currency: str = Field(default="INR", description="Budget currency")
    interests: list[str] = Field(default_factory=list, description="Travel interests")
    hotel_preference: str = Field(default="mid-range", description="Hotel preference")
    activity_preferences: list[str] = Field(default_factory=list)
    travel_dates: Optional[str] = Field(default=None, description="Date range or time window")


class FlightOption(BaseModel):
    """Flight recommendation schema."""

    origin: str
    destination: str
    airline: Optional[str] = None
    estimated_cost: float
    notes: str = "Mock data only; not a real-time live quote."


class HotelOption(BaseModel):
    """Hotel recommendation schema."""

    destination: str
    category: str
    estimated_cost_per_night: float
    notes: str = "Mock data only; not a live hotel availability check."


class Activity(BaseModel):
    """Activity recommendation schema."""

    name: str
    category: str
    estimated_cost: float
    notes: str = "Demo activity recommendation."


class BudgetBreakdown(BaseModel):
    """Budget summary schema."""

    flight_cost: float = 0.0
    hotel_cost: float = 0.0
    food: float = 0.0
    local_transport: float = 0.0
    activities: float = 0.0
    miscellaneous: float = 0.0
    contingency: float = 0.0
    total_estimated_cost: float = 0.0
    remaining_budget: float = 0.0
    utilization_percent: float = 0.0
    categories_exceeding_budget: list[str] = Field(default_factory=list)


class DailyItinerary(BaseModel):
    """A single day in the itinerary."""

    day: int
    title: str
    activities: list[str]


class TravelReview(BaseModel):
    """Structured review produced by the Grok reviewer."""

    approved: bool = True
    issues: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class FinalTravelPlan(BaseModel):
    """Final travel plan structure."""

    destination: str
    duration_days: int
    flight_recommendation: Optional[FlightOption] = None
    hotel_recommendation: Optional[HotelOption] = None
    activities: list[str] = Field(default_factory=list)
    budget: BudgetBreakdown
    itinerary: list[DailyItinerary] = Field(default_factory=list)
    travel_tips: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    review_summary: str = ""


__all__ = [
    "TravelRequest",
    "FlightOption",
    "HotelOption",
    "Activity",
    "BudgetBreakdown",
    "DailyItinerary",
    "TravelReview",
    "FinalTravelPlan",
]
