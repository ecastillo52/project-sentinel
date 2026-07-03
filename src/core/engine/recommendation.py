# core/engine/recommendations.py

"""
Project Sentinel

Recommendations Engine

Generates maintenance and performance recommendations
from a completed Report.

This module performs no rendering.

It only produces recommendation data.
"""

from __future__ import annotations

from core.models.report import Report
from core.models.sensor import Sensor


# ==========================================================
# Public API
# ==========================================================

def generate(report: Report) -> list[dict[str, str]]:
    """
    Generate recommendations from a completed Report.
    """

    recommendations: list[dict[str, str]] = []

    sensors = report.sensors

    cpu = _sensor(sensors, "cpu_temperature")
    gpu = _sensor(sensors, "gpu_temperature")
    memory = _sensor(sensors, "memory_usage")
    fps = _sensor(sensors, "fps")

    if cpu:
        recommendations.extend(
            cpu_recommendations(cpu)
        )

    if gpu:
        recommendations.extend(
            gpu_recommendations(gpu)
        )

    if memory:
        recommendations.extend(
            memory_recommendations(memory)
        )

    if fps:
        recommendations.extend(
            performance_recommendations(fps)
        )

    return recommendations


# ==========================================================
# Helpers
# ==========================================================

def _sensor(
    sensors: dict[str, Sensor],
    sensor_id: str,
) -> Sensor | None:
    """
    Return a Sensor from the report.
    """

    sensor = sensors.get(sensor_id)

    if isinstance(sensor, Sensor):
        return sensor

    return None


# ==========================================================
# CPU
# ==========================================================

def cpu_recommendations(
    sensor: Sensor,
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    peak = sensor.maximum

    if peak is None:
        return recommendations

    if peak >= 90:

        recommendations.append(
            {
                "level": "CRITICAL",
                "title": "CPU Running Extremely Hot",
                "message": (
                    "CPU temperatures exceeded 90°C. "
                    "Inspect the cooling system immediately."
                ),
            }
        )

    elif peak >= 80:

        recommendations.append(
            {
                "level": "Warning",
                "title": "CPU Temperature Elevated",
                "message": (
                    "CPU temperatures are higher than ideal. "
                    "Monitor cooling performance and airflow."
                ),
            }
        )

    return recommendations


# ==========================================================
# GPU
# ==========================================================

def gpu_recommendations(
    sensor: Sensor,
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    peak = sensor.maximum

    if peak is None:
        return recommendations

    if peak >= 85:

        recommendations.append(
            {
                "level": "Warning",
                "title": "GPU Temperature Elevated",
                "message": (
                    "GPU temperatures reached elevated levels "
                    "during gameplay. Monitor cooling and fan "
                    "performance."
                ),
            }
        )

    return recommendations


# ==========================================================
# Memory
# ==========================================================

def memory_recommendations(
    sensor: Sensor,
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    peak = sensor.maximum

    if peak is None:
        return recommendations

    if peak >= 90:

        recommendations.append(
            {
                "level": "Warning",
                "title": "High Memory Usage",
                "message": (
                    "System memory usage exceeded 90%. "
                    "Consider closing background applications "
                    "or upgrading system memory."
                ),
            }
        )

    return recommendations


# ==========================================================
# Performance
# ==========================================================

def performance_recommendations(
    sensor: Sensor,
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    average = sensor.average

    if average is None:
        return recommendations

    if average < 60:

        recommendations.append(
            {
                "level": "Warning",
                "title": "Low Average FPS",
                "message": (
                    "Average FPS dropped below 60. "
                    "Lower graphics settings or investigate "
                    "system bottlenecks."
                ),
            }
        )

    elif average < 120:

        recommendations.append(
            {
                "level": "Information",
                "title": "Performance Can Be Improved",
                "message": (
                    "Performance is playable but below high-refresh "
                    "gaming targets."
                ),
            }
        )

    return recommendations