# core/intelligence/renderer.py

"""
Project Sentinel

Historical Intelligence Renderer

Renders historical intelligence reports produced by the
Sentinel Intelligence engine.

This module performs no calculations.
It only formats and displays report data.
"""

from __future__ import annotations

from textwrap import fill
from typing import Any


# ==========================================================
# Constants
# ==========================================================

REPORT_WIDTH = 54
LABEL_WIDTH = 24

LINE = "=" * REPORT_WIDTH

ICONS = {
    "Critical": "✖",
    "Warning": "⚠",
    "Information": "ℹ",
}


# ==========================================================
# Public API
# ==========================================================

def render(report: dict) -> None:
    """
    Render a complete historical intelligence report.
    """

    print_header()

    render_game(report.get("game"))

    render_standard_section(
        "Performance",
        report.get("performance"),
        (
            ("Average FPS", "average_fps", format_fps),
            ("Best Session", "best_session", format_session),
            ("Trend", "trend", str),
        ),
    )

    render_standard_section(
        "CPU",
        report.get("cpu"),
        (
            ("Average Temp", "average_temperature", format_temperature),
            ("Highest Temp", "highest_temperature", format_temperature),
            ("Trend", "trend", str),
        ),
    )

    render_standard_section(
        "GPU",
        report.get("gpu"),
        (
            ("Average Temp", "average_temperature", format_temperature),
            ("Highest Temp", "highest_temperature", format_temperature),
            ("Trend", "trend", str),
        ),
    )

    render_standard_section(
        "Memory",
        report.get("memory"),
        (
            ("Average Load", "average_load", format_percent),
            ("Highest Load", "highest_load", format_percent),
            ("Trend", "trend", str),
        ),
    )

    render_recommendations(
        report.get("recommendations", [])
    )


# ==========================================================
# Header
# ==========================================================

def print_header() -> None:
    divider()
    print("SENTINEL INTELLIGENCE".center(REPORT_WIDTH))
    divider()
    blank()


# ==========================================================
# Game
# ==========================================================

def render_game(game: dict | None) -> None:
    if not game:
        return

    heading("Game")

    field("Name", game.get("name"))
    field("Sessions", game.get("sessions"))

    field(
        "First Session",
        format_session(game.get("first_session")),
    )

    field(
        "Latest Session",
        format_session(game.get("latest_session")),
    )

    blank()


# ==========================================================
# Generic Section Renderer
# ==========================================================

def render_standard_section(
    title: str,
    section: dict | None,
    fields_to_render,
) -> None:
    """
    Render a standard report section.

    fields_to_render:

        (
            ("Average FPS", "average_fps", formatter),
            ...
        )
    """

    if not section:
        return

    heading(title)

    for label, key, formatter in fields_to_render:

        value = section.get(key)

        field(
            label,
            formatter(value),
        )

    intelligence = section.get(
        "intelligence",
        [],
    )

    if intelligence:
        blank()
        print("Historical Intelligence")
        blank()

        for statement in intelligence:

            print(
                fill(
                    statement,
                    width=REPORT_WIDTH - 4,
                    initial_indent="• ",
                    subsequent_indent="  ",
                )
            )

    blank()


# ==========================================================
# Recommendations
# ==========================================================

def render_recommendations(
    recommendations: list[dict],
) -> None:

    heading("Recommendations")

    if not recommendations:

        print("No recommendations.")
        blank()
        return

    for recommendation in recommendations:

        render_recommendation(
            recommendation,
        )

    blank()


def render_recommendation(
    recommendation: dict,
) -> None:

    level = recommendation.get(
        "level",
        "",
    )

    icon = ICONS.get(
        level,
        "•",
    )

    title = recommendation.get(
        "title",
        "",
    )

    message = recommendation.get(
        "message",
        "",
    )

    print(f"{icon} {title}")
    blank()

    print(
        fill(
            message,
            width=REPORT_WIDTH - 4,
            initial_indent="    ",
            subsequent_indent="    ",
        )
    )

    blank()


# ==========================================================
# Formatting
# ==========================================================

def format_session(
    value: Any,
) -> str:

    if value is None:
        return "--"

    if isinstance(value, dict):

        return (
            value.get("display_name")
            or value.get("game")
            or "--"
        )

    return str(value)


def format_temperature(
    value: Any,
) -> str:

    if value is None:
        return "--"

    return f"{value:.1f} °C"


def format_percent(
    value: Any,
) -> str:

    if value is None:
        return "--"

    return f"{value:.1f} %"


def format_fps(
    value: Any,
) -> str:

    if value is None:
        return "--"

    return f"{value:.1f} FPS"


# ==========================================================
# Console Helpers
# ==========================================================

def heading(
    title: str,
) -> None:

    divider()
    print(title)
    divider()
    blank()


def field(
    label: str,
    value: Any,
) -> None:

    if value is None:
        value = "--"

    print(
        f"{label:<{LABEL_WIDTH}} {value}"
    )


def divider() -> None:
    print(LINE)


def blank() -> None:
    print()