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
    load_path_settings,
    save_path_settings,
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

        self._configure_storage(load_path_settings())

        self._reader = Reader()
        self._analyzer = Analyzer()
        self._health_engine = HealthEngine()
        self._report_builder = ReportBuilder()
        self._configure_analysis_service()

    def _configure_storage(self, paths) -> None:
        """Build persistence services from the current folder settings."""

        self._incoming_folder = paths["incoming_folder"]
        self._archive_folder = paths["archive_folder"]
        self._processed_folder = paths["processed_folder"]
        self._exports_folder = paths["exports_folder"]

        # ==================================================
        # Persistence
        # ==================================================

        self._store = SessionStore(
            self._processed_folder,
        )

        self._database = SessionDatabase(
            self._store,
        )

        self._archive = SessionArchive(
            database=self._database,
            archive_directory=self._archive_folder,
        )

    def _configure_analysis_service(self) -> None:
        """Wire the analysis service after persistence is configured."""

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
        return self._incoming_folder

    @property
    def settings(self):
        """Configured application folders used by this session."""
        return {
            "incoming_folder": self._incoming_folder,
            "archive_folder": self._archive_folder,
            "processed_folder": self._processed_folder,
            "exports_folder": self._exports_folder,
        }

    def save_settings(self, paths) -> None:
        """Persist paths and immediately reconfigure Sentinel services."""
        self._configure_storage(save_path_settings(paths))
        self._configure_analysis_service()

    def export_html(
        self,
        session,
    ):
        """
        Export a stored session as an HTML report.
        """

        self.refresh_session_health(session)

        return html.export(session, directory=self._exports_folder)

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
            directory=self._archive_folder / game,
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
