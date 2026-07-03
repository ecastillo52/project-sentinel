# core/models/session.py

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

from __future__ import annotations

import json

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from core.models.report import Report


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

    report: Report = field(default_factory=Report)

    # ======================================================
    # Convenience Properties
    # ======================================================

    @property
    def archive(self) -> Path:
        """
        Return the archived CSV path.
        """
        return Path(self.archive_path)

    @property
    def date(self) -> datetime:
        """
        Return the analysis timestamp.
        """
        return datetime.fromisoformat(self.analyzed_at)

    @property
    def label(self) -> str:
        """
        Example:
            Session 3
        """
        return f"Session {self.session_number}"

    @property
    def display_name(self) -> str:
        """
        Example:
            Cyberpunk - Session 5
        """
        return f"{self.game} - {self.label}"

    @property
    def json_filename(self) -> str:
        """
        Filename used when saving this session.
        """
        return f"{self.id}.json"

    @property
    def age(self):
        """
        Time elapsed since analysis.
        """
        return datetime.now() - self.date

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict:
        """
        Convert the session into the Sentinel database format.
        """

        return {
            "id": self.id,
            "game": {
                "name": self.game,
                "session": self.session_number,
            },
            "source": {
                "filename": self.filename,
                "archive_path": self.archive_path,
                "hash": self.hash,
            },
            "analysis": {
                "created": self.analyzed_at,
                "version": self.version,
                "engine": self.engine,
            },
            "report": self.report.to_dict(),
        }

    def to_json(self, *, indent: int = 4) -> str:
        """
        Serialize the session as JSON.
        """
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
        )

    def save(self, path: Path) -> None:
        """
        Save this session to disk.
        """
        path.write_text(
            self.to_json(),
            encoding="utf-8",
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        """
        Build a Session from either the new or legacy
        Sentinel database schema.
        """

        # --------------------------------------------------
        # New schema
        # --------------------------------------------------

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
                    "0.2.0",
                ),
                engine=data["analysis"].get(
                    "engine",
                    "Sentinel Analysis Engine",
                ),
                report=Report.from_dict(
                    data.get("report", {})
                ),
            )

        # --------------------------------------------------
        # Legacy schema
        # --------------------------------------------------

        return cls(
            id=data["id"],
            game=data.get("game", "Unknown"),
            session_number=data.get(
                "session_number",
                1,
            ),
            filename=data["filename"],
            archive_path=data["archive_path"],
            hash=data["hash"],
            analyzed_at=data["analyzed_at"],
            version="0.1.0",
            engine="Legacy Database",
            report=Report.from_dict(
                data.get("report", {})
            ),
        )

    @classmethod
    def from_json(cls, text: str) -> "Session":
        """
        Build a Session from a JSON string.
        """
        return cls.from_dict(json.loads(text))

    @classmethod
    def load(cls, path: Path) -> "Session":
        """
        Load a Session from disk.
        """
        return cls.from_json(
            path.read_text(encoding="utf-8")
        )

    # ======================================================
    # Comparisons
    # ======================================================

    def __eq__(self, other):
        if not isinstance(other, Session):
            return NotImplemented

        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Session):
            return NotImplemented

        return self.date < other.date

    # ======================================================
    # Display
    # ======================================================

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return (
            f"Session("
            f"id='{self.id}', "
            f"game='{self.game}', "
            f"session={self.session_number})"
        )