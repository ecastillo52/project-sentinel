# core/report/renderer.py

"""
Project Sentinel

Console Report Renderer

Responsible for displaying a completed Sentinel report.

This module performs no analysis.
It only formats and displays data produced by the engine.

Report Flow

    Header
        ↓
    Session Information
        ↓
    Machine Information
        ↓
    Sensor Reports
        ↓
    Session Summary
"""

from collections import OrderedDict
from core.config import APP_NAME, APP_VERSION

# ==========================================================
# Constants
# ==========================================================

REPORT_WIDTH = 52
LABEL_WIDTH = 20


LINE = "=" * REPORT_WIDTH
SECTION = "-" * REPORT_WIDTH

HEALTH_ICONS = {
    "Healthy": "✓",
    "Warm": "⚠",
    "Critical": "✗",
    "Excellent": "✓",
}


# ==========================================================
# Public API
# ==========================================================

def render(report, session=None):
    """Render a complete Sentinel report."""

    if session is not None:
        print_saved_session_header(session)

    print_header()
    print_session(report)
    print_machine(report)
    print_sensors(report)
    print_summary(report)

def print_saved_session_header(session):
    """Print metadata for a saved session."""

    divider()

    print(session.game.center(REPORT_WIDTH))

    divider()
    blank()

    field("Session", session.session_number)
    field("Analyzed", session.date.strftime("%Y-%m-%d %H:%M:%S"))
    field("Source", session.filename)
    field("Archive", session.archive)
    field("Version", session.version)
    field("Engine", session.engine)

    blank()

# ==========================================================
# Header
# ==========================================================

def print_header():
    """Print the report header."""

    divider()

    print(APP_NAME.center(REPORT_WIDTH))
    print(f"Version {APP_VERSION}".center(REPORT_WIDTH))

    divider()
    blank()


# ==========================================================
# Session Information
# ==========================================================

def print_session(report):
    """Print session information."""

    session = report["session"]

    print("Session Information")
    blank()

    field("Game", session["game"])
    field("Log File", session["log_file"])
    field("Date", session["date"])

    blank()
    divider()
    blank()


# ==========================================================
# Machine Information
# ==========================================================

def print_machine(report):
    """Print machine information."""

    machine = report["machine"]

    print("Machine Information")
    blank()

    field("CPU", machine["cpu"])
    field("GPU", machine["gpu"])
    field("RAM", machine["ram"])
    field("Motherboard", machine["motherboard"])

    blank()
    divider()
    blank()


# ==========================================================
# Sensor Reports
# ==========================================================

def print_sensors(report):
    """
    Print all analyzed sensors grouped by category.
    """

    print("Sensor Reports")
    blank()

    categories = OrderedDict()

    for sensor in report["sensors"].values():
        categories.setdefault(
            sensor["category"],
            []
        ).append(sensor)

    for category, sensors in categories.items():

        divider()
        print(category)
        divider()
        blank()

        for sensor in sensors:
            print_sensor(sensor)

def print_sensor(sensor):
    """Print a single sensor."""

    section()

    print(sensor["display"])

    section()
    blank()

    stats = sensor["stats"]

    field("Current", format_value(stats["current"], sensor["unit"]))
    field("Average", format_value(stats["average"], sensor["unit"]))
    field("Minimum", format_value(stats["minimum"], sensor["unit"]))
    field("Maximum", format_value(stats["maximum"], sensor["unit"]))

    blank()

    field("Status", health(sensor["status"]))

    blank()


# ==========================================================
# Session Summary
# ==========================================================

def print_summary(report):
    """
    Print the session summary.
    """

    summary = report["summary"]

    divider()
    print("SESSION SUMMARY".center(REPORT_WIDTH))
    divider()
    blank()

    field(
        "Average FPS",
        format_value(summary["average_fps"], "FPS")
    )

    field(
        "Peak CPU Temp",
        format_value(summary["peak_cpu_temp"], "°C")
    )

    field(
        "Peak GPU Temp",
        format_value(summary["peak_gpu_temp"], "°C")
    )

    field(
        "Peak RAM Usage",
        format_value(summary["peak_ram_usage"], "%")
    )

    blank()

    field(
        "Overall Health",
        health(summary["overall_health"])
    )

    blank()


# ==========================================================
# Formatting Helpers
# ==========================================================

def format_value(value, unit):
    """
    Format a sensor value with its unit.

    Falls back gracefully if data is missing.
    """

    if value is None:
        return "--"

    if unit == "°C":
        return f"{value:.1f} °C"

    if unit == "GB":
        return f"{value:.1f} GB"

    if unit == "%":
        return f"{value:.1f} %"

    if unit == "FPS":
        return f"{value:.0f} FPS"

    return f"{value:.2f} {unit}".strip()


def health(status):
    """
    Format a health status with an icon.
    """

    if isinstance(status, dict):
        status = status.get("status", "Unknown")

    icon = HEALTH_ICONS.get(status, "•")

    return f"{icon} {status}"


# ==========================================================
# Printing Helpers
# ==========================================================

def field(label, value):
    """Print an aligned label/value pair."""

    print(f"{label:<{LABEL_WIDTH}} {value}")


def divider():
    """Print a major divider."""

    print(LINE)


def section():
    """Print a section divider."""

    print(SECTION)


def blank():
    """Print a blank line."""

    print()