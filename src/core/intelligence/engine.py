# core/intelligence/engine.py

"""
Project Sentinel

Historical Intelligence Engine

Coordinates the historical analysis pipeline.

History
    ↓
Analyzer
    ↓
Historical Report
"""

from core.history.loader import load_history

from .analyzer import analyze
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

    analysis = analyze(history)

    return build_report(
        history,
        analysis,
    )