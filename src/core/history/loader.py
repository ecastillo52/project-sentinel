# core/history/loader.py

"""
Project Sentinel

History Loader

Provides access to historical Sentinel sessions.

This module performs no analysis.
It only loads previously saved sessions.
"""

from core.models.session import Session
from core.metadata.history import get_all_sessions


def load_history() -> list[Session]:
    """
    Load every historical Sentinel session.
    """

    return get_all_sessions()