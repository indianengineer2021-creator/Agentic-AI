"""Workflow tests for the LangGraph planner."""

from __future__ import annotations

import pytest

from graph.workflow import run_workflow


def test_workflow_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Run a sample travel request through the workflow and expect a final plan."""
    monkeypatch.setattr("graph.nodes.retrieve_travel_context", lambda destination, query: ["test travel guidance"])
    result = run_workflow("I want to travel from Chennai to Singapore for 4 days for 2 people with a budget of ₹100000. I like sightseeing, food and shopping.")
    assert result.get("final_plan")
    assert result.get("workflow_status") in {"complete", "finalized_with_warnings", "approved"}


def test_workflow_stops_optimizing_when_budget_cannot_be_met(monkeypatch: pytest.MonkeyPatch) -> None:
    """Finalize an over-budget plan after the optimization retry limit."""
    monkeypatch.setattr("graph.nodes.retrieve_travel_context", lambda destination, query: ["test travel guidance"])
    result = run_workflow(
        "I want to travel from Chennai to Singapore for 4 days for 2 people "
        "with a budget of ₹1000. I like sightseeing, food and shopping."
    )

    assert result.get("final_plan")
    assert result["optimization_count"] == 3
    assert result["final_plan"]["budget"]["total_estimated_cost"] > result["budget"]
    assert result["final_plan"]["review_summary"]
