# core/intelligence/report.py

"""
Project Sentinel

Historical Intelligence Report

Builds the complete historical intelligence report.

This module coordinates the intelligence pipeline.
It performs no calculations itself.
"""

from __future__ import annotations

from core.models.session import Session

from . import historical
from . import insights
from . import metrics
from . import recommendations


# ==========================================================
# Helpers
# ==========================================================

def _session(
    session: Session | None,
) -> dict | None:
    """
    Convert a Session into report-safe primitives.
    """

    if session is None:
        return None

    return {
        "game": session.game,
        "session_number": session.session_number,
        "display_name": session.display_name,
        "date": session.analyzed_at,
    }


def _oldest_session(
    history: list[Session],
) -> Session | None:
    """
    Return the oldest session.
    """

    if not history:
        return None

    return min(
        history,
        key=lambda session: session.analyzed_at,
    )


def _latest_session(
    history: list[Session],
) -> Session | None:
    """
    Return the most recent session.
    """

    if not history:
        return None

    return max(
        history,
        key=lambda session: session.analyzed_at,
    )


# ==========================================================
# Public API
# ==========================================================

def build_report(
    history: list[Session],
    game: str,
) -> dict:
    """
    Build the complete historical intelligence report.
    """

    report = {

        # --------------------------------------------------
        # Game
        # --------------------------------------------------

        "game": {

            "name": game,

            "sessions": len(history),

            "first_session": _session(
                _oldest_session(history)
            ),

            "latest_session": _session(
                _latest_session(history)
            ),
        },

        # --------------------------------------------------
        # Performance
        # --------------------------------------------------

        "performance": {

            "average_fps":
                metrics.average_fps(history),

            "best_session":
                _session(
                    insights.best_fps_session(history)
                ),

            "trend":
                insights.fps_direction(history),

            "intelligence":
                historical.performance(history),
        },

        # --------------------------------------------------
        # CPU
        # --------------------------------------------------

        "cpu": {

            "average_temperature":
                metrics.average_cpu_temperature(history),

            "highest_temperature":
                metrics.highest_cpu_temperature(history),

            "trend":
                insights.cpu_temperature_direction(history),

            "intelligence":
                historical.cpu(history),
        },

        # --------------------------------------------------
        # GPU
        # --------------------------------------------------

        "gpu": {

            "average_temperature":
                metrics.average_gpu_temperature(history),

            "highest_temperature":
                metrics.highest_gpu_temperature(history),

            "trend":
                insights.gpu_temperature_direction(history),

            "intelligence":
                historical.gpu(history),
        },

        # --------------------------------------------------
        # Memory
        # --------------------------------------------------

        "memory": {

            "average_load":
                metrics.average_memory_load(history),

            "highest_load":
                metrics.highest_memory_load(history),

            "trend":
                insights.memory_usage_direction(history),

            "intelligence":
                historical.memory(history),
        },
    }

    # ------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------

    report["recommendations"] = (
        recommendations.generate(history)
    )

    return report