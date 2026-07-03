# core/database/session_database.py

"""
Project Sentinel

Session Database

High-level interface for querying Session objects.

This class provides searching, filtering, and statistics
while delegating persistence to SessionStore.
"""

from __future__ import annotations

from datetime import datetime

from core.database.session_store import SessionStore
from core.models.session import Session


class SessionDatabase:
    """
    High-level interface for Session objects.
    """

    def __init__(self, store: SessionStore) -> None:
        self.store = store
        self._load()

    # ======================================================
    # Internal
    # ======================================================

    def _load(self) -> None:
        """
        Load all sessions from the backing store.
        """

        self._sessions: dict[str, Session] = {
            session.id: session
            for session in self.store.load_all()
        }

    # ======================================================
    # Public
    # ======================================================

    def reload(self) -> None:
        """
        Reload all sessions from disk.
        """

        self._load()

    # ======================================================
    # CRUD
    # ======================================================

    def save(self, session: Session) -> None:
        """
        Save a session.
        """

        self.store.save(session)
        self._sessions[session.id] = session

    def delete(self, session_id: str) -> None:
        """
        Delete a session.
        """

        self.store.delete(session_id)
        self._sessions.pop(session_id, None)

    # ======================================================
    # Retrieval
    # ======================================================

    def find(self, session_id: str) -> Session | None:
        """
        Find a session by its ID.
        """

        return self._sessions.get(session_id)

    def all(self) -> list[Session]:
        """
        Return every stored session.
        """

        return sorted(self._sessions.values())

    def latest(self) -> Session | None:
        """
        Return the newest stored session.
        """

        sessions = self.all()

        return sessions[-1] if sessions else None

    # ======================================================
    # Queries
    # ======================================================

    def by_game(self, game: str) -> list[Session]:
        """
        Return every session for a game.
        """

        return sorted(
            session
            for session in self._sessions.values()
            if session.game == game
        )

    def latest_for_game(
        self,
        game: str,
    ) -> Session | None:
        """
        Return the newest session for a game.
        """

        sessions = self.by_game(game)

        return sessions[-1] if sessions else None

    def by_date(
        self,
        start: datetime,
        end: datetime,
    ) -> list[Session]:
        """
        Return every session within a date range.
        """

        return sorted(
            session
            for session in self._sessions.values()
            if start <= session.date <= end
        )

    def games(self) -> list[str]:
        """
        Return every unique game.
        """

        return sorted(
            {
                session.game
                for session in self._sessions.values()
            }
        )

    # ======================================================
    # Statistics
    # ======================================================

    def count(self) -> int:
        """
        Return the number of stored sessions.
        """

        return len(self)

    def empty(self) -> bool:
        """
        Determine whether the database is empty.
        """

        return not self._sessions

    def __contains__(self, session_id: str) -> bool:
        """
        Determine whether a session exists.
        """

        return session_id in self._sessions

    def contains_hash(
            self,
            file_hash: str,
    ) -> bool:
        """
        Determine whether a session already exists for a file hash.
        """

        return any(
            session.hash == file_hash
            for session in self._sessions.values()
        )

    # ======================================================
    # Python Protocols
    # ======================================================

    def __len__(self) -> int:
        """
        Return the number of stored sessions.
        """

        return len(self._sessions)

    def __iter__(self):
        """
        Iterate over all sessions.
        """

        return iter(self.all())

    def __contains__(self, session_id: str) -> bool:
        """
        Determine whether a session exists.
        """

        return session_id in self._sessions

