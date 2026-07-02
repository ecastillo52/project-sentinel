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

# ==========================================================
# Constants
# ==========================================================

REPORT_WIDTH = 52
LABEL_WIDTH = 20

TITLE = "PROJECT SENTINEL"
VERSION = "Version 0.1.0"

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

def render(report):
    """Render a complete Sentinel report."""

    print_header()
    print_session(report)
    print_machine(report)
    print_sensors(report)
    print_summary(report)


# ==========================================================
# Header
# ==========================================================

def print_header():
    """Print the report header."""

    divider()

    print(TITLE.center(REPORT_WIDTH))
    print(VERSION.center(REPORT_WIDTH))

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

    print("Machine Information")
    blank()

    field("CPU", "(placeholder)")
    field("GPU", "(placeholder)")
    field("RAM", "(placeholder)")
    field("Motherboard", "(placeholder)")

    blank()
    divider()
    blank()


# ==========================================================
# Sensor Reports
# ==========================================================

def print_sensors(report):
    """Print every analyzed sensor."""

    print("Sensor Reports")
    blank()

    for sensor in report["sensors"].values():
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
    """Print the session summary."""

    divider()
    print("SESSION SUMMARY".center(REPORT_WIDTH))
    divider()
    blank()

    field("Average FPS", "(placeholder)")
    field("Peak CPU Temp", "(placeholder)")
    field("Peak GPU Temp", "(placeholder)")
    field("Peak RAM Usage", "(placeholder)")

    blank()

    field("Overall Health", "✓ Excellent")

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