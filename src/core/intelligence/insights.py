# core/intelligence/insights.py

"""
Project Sentinel

Historical Insights

Produces historical trends and identifies notable
sessions from Sentinel history.
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
    Determine the direction of a series.
    """

    if len(values) < 2:
        return "Unknown"

    difference = values[-1] - values[0]

    if abs(difference) < 1:
        return "Stable"

    return "Increasing" if difference > 0 else "Decreasing"


def _trend(
    history: list[Session],
    sensor_id: str,
) -> str:
    """
    Determine the historical trend for a sensor.
    """

    return _direction(
        metrics.sensor_values(
            history,
            sensor_id,
        )
    )


def _best_session(
    history: list[Session],
    sensor_id: str,
) -> Session | None:
    """
    Return the session with the highest average value
    for a sensor.
    """

    best = None
    highest = None

    for session in history:

        value = metrics.sensor_average(
            session,
            sensor_id,
        )

        if value is None:
            continue

        if highest is None or value > highest:

            highest = value
            best = session

    return best


# ==========================================================
# Trends
# ==========================================================

def fps_direction(history):
    return _trend(history, metrics.FPS)


def cpu_temperature_direction(history):
    return _trend(history, metrics.CPU_TEMPERATURE)


def cpu_usage_direction(history):
    return _trend(history, metrics.CPU_USAGE)


def gpu_temperature_direction(history):
    return _trend(history, metrics.GPU_TEMPERATURE)


def gpu_usage_direction(history):
    return _trend(history, metrics.GPU_USAGE)


def memory_used_direction(history):
    return _trend(history, metrics.MEMORY_USED)


def memory_usage_direction(history):
    return _trend(history, metrics.MEMORY_USAGE)


# ==========================================================
# Best Sessions
# ==========================================================

def best_fps_session(history):
    return _best_session(
        history,
        metrics.FPS,
    )


def hottest_cpu_session(history):
    return _best_session(
        history,
        metrics.CPU_TEMPERATURE,
    )


def hottest_gpu_session(history):
    return _best_session(
        history,
        metrics.GPU_TEMPERATURE,
    )


def highest_memory_session(history):
    return _best_session(
        history,
        metrics.MEMORY_USAGE,
    )
