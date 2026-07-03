# core/intelligence/metrics.py

"""
Project Sentinel

Historical Metrics

Computes numerical metrics from historical Sentinel
sessions.

This module performs no interpretation.

Input:
    list[Session]

Output:
    numbers
"""

from __future__ import annotations

from statistics import mean
from typing import Any

from core.models.session import Session


# ==========================================================
# Helpers
# ==========================================================


def _sensor_average(
    session: Session,
    sensor_id: str,
) -> float | None:
    """
    Return the average value recorded for a sensor.
    """

    sensor = session.report.sensors.get(sensor_id)

    if sensor is None:
        return None

    return sensor.average


def _values(
    history: list[Session],
    sensor_id: str,
) -> list[float]:
    """
    Return all historical averages for a sensor.
    """

    values = []

    for session in history:

        value = _sensor_average(
            session,
            sensor_id,
        )

        if value is not None:
            values.append(value)

    return values


# ==========================================================
# Generic Metrics
# ==========================================================


def average_sensor(
    history: list[Session],
    sensor_id: str,
) -> float | None:

    values = _values(history, sensor_id)

    if not values:
        return None

    return round(mean(values), 2)


def highest_sensor(
    history: list[Session],
    sensor_id: str,
) -> float | None:

    values = _values(history, sensor_id)

    if not values:
        return None

    return max(values)


def lowest_sensor(
    history: list[Session],
    sensor_id: str,
) -> float | None:

    values = _values(history, sensor_id)

    if not values:
        return None

    return min(values)


# ==========================================================
# CPU
# ==========================================================


def average_cpu_temperature(history):

    return average_sensor(
        history,
        "cpu_temperature",
    )


def highest_cpu_temperature(history):

    return highest_sensor(
        history,
        "cpu_temperature",
    )


# ==========================================================
# GPU
# ==========================================================


def average_gpu_temperature(history):

    return average_sensor(
        history,
        "gpu_temperature",
    )


def highest_gpu_temperature(history):

    return highest_sensor(
        history,
        "gpu_temperature",
    )


# ==========================================================
# Memory
# ==========================================================


def average_memory_load(history):

    return average_sensor(
        history,
        "memory_usage",
    )


def highest_memory_load(history):

    return highest_sensor(
        history,
        "memory_usage",
    )


# ==========================================================
# FPS
# ==========================================================


def average_fps(history):

    return average_sensor(
        history,
        "fps",
    )


def highest_fps(history):

    return highest_sensor(
        history,
        "fps",
    )