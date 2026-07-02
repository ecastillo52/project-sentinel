# core/history/comparisons.py

"""
Project Sentinel

History Comparisons

Compare two Sentinel sessions.
"""

from core.models.session import Session


# ==========================================================
# Generic Comparisons
# ==========================================================

def sensor_difference(
    previous: Session,
    current: Session,
    sensor_id: str,
) -> float:
    """
    Compare average values for a sensor.
    """

    previous_value = (
        previous.report["sensors"][sensor_id]["stats"]["average"]
    )

    current_value = (
        current.report["sensors"][sensor_id]["stats"]["average"]
    )

    return current_value - previous_value


# ==========================================================
# Sensor Comparisons
# ==========================================================

def fps_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare average FPS.
    """

    return sensor_difference(
        previous,
        current,
        "fps",
    )


def cpu_temperature_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare CPU temperature.
    """

    return sensor_difference(
        previous,
        current,
        "cpu_temp",
    )


def cpu_usage_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare CPU usage.
    """

    return sensor_difference(
        previous,
        current,
        "cpu_usage",
    )


def gpu_temperature_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare GPU temperature.
    """

    return sensor_difference(
        previous,
        current,
        "gpu_temp",
    )


def gpu_usage_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare GPU usage.
    """

    return sensor_difference(
        previous,
        current,
        "gpu_usage",
    )


def memory_used_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare physical memory used.
    """

    return sensor_difference(
        previous,
        current,
        "memory_used",
    )


def memory_available_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare physical memory available.
    """

    return sensor_difference(
        previous,
        current,
        "memory_available",
    )


def memory_load_difference(
    previous: Session,
    current: Session,
) -> float:
    """
    Compare physical memory load.
    """

    return sensor_difference(
        previous,
        current,
        "memory_load",
    )