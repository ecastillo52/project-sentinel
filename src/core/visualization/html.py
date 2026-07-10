"""
Project Sentinel

HTML Report Renderer

Exports completed Sentinel sessions as standalone HTML
reports.

This module performs no analysis.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from re import sub
from typing import Any

from core.config import APP_NAME, APP_VERSION, EXPORTS_FOLDER
from core.models.report import Report
from core.models.sensor import Sensor
from core.models.session import Session
from core.visualization import charts


# ==========================================================
# Public API
# ==========================================================

def export(
    session: Session,
    *,
    directory: Path | str = EXPORTS_FOLDER,
) -> Path:
    """
    Render a session report and write it to disk.
    """

    directory = Path(directory)
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = directory / filename(session)

    path.write_text(
        render(session),
        encoding="utf-8",
    )

    return path


def export_game(
    sessions: list[Session],
    *,
    game: str,
    directory: Path | str,
) -> Path:
    """
    Render the rolling game trend report and write it.
    """

    directory = Path(directory)
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = directory / "sentinel_trends.html"

    path.write_text(
        render_game(sessions, game=game),
        encoding="utf-8",
    )

    return path


def render(session: Session) -> str:
    """
    Render a complete standalone HTML report.
    """

    report = session.report
    chart_html = charts.build(report)

    return "\n".join(
        (
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{escape(session.display_name)} - Sentinel Report</title>",
            f"<style>{_css()}</style>",
            "</head>",
            "<body>",
            '<main class="page">',
            _header(session),
            _print_actions(),
            _summary(report),
            _machine(report),
            _charts(chart_html),
            _sensors(report),
            _recommendations(report),
            "</main>",
            "</body>",
            "</html>",
        )
    )


def render_game(
    sessions: list[Session],
    *,
    game: str,
) -> str:
    """
    Render a game-level trend report.
    """

    sessions = sorted(sessions)
    trend_charts = _game_trend_charts(sessions)

    return "\n".join(
        (
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{escape(game)} - Sentinel Trends</title>",
            f"<style>{_css()}</style>",
            "</head>",
            "<body>",
            '<main class="page">',
            _game_header(game, sessions),
            _print_actions(),
            _trend_summary(sessions),
            _trend_charts(trend_charts),
            _trend_table(sessions),
            "</main>",
            "</body>",
            "</html>",
        )
    )


def filename(session: Session) -> str:
    """
    Build a stable export filename for a session.
    """

    game = _slug(session.game)

    return (
        f"{game}-session-{session.session_number:03d}-"
        f"{session.id[:8]}.html"
    )


# ==========================================================
# Sections
# ==========================================================

def _header(session: Session) -> str:
    return f"""
<header class="report-header">
  <div>
    <p class="eyebrow">{escape(APP_NAME)} {escape(APP_VERSION)}</p>
    <h1>{escape(session.game)}</h1>
    <p>{escape(session.label)} analyzed {escape(session.analyzed_at)}</p>
  </div>
  <dl class="session-meta">
    {_field("Source", session.filename)}
    {_field("Archive", session.archive_path)}
    {_field("Session ID", session.id)}
  </dl>
</header>
"""


def _game_header(
    game: str,
    sessions: list[Session],
) -> str:
    latest = sessions[-1].analyzed_at if sessions else "--"

    return f"""
<header class="report-header">
  <div>
    <p class="eyebrow">{escape(APP_NAME)} {escape(APP_VERSION)}</p>
    <h1>{escape(game)} Trends</h1>
    <p>{len(sessions)} sessions tracked. Latest session: {escape(latest)}</p>
  </div>
  <dl class="session-meta">
    {_field("Report", "Rolling game archive")}
    {_field("Updated", latest)}
    {_field("PDF", "Use Print / Save as PDF")}
  </dl>
</header>
"""


def _print_actions() -> str:
    return """
<div class="print-actions">
  <button type="button" onclick="window.print()">Print or Save as PDF</button>
