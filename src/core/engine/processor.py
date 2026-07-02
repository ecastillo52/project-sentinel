# core/engine/processor.py

"""
Project Sentinel

Processing Pipeline

Reader
    ↓
Analyzer
    ↓
Health Engine
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from core.config import REPORT_SCHEMA
from core.engine.reader import load_hwinfo_log
from core.engine.summary import build_summary
from core.metadata.machine import get_machine_info

from . import health
from .analyzer import analyze_sensor
from .sensors import get_all_sensors


def run(
    file_path: str | Path,
    game: str = "Unknown",
) -> dict[str, Any]:
    """
    Analyze one HWiNFO log.

    Returns a structured report dictionary.
    """

    log = load_hwinfo_log(file_path)

    report: dict[str, Any] = {
        "schema": REPORT_SCHEMA,
        "session": build_session(file_path, game),
        "machine": get_machine_info(),
        "sensors": {},
        "summary": {},
    }

    for sensor in get_all_sensors():

        stats = analyze_sensor(
            log,
            sensor,
        )

        health_function = getattr(
            health,
            sensor["health"],
        )

        report["sensors"][sensor["id"]] = {
            "display": sensor["display"],
            "category": sensor["category"],
            "unit": sensor["unit"],
            "description": sensor["description"],
            "stats": stats,
            "status": health_function(stats),
        }

    report["summary"] = build_summary(report)

    return report


# ==========================================================
# Builders
# ==========================================================

def build_session(
    file_path: str | Path,
    game: str,
) -> dict[str, str]:
    """
    Build the Session Information section.
    """

    return {
        "game": game,
        "log_file": Path(file_path).name,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }