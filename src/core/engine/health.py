# core/health.py

"""
Project Sentinel

Health Engine

Determines health classifications from analyzed statistics.

Every function receives a statistics dictionary:

{
    "current": ...,
    "minimum": ...,
    "maximum": ...,
    "average": ...,
    "samples": ...
}
"""

from typing import Any

Stats = dict[str, Any] | None


def average(stats: Stats) -> float | None:
    """
    Return the average value from a statistics dictionary.
    """

    if stats is None:
        return None

    return stats["average"]


# ==========================================================
# CPU
# ==========================================================


def cpu_temperature_status(stats: Stats) -> str:

    avg = average(stats)

    if avg is None:
        return "Unknown"

    if avg < 65:
        return "Excellent"

    if avg < 75:
        return "Healthy"

    if avg < 85:
        return "Warm"

    return "Critical"


def cpu_usage_status(stats: Stats) -> str:

    avg = average(stats)

    if avg is None:
        return "Unknown"

    if avg < 70:
        return "Healthy"

    if avg < 95:
        return "Busy"

    return "Maxed"


# ==========================================================
# GPU
# ==========================================================


def gpu_temperature_status(stats: Stats) -> str:

    avg = average(stats)

    if avg is None:
        return "Unknown"

    if avg < 60:
        return "Excellent"

    if avg < 70:
        return "Healthy"

    if avg < 82:
        return "Warm"

    return "Critical"


def gpu_usage_status(stats: Stats) -> str:

    avg = average(stats)

    if avg is None:
        return "Unknown"

    if avg < 85:
        return "Healthy"

    if avg < 97:
        return "Busy"

    return "Maxed"


# ==========================================================
# Memory
# ==========================================================


def memory_usage_status(stats: Stats) -> str:

    avg = average(stats)

    if avg is None:
        return "Unknown"

    if avg < 70:
        return "Healthy"

    if avg < 90:
        return "High"

    return "Critical"


# ==========================================================
# Performance
# ==========================================================


def fps_status(stats: Stats) -> str:

    avg = average(stats)

    if avg is None:
        return "Unknown"

    if avg >= 144:
        return "Excellent"

    if avg >= 120:
        return "Healthy"

    if avg >= 60:
        return "Playable"

    return "Poor"