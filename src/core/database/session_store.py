# core/database/session_store.py

"""
Project Sentinel

Session Store

Low-level persistence layer responsible for reading and
writing Session objects to disk.

The SessionStore knows nothing about querying or searching.
It simply manages JSON files.
"""

from __future__ import annotations

from pathlib import Path

from core.models.session import Session


class SessionStore:
    """
    Handles persistence of Session objects.
    """

    def __init__(self, directory: Path | str) -> None:

        self._directory = Path(directory)
        self._directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def path(self) -> Path:
        """
        Root directory used for session storage.
        """

        return self._directory

    # ======================================================
    # Helpers
    # ======================================================

    def session_path(self, session_id: str) -> Path:
        """
        Return the JSON path for a session.
        """

        return self._directory / f"{session_id}.json"

    # ======================================================
    # CRUD
    # ======================================================

    def save(self, session: Session) -> None:
        """
        Save a Session to disk.
        """

        session.save(self.session_path(session.id))

    def load(self, session_id: str) -> Session:
        """
        Load a Session from disk.
        """

        return Session.load(
            self.session_path(session_id)
        )

    def delete(self, session_id: str) -> None:
        """
        Delete a stored Session.
        """

        self.session_path(session_id).unlink(
            missing_ok=True
        )

    def exists(self, session_id: str) -> bool:
        """
        Determine whether a Session exists.
        """

        return self.session_path(session_id).exists()

    # ======================================================
    # Enumeration
    # ======================================================

    def load_all(self) -> list[Session]:
        """
        Load every stored Session.
        """

        sessions = sorted(
            (
                Session.load(path)
                for path in self._directory.glob("*.json")
            )
        )

        return sessions

    # ======================================================
    # Python Protocols
    # ======================================================

    def __len__(self) -> int:
        """
        Return the number of stored session files.
        """

        return len(list(self._directory.glob("*.json")))