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

from core.engine.reader import load_hwinfo_log
from .sensors import get_all_sensors
from .analyzer import analyze_sensor
from ..engine import health


def run(file_path, game="Unknown"):
    """
    Analyze one HWiNFO log.

    Returns a structured report dictionary.
    """

    # Load the log
    log = load_hwinfo_log(file_path)

    # Build the report object
    report = {
        "session": build_session(file_path, game),
        "machine": {},
        "sensors": {},
        "summary": {}
    }

    # Analyze each configured sensor
    for sensor in get_all_sensors():

        stats = analyze_sensor(
            log,
            sensor["keyword"],
            sensor["value_type"]
        )

        health_function = getattr(
            health,
            sensor["health"]
        )

        status = health_function(stats)

        report["sensors"][sensor["id"]] = {
            "display": sensor["display"],
            "category": sensor["category"],
            "unit": sensor["unit"],
            "description": sensor["description"],
            "stats": stats,
            "status": status
        }

    return report


# ==========================================================
# Builders
# ==========================================================

def build_session(file_path, game):
    """
    Build the Session Information section.
    """

    return {
        "game": game,
        "log_file": Path(file_path).name,
        "date": datetime.now().strftime("%Y-%m-%d")
    }