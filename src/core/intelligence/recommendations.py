# core/intelligence/recommendations.py

"""
Project Sentinel

Recommendations Engine

Generates maintenance and performance recommendations
from historical Sentinel analysis.

This module performs no rendering.
It only produces recommendations.
"""

from __future__ import annotations


# ==========================================================
# Public API
# ==========================================================

def generate(report: dict) -> list[dict]:
    """
    Generate recommendations from a historical report.
    """

    recommendations: list[dict] = []

    recommendations.extend(
        cpu_recommendations(
            report.get("cpu", {}),
        )
    )

    recommendations.extend(
        gpu_recommendations(
            report.get("gpu", {}),
        )
    )

    recommendations.extend(
        memory_recommendations(
            report.get("memory", {}),
        )
    )

    recommendations.extend(
        performance_recommendations(
            report.get("performance", {}),
        )
    )

    return recommendations


# ==========================================================
# CPU
# ==========================================================

def cpu_recommendations(
    cpu: dict,
) -> list[dict]:

    recommendations = []

    peak = cpu.get("highest_temperature")

    if peak is None:
        return recommendations

    if peak >= 90:

        recommendations.append(
            {
                "level": "Critical",
                "title": "CPU Running Extremely Hot",
                "message": (
                    "CPU temperatures exceeded 90 °C. "
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
    gpu: dict,
) -> list[dict]:

    recommendations = []

    peak = gpu.get("highest_temperature")

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
    memory: dict,
) -> list[dict]:

    recommendations = []

    peak = memory.get("highest_load")

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
    performance: dict,
) -> list[dict]:

    recommendations = []

    trend = performance.get("trend")

    if trend == "Decreasing":

        recommendations.append(
            {
                "level": "Information",
                "title": "Performance Trending Downward",
                "message": (
                    "Average FPS has declined across historical "
                    "sessions. Continue monitoring future runs "
                    "for consistency."
                ),
            }
        )

    return recommendations