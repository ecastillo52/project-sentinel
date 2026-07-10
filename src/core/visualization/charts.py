"""
Project Sentinel

Chart Helpers

Builds small, dependency-free SVG charts for Sentinel
HTML reports.

This module performs no analysis. It only visualizes
Report and Sensor models.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Iterable

from core.models.report import Report
from core.models.sensor import Sensor


# ==========================================================
# Models
# ==========================================================

@dataclass(frozen=True, slots=True)
class ChartSensor:
    """
    Report-safe sensor data used by the chart renderer.
    """

    name: str
    category: str
    unit: str
    current: float | None
    minimum: float | None
    maximum: float | None
    average: float | None
    status: str


# ==========================================================
# Public API
# ==========================================================

def build(report: Report) -> dict[str, str]:
    """
    Build every chart used by the HTML report.
    """

    sensors = list(_chart_sensors(report))

    return {
        "status": status_chart(sensors),
        "temperatures": metric_chart(
            sensors,
            title="Temperature",
            units={"C", "°C", "Â°C"},
            empty_message="No temperature sensors found.",
        ),
        "loads": metric_chart(
            sensors,
            title="Load",
            units={"%"},
            empty_message="No load sensors found.",
        ),
        "memory": metric_chart(
            sensors,
            title="Memory",
            units={"GB"},
            empty_message="No memory sensors found.",
        ),
    }


def line_chart(
    points: list[tuple[str, float | int | None]],
    *,
    title: str,
    unit: str,
    empty_message: str = "Not enough data to chart.",
) -> str:
    """
    Render one metric across sessions.
    """

    values = [
        (label, float(value))
        for label, value in points
        if isinstance(value, (int, float))
    ]

    if len(values) < 2:
        return empty_chart(empty_message)

    width = 760
    height = 260
    left = 58
    right = 26
    top = 42
    bottom = 48
    chart_width = width - left - right
    chart_height = height - top - bottom

    minimum = min(value for _, value in values)
    maximum = max(value for _, value in values)

    if minimum == maximum:
        padding = abs(maximum) * 0.1 or 1
        minimum -= padding
        maximum += padding

    span = maximum - minimum

    coords: list[tuple[float, float, str, float]] = []

    for index, (label, value) in enumerate(values):
        if len(values) == 1:
            x = left + chart_width
        else:
            x = left + (chart_width * index / (len(values) - 1))

        y = top + chart_height - (
            chart_height * ((value - minimum) / span)
        )

        coords.append((x, y, label, value))

    path = " ".join(
        f"{x:.1f},{y:.1f}"
        for x, y, _, _ in coords
    )

    parts = [_svg_open(width, height)]
    parts.append(_title(title, 20, 24))
    parts.append(
        '<line x1="58" y1="212" x2="734" y2="212" '
        'stroke="#d9e0e8" stroke-width="1" />'
    )
    parts.append(
        '<line x1="58" y1="42" x2="58" y2="212" '
        'stroke="#d9e0e8" stroke-width="1" />'
    )
    parts.append(_text(format_value(maximum, unit), 12, top + 4, "muted"))
    parts.append(_text(format_value(minimum, unit), 12, bottom + chart_height, "muted"))
    parts.append(
        f'<polyline points="{path}" fill="none" '
        'stroke="#2364aa" stroke-width="3" '
        'stroke-linejoin="round" stroke-linecap="round" />'
    )

    for x, y, label, value in coords:
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" '
            'fill="#2364aa" />'
        )
        parts.append(
            f'<title>{escape(label)}: '
            f'{escape(format_value(value, unit))}</title>'
        )

    first_x, _, first_label, _ = coords[0]
    last_x, _, last_label, last_value = coords[-1]

    parts.append(_text(_truncate(first_label, 14), int(first_x), 238, "muted"))
    parts.append(_text(_truncate(last_label, 14), int(last_x - 56), 238, "muted"))
    parts.append(
        _text(
            format_value(last_value, unit),
            int(last_x - 70),
            34,
            "value",
        )
    )

    parts.append("</svg>")

    return "".join(parts)


def status_chart(
    sensors: Iterable[ChartSensor],
) -> str:
    """
    Render a compact bar chart grouped by health status.
    """

    counts: dict[str, int] = {}

    for sensor in sensors:
        status = _normalize_status(sensor.status)
        counts[status] = counts.get(status, 0) + 1

    if not counts:
        return empty_chart("No sensor status data found.")

    ordered = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )

    width = 680
    row_height = 34
    top = 28
    left = 126
    bar_width = 490
    height = top + (len(ordered) * row_height) + 22
    maximum = max(counts.values())

    parts = [_svg_open(width, height)]
    parts.append(_title("Sensor Health", 20, 20))

    for index, (label, count) in enumerate(ordered):
        y = top + (index * row_height)
        size = int(bar_width * (count / maximum))

        parts.append(_text(label.title(), 20, y + 22, "label"))
        parts.append(_rect(left, y + 7, size, 16, _status_color(label)))
        parts.append(_text(str(count), left + size + 10, y + 21, "value"))

    parts.append("</svg>")

    return "".join(parts)


def metric_chart(
    sensors: Iterable[ChartSensor],
    *,
    title: str,
    units: set[str],
    empty_message: str,
) -> str:
    """
    Render min/average/max bars for sensors matching units.
    """

    rows = [
        sensor
        for sensor in sensors
        if sensor.unit in units and sensor.maximum is not None
    ]

    rows.sort(
        key=lambda sensor: (
            sensor.category,
            sensor.name,
        )
    )

    if not rows:
        return empty_chart(empty_message)

    width = 760
    row_height = 42
    top = 34
    left = 220
    chart_width = 460
    height = top + (len(rows) * row_height) + 38
    maximum = max(sensor.maximum or 0 for sensor in rows)

    if maximum <= 0:
        return empty_chart(empty_message)

    parts = [_svg_open(width, height)]
    parts.append(_title(title, 20, 22))

    for index, sensor in enumerate(rows):
        y = top + (index * row_height)
        value = sensor.average

        if value is None:
            value = sensor.current

        if value is None:
            continue

        minimum = sensor.minimum or 0
        average = max(float(value), 0)
        peak = max(float(sensor.maximum or 0), average)

        min_width = int(chart_width * (minimum / maximum))
        avg_width = int(chart_width * (average / maximum))
        max_width = int(chart_width * (peak / maximum))

        label = _truncate(sensor.name, 28)
        display_value = format_value(average, sensor.unit)

        parts.append(_text(label, 20, y + 23, "label"))
        parts.append(_rect(left, y + 8, max_width, 18, "#d7dee8"))
        parts.append(_rect(left, y + 8, avg_width, 18, _status_color(sensor.status)))
        parts.append(_rect(left, y + 8, min_width, 18, "#788391"))
        parts.append(_text(display_value, left + chart_width + 14, y + 23, "value"))

    parts.append("</svg>")

    return "".join(parts)


def empty_chart(message: str) -> str:
    """
    Render a chart-shaped empty state.
    """

    width = 680
    height = 96

    return "".join(
        (
            _svg_open(width, height),
            _title("Chart", 20, 22),
            _text(message, 20, 58, "muted"),
            "</svg>",
        )
    )


def format_value(
    value: float | int | None,
    unit: str,
) -> str:
    """
    Format a chart value for labels.
    """

    if value is None:
        return "--"

    if unit in {"C", "°C", "Â°C"}:
        return f"{value:.1f} °C"

    if unit == "%":
        return f"{value:.1f} %"

    if unit == "GB":
        return f"{value:.1f} GB"

    if unit == "FPS":
        return f"{value:.0f} FPS"

    return f"{value:g} {unit}".strip()


# ==========================================================
# Sensor Conversion
# ==========================================================

def _chart_sensors(report: Report) -> Iterable[ChartSensor]:
    for sensor in report.sensors.values():
        if not isinstance(sensor, Sensor):
            continue

        yield ChartSensor(
            name=sensor.display or sensor.name,
            category=sensor.category or "Other",
            unit=sensor.unit,
            current=_number(sensor.current),
            minimum=_number(sensor.minimum),
            maximum=_number(sensor.maximum),
            average=_number(sensor.average),
            status=sensor.status or "UNKNOWN",
        )


def _number(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)

    return None


# ==========================================================
# SVG Helpers
# ==========================================================

def _svg_open(width: int, height: int) -> str:
    return (
        f'<svg viewBox="0 0 {width} {height}" '
        'role="img" xmlns="http://www.w3.org/2000/svg">'
    )


def _title(value: str, x: int, y: int) -> str:
    return _text(value, x, y, "title")


def _rect(
    x: int,
    y: int,
    width: int,
    height: int,
    color: str,
) -> str:
    width = max(width, 1)

    return (
        f'<rect x="{x}" y="{y}" width="{width}" '
        f'height="{height}" rx="4" fill="{color}" />'
    )


def _text(
    value: str,
    x: int,
    y: int,
    class_name: str,
) -> str:
    return (
        f'<text x="{x}" y="{y}" class="{class_name}">'
        f"{escape(str(value))}</text>"
    )


def _truncate(value: str, length: int) -> str:
    if len(value) <= length:
        return value

    return f"{value[: length - 1]}..."


def _normalize_status(status: str) -> str:
    value = str(status).strip().upper()

    if value in {"GOOD", "PASS", "HEALTHY", "EXCELLENT", "PLAYABLE"}:
        return "GOOD"

    if value in {"WARNING", "WARN", "WARM", "BUSY", "HIGH", "LOW"}:
        return "WARNING"

    if value in {"CRITICAL", "FAIL", "FAILED", "MAXED", "POOR"}:
        return "CRITICAL"

    return value or "UNKNOWN"


def _status_color(status: str) -> str:
    status = _normalize_status(status)

    return {
        "GOOD": "#2f9e44",
        "WARNING": "#f08c00",
        "CRITICAL": "#d9480f",
        "UNKNOWN": "#687385",
    }.get(status, "#687385")
