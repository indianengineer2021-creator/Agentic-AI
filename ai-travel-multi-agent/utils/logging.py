"""Application logging helpers."""

from __future__ import annotations

import logging
import os

from config.settings import LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    """Create a project logger without exposing credentials."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, str(LOG_LEVEL).upper(), logging.INFO))
    return logger


__all__ = ["get_logger"]
