# core/services/analysis_service.py

"""
Project Sentinel

Analysis Service

Coordinates the complete Sentinel analysis workflow.

Transforms a raw HWiNFO CSV log into a stored Session.

The service performs no analysis itself. Instead, it
coordinates the Reader, Analyzer, Health Engine,
Report Builder, Session Database, and Session Archive.
"""

from __future__ import annotations

from pathlib import Path

from core.archive.session_archive import SessionArchive
from core.database.session_database import SessionDatabase
from core.metadata.machine import get_machine_info
from core.models.session import Session
from core.utils.hash import sha256


class AnalysisService:
    """
    Coordinates the complete Sentinel analysis workflow.
    """

    def __init__(
        self,
        *,
        reader,
        analyzer,
        health_engine,
        report_builder,
        database: SessionDatabase,
        archive: SessionArchive,
    ) -> None:

        self.reader = reader
        self.analyzer = analyzer
        self.health_engine = health_engine
        self.report_builder = report_builder
        self.database = database
        self.archive = archive

    # ======================================================
    # Public API
    # ======================================================

    def analyze(
        self,
        *,
        csv_path: Path | str,
        game: str,
    ) -> Session | None:
        """
        Analyze a HWiNFO CSV log.

        Returns
        -------
        Session
            Newly archived session.

        None
            If this CSV has already been analyzed.
        """

        csv_path = Path(csv_path)

        # --------------------------------------------------
        # Duplicate Detection
        # --------------------------------------------------

        file_hash = sha256(csv_path)

        if self.database.contains_hash(file_hash):
            return None

        # --------------------------------------------------
        # Read Log
        # --------------------------------------------------

        log = self.reader.read(csv_path)

        # --------------------------------------------------
        # Analyze Sensor Data
        # --------------------------------------------------

        analysis = self.analyzer.analyze(log)

        # --------------------------------------------------
        # Evaluate Hardware Health
        # --------------------------------------------------

        health = self.health_engine.evaluate(analysis)

        # --------------------------------------------------
        # Gather Machine Metadata
        # --------------------------------------------------

        machine = get_machine_info()

        # --------------------------------------------------
        # Build Report
        # --------------------------------------------------

        report = self.report_builder.build(
            analysis=analysis,
            health=health,
            machine=machine,
        )

        # --------------------------------------------------
        # Archive Session
        # --------------------------------------------------

        session = self.archive.archive(
            game=game,
            csv_path=csv_path,
            report=report,
            hash=file_hash,
        )

        return session