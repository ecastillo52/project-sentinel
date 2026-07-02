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
# Public API
# ==========================================================

def generate(report):
    """
    Generate recommendations from a historical report.

    Parameters
    ----------
    report : dict

    Returns
    -------
    list[dict]
        Recommendation objects.
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

def cpu_recommendations(report):
    """
    Generate CPU recommendations.
    """

    recommendations = []

    cpu = report["cpu"]

    if cpu["highest_temperature"] is None:
        return recommendations

    if cpu["highest_temperature"] >= 90:

        recommendations.append({

            "level": "Critical",

            "title": "CPU Running Extremely Hot",

            "message":
                "CPU temperatures exceeded 90°C. "
                "Inspect cooling immediately.",

        })

    elif cpu["highest_temperature"] >= 80:

        recommendations.append({

            "level": "Warning",

            "title": "CPU Temperature Elevated",

            "message":
                "Monitor CPU cooling performance.",

        })

    return recommendations


# ==========================================================
# GPU
# ==========================================================

def gpu_recommendations(report):
    """
    Generate GPU recommendations.
    """

    recommendations = []

    gpu = report["gpu"]

    if gpu["highest_temperature"] is None:
        return recommendations

    if gpu["highest_temperature"] >= 85:

        recommendations.append({

            "level": "Warning",

            "title": "GPU Temperature Elevated",

            "message":
                "Monitor GPU temperatures during gaming.",

        })

    return recommendations


# ==========================================================
# Memory
# ==========================================================

def memory_recommendations(report):
    """
    Generate memory recommendations.
    """

    recommendations = []

    memory = report["memory"]

    if memory["highest_load"] is None:
        return recommendations

    if memory["highest_load"] >= 90:

        recommendations.append({

            "level": "Warning",

            "title": "High Memory Usage",

            "message":
                "Applications are consuming most of "
                "available system memory.",

        })

    return recommendations


# ==========================================================
# Performance
# ==========================================================

def performance_recommendations(report):
    """
    Generate performance recommendations.
    """

    recommendations = []

    performance = report["performance"]

    if performance["trend"] == "Decreasing":

        recommendations.append({

            "level": "Information",

            "title": "Performance Trending Downward",

            "message":
                "Average FPS has decreased over time. "
                "Monitor future sessions.",

        })

    return recommendations