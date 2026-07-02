# core/intelligence/engine.py

"""
Project Sentinel

Historical Intelligence Engine

Coordinates the historical intelligence pipeline.

History
    ↓
Historical Report
    ↓
Renderer
"""

from core.history.loader import load_history

from .report import build_report


# ==========================================================
# Public API
# ==========================================================

def run():
    """
    Execute the historical intelligence pipeline.

    Returns
    -------
    dict
        Historical intelligence report.
    """

    history = load_history()

    return build_report(history)