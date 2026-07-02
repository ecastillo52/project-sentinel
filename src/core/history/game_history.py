# core/intelligence/game_history.py

"""
Project Sentinel

Game History

Utilities for analyzing historical performance for a
single game.

Every function in this module operates only on sessions
belonging to the requested game.
"""

from core.models.session import Session
from core.history import metrics


# ==========================================================
# Session Selection
# ==========================================================

def sessions_for_game(
    history: list[Session],
    game: str,
) -> list[Session]:
    """
    Return all sessions for a game ordered by date.

    Parameters
    ----------
    history : list[Session]

    game : str

    Returns
    -------
    list[Session]
    """

    sessions = [

        session

        for session in history

        if session.game == game

    ]

    return sorted(
        sessions,
        key=lambda session: session.date,
    )


def latest_session(
    history: list[Session],
    game: str,
) -> Session | None:
    """
    Return the newest recorded session for a game.
    """

    sessions = sessions_for_game(history, game)

    if not sessions:
        return None

    return sessions[-1]


def total_sessions(
    history: list[Session],
    game: str,
) -> int:
    """
    Return the number of recorded sessions.
    """

    return len(
        sessions_for_game(history, game)
    )


# ==========================================================
# Internal Helpers
# ==========================================================

def average_sensor(
    session: Session,
    sensor_id: str,
) -> float | None:
    """
    Return the average value for a sensor in a session.
    """

    sensors = session.report.get("sensors", {})

    sensor = sensors.get(sensor_id)

    if sensor is None:
        return None

    stats = sensor.get("stats", {})

    return stats.get("average")


def sensor_history(
    history: list[Session],
    game: str,
    sensor_id: str,
) -> list[float]:
    """
    Return all recorded average values for a sensor.
    """

    sessions = sessions_for_game(
        history,
        game,
    )

    values = [

        average_sensor(
            session,
            sensor_id,
        )

        for session in sessions

    ]

    return [

        value

        for value in values

        if value is not None

    ]


# ==========================================================
# Performance
# ==========================================================

def average_fps(
    history: list[Session],
    game: str,
) -> float | None:
    """
    Return the historical average FPS for a game.
    """

    sessions = sessions_for_game(
        history,
        game,
    )

    return metrics.average_fps(sessions)


def best_fps(
    history: list[Session],
    game: str,
) -> float | None:
    """
    Return the highest average FPS recorded for a game.
    """

    values = sensor_history(
        history,
        game,
        "fps",
    )

    if not values:
        return None

    return max(values)


def worst_fps(
    history: list[Session],
    game: str,
) -> float | None:
    """
    Return the lowest average FPS recorded for a game.
    """

    values = sensor_history(
        history,
        game,
        "fps",
    )

    if not values:
        return None

    return min(values)