# core/history/query.py

"""
Project Sentinel

History Query

Provides helpers for retrieving historical Sentinel sessions.

This module performs no analysis.
It only filters and returns Session objects.
"""

from datetime import datetime

from core.models.session import Session


# ==========================================================
# Session Queries
# ==========================================================

def newest(
    history: list[Session],
) -> Session | None:
    """
    Return the newest session.
    """

    if not history:
        return None

    return max(
        history,
        key=lambda session: session.date
    )


def oldest(
    history: list[Session],
) -> Session | None:
    """
    Return the oldest session.
    """

    if not history:
        return None

    return min(
        history,
        key=lambda session: session.date
    )


def last(
    history: list[Session],
    count: int = 10,
) -> list[Session]:
    """
    Return the most recent sessions.
    """

    return sorted(
        history,
        key=lambda session: session.date,
        reverse=True,
    )[:count]


# ==========================================================
# Game Queries
# ==========================================================

def game(
    history: list[Session],
    name: str,
) -> list[Session]:
    """
    Return every session for a game.
    """

    return [

        session

        for session in history

        if session.game.lower() == name.lower()

    ]


# ==========================================================
# Date Queries
# ==========================================================

def between(
    history: list[Session],
    start: datetime,
    end: datetime,
) -> list[Session]:
    """
    Return sessions between two dates.
    """

    return [

        session

        for session in history

        if start <= session.date <= end

    ]


def after(
    history: list[Session],
    date: datetime,
) -> list[Session]:
    """
    Return sessions after a date.
    """

    return [

        session

        for session in history

        if session.date >= date

    ]


def before(
    history: list[Session],
    date: datetime,
) -> list[Session]:
    """
    Return sessions before a date.
    """

    return [

        session

        for session in history

        if session.date <= date

    ]


# ==========================================================
# Hardware Queries
# ==========================================================

def cpu(
    history: list[Session],
    cpu_name: str,
) -> list[Session]:
    """
    Return sessions recorded on a CPU.
    """

    return [

        session

        for session in history

        if session.report["machine"]["cpu"] == cpu_name

    ]


def gpu(
    history: list[Session],
    gpu_name: str,
) -> list[Session]:
    """
    Return sessions recorded on a GPU.
    """

    return [

        session

        for session in history

        if session.report["machine"]["gpu"] == gpu_name

    ]