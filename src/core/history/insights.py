# core/history/insights.py

"""
Project Sentinel

History Insights

Generates high-level observations from
historical Sentinel data.

This module performs no rendering.
It only produces human-readable insights.
"""

from core.models.session import Session

from . import metrics
from . import trends


def hottest_cpu_session(
    sessions: list[Session],
) -> Session | None:
    """
    Return the session with the hottest CPU.
    """

    if not sessions:
        return None

    return max(
        sessions,
        key=lambda session:
        session.report["sensors"]["cpu_temp"]["stats"]["maximum"]
    )


def best_fps_session(
    sessions: list[Session],
) -> Session | None:
    """
    Return the session with the highest FPS.
    """

    if not sessions:
        return None

    return max(
        sessions,
        key=lambda session:
        session.report["sensors"]["fps"]["stats"]["average"]
    )


def cpu_temperature_direction(
    sessions: list[Session],
) -> str:
    """
    Describe the long-term CPU temperature trend.
    """

    trend = trends.average_sensor_trend(
        sessions,
        "cpu_temp",
    )

    if trend is None:
        return "Unknown"

    return trends.direction(trend)


def fps_direction(
    sessions: list[Session],
) -> str:
    """
    Describe the long-term FPS trend.
    """

    trend = trends.average_sensor_trend(
        sessions,
        "fps",
    )

    if trend is None:
        return "Unknown"

    return trends.direction(trend)


def historical_average_fps(
    sessions: list[Session],
) -> float | None:
    """
    Return the historical average FPS.
    """

    return metrics.average_fps(sessions)


def historical_average_cpu_temperature(
    sessions: list[Session],
) -> float | None:
    """
    Return the historical average CPU temperature.
    """

    return metrics.average_cpu_temperature(sessions)