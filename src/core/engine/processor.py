# core/processor.py

"""
Project Sentinel

Processing Pipeline

Reader
    ↓
Analyzer
    ↓
Health Engine
"""

from core.reader import load_hwinfo_log
from core.sensors import get_all_sensors
from core.analyzer import analyze_sensor
from core import health


def run(file_path):
    """
    Analyze one HWiNFO log.

    Returns a dictionary of analyzed sensors.
    """

    log = load_hwinfo_log(file_path)

    results = {}

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

        results[sensor["id"]] = {

            "display": sensor["display"],

            "category": sensor["category"],

            "unit": sensor["unit"],

            "description": sensor["description"],

            "stats": stats,

            "status": status

        }

    return {

        "filename": log["filename"],

        "filepath": log["filepath"],

        "samples": log["sample_count"],

        "results": results

    }