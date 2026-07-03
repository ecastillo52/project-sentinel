# core/engine/summary.py

"""
Project Sentinel

Session Summary

Builds the executive summary for a completed Report.

This module performs no analysis.

It summarizes data that has already been analyzed.
"""

from __future__ import annotations

from core.models.report import Report
from core.models.sensor import Sensor


# ==========================================================
# Constants
# ==========================================================

HEALTH_PRIORITY = (
    "CRITICAL",
    "POOR",
    "HIGH",
    "WARM",
    "HEALTHY",
    "EXCELLENT",
)


# ==========================================================
# Public API
# ==========================================================

def build_summary(report: Report) -> dict[str, float | str | None]:
    """
    Build an executive summary from a completed Report.
    """

    return {
        "average_fps": _average_fps(report),
        "peak_cpu_temp": _peak_cpu_temp(report),
        "peak_gpu_temp": _peak_gpu_temp(report),
        "peak_ram_usage": _peak_ram_usage(report),
        "overall_health": _overall_health(report),
    }


# ==========================================================
# Summary Builders
# ==========================================================

def _average_fps(report: Report) -> float | None:
    return _sensor_stat(report, "fps", "average")


def _peak_cpu_temp(report: Report) -> float | None:
    return _sensor_stat(report, "cpu_temp", "maximum")


def _peak_gpu_temp(report: Report) -> float | None:
    return _sensor_stat(report, "gpu_temp", "maximum")


def _peak_ram_usage(report: Report) -> float | None:
    return _sensor_stat(report, "memory_load", "maximum")


def _overall_health(report: Report) -> str:
    """
    Determine the overall health of the session.

    The worst health classification found among all sensors
    becomes the overall session health.
    """

    statuses = {
        (sensor.status or "").upper()
        for sensor in report.sensors.values()
        if isinstance(sensor, Sensor)
    }

    for level in HEALTH_PRIORITY:
        if level in statuses:
            return level

    return "Unknown"


# ==========================================================
# Helpers
# ==========================================================

def _sensor_stat(
    report: Report,
    sensor_id: str,
    attribute: str,
) -> float | None:
    """
    Return a statistic from a sensor.

    Parameters
    ----------
    report
        Completed Report.

    sensor_id
        Sensor registry identifier.

    attribute
        Sensor attribute (average, maximum, minimum, current).
    """

    sensor = report.sensors.get(sensor_id)

    if not isinstance(sensor, Sensor):
        return None

    return getattr(sensor, attribute, None)