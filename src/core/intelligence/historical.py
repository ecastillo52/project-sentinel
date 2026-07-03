# core/intelligence/historical.py

"""
Project Sentinel

Historical Intelligence

Converts historical metrics and trends into
human-readable observations.

This module performs no calculations.

It relies entirely on metrics.py and insights.py.
"""

from __future__ import annotations

from core.models.session import Session

from . import insights
from . import metrics


# ==========================================================
# Performance
# ==========================================================

def performance(
    history: list[Session],
) -> list[str]:
    """
    Generate performance observations.
    """

    statements: list[str] = []

    average = metrics.average_fps(history)

    if average is not None:
        statements.append(
            f"Average gaming performance is {average:.1f} FPS."
        )

    trend = insights.fps_direction(history)

    if trend != "Unknown":
        statements.append(
            f"Performance is {trend.lower()} over time."
        )

    best = insights.best_fps_session(history)

    if best is not None:
        statements.append(
            f"Best recorded performance occurred during "
            f"{best.display_name}."
        )

    return statements


# ==========================================================
# CPU
# ==========================================================

def cpu(
    history: list[Session],
) -> list[str]:
    """
    Generate CPU observations.
    """

    statements: list[str] = []

    average = metrics.average_cpu_temperature(history)

    if average is not None:
        statements.append(
            f"Average CPU temperature is "
            f"{average:.1f} °C."
        )

    trend = insights.cpu_temperature_direction(history)

    if trend != "Unknown":
        statements.append(
            f"CPU temperatures are {trend.lower()} over time."
        )

    hottest = insights.hottest_cpu_session(history)

    if hottest is not None:
        statements.append(
            f"The hottest CPU session was "
            f"{hottest.display_name}."
        )

    return statements


# ==========================================================
# GPU
# ==========================================================

def gpu(
    history: list[Session],
) -> list[str]:
    """
    Generate GPU observations.
    """

    statements: list[str] = []

    average = metrics.average_gpu_temperature(history)

    if average is not None:
        statements.append(
            f"Average GPU temperature is "
            f"{average:.1f} °C."
        )

    trend = insights.gpu_temperature_direction(history)

    if trend != "Unknown":
        statements.append(
            f"GPU temperatures are {trend.lower()} over time."
        )

    hottest = insights.hottest_gpu_session(history)

    if hottest is not None:
        statements.append(
            f"The hottest GPU session was "
            f"{hottest.display_name}."
        )

    return statements


# ==========================================================
# Memory
# ==========================================================

def memory(
    history: list[Session],
) -> list[str]:
    """
    Generate memory observations.
    """

    statements: list[str] = []

    average = metrics.average_memory_load(history)

    if average is not None:
        statements.append(
            f"Average memory usage is "
            f"{average:.1f}%."
        )

    trend = insights.memory_usage_direction(history)

    if trend != "Unknown":
        statements.append(
            f"Memory usage is {trend.lower()} over time."
        )

    highest = insights.highest_memory_session(history)

    if highest is not None:
        statements.append(
            f"Highest memory usage occurred during "
            f"{highest.display_name}."
        )

    return statements