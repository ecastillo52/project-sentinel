"""PySide6 desktop interface for Project Sentinel.

This module is deliberately a presentation layer: analysis remains in
``AnalysisService`` and all session data continues to live in the existing
database models.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPixmap, QPolygon
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QFileDialog, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow,
    QMessageBox, QPushButton, QScrollArea, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget, QSplitter,
)

from core.app import App
from core.engine.scanner import find_logs
from core.metadata.game_detector import detect_game, learn_alias
from core.models.sensor import Sensor


ACCENT = "#28d7a1"
PANEL = "#17212b"
BACKGROUND = "#0d141b"


def _value(value: Any, unit: str = "") -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        value = round(value, 1)
    return f"{value}{unit}".strip()


def _sensor(session, sensor_id: str) -> Sensor | None:
    candidate = session.report.sensors.get(sensor_id)
    return candidate if isinstance(candidate, Sensor) else None


class Logo(QLabel):
    """Small programmatic shield mark, avoiding an external asset dependency."""

    def __init__(self) -> None:
        super().__init__()
        pixmap = QPixmap(46, 52)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(ACCENT))
        painter.setBrush(QColor("#123f39"))
        painter.drawPolygon(QPolygon([
            QPoint(23, 2), QPoint(43, 10), QPoint(39, 35),
            QPoint(23, 49), QPoint(7, 35), QPoint(3, 10),
        ]))
        painter.setPen(QColor("#d9fff3"))
        painter.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "S")
        painter.end()
        self.setPixmap(pixmap)


class MetricCard(QFrame):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.setObjectName("metricCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 13, 16, 13)
        title = QLabel(label.upper())
        title.setObjectName("metricLabel")
        self.value = QLabel("—")
        self.value.setObjectName("metricValue")
        self.status = QLabel("No session loaded")
        self.status.setObjectName("metricStatus")
        layout.addWidget(title)
        layout.addWidget(self.value)
        layout.addWidget(self.status)

    def set_sensor(self, sensor: Sensor | None) -> None:
        if sensor is None:
            self.value.setText("—")
            self.status.setText("Not recorded")
            return
        self.value.setText(_value(sensor.current, sensor.unit))
        self.status.setText(sensor.status.title())


class TrendChart(QWidget):
    """A lightweight Qt chart for a metric across a game's saved sessions."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title
        self.values: list[float] = []
        self.unit = ""
        self.setMinimumHeight(165)
        self.setObjectName("trendChart")

    def set_values(self, values: list[float], unit: str) -> None:
        self.values, self.unit = values, unit
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(12, 12, -12, -12)
        painter.setPen(QColor("#b8c8d4"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        painter.drawText(rect.left(), rect.top() + 12, self.title)
        if not self.values:
            painter.setPen(QColor("#91a5b5"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No recorded data")
            return
        plot = rect.adjusted(0, 28, 0, -20)
        low, high = min(self.values), max(self.values)
        span = high - low or 1
        painter.setPen(QPen(QColor("#2a3b47"), 1))
        painter.drawLine(plot.bottomLeft(), plot.bottomRight())
        painter.drawLine(plot.bottomLeft(), plot.topLeft())
        points = []
        for index, value in enumerate(self.values):
            x = plot.left() + (plot.width() * index / max(1, len(self.values) - 1))
            y = plot.bottom() - (plot.height() * (value - low) / span)
            points.append((int(x), int(y)))
        painter.setPen(QPen(QColor(ACCENT), 2))
        for first, second in zip(points, points[1:]):
            painter.drawLine(*first, *second)
        painter.setBrush(QColor(ACCENT))
        painter.setPen(Qt.PenStyle.NoPen)
        for x, y in points:
            painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(QColor("#91a5b5"))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(plot.left(), rect.bottom(), f"{round(low, 1)}{self.unit}")
        painter.drawText(plot.right() - 55, rect.bottom(), f"{round(high, 1)}{self.unit}")


class SessionReportDialog(QDialog):
    """Resizable, single-session report opened from the history page."""

    def __init__(self, session, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Session Report - {session.display_name}")
        self.resize(1050, 650)
        self.setMinimumSize(720, 420)
        layout = QVBoxLayout(self)
        heading = QLabel(session.display_name)
        heading.setObjectName("heading")
        detail = QLabel(f"{session.analyzed_at}  |  {session.filename}")
        detail.setObjectName("description")
        layout.addWidget(heading)
        layout.addWidget(detail)
        machine = session.report.metadata.get("machine", {})
        if isinstance(machine, dict):
            machine_info = QLabel(
                "Machine information: "
                f"CPU: {machine.get('cpu', 'Unknown')}  |  "
                f"GPU: {machine.get('gpu', 'Unknown')}  |  "
                f"RAM: {machine.get('ram', 'Unknown')}"
            )
            machine_info.setObjectName("description")
            machine_info.setWordWrap(True)
            layout.addWidget(machine_info)
        summary = session.report.summary
        status = QLabel(
            f"Overall health: {summary.get('overall_health', 'Unknown')}     "
            f"Average FPS: {_value(summary.get('average_fps'), ' FPS')}"
        )
        status.setObjectName("healthBanner")
        layout.addWidget(status)
        table = QTableWidget(4, 1)
        table.setHorizontalHeaderLabels(["Reading"])
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        sensors = [sensor for sensor in session.report.sensors.values() if isinstance(sensor, Sensor)]
        table.setColumnCount(len(sensors) + 1)
        table.setHorizontalHeaderLabels(["Reading"] + [sensor.display or sensor.name or sensor.id for sensor in sensors])
        for row, label in enumerate(("Average", "Minimum", "Maximum", "Health")):
            table.setItem(row, 0, QTableWidgetItem(label))
        for column, sensor in enumerate(sensors, start=1):
            values = (
                _value(sensor.average, sensor.unit), _value(sensor.minimum, sensor.unit),
                _value(sensor.maximum, sensor.unit), sensor.status,
            )
            for row, value in enumerate(values):
                table.setItem(row, column, QTableWidgetItem(value))
        layout.addWidget(table, 1)
        close = QPushButton("Close")
        close.setObjectName("primary")
        close.clicked.connect(self.accept)
        layout.addWidget(close, alignment=Qt.AlignmentFlag.AlignRight)


class MainWindow(QMainWindow):
    def __init__(self, app: App) -> None:
        super().__init__()
        self.app = app
        self.current_session = None
        self.setWindowTitle("Project Sentinel")
        self.resize(1180, 760)
        self.setMinimumSize(900, 600)
        self._build()
        self.refresh_history()
        latest = self.app.sessions.latest()
        if latest:
            self.show_report(latest)
        else:
            self.show_page(0)

    def _build(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(235)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(20, 24, 20, 20)
        brand = QHBoxLayout()
        brand.addWidget(Logo())
        brand_text = QVBoxLayout()
        title = QLabel("SENTINEL")
        title.setObjectName("brand")
        subtitle = QLabel("SYSTEM PERFORMANCE")
        subtitle.setObjectName("subtitle")
        brand_text.addWidget(title); brand_text.addWidget(subtitle)
        brand.addLayout(brand_text); brand.addStretch()
        side.addLayout(brand)
        side.addSpacing(30)
        self.nav_buttons: list[QPushButton] = []
        for label, index in (("Overview", 0), ("Analyze Latest Log", 1), ("History", 2), ("Compare Sessions", 3), ("Settings", 4)):
            button = QPushButton(label)
            button.setObjectName("nav")
            button.clicked.connect(lambda checked=False, i=index: self.show_page(i))
            side.addWidget(button)
            self.nav_buttons.append(button)
        side.addStretch()
        exit_button = QPushButton("Exit")
        exit_button.setObjectName("exitButton")
        exit_button.clicked.connect(self.close)
        side.addWidget(exit_button)
        layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.pages.addWidget(self._overview_page())
        self.pages.addWidget(self._analyze_page())
        self.pages.addWidget(self._history_page())
        self.pages.addWidget(self._compare_page())
        self.pages.addWidget(self._settings_page())
        layout.addWidget(self.pages, 1)
        self.setStyleSheet(STYLESHEET)

    def _page(self, title: str, description: str) -> tuple[QWidget, QVBoxLayout]:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(34, 28, 34, 28)
        heading = QLabel(title)
        heading.setObjectName("heading")
        detail = QLabel(description)
        detail.setObjectName("description")
        layout.addWidget(heading); layout.addWidget(detail)
        return page, layout

    def _overview_page(self) -> QWidget:
        page, layout = self._page("Game Performance Overview", "Trends and aggregate metrics across every recorded session for a game.")
        chooser = QHBoxLayout()
        chooser.addWidget(QLabel("Game"))
        self.overview_game = QComboBox()
        self.overview_game.currentTextChanged.connect(self.refresh_overview)
        chooser.addWidget(self.overview_game, 1)
        layout.addLayout(chooser)
        self.overview_session = QLabel("Choose a game to view its history")
        self.overview_session.setObjectName("sessionTitle")
        layout.addWidget(self.overview_session)
        grid = QGridLayout(); grid.setSpacing(12)
        self.cards = {}
        for index, (key, name) in enumerate((
            ("cpu_temp", "CPU Temperature"), ("gpu_temp", "GPU Temperature"),
            ("cpu_usage", "CPU Usage"), ("gpu_usage", "GPU Usage"),
            ("memory_load", "RAM Usage"), ("fps", "Frame Rate"),
        )):
            card = MetricCard(name); self.cards[key] = card
            grid.addWidget(card, index // 3, index % 3)
        layout.addLayout(grid)
        self.health_label = QLabel("Overall game health: —")
        self.health_label.setObjectName("healthBanner")
        layout.addWidget(self.health_label)
        layout.addSpacing(12)
        report_section = QWidget()
        report_layout = QVBoxLayout(report_section)
        report_layout.setContentsMargins(0, 0, 0, 0)
        report_title = QLabel("Game Sensor Report")
        report_title.setObjectName("sectionTitle")
        report_layout.addWidget(report_title)
        self.sensor_table = QTableWidget(0, 1)
        self.sensor_table.setHorizontalHeaderLabels(["Reading"])
        self.sensor_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.sensor_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sensor_table.horizontalHeader().setStretchLastSection(True)
        self.sensor_table.setMinimumHeight(240)
        report_layout.addWidget(self.sensor_table, 1)
        trends_section = QWidget()
        trends_layout = QVBoxLayout(trends_section)
        trends_layout.setContentsMargins(0, 0, 0, 0)
        chart_title = QLabel("Performance Trends")
        chart_title.setObjectName("sectionTitle")
        trends_layout.addWidget(chart_title)
        charts = QGridLayout(); charts.setSpacing(12)
        self.trend_charts = {}
        for index, (sensor_id, title) in enumerate((
            ("fps", "FPS over sessions"), ("cpu_temp", "CPU temperature"),
            ("gpu_temp", "GPU temperature"), ("cpu_usage", "CPU usage"),
            ("gpu_usage", "GPU usage"), ("memory_load", "RAM usage"),
        )):
            chart = TrendChart(title); self.trend_charts[sensor_id] = chart
            charts.addWidget(chart, index // 3, index % 3)
        trends_layout.addLayout(charts)
        self.overview_splitter = QSplitter(Qt.Orientation.Vertical)
        self.overview_splitter.setChildrenCollapsible(False)
        self.overview_splitter.addWidget(report_section)
        self.overview_splitter.addWidget(trends_section)
        self.overview_splitter.setSizes([360, 420])
        self.overview_splitter.setMinimumHeight(620)
        layout.addWidget(self.overview_splitter)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(page)
        return scroll

    def _analyze_page(self) -> QWidget:
        page, layout = self._page("Analyze Latest Logs", "Analyze HWiNFO CSV files using the existing Analysis Service.")
        self.log_list = QListWidget()
        layout.addWidget(self.log_list, 1)
        actions = QHBoxLayout()
        scan = QPushButton("Scan folder")
        scan.clicked.connect(self.scan_logs)
        analyze = QPushButton("Analyze selected")
        analyze.setObjectName("primary")
        analyze.clicked.connect(self.analyze_selected)
        actions.addWidget(scan); actions.addWidget(analyze); actions.addStretch()
        layout.addLayout(actions)
        return page

    def _history_page(self) -> QWidget:
        page, layout = self._page("Session History", "Choose a game, then select one of its recorded sessions.")
        browser = QHBoxLayout()
        games_column = QVBoxLayout()
        games_column.addWidget(QLabel("Games"))
        self.history_games = QListWidget()
        self.history_games.setMinimumWidth(210)
        self.history_games.currentTextChanged.connect(self.populate_history_sessions)
        games_column.addWidget(self.history_games, 1)
        browser.addLayout(games_column)
        sessions_column = QVBoxLayout()
        sessions_column.addWidget(QLabel("Sessions"))
        self.history_table = QTableWidget(0, 4)
        self.history_table.setHorizontalHeaderLabels(["Date", "Machine", "Average FPS", "Session"])
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.cellDoubleClicked.connect(lambda row, column: self.load_history_row(row))
        sessions_column.addWidget(self.history_table, 1)
        browser.addLayout(sessions_column, 1)
        layout.addLayout(browser, 1)
        open_report = QPushButton("Open selected report")
        open_report.setObjectName("primary")
        open_report.clicked.connect(lambda: self.load_history_row(self.history_table.currentRow()))
        layout.addWidget(open_report, alignment=Qt.AlignmentFlag.AlignLeft)
        return page

    def _compare_page(self) -> QWidget:
        page, layout = self._page("Compare Sessions", "Compare average sensor values between two recorded sessions.")
        selectors = QHBoxLayout()
        self.compare_a = QComboBox(); self.compare_b = QComboBox()
        selectors.addWidget(QLabel("Session A")); selectors.addWidget(self.compare_a, 1)
        selectors.addWidget(QLabel("Session B")); selectors.addWidget(self.compare_b, 1)
        button = QPushButton("Compare"); button.setObjectName("primary"); button.clicked.connect(self.compare_sessions)
        selectors.addWidget(button); layout.addLayout(selectors)
        self.comparison = QTableWidget(0, 4)
        self.comparison.setHorizontalHeaderLabels(["Metric", "Session A", "Session B", "Difference (B − A)"])
        self.comparison.horizontalHeader().setStretchLastSection(True)
        self.comparison.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.comparison, 1)
        return page

    def _settings_page(self) -> QWidget:
        page, layout = self._page("Settings", "Current locations supplied by Sentinel’s configuration module.")
        form = QFormLayout()
        self.settings_fields = {}
        for key, label in (
            ("incoming_folder", "HWiNFO log folder"),
            ("archive_folder", "Archived CSV folder"),
            ("processed_folder", "Session database folder"),
            ("exports_folder", "Report export folder"),
        ):
            field = QLineEdit(str(self.app.settings[key]))
            self.settings_fields[key] = field
            form.addRow(label, field)
        layout.addLayout(form)
        save = QPushButton("Save settings")
        save.setObjectName("primary")
        save.clicked.connect(self.save_settings)
        layout.addWidget(save, alignment=Qt.AlignmentFlag.AlignLeft)
        note = QLabel("Changes take effect immediately. Existing data is not moved automatically.")
        note.setWordWrap(True); note.setObjectName("description"); layout.addWidget(note); layout.addStretch()
        return page

    def save_settings(self) -> None:
        paths = {key: field.text().strip() for key, field in self.settings_fields.items()}
        if not all(paths.values()):
            QMessageBox.warning(self, "Settings", "Every folder location is required.")
            return
        try:
            self.app.save_settings(paths)
        except OSError as exc:
            QMessageBox.critical(self, "Settings", f"Could not save settings: {exc}")
            return
        self.scan_logs()
        QMessageBox.information(self, "Settings", "Settings saved.")

    def show_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        for i, button in enumerate(self.nav_buttons): button.setProperty("active", i == index); button.style().unpolish(button); button.style().polish(button)
        if index == 0: self.refresh_overview()
        if index == 1: self.scan_logs()
        if index in (2, 3): self.refresh_history()

    def scan_logs(self) -> None:
        self.log_list.clear()
        for path in find_logs(self.app.incoming_folder):
            self.log_list.addItem(str(path))
        if not self.log_list.count(): self.log_list.addItem("No CSV logs found in the configured incoming folder.")

    def analyze_selected(self) -> None:
        item = self.log_list.currentItem()
        if item is None or not Path(item.text()).is_file():
            QMessageBox.information(self, "Analyze logs", "Select a CSV log first."); return
        path = Path(item.text())
        game = detect_game(path.name)
        if game is None:
            game, keyword, ok = GameDialog.get_game(self)
            if not ok:
                return
            learn_alias(keyword or game, game)
        try:
            session = self.app.analysis.analyze(csv_path=path, game=game)
        except Exception as exc:
            QMessageBox.critical(self, "Analysis failed", str(exc)); return
        self.refresh_history()
        self.overview_game.setCurrentText(session.game)
        self.show_page(0)
        QMessageBox.information(self, "Analysis complete", f"Saved {session.display_name}.")

    def refresh_history(self) -> None:
        sessions = self.app.sessions.all()
        selected_game = self.overview_game.currentText()
        self.overview_game.blockSignals(True)
        self.overview_game.clear()
        self.overview_game.addItems(self.app.sessions.games())
        self.overview_game.setCurrentText(selected_game)
        self.overview_game.blockSignals(False)
        selected_game = self.history_games.currentItem().text() if self.history_games.currentItem() else ""
        self.history_games.blockSignals(True)
        self.history_games.clear()
        self.history_games.addItems(self.app.sessions.games())
        matches = self.history_games.findItems(selected_game, Qt.MatchFlag.MatchExactly)
        if matches:
            self.history_games.setCurrentItem(matches[0])
        elif self.history_games.count():
            self.history_games.setCurrentRow(0)
        self.history_games.blockSignals(False)
        self.populate_history_sessions(self.history_games.currentItem().text() if self.history_games.currentItem() else "")
        self.compare_a.clear(); self.compare_b.clear()
        for session in sessions:
            label = f"{session.analyzed_at} — {session.display_name}"
            self.compare_a.addItem(label, session.id); self.compare_b.addItem(label, session.id)
        if len(sessions) > 1: self.compare_b.setCurrentIndex(1)

    def populate_history_sessions(self, game: str) -> None:
        self.history_sessions = self.app.sessions.by_game(game) if game else []
        self.history_table.setRowCount(len(self.history_sessions))
        for row, session in enumerate(self.history_sessions):
            machine = session.report.metadata.get("machine", {})
            cpu = machine.get("cpu", "Unknown") if isinstance(machine, dict) else "Unknown"
            fps = session.report.summary.get("average_fps")
            values = [session.analyzed_at, str(cpu), _value(fps, " FPS"), session.label]
            for col, value in enumerate(values): self.history_table.setItem(row, col, QTableWidgetItem(value))

    def load_history_row(self, row: int) -> None:
        if 0 <= row < len(self.history_sessions):
            dialog = SessionReportDialog(self.history_sessions[row], self)
            dialog.exec()

    def show_report(self, session) -> None:
        """Open the selected session's game in the aggregate overview."""
        self.overview_game.setCurrentText(session.game)
        self.show_page(0)

    def refresh_overview(self) -> None:
        game = self.overview_game.currentText()
        sessions = self.app.sessions.by_game(game) if game else []
        if not sessions:
            self.overview_session.setText("No game sessions recorded")
            return
        self.overview_session.setText(f"{game}  ·  {len(sessions)} recorded session{'s' if len(sessions) != 1 else ''}")
        latest = sessions[-1]
        for key, card in self.cards.items():
            values = [sensor.average for session in sessions if (sensor := _sensor(session, key)) and isinstance(sensor.average, (int, float))]
            latest_sensor = _sensor(latest, key)
            if values and latest_sensor:
                aggregate = Sensor(current=sum(values) / len(values), unit=latest_sensor.unit, status=latest_sensor.status)
                card.set_sensor(aggregate)
                card.status.setText(f"{len(values)} session average{'s' if len(values) != 1 else ''}")
            else:
                card.set_sensor(None)
        health = latest.report.summary.get("overall_health", "Unknown")
        self.health_label.setText(f"Latest session health: {health}     Game average FPS: {_value(sum(v for s in sessions if (v := s.report.summary.get('average_fps')) is not None) / max(1, sum(1 for s in sessions if s.report.summary.get('average_fps') is not None)), ' FPS')}")
        self._populate_game_sensor_report(sessions)
        for sensor_id, chart in self.trend_charts.items():
            sensors = [_sensor(session, sensor_id) for session in sessions]
            values = [sensor.average for sensor in sensors if sensor and isinstance(sensor.average, (int, float))]
            unit = next((sensor.unit for sensor in sensors if sensor), "")
            chart.set_values(values, unit)

    def _populate_game_sensor_report(self, sessions) -> None:
        sensor_ids = []
        for session in sessions:
            for sensor_id, sensor in session.report.sensors.items():
                if isinstance(sensor, Sensor) and sensor_id not in sensor_ids:
                    sensor_ids.append(sensor_id)
        self.sensor_table.setRowCount(4)
        self.sensor_table.setColumnCount(len(sensor_ids) + 1)
        self.sensor_table.setHorizontalHeaderLabels(["Reading"] + [(_sensor(sessions[-1], sensor_id).display or _sensor(sessions[-1], sensor_id).name or sensor_id) if _sensor(sessions[-1], sensor_id) else sensor_id for sensor_id in sensor_ids])
        for row, label in enumerate(("Average", "Minimum", "Maximum", "Health")):
            self.sensor_table.setItem(row, 0, QTableWidgetItem(label))
        for col, sensor_id in enumerate(sensor_ids, start=1):
            readings = [_sensor(session, sensor_id) for session in sessions]
            available = [sensor for sensor in readings if sensor]
            if not available: continue
            unit = available[-1].unit
            averages = [sensor.average for sensor in available if isinstance(sensor.average, (int, float))]
            minimums = [sensor.minimum for sensor in available if isinstance(sensor.minimum, (int, float))]
            maximums = [sensor.maximum for sensor in available if isinstance(sensor.maximum, (int, float))]
            values = [_value(sum(averages) / len(averages), unit) if averages else "—", _value(min(minimums), unit) if minimums else "—", _value(max(maximums), unit) if maximums else "—", available[-1].status]
            for row, value in enumerate(values): self.sensor_table.setItem(row, col, QTableWidgetItem(value))

    def compare_sessions(self) -> None:
        a = self.app.sessions.find(self.compare_a.currentData()); b = self.app.sessions.find(self.compare_b.currentData())
        if not a or not b: return
        metrics = [("FPS", "fps"), ("CPU Temperature", "cpu_temp"), ("GPU Temperature", "gpu_temp"), ("CPU Usage", "cpu_usage"), ("GPU Usage", "gpu_usage"), ("RAM Usage", "memory_load")]
        self.comparison.setRowCount(len(metrics))
        for row, (name, sensor_id) in enumerate(metrics):
            first, second = _sensor(a, sensor_id), _sensor(b, sensor_id)
            va = first.average if first else None; vb = second.average if second else None
            unit = (first or second).unit if (first or second) else ""
            diff = vb - va if isinstance(va, (int, float)) and isinstance(vb, (int, float)) else None
            for col, value in enumerate((name, _value(va, unit), _value(vb, unit), _value(diff, unit))): self.comparison.setItem(row, col, QTableWidgetItem(value))


class GameDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent); self.setWindowTitle("Game name")
        layout = QVBoxLayout(self); layout.addWidget(QLabel("Game played:")); self.field = QLineEdit(); layout.addWidget(self.field)
        layout.addWidget(QLabel("Filename nickname (used to identify future logs):")); self.keyword = QLineEdit(); layout.addWidget(self.keyword)
        buttons = QHBoxLayout(); ok = QPushButton("Analyze"); cancel = QPushButton("Cancel"); ok.clicked.connect(self.accept); cancel.clicked.connect(self.reject); buttons.addWidget(ok); buttons.addWidget(cancel); layout.addLayout(buttons)
    @classmethod
    def get_game(cls, parent) -> tuple[str, str, bool]:
        dialog = cls(parent); accepted = dialog.exec() == QDialog.DialogCode.Accepted
        game = dialog.field.text().strip() or "Unknown Game"
        return game, dialog.keyword.text().strip(), accepted


def run(app: App | None = None) -> int:
    qt_app = QApplication.instance() or QApplication(sys.argv)
    qt_app.setApplicationName("Project Sentinel")
    window = MainWindow(app or App())
    window.show()
    return qt_app.exec()


STYLESHEET = f"""
QWidget {{ background: {BACKGROUND}; color: #e8eef3; font-family: 'Segoe UI'; font-size: 13px; }}
#sidebar {{ background: #101a23; border-right: 1px solid #263541; }}
#brand {{ color: {ACCENT}; font-size: 20px; font-weight: 700; letter-spacing: 2px; }} #subtitle, #description, #metricLabel, #metricStatus {{ color: #91a5b5; }}
#heading {{ font-size: 28px; font-weight: 650; }} #sessionTitle {{ font-size: 15px; color: #b9c8d3; margin-top: 12px; }} #sectionTitle {{ font-size: 16px; font-weight: 600; }}
QPushButton {{ background: transparent; border: 1px solid transparent; border-radius: 7px; padding: 11px 12px; text-align: left; }} QPushButton:hover, QPushButton[active='true'] {{ background: #1c2c36; color: {ACCENT}; }} #primary {{ background: {ACCENT}; color: #07211a; font-weight: 700; text-align: center; }} #primary:hover {{ background: #5be5bb; }} #exitButton {{ color: #d6a2a2; }}
#metricCard {{ background: {PANEL}; border: 1px solid #253743; border-radius: 10px; }} #metricValue {{ font-size: 24px; font-weight: 650; padding: 3px 0; }} #healthBanner {{ background: #12352e; color: #b8f8df; border-radius: 8px; padding: 13px; font-weight: 600; }}
QTableWidget, QListWidget, QComboBox, QLineEdit {{ background: {PANEL}; border: 1px solid #2a3b47; border-radius: 7px; padding: 7px; }} QHeaderView::section {{ background: #1c2b35; color: #9fb2c1; border: 0; padding: 8px; }} QTableWidget::item:selected, QListWidget::item:selected {{ background: #275047; }}
"""
