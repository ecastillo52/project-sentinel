# core/intelligence/metrics.py

"""
Project Sentinel

Historical Metrics

Computes numerical metrics from historical Sentinel
sessions.

This module performs no interpretation.
"""

from __future__ import annotations

from statistics import mean

from core.models.sensor import Sensor
from core.models.session import Session


# ==========================================================
# Sensor Registry IDs
# ==========================================================

CPU_TEMPERATURE = "cpu_temp"
GPU_TEMPERATURE = "gpu_temp"
MEMORY_USAGE = "memory_load"
FPS = "fps"


# ==========================================================
# Helpers
# ==========================================================

def _sensor(
    session: Session,
    sensor_id: str,
) -> Sensor | None:
    """
    Return a sensor from a session.
    """

    sensor = session.report.sensors.get(sensor_id)

    if isinstance(sensor, Sensor):
        return sensor

    return None


def sensor_average(
    session: Session,
    sensor_id: str,
) -> float | None:
    """
    Return the average value recorded for a sensor.
    """

    sensor = _sensor(session, sensor_id)

    return None if sensor is None else sensor.average


def sensor_values(
    history: list[Session],
    sensor_id: str,
) -> list[float]:
    """
    Return all recorded averages for a sensor.
    """

    values: list[float] = []

    for session in history:

        value = sensor_average(
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

    values = sensor_values(history, sensor_id)

    if not values:
        return None

    return round(mean(values), 2)


def highest_sensor(
    history: list[Session],
    sensor_id: str,
) -> float | None:

    values = sensor_values(history, sensor_id)

    return max(values) if values else None


def lowest_sensor(
    history: list[Session],
    sensor_id: str,
) -> float | None:

    values = sensor_values(history, sensor_id)

    return min(values) if values else None


# ==========================================================
# Convenience Wrappers
# ==========================================================

def average_cpu_temperature(history):
    return average_sensor(history, CPU_TEMPERATURE)


def highest_cpu_temperature(history):
    return highest_sensor(history, CPU_TEMPERATURE)


def average_gpu_temperature(history):
    return average_sensor(history, GPU_TEMPERATURE)


def highest_gpu_temperature(history):
    return highest_sensor(history, GPU_TEMPERATURE)


def average_memory_load(history):
    return average_sensor(history, MEMORY_USAGE)


def highest_memory_load(history):
    return highest_sensor(history, MEMORY_USAGE)


def average_fps(history):
    return average_sensor(history, FPS)


def highest_fps(history):
    return highest_sensor(history, FPS)