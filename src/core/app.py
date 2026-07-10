# core/app.py

"""
Project Sentinel

Application

Constructs and wires together every major Sentinel
component.

This is the application's composition root.

No business logic belongs here.
"""

from __future__ import annotations

from core.archive.session_archive import SessionArchive

from core.config import (
    ARCHIVE_FOLDER,
    INCOMING_FOLDER,
    PROCESSED_FOLDER,
)

from core.database.session_database import SessionDatabase
from core.database.session_store import SessionStore

from core.engine.analyzer import Analyzer
from core.engine.health_engine import HealthEngine
from core.engine.recommendation import (
    generate as build_recommendations,
)
from core.engine.reader import Reader
from core.engine.summary import build_summary

from core.report.builder import ReportBuilder

from core.services.analysis_service import AnalysisService
from core.models.sensor import Sensor
from core.visualization import html


class App:
    """
    Sentinel application.

    Responsible for constructing and exposing the
    application's top-level services.
    """

    def __init__(self) -> None:

        # ==================================================
        # Persistence
        # ==================================================

        self._store = SessionStore(
            PROCESSED_FOLDER,
        )

        self._database = SessionDatabase(
            self._store,
        )

        self._archive = SessionArchive(
            database=self._database,
            archive_directory=ARCHIVE_FOLDER,
        )

        # ==================================================
        # Engine
        # ==================================================

        self._reader = Reader()

        self._analyzer = Analyzer()

        self._health_engine = HealthEngine()

        self._report_builder = ReportBuilder()

        # ==================================================
        # Services
        # ==================================================

        self._analysis = AnalysisService(
            reader=self._reader,
            analyzer=self._analyzer,
            health_engine=self._health_engine,
            report_builder=self._report_builder,
            database=self._database,
            archive=self._archive,
        )

    # ======================================================
    # Public Services
    # ======================================================

    @property
    def analysis(self) -> AnalysisService:
        """
        High-level analysis service.
        """
        return self._analysis

    @property
    def sessions(self) -> SessionDatabase:
        """
        High-level session database.
        """
        return self._database

    @property
    def incoming_folder(self):
        """
        Folder containing new HWiNFO logs.
        """
        return INCOMING_FOLDER

    def export_html(
        self,
        session,
    ):
        """
        Export a stored session as an HTML report.
        """

        self.refresh_session_health(session)

        return html.export(session)

    def export_game_trends(
        self,
        game: str,
    ):
        """
        Export the rolling trend report for a game.
        """

        for session in self.sessions.by_game(game):
            self.refresh_session_health(session)

        return html.export_game(
            self.sessions.by_game(game),
            game=game,
            directory=ARCHIVE_FOLDER / game,
        )

    def export_all_game_trends(self):
        """
        Export rolling trend reports for every known game.
        """

        return [
            self.export_game_trends(game)
            for game in self.sessions.games()
        ]

    def refresh_session_health(
        self,
        session,
    ):
        """
        Re-evaluate stored session health metadata.
        """

        sensors = [
            sensor
            for sensor in session.report.sensors.values()
            if isinstance(sensor, Sensor)
        ]

        self._health_engine.evaluate(sensors)

        session.report.health = {
            sensor.id: sensor.status
            for sensor in sensors
        }

        session.report.summary = build_summary(
            session.report
        )

        session.report.recommendations = (
            build_recommendations(session.report)
        )

        self.sessions.save(session)

        return session
