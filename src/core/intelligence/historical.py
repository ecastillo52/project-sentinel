# core/intelligence/historical.py

"""
Project Sentinel

Historical Intelligence

Generates human-readable observations from historical
Sentinel data.

This module performs no rendering.

Each function returns a list of intelligence statements
for a specific report section.
"""

from core.history import insights


# ==========================================================
# Performance
# ==========================================================

def performance(history) -> list[str]:
    """
    Generate performance intelligence.
    """

    statements = []

    trend = insights.fps_direction(history)

    if trend != "Unknown":
        statements.append(
            f"Gaming performance is {trend.lower()} over time."
        )

    average = insights.historical_average_fps(history)

    if average is not None:
        statements.append(
            f"Historical average performance is "
            f"{average:.1f} FPS."
        )

    best = insights.best_fps_session(history)

    if best is not None:
        statements.append(
            f"The strongest performance was recorded during "
            f"{best.display_name}."
        )

    return statements


# ==========================================================
# CPU
# ==========================================================

def cpu(history) -> list[str]:
    """
    Generate CPU intelligence.
    """

    statements = []

    trend = insights.cpu_temperature_direction(history)

    if trend != "Unknown":
        statements.append(
            f"CPU temperatures are {trend.lower()} over time."
        )

    average = insights.historical_average_cpu_temperature(
        history
    )

    if average is not None:
        statements.append(
            f"Historical average CPU temperature is "
            f"{average:.1f} °C."
        )

    hottest = insights.hottest_cpu_session(history)

    if hottest is not None:
        statements.append(
            f"The highest CPU temperatures occurred during "
            f"{hottest.display_name}."
        )

    return statements


# ==========================================================
# GPU
# ==========================================================

def gpu(history) -> list[str]:
    """
    Generate GPU intelligence.
    """

    return []


# ==========================================================
# Memory
# ==========================================================

def memory(history) -> list[str]:
    """
    Generate memory intelligence.
    """

    return []