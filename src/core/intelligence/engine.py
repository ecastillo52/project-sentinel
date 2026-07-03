# core/intelligence/engine.py

"""
Project Sentinel

Historical Intelligence Engine

Coordinates the historical intelligence pipeline.

Sessions
    ↓
Game Filter
    ↓
Historical Report
"""

from __future__ import annotations

from core.models.session import Session

from .report import build_report


# ==========================================================
# Public API
# ==========================================================

def run(
    sessions: list[Session],
    game: str,
) -> dict:
    """
    Execute the historical intelligence pipeline for a
    single game.
    """

    history = [
        session
        for session in sessions
        if session.game == game
    ]

    return build_report(
        history=history,
        game=game,
    )