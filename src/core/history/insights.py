# core/history/insights.py

"""
Project Sentinel

History Insights

Generates high-level observations from historical
Sentinel data.

This module performs no rendering.
It only produces high-level observations derived from
saved Session objects.
"""

from core.models.session import Session

from . import metrics
from . import trends


# ==========================================================
# Internal Helpers
# ==========================================================

def _sensor_stat(
    session: Session,
    sensor_id: str,
    statistic: str,
) -> float | None:
    """
    Safely retrieve a sensor statistic.
    """

    sensors = session.report.get("sensors", {})

    sensor = sensors.get(sensor_id)

    if sensor is None:
        return None

    stats = sensor.get("stats", {})

    return stats.get(statistic)


# ==========================================================
# Session Insights
# ==========================================================

def hottest_cpu_session(
    sessions: list[Session],
) -> Session | None:
    """
    Return the session with the highest CPU temperature.
    """

    valid = [
        session
        for session in sessions
        if _sensor_stat(
            session,
            "cpu_temp",
            "maximum",
        )
        is not None
    ]

    if not valid:
        return None

    return max(
        valid,
        key=lambda session: _sensor_stat(
            session,
            "cpu_temp",
            "maximum",
        ),
    )


def best_fps_session(
    sessions: list[Session],
) -> Session | None:
    """
    Return the session with the highest average FPS.
    """

    valid = [
        session
        for session in sessions
        if _sensor_stat(
            session,
            "fps",
            "average",
        )
        is not None
    ]

    if not valid:
        return None

    return max(
        valid,
        key=lambda session: _sensor_stat(
            session,
            "fps",
            "average",
        ),
    )


# ==========================================================
# Trend Insights
# ==========================================================

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


# ==========================================================
# Historical Metrics
# ==========================================================

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