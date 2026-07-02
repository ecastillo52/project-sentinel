# core/history/loader.py

"""
Project Sentinel

History Loader

Provides access to historical Sentinel sessions.

This module performs no analysis.
It only loads previously saved sessions.
"""

from core.metadata.history import get_sessions
from core.models.session import Session


def load_history() -> list[Session]:
    """
    Load every historical Sentinel session.
    """

    return get_sessions()