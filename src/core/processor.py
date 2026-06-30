# core/processor.py

from core.sensors import get_all_sensors
from core.analyzer import analyze_sensor
from core import health
log = load_hwinfo_log(file_path)
from core.reader import load_hwinfo_log

def run(file_path):
    log = load_hwinfo_log(file_path)
    results = []

    for sensor in get_all_sensors():
        stats = analyze_sensor(
            log,
            sensor["keyword"]
        )

        status_function = getattr(
            health,
            sensor["health"]
        )

        status = status_function(stats)

        results.append({
            "sensor": sensor,
            "stats": stats,
            "status": status,
        })

    return results