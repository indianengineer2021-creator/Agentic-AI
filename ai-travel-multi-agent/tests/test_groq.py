"""Tests for the optional Groq reviewer client."""

from __future__ import annotations

import pytest

import llm.groq as groq_module
from agents.reviewer_agent import review_plan
from models.schemas import TravelReview


def test_groq_client_requires_an_api_key() -> None:
    """Do not attempt model calls when Groq is not configured."""
    client = groq_module.GroqClient(api_key="")

    assert not client.is_configured()
    with pytest.raises(RuntimeError, match="Groq API key is not configured"):
        client.review("Review the travel plan.")


def test_groq_reviewer_analyzes_agent_outputs_and_preserves_rule_issues() -> None:
    """Combine model feedback with deterministic budget validation."""

    class FakeGroqClient(groq_module.GroqClient):
        def __init__(self) -> None:
            super().__init__(api_key="")

        def is_configured(self) -> bool:
            return True

        def review(self, prompt: str) -> TravelReview:
            assert '"flight_agent"' in prompt
            assert '"itinerary_agent"' in prompt
            return TravelReview(
                approved=True,
                warnings=["The itinerary has an unverified transfer."],
                suggestions=["Verify airport transfer times."],
                provider="groq",
                model="test-model",
            )

    review = review_plan(
        {
            "budget": 100,
            "budget_analysis": {"total_estimated_cost": 200},
            "itinerary": [{"day": 1, "title": "Arrival", "activities": ["Check in"]}],
            "retrieved_information": ["Use official travel guidance."],
        },
        groq_client=FakeGroqClient(),
    )

    assert not review.approved
    assert "Total estimate exceeds the requested budget." in review.issues
    assert "The itinerary has an unverified transfer." in review.warnings
    assert review.provider == "groq"
    assert review.model == "test-model"


def test_groq_client_returns_validated_structured_review(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use the configured model and validate its structured response."""
    calls: dict[str, object] = {}

    class FakeStructuredModel:
        def invoke(self, prompt: str) -> dict[str, object]:
            calls["prompt"] = prompt
            return {"approved": True, "warnings": ["Check local opening hours."]}

    class FakeChatGroq:
        def __init__(self, **kwargs: object) -> None:
            calls["config"] = kwargs

        def with_structured_output(self, schema: type[TravelReview]) -> FakeStructuredModel:
            calls["schema"] = schema
            return FakeStructuredModel()

    monkeypatch.setattr(groq_module, "ChatGroq", FakeChatGroq)
    client = groq_module.GroqClient(api_key="test-key", model_name="test-model")
    review = client.review("Review the agent outputs.")

    assert calls["config"] == {
        "model": "test-model",
        "groq_api_key": "test-key",
        "temperature": 0.2,
    }
    assert calls["schema"] is TravelReview
    assert review.warnings == ["Check local opening hours."]
    assert review.provider == "groq"
    assert review.model == "test-model"
