# core/history/timeline.py

"""
Project Sentinel

Historical Timeline

Utilities for building chronological session history.
"""


# ==========================================================
# Public API
# ==========================================================

def recent_sessions(history, limit=10):
    """
    Return the newest sessions.

    Parameters
    ----------
    history : list[Session]

    limit : int

    Returns
    -------
    list[dict]
    """

    if not history:
        return []

    newest = sorted(
        history,
        key=lambda session: session.date,
        reverse=True,
    )[:limit]

    return [
        {
            "game": session.game,
            "session": session.session_number,
            "date": session.date,
        }
        for session in newest
    ]