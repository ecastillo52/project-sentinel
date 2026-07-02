# core/intelligence/report.py

"""
Project Sentinel

Historical Intelligence Report

Builds the final historical intelligence report.

This module performs no rendering.
It assembles historical intelligence from the
history analysis modules.
"""

from . import (
    historical,
    recommendations,
)

from core.history import (
    statistics,
    metrics,
    insights,
)


# ==========================================================
# Helpers
# ==========================================================

def _session_safe(session):
    """
    Convert Session objects into safe primitives for reporting.
    """

    if session is None:
        return None

    return {
        "game": getattr(session, "game", None),
        "session_number": getattr(session, "session_number", None),
        "date": getattr(session, "date", None),
        "display_name": getattr(session, "display_name", None),
    }


# ==========================================================
# Public API
# ==========================================================

def build_report(history, game: str) -> dict:
    """
    Build the historical intelligence report.
    """

    report = {
        # --------------------------------------------------
        # Game Overview
        # --------------------------------------------------
        "game": {
            "name": game,
            "sessions": statistics.total_sessions(history),
            "first_session": _session_safe(statistics.oldest_session(history)),
            "latest_session": _session_safe(statistics.latest_session(history)),
        },

        # --------------------------------------------------
        # Performance
        # --------------------------------------------------
        "performance": {
            "average_fps": metrics.average_fps(history),
            "best_session": _session_safe(insights.best_fps_session(history)),
            "trend": insights.fps_direction(history),
            "intelligence": historical.performance(history),
        },

        # --------------------------------------------------
        # CPU
        # --------------------------------------------------
        "cpu": {
            "average_temperature": metrics.average_cpu_temperature(history),
            "highest_temperature": metrics.highest_cpu_temperature(history),
            "trend": insights.cpu_temperature_direction(history),
            "intelligence": historical.cpu(history),
        },

        # --------------------------------------------------
        # GPU
        # --------------------------------------------------
        "gpu": {
            "average_temperature": metrics.average_gpu_temperature(history),
            "highest_temperature": metrics.highest_gpu_temperature(history),

            # FIX: GPU does NOT reuse CPU trend
            "trend": "Unknown",

            "intelligence": historical.gpu(history),
        },

        # --------------------------------------------------
        # Memory
        # --------------------------------------------------
        "memory": {
            "average_load": metrics.average_memory_load(history),
            "highest_load": metrics.highest_memory_load(history),

            # FIX: Memory does NOT reuse CPU trend
            "trend": "Unknown",

            "intelligence": historical.memory(history),
        },
    }

    # ------------------------------------------------------
    # Recommendations (post-processing step)
    # ------------------------------------------------------
    report["recommendations"] = recommendations.generate(report)

    return report