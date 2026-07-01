# core/processor.py

from core.sensors import get_all_sensors
from core.analyzer import analyze_sensor
from core.reader import load_hwinfo_log
from core import health


def run(file_path):
    log = load_hwinfo_log(file_path)
    results = []

    for sensor in get_all_sensors():

        stats = analyze_sensor(
            log,
            sensor["keyword"]
        )

        health_function = getattr(
            health,
            sensor["health"]
        )

        status = health_function(stats)

        results.append({
            "sensor": sensor,
            "stats": stats,
            "status": status
        })

    return results