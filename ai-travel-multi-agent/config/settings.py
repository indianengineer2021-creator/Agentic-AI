"""Application settings and environment configuration."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true").lower() == "true"
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "ai-travel-planner")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GROK_MODEL = os.getenv("GROK_MODEL", "grok-2-latest")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
APP_NAME = os.getenv("APP_NAME", "AI Travel Planner")
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def is_gemini_configured() -> bool:
    """Return True when the Gemini API key is available."""
    return bool(GEMINI_API_KEY)


def is_grok_configured() -> bool:
    """Return True when the xAI Grok API key is available."""
    return bool(XAI_API_KEY)


def is_groq_configured() -> bool:
    """Return True when the Groq API key is available."""
    return bool(GROQ_API_KEY)


def is_langsmith_configured() -> bool:
    """Return True when the LangSmith API key is available."""
    return bool(LANGSMITH_API_KEY)


__all__ = [
    "BASE_DIR",
    "GEMINI_API_KEY",
    "XAI_API_KEY",
    "GROQ_API_KEY",
    "LANGSMITH_API_KEY",
    "LANGSMITH_TRACING",
    "LANGSMITH_PROJECT",
    "GEMINI_MODEL",
    "GROK_MODEL",
    "GROQ_MODEL",
    "APP_NAME",
    "APP_ENV",
    "LOG_LEVEL",
    "is_gemini_configured",
    "is_grok_configured",
    "is_groq_configured",
    "is_langsmith_configured",
]
