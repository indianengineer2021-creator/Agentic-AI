"""Configuration tests for the application."""

from __future__ import annotations

from config.settings import APP_NAME, BASE_DIR, GEMINI_MODEL, LANGSMITH_PROJECT, is_gemini_configured


def test_settings_values() -> None:
    """Ensure the configuration centralizes defaults correctly."""
    assert APP_NAME == "AI Travel Planner"
    assert BASE_DIR.name == "ai-travel-multi-agent"
    assert GEMINI_MODEL == "gemini-2.0-flash"
    assert LANGSMITH_PROJECT == "ai-travel-planner"
    assert isinstance(is_gemini_configured(), bool)
