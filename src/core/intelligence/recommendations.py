# core/intelligence/recommendations.py

"""
Project Sentinel

Historical Recommendations

Generates long-term recommendations from historical
Sentinel sessions.

Unlike the engine recommendation system, this module
analyzes trends across multiple sessions rather than
individual sensor readings from a single report.
"""

from __future__ import annotations

from core.models.session import Session

from . import insights
from . import metrics


# ==========================================================
# Public API
# ==========================================================

def generate(
    history: list[Session],
) -> list[dict[str, str]]:
    """
    Generate historical recommendations.

    Parameters
    ----------
    history
        Historical Sentinel sessions.

    Returns
    -------
    list[dict[str, str]]
        Historical recommendations.
    """

    recommendations: list[dict[str, str]] = []

    recommendations.extend(cpu(history))
    recommendations.extend(gpu(history))
    recommendations.extend(memory(history))
    recommendations.extend(performance(history))

    return recommendations


# ==========================================================
# CPU
# ==========================================================

def cpu(
    history: list[Session],
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    average = metrics.average_cpu_temperature(history)
    trend = insights.cpu_temperature_direction(history)

    if average is None:
        return recommendations

    if average >= 80:

        recommendations.append(
            {
                "level": "Warning",
                "title": "CPU Temperatures Consistently High",
                "message": (
                    "Historical sessions show consistently "
                    "elevated CPU temperatures. Inspect cooling "
                    "performance and system airflow."
                ),
            }
        )

    if trend == "Increasing":

        recommendations.append(
            {
                "level": "Information",
                "title": "CPU Temperatures Trending Upward",
                "message": (
                    "CPU temperatures have increased over recent "
                    "sessions. Monitor for continued thermal "
                    "degradation."
                ),
            }
        )

    return recommendations


# ==========================================================
# GPU
# ==========================================================

def gpu(
    history: list[Session],
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    average = metrics.average_gpu_temperature(history)
    trend = insights.gpu_temperature_direction(history)

    if average is None:
        return recommendations

    if average >= 75:

        recommendations.append(
            {
                "level": "Warning",
                "title": "GPU Temperatures Consistently High",
                "message": (
                    "Historical GPU temperatures remain elevated. "
                    "Consider inspecting cooling performance."
                ),
            }
        )

    if trend == "Increasing":

        recommendations.append(
            {
                "level": "Information",
                "title": "GPU Temperatures Trending Upward",
                "message": (
                    "GPU temperatures have gradually increased "
                    "across recent sessions."
                ),
            }
        )

    return recommendations


# ==========================================================
# Memory
# ==========================================================

def memory(
    history: list[Session],
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    average = metrics.average_memory_load(history)
    trend = insights.memory_usage_direction(history)

    if average is None:
        return recommendations

    if average >= 85:

        recommendations.append(
            {
                "level": "Warning",
                "title": "Memory Usage Remains High",
                "message": (
                    "Memory utilization has remained consistently "
                    "high across multiple sessions."
                ),
            }
        )

    if trend == "Increasing":

        recommendations.append(
            {
                "level": "Information",
                "title": "Memory Usage Trending Upward",
                "message": (
                    "Memory usage has steadily increased over time. "
                    "Monitor background applications."
                ),
            }
        )

    return recommendations


# ==========================================================
# Performance
# ==========================================================

def performance(
    history: list[Session],
) -> list[dict[str, str]]:

    recommendations: list[dict[str, str]] = []

    average = metrics.average_fps(history)
    trend = insights.fps_direction(history)

    if average is None:
        return recommendations

    if average < 60:

        recommendations.append(
            {
                "level": "Warning",
                "title": "Performance Below Target",
                "message": (
                    "Average FPS has remained below 60 across "
                    "historical sessions."
                ),
            }
        )

    elif average < 120:

        recommendations.append(
            {
                "level": "Information",
                "title": "Performance Can Be Improved",
                "message": (
                    "Historical performance is stable but below "
                    "high-refresh gaming targets."
                ),
            }
        )

    if trend == "Decreasing":

        recommendations.append(
            {
                "level": "Warning",
                "title": "Performance Trending Downward",
                "message": (
                    "Average FPS has declined over recent sessions. "
                    "Investigate possible hardware or software "
                    "changes."
                ),
            }
        )

    return recommendations