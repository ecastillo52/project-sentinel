# core/intelligence/recommendations.py

"""
Project Sentinel

Recommendations Engine

Generates maintenance and performance recommendations
from historical Sentinel analysis.

This module performs no rendering.
It only produces recommendations.
"""


# ==========================================================
# Helpers
# ==========================================================

def _safe(report: dict, *path, default=None):
    """
    Safely traverse nested dictionaries.
    """
    current = report

    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

        if current is None:
            return default

    return current


# ==========================================================
# Public API
# ==========================================================

def generate(report: dict) -> list[dict]:
    """
    Generate recommendations from a historical report.
    """

    recommendations = []

    recommendations.extend(cpu_recommendations(report))
    recommendations.extend(gpu_recommendations(report))
    recommendations.extend(memory_recommendations(report))
    recommendations.extend(performance_recommendations(report))

    return recommendations


# ==========================================================
# CPU
# ==========================================================

def cpu_recommendations(report: dict) -> list[dict]:
    recommendations = []

    cpu_peak = _safe(report, "cpu", "highest_temperature")

    if cpu_peak is None:
        return recommendations

    if cpu_peak >= 90:
        recommendations.append({
            "level": "Critical",
            "title": "CPU Running Extremely Hot",
            "message": (
                "CPU temperatures exceeded 90°C. "
                "Inspect cooling immediately."
            ),
        })

    elif cpu_peak >= 80:
        recommendations.append({
            "level": "Warning",
            "title": "CPU Temperature Elevated",
            "message": "Monitor CPU cooling performance.",
        })

    return recommendations


# ==========================================================
# GPU
# ==========================================================

def gpu_recommendations(report: dict) -> list[dict]:
    recommendations = []

    gpu_peak = _safe(report, "gpu", "highest_temperature")

    if gpu_peak is None:
        return recommendations

    if gpu_peak >= 85:
        recommendations.append({
            "level": "Warning",
            "title": "GPU Temperature Elevated",
            "message": "Monitor GPU temperatures during gaming.",
        })

    return recommendations


# ==========================================================
# Memory
# ==========================================================

def memory_recommendations(report: dict) -> list[dict]:
    recommendations = []

    memory_peak = _safe(report, "memory", "highest_load")

    if memory_peak is None:
        return recommendations

    if memory_peak >= 90:
        recommendations.append({
            "level": "Warning",
            "title": "High Memory Usage",
            "message": (
                "Applications are consuming most of "
                "available system memory."
            ),
        })

    return recommendations


# ==========================================================
# Performance
# ==========================================================

def performance_recommendations(report: dict) -> list[dict]:
    recommendations = []

    trend = _safe(report, "performance", "trend")

    if trend == "Decreasing":
        recommendations.append({
            "level": "Information",
            "title": "Performance Trending Downward",
            "message": (
                "Average FPS has decreased over time. "
                "Monitor future sessions."
            ),
        })

    return recommendations