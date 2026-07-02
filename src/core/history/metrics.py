# core/history/metrics.py

"""
Project Sentinel

History Metrics

Calculates historical metrics for Sentinel sessions.

This module performs no rendering.
It only computes aggregate values.
"""

from core.models.session import Session


# ==========================================================
# Helpers
# ==========================================================

def _sensor_values(
    sessions: list[Session],
    sensor_id: str,
    statistic: str = "average",
) -> list[float]:
    """
    Return every recorded value for a sensor statistic.
    """

    values = []

    for session in sessions:

        sensor = session.report["sensors"].get(sensor_id)

        if sensor is None:
            continue

        value = sensor["stats"].get(statistic)

        if value is not None:
            values.append(value)

    return values


# ==========================================================
# Generic Metrics
# ==========================================================

def average_sensor(
    sessions: list[Session],
    sensor_id: str,
) -> float | None:
    """
    Return the historical average of a sensor.
    """

    values = _sensor_values(
        sessions,
        sensor_id,
        "average",
    )

    if not values:
        return None

    return sum(values) / len(values)


def highest_sensor(
    sessions: list[Session],
    sensor_id: str,
) -> float | None:
    """
    Return the highest recorded peak.
    """

    values = _sensor_values(
        sessions,
        sensor_id,
        "maximum",
    )

    if not values:
        return None

    return max(values)


def lowest_sensor(
    sessions: list[Session],
    sensor_id: str,
) -> float |None:
    """
    Return the lowest recorded minimum.
    """

    values = _sensor_values(
        sessions,
        sensor_id,
        "minimum",
    )

    if not values:
        return None

    return min(values)


# ==========================================================
# Convenience Metrics
# ==========================================================

def average_fps(
    sessions: list[Session],
) -> float | None:

    return average_sensor(
        sessions,
        "fps",
    )


def average_cpu_temperature(
    sessions: list[Session],
) -> float | None:

    return average_sensor(
        sessions,
        "cpu_temp",
    )


def average_gpu_temperature(
    sessions: list[Session],
) -> float | None:

    return average_sensor(
        sessions,
        "gpu_temp",
    )


def average_memory_load(
    sessions: list[Session],
) -> float | None:

    return average_sensor(
        sessions,
        "memory_load",
    )


def highest_cpu_temperature(
    sessions: list[Session],
) -> float | None:

    return highest_sensor(
        sessions,
        "cpu_temp",
    )


def highest_gpu_temperature(
    sessions: list[Session],
) -> float | None:

    return highest_sensor(
        sessions,
        "gpu_temp",
    )


def highest_memory_load(
    sessions: list[Session],
) -> float | None:

    return highest_sensor(
        sessions,
        "memory_load",
    )