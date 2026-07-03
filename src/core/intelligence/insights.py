# core/intelligence/insights.py

"""
Project Sentinel

Historical Insights

Produces observations from historical metrics.

Input:
    list[Session]

Output:
    trends
    best sessions
    worst sessions
"""

from __future__ import annotations

from core.models.session import Session

from . import metrics


# ==========================================================
# Helpers
# ==========================================================


def _direction(
    values: list[float],
) -> str:
    """
    Determine the direction of a historical series.
    """

    if len(values) < 2:
        return "Unknown"

    first = values[0]
    last = values[-1]

    difference = last - first

    if abs(difference) < 1:
        return "Stable"

    if difference > 0:
        return "Increasing"

    return "Decreasing"


def _sensor_average(
    session: Session,
    sensor_id: str,
):
    sensor = session.report.sensors.get(sensor_id)

    if sensor is None:
        return None

    return sensor.average


def _trend(
    history,
    sensor_id,
):

    values = []

    for session in history:

        value = _sensor_average(
            session,
            sensor_id,
        )

        if value is not None:
            values.append(value)

    return _direction(values)


# ==========================================================
# Trends
# ==========================================================


def fps_direction(history):

    return _trend(
        history,
        "fps",
    )


def cpu_temperature_direction(history):

    return _trend(
        history,
        "cpu_temperature",
    )


def gpu_temperature_direction(history):

    return _trend(
        history,
        "gpu_temperature",
    )


def memory_usage_direction(history):

    return _trend(
        history,
        "memory_usage",
    )


# ==========================================================
# Best Sessions
# ==========================================================


def best_fps_session(history):

    best = None
    best_value = None

    for session in history:

        value = _sensor_average(
            session,
            "fps",
        )

        if value is None:
            continue

        if best_value is None or value > best_value:

            best_value = value
            best = session

    return best


def hottest_cpu_session(history):

    hottest = None
    highest = None

    for session in history:

        value = _sensor_average(
            session,
            "cpu_temperature",
        )

        if value is None:
            continue

        if highest is None or value > highest:

            highest = value
            hottest = session

    return hottest


def hottest_gpu_session(history):

    hottest = None
    highest = None

    for session in history:

        value = _sensor_average(
            session,
            "gpu_temperature",
        )

        if value is None:
            continue

        if highest is None or value > highest:

            highest = value
            hottest = session

    return hottest

def highest_memory_session(history):

    hottest = None
    highest = None

    for session in history:

        value = _sensor_average(
            session,
            "Physical Memory Load",
        )

        if value is None:
            continue

        if highest is None or value > highest:

            highest = value
            hottest = session

    return hottest