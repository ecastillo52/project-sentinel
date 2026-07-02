# core/intelligence/analyzer.py

"""
Project Sentinel

Historical Analyzer

Coordinates historical analysis modules.

This module performs no rendering.
"""

from core.history import (
    statistics,
    metrics,
    trends,
    insights,
)


# ==========================================================
# Public API
# ==========================================================

def analyze(history):
    """
    Analyze historical Sentinel sessions.

    Parameters
    ----------
    history : list[Session]

    Returns
    -------
    dict
        Historical analysis.
    """

    return {

        "statistics": {

            "total_sessions":
                statistics.total_sessions(history),

            "total_games":
                statistics.total_games(history),

            "latest_session":
                statistics.latest_session(history),

            "oldest_session":
                statistics.oldest_session(history),

        },

        "metrics": {

            "average_fps":
                metrics.average_fps(history),

            "average_cpu_temperature":
                metrics.average_cpu_temperature(history),

            "average_gpu_temperature":
                metrics.average_gpu_temperature(history),

            "average_memory_load":
                metrics.average_memory_load(history),

            "highest_cpu_temperature":
                metrics.highest_cpu_temperature(history),

            "highest_gpu_temperature":
                metrics.highest_gpu_temperature(history),

            "highest_memory_load":
                metrics.highest_memory_load(history),

        },

        "trends": {

            "fps":
                trends.average_sensor_trend(
                    history,
                    "fps",
                ),

            "cpu_temperature":
                trends.average_sensor_trend(
                    history,
                    "cpu_temp",
                ),

            "gpu_temperature":
                trends.average_sensor_trend(
                    history,
                    "gpu_temp",
                ),

            "memory_load":
                trends.average_sensor_trend(
                    history,
                    "memory_load",
                ),

        },

        "insights": {

            "best_fps_session":
                insights.best_fps_session(history),

            "hottest_cpu_session":
                insights.hottest_cpu_session(history),

            "fps_direction":
                insights.fps_direction(history),

            "cpu_temperature_direction":
                insights.cpu_temperature_direction(history),

        },

    }