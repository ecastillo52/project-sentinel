# core/history/statistics.py

"""
Project Sentinel

History Statistics

Calculates historical statistics from saved Sentinel sessions.

This module performs no rendering.
It only computes values.
"""

from core.models.session import Session


# ==========================================================
# Session Statistics
# ==========================================================

def total_sessions(history: list[Session]) -> int:
    """
    Return the total number of recorded sessions.
    """

    return len(history)


def latest_session(
    history: list[Session],
) -> Session | None:
    """
    Return the newest recorded session.
    """

    if not history:
        return None

    return max(
        history,
        key=lambda session: session.date
    )


def oldest_session(
    history: list[Session],
) -> Session | None:
    """
    Return the oldest recorded session.
    """

    if not history:
        return None

    return min(
        history,
        key=lambda session: session.date
    )


# ==========================================================
# Game Statistics
# ==========================================================

def games_played(
    history: list[Session],
) -> list[str]:
    """
    Return every unique recorded game.
    """

    return sorted({

        session.game

        for session in history

    })


def total_games(
    history: list[Session],
) -> int:
    """
    Return the number of unique games.
    """

    return len(
        games_played(history)
    )


def sessions_for_game(
    history: list[Session],
    game: str,
) -> list[Session]:
    """
    Return every recorded session for a game.
    """

    return [

        session

        for session in history

        if session.game == game

    ]