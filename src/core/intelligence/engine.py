"""
Project Sentinel

Historical Intelligence Engine

Coordinates the historical intelligence pipeline.

History
    ↓
Game Filter
    ↓
Historical Report
    ↓
Renderer
"""

from core.history.loader import load_history
from core.history.game_history import sessions_for_game

from .report import build_report


# ==========================================================
# Public API
# ==========================================================

def run(
    game: str,
) -> dict:
    """
    Execute the historical intelligence pipeline for a
    single game.

    Parameters
    ----------
    game : str

    Returns
    -------
    dict
        Historical intelligence report.
    """

    history = load_history()

    history = sessions_for_game(
        history,
        game,
    )

    return build_report(
        history,
        game,
    )