</div>
"""


def _summary(report: Report) -> str:
    summary = report.summary or {}

    items = (
        ("Average FPS", _format(summary.get("average_fps"), "FPS")),
        ("Peak CPU Temp", _format(summary.get("peak_cpu_temp"), "°C")),
        ("Peak GPU Temp", _format(summary.get("peak_gpu_temp"), "°C")),
        ("Peak RAM Usage", _format(summary.get("peak_ram_usage"), "%")),
        ("Overall Health", summary.get("overall_health", "Unknown")),
    )

    return f"""
<section>
  <h2>Session Summary</h2>
  <div class="summary-grid">
    {"".join(_metric(label, value) for label, value in items)}
  </div>
</section>
"""


def _trend_summary(sessions: list[Session]) -> str:
    latest = sessions[-1] if sessions else None
    summary = latest.report.summary if latest else {}

    items = (
        ("Sessions", len(sessions)),
        ("Latest FPS", _format(summary.get("average_fps"), "FPS")),
        ("Latest CPU Peak", _format(summary.get("peak_cpu_temp"), "C")),
        ("Latest GPU Peak", _format(summary.get("peak_gpu_temp"), "C")),
        ("Latest RAM Peak", _format(summary.get("peak_ram_usage"), "%")),
    )

    return f"""
<section>
  <h2>Current Snapshot</h2>
  <div class="summary-grid">
    {"".join(_metric(label, value) for label, value in items)}
  </div>
</section>
"""


def _machine(report: Report) -> str:
    machine = report.metadata.get("machine", {})

    if not machine:
        return ""

    return f"""
<section>
  <h2>Machine</h2>
  <dl class="details">
    {_field("CPU", machine.get("cpu", "--"))}
    {_field("GPU", machine.get("gpu", "--"))}
    {_field("RAM", machine.get("ram", "--"))}
    {_field("Motherboard", machine.get("motherboard", "--"))}
  </dl>
</section>
"""


def _trend_charts(chart_html: list[str]) -> str:
    if not chart_html:
        return ""

    return f"""
<section>
  <h2>Session Trends</h2>
  <div class="chart-grid trend-grid">
    {"".join(_chart_card(chart) for chart in chart_html)}
  </div>
</section>
"""


def _charts(chart_html: dict[str, str]) -> str:
    return f"""
<section>
  <h2>Charts</h2>
  <div class="chart-grid">
    {_chart_card(chart_html["status"])}
    {_chart_card(chart_html["temperatures"])}
    {_chart_card(chart_html["loads"])}
    {_chart_card(chart_html["memory"])}
  </div>
</section>
"""


def _trend_table(sessions: list[Session]) -> str:
    if not sessions:
        return ""

    rows = "".join(
        f"""
<tr>
  <td>{escape(session.label)}</td>
  <td>{escape(session.analyzed_at)}</td>
  <td>{escape(_format(session.report.summary.get("average_fps"), "FPS"))}</td>
  <td>{escape(_format(session.report.summary.get("peak_cpu_temp"), "C"))}</td>
  <td>{escape(_format(session.report.summary.get("peak_gpu_temp"), "C"))}</td>
  <td>{escape(_format(session.report.summary.get("peak_ram_usage"), "%"))}</td>
  <td>{escape(str(session.report.summary.get("overall_health", "Unknown")))}</td>
</tr>
"""
        for session in sessions
    )

    return f"""
<section>
  <h2>Sessions</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Session</th>
          <th>Analyzed</th>
          <th>Average FPS</th>
          <th>CPU Peak</th>
          <th>GPU Peak</th>
          <th>RAM Peak</th>
          <th>Health</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>
"""


def _sensors(report: Report) -> str:
    sensors = [
        sensor
        for sensor in report.sensors.values()
        if isinstance(sensor, Sensor)
    ]

    sensors.sort(
        key=lambda sensor: (
            sensor.category,
            sensor.display or sensor.name,
        )
    )

    if not sensors:
        return ""

    rows = "".join(_sensor_row(sensor) for sensor in sensors)

    return f"""
