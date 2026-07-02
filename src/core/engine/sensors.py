# core/sensors.py

"""
Project Sentinel

Sensor Registry

This module contains ONLY sensor metadata.

No imports from the analysis engine.
No business logic.
No execution.

Every sensor supported by Sentinel is registered here.
"""

from typing import Any

Sensor = dict[str, Any]

SENSORS = {

    # ==========================================================
    # CPU
    # ==========================================================

    "cpu_temp": {
        "display": "CPU Temperature",
        "keyword": "cpu (tctl/tdie)",
        "unit": "°C",
        "value_type": "float",
        "type": "temperature",
        "category": "CPU",
        "priority": 1,
        "description": "Overall CPU package temperature.",
        "health": "cpu_temperature_status",
    },

    "cpu_usage": {
        "display": "CPU Usage",
        "keyword": "total cpu usage",
        "unit": "%",
        "value_type": "float",
        "type": "usage",
        "category": "CPU",
        "priority": 2,
        "description": "Overall processor utilization.",
        "health": "cpu_usage_status",
    },

    # ==========================================================
    # GPU
    # ==========================================================

    "gpu_temp": {
        "display": "GPU Temperature",
        "keyword": "gpu temperature",
        "unit": "°C",
        "value_type": "float",
        "type": "temperature",
        "category": "GPU",
        "priority": 1,
        "description": "GPU core temperature.",
        "health": "gpu_temperature_status",
    },

    "gpu_usage": {
        "display": "GPU Usage",
        "keyword": "gpu core load",
        "unit": "%",
        "value_type": "float",
        "type": "usage",
        "category": "GPU",
        "priority": 2,
        "description": "GPU utilization.",
        "health": "gpu_usage_status",
    },

    # ==========================================================
    # Memory
    # ==========================================================

    "memory_used": {
        "display": "Physical Memory Used",
        "keyword": "physical memory used",
        "unit": "GB",
        "value_type": "float",
        "type": "memory",
        "category": "Memory",
        "priority": 1,
        "description": "Amount of physical memory currently in use.",
        "health": "memory_usage_status",
    },

    "memory_available": {
        "display": "Physical Memory Available",
        "keyword": "physical memory available",
        "unit": "GB",
        "value_type": "float",
        "type": "memory",
        "category": "Memory",
        "priority": 2,
        "description": "Amount of available physical memory.",
        "health": "memory_usage_status",
    },

    "memory_load": {
        "display": "Physical Memory Load",
        "keyword": "physical memory load",
        "unit": "%",
        "value_type": "float",
        "type": "memory",
        "category": "Memory",
        "priority": 3,
        "description": "Overall physical memory utilization.",
        "health": "memory_usage_status",
    },

    # ==========================================================
    # Performance
    # ==========================================================

    "fps": {
        "display": "Average FPS",
        "keyword": "framerate displayed (avg)",
        "unit": "FPS",
        "value_type": "float",
        "type": "performance",
        "category": "Performance",
        "priority": 1,
        "description": "Average displayed framerate.",
        "health": "fps_status",
    },

}


def _build_sensor(sensor_id: str) -> Sensor:
    """
    Return a copy of a sensor definition with its ID attached.
    """

    sensor = SENSORS[sensor_id].copy()
    sensor["id"] = sensor_id

    return sensor


def get_sensor(sensor_name: str) -> Sensor:
    """
    Return a single sensor definition.
    """

    return _build_sensor(sensor_name)


def get_all_sensors() -> list[Sensor]:
    """
    Return every registered sensor sorted by category and priority.
    """

    sensors = [
        _build_sensor(sensor_id)
        for sensor_id in SENSORS
    ]

    return sorted(
        sensors,
        key=lambda sensor: (
            sensor["category"],
            sensor["priority"],
        ),
    )


def get_category(category: str) -> list[Sensor]:
    """
    Return every sensor belonging to a category.
    """

    sensors = [
        _build_sensor(sensor_id)
        for sensor_id, sensor in SENSORS.items()
        if sensor["category"] == category
    ]

    return sorted(
        sensors,
        key=lambda sensor: sensor["priority"],
    )