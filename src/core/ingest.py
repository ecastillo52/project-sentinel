# core/ingest.py

from datetime import datetime
from core.reader import load_hwinfo_log
from core.sensors import get_sensor
from core.database import insert_record


def process_file(file_path):
    """
    Reads + analyzes + stores ONE CSV file.
    """

    log = load_hwinfo_log(file_path)

    record = {
        "filename": log["filename"],
        "filepath": log["filepath"],
        "timestamp": datetime.utcnow().isoformat(),

        "metrics": {
            "cpu_temp": get_sensor(log, "cpu_temp"),
            "cpu_usage": get_sensor(log, "cpu_usage"),
            "gpu_temp": get_sensor(log, "gpu_temp"),
            "gpu_usage": get_sensor(log, "gpu_usage"),
            "ram_usage": get_sensor(log, "ram_usage"),
            "fps": get_sensor(log, "fps"),
        }
    }

    insert_record(record)

    return record