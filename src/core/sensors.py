# core/sensors.py

from core.analyzer import analyze_sensor

SENSORS = {

    "cpu_temp": {
        "keyword": "cpu (tctl/tdie)",
        "display": "CPU Temperature",
        "unit": "°C",
        "type": "float",
    },

    "cpu_usage": {
        "keyword": "total cpu usage",
        "display": "CPU Usage",
        "unit": "%",
        "type": "float",
    },

    "gpu_temp": {
        "keyword": "gpu temperature",
        "display": "GPU Temperature",
        "unit": "°C",
        "type": "float",
    },

    "gpu_usage": {
        "keyword": "gpu core load",
        "display": "GPU Usage",
        "unit": "%",
        "type": "float",
    },

    "ram_usage": {
        "keyword": "physical memory load",
        "display": "RAM Usage",
        "unit": "%",
        "type": "float",
    },

    "fps": {
        "keyword": "framerate displayed (avg)",
        "display": "Average FPS",
        "unit": "FPS",
        "type": "float",
    },

}


def get_sensor(log, sensor_name):

    if sensor_name not in SENSORS:
        raise ValueError(
            f"Unknown sensor '{sensor_name}'."
        )

    sensor = SENSORS[sensor_name]

    stats = analyze_sensor(
        log,
        sensor["keyword"],
        sensor["type"],
    )

    return {
        "display": sensor["display"],
        "unit": sensor["unit"],
        "stats": stats,
    }