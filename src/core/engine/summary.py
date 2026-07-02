# core/engine/summary.py

"""
Project Sentinel

Session Summary

Build the executive summary displayed at the end
of every Sentinel report.

This module performs no analysis.

It summarizes data that has already been analyzed.
"""

from typing import Any


# ==========================================================
# Constants
# ==========================================================

HEALTH_PRIORITY = (
    "Critical",
    "Poor",
    "High",
    "Warm",
    "Healthy",
    "Excellent",
)


# ==========================================================
# Public API
# ==========================================================

def build_summary(report: dict[str, Any]) -> dict[str, Any]:
    """
    Build the session summary.

    Parameters
    ----------
    report : dict
        Completed Sentinel report.

    Returns
    -------
    dict
        Executive summary.
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

def _average_fps(report: dict[str, Any]) -> float | None:
    """Return the average FPS."""

    return _sensor_stat(report, "fps", "average")


def _peak_cpu_temp(report: dict[str, Any]) -> float | None:
    """Return the peak CPU temperature."""

    return _sensor_stat(report, "cpu_temp", "maximum")


def _peak_gpu_temp(report: dict[str, Any]) -> float | None:
    """Return the peak GPU temperature."""

    return _sensor_stat(report, "gpu_temp", "maximum")


def _peak_ram_usage(report: dict[str, Any]) -> float | None:
    """Return the peak memory load."""

    return _sensor_stat(report, "memory_load", "maximum")


def _overall_health(report: dict[str, Any]) -> str:
    """
    Determine overall session health.

    Priority (worst to best):

        Critical
        Poor
        High
        Warm
        Healthy
        Excellent
    """

    statuses = {
        (
            sensor["status"]
            if not isinstance(sensor["status"], dict)
            else sensor["status"].get("status", "Unknown")
        )
        for sensor in report["sensors"].values()
    }

    for level in HEALTH_PRIORITY:
        if level in statuses:
            return level

    return "Unknown"


# ==========================================================
# Helpers
# ==========================================================

def _sensor_stat(
    report: dict[str, Any],
    sensor_id: str,
    stat: str,
) -> float | None:
    """
    Return a statistic from a sensor.

    Returns None if the sensor or its statistics
    are unavailable.
    """

    sensor = report["sensors"].get(sensor_id)

    if sensor is None:
        return None

    stats = sensor.get("stats")

    if stats is None:
        return None

    return stats.get(stat)