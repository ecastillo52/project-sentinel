# core/report/renderer.py

"""
Project Sentinel

Console Report Renderer

Renders completed Sentinel reports.

This module performs no analysis.
It only displays Report and Session models.
"""

from __future__ import annotations

from core.config import APP_NAME, APP_VERSION
from core.models.report import Report
from core.models.session import Session
from core.models.sensor import Sensor


# ==========================================================
# Constants
# ==========================================================

REPORT_WIDTH = 52
LABEL_WIDTH = 20

LINE = "=" * REPORT_WIDTH
SECTION = "-" * REPORT_WIDTH

HEALTH_ICONS = {
    "GOOD": "✓",
    "PASS": "✓",
    "HEALTHY": "✓",
    "EXCELLENT": "✓",
    "PLAYABLE": "✓",
    "WARNING": "⚠",
    "WARN": "⚠",
    "WARM": "⚠",
    "BUSY": "⚠",
    "HIGH": "⚠",
    "LOW": "⚠",
    "CRITICAL": "✗",
    "FAIL": "✗",
    "MAXED": "✗",
    "POOR": "✗",
}


# ==========================================================
# Public API
# ==========================================================

def render(
    report: Report,
    *,
    session: Session | None = None,
) -> None:
    """
    Render a completed Sentinel report.
    """

    if session is not None:
        print_saved_session_header(session)

    print_header()
    print_machine(report)
    print_sensors(report)
    print_summary(report)


# ==========================================================
# Saved Session Header
# ==========================================================

def print_saved_session_header(
    session: Session,
) -> None:

    divider()
    print(session.game.center(REPORT_WIDTH))
    divider()
    blank()

    field("Session", session.session_number)
    field("Analyzed", session.analyzed_at)
    field("Source", session.filename)
    field("Archive", session.archive_path)

    blank()


# ==========================================================
# Header
# ==========================================================

def print_header() -> None:

    divider()

    print(APP_NAME.center(REPORT_WIDTH))
    print(f"Version {APP_VERSION}".center(REPORT_WIDTH))

    divider()
    blank()


# ==========================================================
# Machine Information
# ==========================================================

def print_machine(
    report: Report,
) -> None:

    machine = report.metadata.get("machine", {})

    if not machine:
        return

    print("Machine Information")
    blank()

    field("CPU", machine.get("cpu", "--"))
    field("GPU", machine.get("gpu", "--"))
    field("RAM", machine.get("ram", "--"))
    field("Motherboard", machine.get("motherboard", "--"))

    blank()
    divider()
    blank()


# ==========================================================
# Sensors
# ==========================================================

def print_sensors(
    report: Report,
) -> None:

    if not report.sensors:
        return

    print("Sensor Reports")
    blank()

    categories: dict[str, list[Sensor]] = {}

    for sensor in report.sensors.values():

        if not isinstance(sensor, Sensor):
            continue

        category = getattr(sensor, "category", "Other")

        categories.setdefault(
            category,
            [],
        ).append(sensor)

    for category, sensors in categories.items():

        divider()
        print(category)
        divider()
        blank()

        for sensor in sensors:
            print_sensor(sensor)


def print_sensor(
    sensor: Sensor,
) -> None:

    section()

    print(sensor.name)

    section()
    blank()

    field(
        "Current",
        format_value(sensor.current, sensor.unit),
    )

    field(
        "Average",
        format_value(sensor.average, sensor.unit),
    )

    field(
        "Minimum",
        format_value(sensor.minimum, sensor.unit),
    )

    field(
        "Maximum",
        format_value(sensor.maximum, sensor.unit),
    )

    blank()

    field(
        "Status",
        health(sensor.status),
    )

    blank()


# ==========================================================
# Summary
# ==========================================================

def print_summary(
    report: Report,
) -> None:

    summary = report.summary

    if not summary:
        return

    divider()

    print("SESSION SUMMARY".center(REPORT_WIDTH))

    divider()
    blank()

    field(
        "Average FPS",
        format_value(
            summary.get("average_fps"),
            "FPS",
        ),
    )

    field(
        "Peak CPU Temp",
        format_value(
            summary.get("peak_cpu_temp"),
            "°C",
        ),
    )

    field(
        "Peak GPU Temp",
        format_value(
            summary.get("peak_gpu_temp"),
            "°C",
        ),
    )

    field(
        "Peak RAM Usage",
        format_value(
            summary.get("peak_ram_usage"),
            "%",
        ),
    )

    blank()

    field(
        "Overall Health",
        health(
            summary.get(
                "overall_health",
                "Unknown",
            )
        ),
    )

    blank()


# ==========================================================
# Formatting
# ==========================================================

def format_value(
    value,
    unit: str,
) -> str:

    if value is None:
        return "--"

    if unit == "°C":
        return f"{value:.1f} °C"

    if unit == "%":
        return f"{value:.1f} %"

    if unit == "GB":
        return f"{value:.1f} GB"

    if unit == "FPS":
        return f"{value:.0f} FPS"

    return f"{value} {unit}".strip()


def health(
    status,
) -> str:

    if status is None:
        status = "Unknown"

    icon = HEALTH_ICONS.get(
        str(status),
        "•",
    )

    return f"{icon} {status}"


# ==========================================================
# Helpers
# ==========================================================

def field(
    label: str,
    value,
) -> None:

    if value is None:
        value = "--"

    print(f"{label:<{LABEL_WIDTH}} {value}")


def divider() -> None:
    print(LINE)


def section() -> None:
    print(SECTION)


def blank() -> None:
    print()
