# core/intelligence/report.py

"""
Project Sentinel

Historical Intelligence Report

Builds the final historical intelligence report.

This module performs no rendering.
It assembles historical intelligence from the
history analysis modules.
"""

from . import recommendations

from core.history import (
    statistics,
    metrics,
    insights,
)


# ==========================================================
# Public API
# ==========================================================

def build_report(history):
    """
    Build the historical intelligence report.

    Parameters
    ----------
    history : list[Session]

    Returns
    -------
    dict
    """

    report = {

        "history": {

            "total_sessions":
                statistics.total_sessions(history),

            "total_games":
                statistics.total_games(history),

            "oldest_session":
                statistics.oldest_session(history),

            "latest_session":
                statistics.latest_session(history),

        },

        "performance": {

            "average_fps":
                metrics.average_fps(history),

            "best_session":
                insights.best_fps_session(history),

            "trend":
                insights.fps_direction(history),

        },

        "cpu": {

            "average_temperature":
                metrics.average_cpu_temperature(history),

            "highest_temperature":
                metrics.highest_cpu_temperature(history),

            "trend":
                insights.cpu_temperature_direction(history),

        },

        "gpu": {

            "average_temperature":
                metrics.average_gpu_temperature(history),

            "highest_temperature":
                metrics.highest_gpu_temperature(history),

        },

        "memory": {

            "average_load":
                metrics.average_memory_load(history),

            "highest_load":
                metrics.highest_memory_load(history),

        },

    }

    # ------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------

    report["recommendations"] = recommendations.generate(report)

    return report