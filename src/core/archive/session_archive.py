# core/archive/session_archive.py

"""
Project Sentinel

Session Archive

Coordinates creation and archival of Sentinel sessions.

This class is responsible for creating Session objects,
archiving source CSV files, assigning session numbers,
and storing completed sessions.

It serves as the orchestration layer between the analyzer
and the database.
"""

from __future__ import annotations

import shutil

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from core.database.session_database import SessionDatabase
from core.models.report import Report
from core.models.session import Session


class SessionArchive:
    """
    Creates and archives Sentinel sessions.
    """

    def __init__(
        self,
        database: SessionDatabase,
        archive_directory: Path | str,
    ) -> None:

        self.database = database

        self.archive_directory = Path(archive_directory)
        self.archive_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ======================================================
    # Public
    # ======================================================

    def archive(
        self,
        *,
        game: str,
        csv_path: Path | str,
        report: Report,
        hash: str,
    ) -> Session:
        """
        Archive a completed analysis session.
        """

        csv_path = Path(csv_path)

        session_id = self._generate_id()

        session_number = self._next_session_number(
            game
        )

        archive_path = self._archive_path(
            game,
            session_number,
        )

        self._archive_csv(
            csv_path,
            archive_path,
        )

        session = Session(
            id=session_id,
            game=game,
            session_number=session_number,
            filename=csv_path.name,
            archive_path=str(archive_path),
            hash=hash,
            analyzed_at=datetime.now().isoformat(),
            report=report,
        )

        self.database.save(session)

        return session

    # ======================================================
    # Internal Helpers
    # ======================================================

    def _generate_id(self) -> str:
        """
        Generate a unique session identifier.
        """

        return uuid4().hex

    def _next_session_number(
        self,
        game: str,
    ) -> int:
        """
        Determine the next session number for a game.
        """

        latest = self.database.latest_for_game(
            game
        )

        if latest is None:
            return 1

        return latest.session_number + 1

    def _archive_path(
        self,
        game: str,
        session_number: int,
    ) -> Path:
        """
        Build the destination path for the archived CSV.
        """

        destination = (
            self.archive_directory / game
        )

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        return (
            destination
            / f"Session_{session_number:03d}.csv"
        )

    def _archive_csv(
            self,
            source: Path,
            destination: Path,
    ) -> None:
        """
        Move the original CSV into the archive.
        """

        shutil.move(
            str(source),
            str(destination),
        )