<section>
  <h2>Sensors</h2>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Sensor</th>
          <th>Category</th>
          <th>Current</th>
          <th>Average</th>
          <th>Minimum</th>
          <th>Maximum</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>
"""


def _recommendations(report: Report) -> str:
    if not report.recommendations:
        return ""

    items = "".join(
        f"<li>{escape(str(item))}</li>"
        for item in report.recommendations
    )

    return f"""
<section>
  <h2>Recommendations</h2>
  <ul class="recommendations">{items}</ul>
</section>
"""


# ==========================================================
# HTML Helpers
# ==========================================================

def _metric(label: str, value: Any) -> str:
    return f"""
<article class="metric">
  <span>{escape(str(label))}</span>
  <strong>{escape(str(value))}</strong>
</article>
"""


def _chart_card(svg: str) -> str:
    return f'<article class="chart-card">{svg}</article>'


def _game_trend_charts(sessions: list[Session]) -> list[str]:
    labels = [session.label for session in sessions]

    summary_specs = (
        ("Average FPS", "average_fps", "FPS"),
        ("Peak CPU Temperature", "peak_cpu_temp", "C"),
        ("Peak GPU Temperature", "peak_gpu_temp", "C"),
        ("Peak RAM Usage", "peak_ram_usage", "%"),
    )

    output = [
        charts.line_chart(
            [
                (label, session.report.summary.get(key))
                for label, session in zip(labels, sessions)
            ],
            title=title,
            unit=unit,
        )
        for title, key, unit in summary_specs
    ]

    for sensor_id, label, unit, points in _sensor_series(sessions):
        if len([value for _, value in points if value is not None]) < 2:
            continue

        output.append(
            charts.line_chart(
                points,
                title=label,
                unit=unit,
                empty_message=(
                    f"Not enough data for {sensor_id}."
                ),
            )
        )

    return output


def _sensor_series(
    sessions: list[Session],
) -> list[tuple[str, str, str, list[tuple[str, float | int | None]]]]:
    sensor_ids = sorted(
        {
            sensor_id
            for session in sessions
            for sensor_id, sensor in session.report.sensors.items()
            if isinstance(sensor, Sensor)
        }
    )

    output = []

    for sensor_id in sensor_ids:
        display = sensor_id
        unit = ""
        points = []

        for session in sessions:
            sensor = session.report.sensors.get(sensor_id)
            value = None

            if isinstance(sensor, Sensor):
                display = sensor.display or sensor.name or sensor_id
                unit = sensor.unit
                value = sensor.average

                if value is None:
                    value = sensor.maximum

                if value is None:
                    value = sensor.current

            points.append((session.label, value))

        output.append((sensor_id, display, unit, points))

    return output


def _sensor_row(sensor: Sensor) -> str:
    return f"""
<tr>
  <td>{escape(sensor.display or sensor.name)}</td>
  <td>{escape(sensor.category or "Other")}</td>
  <td>{escape(_format(sensor.current, sensor.unit))}</td>
  <td>{escape(_format(sensor.average, sensor.unit))}</td>
  <td>{escape(_format(sensor.minimum, sensor.unit))}</td>
  <td>{escape(_format(sensor.maximum, sensor.unit))}</td>
  <td><span class="pill {escape(_status_class(sensor.status))}">{escape(sensor.status)}</span></td>
