# core/engine/summary.py

"""
Project Sentinel

Session Summary

Build the executive summary displayed at the end
of every Sentinel report.

This module performs no analysis.

It summarizes data that has already been analyzed.
"""


# ==========================================================
# Public API
# ==========================================================

def build_summary(report):
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

def _average_fps(report):
    """Return the average FPS."""

    return _sensor_average(report, "fps")


def _peak_cpu_temp(report):
    """Return the peak CPU temperature."""

    return _sensor_maximum(report, "cpu_temp")


def _peak_gpu_temp(report):
    """Return the peak GPU temperature."""

    return _sensor_maximum(report, "gpu_temp")


def _peak_ram_usage(report):
    """Return the peak memory load."""

    return _sensor_maximum(report, "memory_load")


def _overall_health(report):
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

    priorities = [
        "Critical",
        "Poor",
        "High",
        "Warm",
        "Healthy",
        "Excellent",
    ]

    statuses = []

    for sensor in report["sensors"].values():

        status = sensor["status"]

        if isinstance(status, dict):
            status = status.get("status", "Unknown")

        statuses.append(status)

    for level in priorities:

        if level in statuses:
            return level

    return "Unknown"


# ==========================================================
# Helpers
# ==========================================================

def _sensor_average(report, sensor_id):
    """Return a sensor's average value."""

    sensor = report["sensors"].get(sensor_id)

    if sensor is None:
        return None

    return sensor["stats"]["average"]


def _sensor_maximum(report, sensor_id):
    """Return a sensor's maximum value."""

    sensor = report["sensors"].get(sensor_id)

    if sensor is None:
        return None

    return sensor["stats"]["maximum"]