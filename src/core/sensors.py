# core/sensors.py

"""
Project Sentinel
----------------

Sensor Registry

This file contains ONLY metadata.

No imports.
No analysis.
No execution.

Every sensor that Sentinel supports should be registered here.
"""

SENSORS = {

    # ==========================================================
    # CPU
    # ==========================================================

    "cpu_temp": {
        "display": "CPU Temperature",
        "keyword": "cpu (tctl/tdie)",
        "unit": "°C",
        "type": "temperature",
        "category": "CPU",
        "priority": 1,
        "description": "Overall CPU package temperature.",
        "health": "cpu_temperature_status"
    },

    "cpu_usage": {
        "display": "CPU Usage",
        "keyword": "total cpu usage",
        "unit": "%",
        "type": "usage",
        "category": "CPU",
        "priority": 2,
        "description": "Overall processor utilization.",
        "health": "cpu_usage_status"
    },

    # ==========================================================
    # GPU
    # ==========================================================

    "gpu_temp": {
        "display": "GPU Temperature",
        "keyword": "gpu temperature",
        "unit": "°C",
        "type": "temperature",
        "category": "GPU",
        "priority": 1,
        "description": "GPU core temperature.",
        "health": "gpu_temperature_status"
    },

    "gpu_usage": {
        "display": "GPU Usage",
        "keyword": "gpu core load",
        "unit": "%",
        "type": "usage",
        "category": "GPU",
        "priority": 2,
        "description": "GPU utilization.",
        "health": "gpu_usage_status"
    },

    # ==========================================================
    # Memory
    # ==========================================================

    "memory_usage": {
        "display": "Memory Usage",
        "keyword": "physical memory load",
        "unit": "%",
        "type": "usage",
        "category": "Memory",
        "priority": 1,
        "description": "System memory utilization.",
        "health": "memory_usage_status"
    },

    # ==========================================================
    # Performance
    # ==========================================================

    "fps": {
        "display": "Average FPS",
        "keyword": "framerate displayed (avg)",
        "unit": "FPS",
        "type": "performance",
        "category": "Performance",
        "priority": 1,
        "description": "Average displayed framerate.",
        "health": "fps_status"
    }

}

def get_sensor(sensor_name):
    """
    Return a sensor definition by its ID.
    """
    return SENSORS[sensor_name]


def get_all_sensors():
    """
    Return the complete sensor registry.
    """
    return SENSORS.values()


def get_category(category):
    """
    Return every sensor in a category.
    """

    return [
        sensor
        for sensor in SENSORS.values()
        if sensor["category"] == category
    ]