</tr>
"""


def _field(label: str, value: Any) -> str:
    if value is None:
        value = "--"

    return (
        f"<div><dt>{escape(str(label))}</dt>"
        f"<dd>{escape(str(value))}</dd></div>"
    )


def _format(value: Any, unit: str) -> str:
    if value is None:
        return "--"

    if isinstance(value, (int, float)):
        if unit in {"C", "°C", "Â°C"}:
            return f"{value:.1f} °C"

        if unit == "%":
            return f"{value:.1f} %"

        if unit == "GB":
            return f"{value:.1f} GB"

        if unit == "FPS":
            return f"{value:.0f} FPS"

        return f"{value:g} {unit}".strip()

    return str(value)


def _status_class(status: str) -> str:
    value = str(status).strip().lower()

    if value in {"good", "pass", "healthy", "excellent", "playable"}:
        return "good"

    if value in {"warning", "warn", "warm", "busy", "high", "low"}:
        return "warning"

    if value in {"critical", "fail", "failed", "maxed", "poor"}:
        return "critical"

    return "unknown"


def _slug(value: str) -> str:
    slug = sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()

    return slug or "sentinel"


def _css() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f4f6f8;
  --panel: #ffffff;
  --text: #16202a;
  --muted: #66717f;
  --line: #d9e0e8;
  --good: #2f9e44;
  --warning: #f08c00;
  --critical: #d9480f;
  --unknown: #687385;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: "Segoe UI", Arial, sans-serif;
  line-height: 1.45;
}

.page {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 32px 0 48px;
}

.report-header,
section {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  margin-bottom: 18px;
}

.report-header {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 24px;
  padding: 28px;
}

h1,
h2,
p {
  margin-top: 0;
}

h1 {
  font-size: 34px;
  margin-bottom: 8px;
}

h2 {
  font-size: 20px;
  margin: 0 0 18px;
}

section {
  padding: 24px;
}

.eyebrow,
.metric span,
dt,
.muted {
  color: var(--muted);
}

.eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.session-meta,
.details {
  display: grid;
  gap: 12px;
  margin: 0;
}

.details {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

dt {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
}

dd {
  margin: 2px 0 0;
  overflow-wrap: anywhere;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
}

.metric {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
}

.metric span,
.metric strong {
  display: block;
}

.metric strong {
  font-size: 22px;
  margin-top: 6px;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.trend-grid {
  grid-template-columns: 1fr;
}

.chart-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  overflow-x: auto;
}

svg {
  display: block;
  width: 100%;
  min-width: 520px;
}

svg .title {
  fill: var(--text);
  font-size: 18px;
  font-weight: 700;
}

svg .label,
svg .value,
svg .muted {
  fill: var(--muted);
  font-size: 13px;
}

svg .value {
  fill: var(--text);
  font-weight: 700;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 820px;
}

th,
td {
  border-bottom: 1px solid var(--line);
  padding: 11px 10px;
  text-align: left;
  vertical-align: top;
}

th {
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
}

.pill {
  border-radius: 999px;
  color: white;
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  min-width: 74px;
  padding: 4px 8px;
  text-align: center;
}

.pill.good {
  background: var(--good);
}

.pill.warning {
  background: var(--warning);
}

.pill.critical {
  background: var(--critical);
}

.pill.unknown {
  background: var(--unknown);
}

.recommendations {
  margin: 0;
  padding-left: 20px;
}

.recommendations li + li {
  margin-top: 8px;
}

.print-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 18px;
}

.print-actions button {
  background: var(--text);
  border: 0;
  border-radius: 6px;
  color: var(--panel);
  cursor: pointer;
  font: inherit;
  font-weight: 700;
  padding: 10px 14px;
}

@media (max-width: 860px) {
  .report-header,
  .details,
  .summary-grid,
  .chart-grid {
    grid-template-columns: 1fr;
  }

  .page {
    width: min(100% - 20px, 1180px);
    padding-top: 16px;
  }
}

@media print {
  @page {
    margin: 0.5in;
    size: letter;
  }

  body {
    background: white;
  }

  .page {
    width: 100%;
    padding: 0;
  }

  .print-actions {
    display: none;
  }

  .report-header,
  section,
  .metric,
  .chart-card {
    border-color: #bfc7d1;
    break-inside: avoid;
  }

  .chart-grid,
  .summary-grid,
  .details,
  .report-header {
    grid-template-columns: 1fr;
  }

  svg {
    min-width: 0;
  }
}
"""
