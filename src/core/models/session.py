# core/models/session.py

"""
Project Sentinel

Session Model

Represents one analyzed HWiNFO logging session.

This model provides a single object that every subsystem
works with instead of passing nested dictionaries around.

Future versions may extend this class with comparison,
trend analysis, HTML export, charts, and SQLite support.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Session:
    """
    Represents one Sentinel analysis session.
    """

    # ======================================================
    # Identity
    # ======================================================

    id: str

    # ======================================================
    # Game Information
    # ======================================================

    game: str

    session_number: int

    # ======================================================
    # Source Information
    # ======================================================

    filename: str

    archive_path: str

    hash: str

    # ======================================================
    # Analysis Information
    # ======================================================

    analyzed_at: str

    version: str = "0.2.0"

    engine: str = "Sentinel Analysis Engine"

    report: list[dict[str, Any]] = field(default_factory=list)

    # ======================================================
    # Convenience Properties
    # ======================================================

    @property
    def archive(self) -> Path:
        """
        Returns the archived CSV as a Path object.
        """

        return Path(self.archive_path)

    @property
    def date(self) -> datetime:
        """
        Returns the analysis timestamp as a datetime.
        """

        return datetime.fromisoformat(self.analyzed_at)

    @property
    def label(self) -> str:
        """
        Session 3
        """

        return f"Session {self.session_number}"

    @property
    def display_name(self) -> str:
        """
        Fortnite - Session 3
        """

        return f"{self.game} - {self.label}"

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict:
        """
        Convert Session into the Sentinel database format.
        """

        return {

            "id": self.id,

            "game": {

                "name": self.game,

                "session": self.session_number

            },

            "source": {

                "filename": self.filename,

                "archive_path": self.archive_path,

                "hash": self.hash

            },

            "analysis": {

                "created": self.analyzed_at,

                "version": self.version,

                "engine": self.engine

            },

            "report": self.report

        }

    @classmethod
    def from_dict(cls, data):
        """
        Build a Session from either the old or new
        Sentinel database format.
        """

        #
        # New schema
        #

        if isinstance(data.get("game"), dict):
            return cls(

                id=data["id"],

                game=data["game"]["name"],

                session_number=data["game"]["session"],

                filename=data["source"]["filename"],

                archive_path=data["source"]["archive_path"],

                hash=data["source"]["hash"],

                analyzed_at=data["analysis"]["created"],

                version=data["analysis"].get(
                    "version",
                    "0.2.0"
                ),

                engine=data["analysis"].get(
                    "engine",
                    "Sentinel Analysis Engine"
                ),

                report=data.get(
                    "report",
                    []
                ),
            )

        #
        # Legacy schema
        #

        return cls(

            id=data["id"],

            game=data.get("game", "Unknown"),

            session_number=data.get(
                "session_number",
                1
            ),

            filename=data["filename"],

            archive_path=data["archive_path"],

            hash=data["hash"],

            analyzed_at=data["analyzed_at"],

            version="0.1.0",

            engine="Legacy Database",

            report=data.get(
                "report",
                []
            ),
        )

    # ======================================================
    # Display
    # ======================================================

    def __str__(self):

        return self.display_name

    def __repr__(self):

        return (
            f"Session("
            f"game='{self.game}', "
            f"session={self.session_number})"
        )