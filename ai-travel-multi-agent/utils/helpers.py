"""Shared helper functions."""

from __future__ import annotations


def safe_float(value: object, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
