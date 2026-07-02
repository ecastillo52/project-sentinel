# core/history/trends.py

"""
Project Sentinel

History Trends

Calculates historical performance trends.

This module performs no rendering.

It measures how values change over time.
"""

from core.models.session import Session


# ==========================================================
# Helpers
# ==========================================================

def change(old: float, new: float) -> float:
    """
    Return the absolute change between two values.
    """

    return new - old


def percent_change(old: float, new: float) -> float:
    """
    Return the percentage change.

    Returns 0 if the original value is zero.
    """

    if old == 0:
        return 0.0

    return ((new - old) / old) * 100


def direction(value: float) -> str:
    """
    Return the trend direction.
    """

    if value > 0:
        return "Increasing"

    if value < 0:
        return "Decreasing"

    return "Stable"


# ==========================================================
# Sensor Trends
# ==========================================================

def average_sensor_trend(
    sessions: list[Session],
    sensor_id: str,
) -> float | None:
    """
    Compare the oldest and newest average values
    for a sensor.
    """

    if len(sessions) < 2:
        return None

    sessions = sorted(
        sessions,
        key=lambda session: session.date
    )

    first = sessions[0]
    last = sessions[-1]

    first_average = (
        first.report["sensors"][sensor_id]["stats"]["average"]
    )

    last_average = (
        last.report["sensors"][sensor_id]["stats"]["average"]
    )

    return change(
        first_average,
        last_average,
    )


def peak_sensor_trend(
    sessions: list[Session],
    sensor_id: str,
) -> float | None:
    """
    Compare the oldest and newest peak values
    for a sensor.
    """

    if len(sessions) < 2:
        return None

    sessions = sorted(
        sessions,
        key=lambda session: session.date
    )

    first = sessions[0]
    last = sessions[-1]

    first_peak = (
        first.report["sensors"][sensor_id]["stats"]["maximum"]
    )

    last_peak = (
        last.report["sensors"][sensor_id]["stats"]["maximum"]
    )

    return change(
        first_peak,
        last_peak,
    )