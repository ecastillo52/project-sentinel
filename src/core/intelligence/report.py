# core/intelligence/report.py

"""
Project Sentinel

Historical Intelligence Report

Builds the final historical intelligence report.

This module performs no calculations.
It only structures analyzed data.
"""


# ==========================================================
# Public API
# ==========================================================

def build_report(
    history,
    analysis,
):
    """
    Build a historical intelligence report.

    Parameters
    ----------
    history : list[Session]

    analysis : dict

    Returns
    -------
    dict
    """

    return {

        "history": {

            "total_sessions":
                analysis["statistics"]["total_sessions"],

            "total_games":
                analysis["statistics"]["total_games"],

            "oldest_session":
                analysis["statistics"]["oldest_session"],

            "latest_session":
                analysis["statistics"]["latest_session"],

        },

        "performance": {

            "average_fps":
                analysis["metrics"]["average_fps"],

            "best_session":
                analysis["insights"]["best_fps_session"],

            "trend":
                analysis["insights"]["fps_direction"],

        },

        "cpu": {

            "average_temperature":
                analysis["metrics"]["average_cpu_temperature"],

            "highest_temperature":
                analysis["metrics"]["highest_cpu_temperature"],

            "trend":
                analysis["insights"]["cpu_temperature_direction"],

        },

        "gpu": {

            "average_temperature":
                analysis["metrics"]["average_gpu_temperature"],

            "highest_temperature":
                analysis["metrics"]["highest_gpu_temperature"],

        },

        "memory": {

            "average_load":
                analysis["metrics"]["average_memory_load"],

            "highest_load":
                analysis["metrics"]["highest_memory_load"],

        },

    }