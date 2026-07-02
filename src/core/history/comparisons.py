# core/history/comparisons.py

"""
Project Sentinel

History Comparisons

Utilities for comparing Sentinel sessions.

These functions compare the most recent session against
the previous session and return structured comparison
objects suitable for historical intelligence reports.
"""

from core.models.session import Session


# ==========================================================
# Helpers
# ==========================================================

def sensor_average(
    session: Session,
    sensor_id: str,
):
    """
    Return the average value for a sensor.

    Parameters
    ----------
    session : Session

    sensor_id : str

    Returns
    -------
    float | None
    """

    try:
        return session.report["sensors"][sensor_id]["stats"]["average"]

    except (KeyError, TypeError):
        return None


def compare_sensor(
    previous: Session,
    current: Session,
    sensor_id: str,
):
    """
    Compare a sensor between two sessions.

    Returns
    -------
    dict
    """

    previous_value = sensor_average(
        previous,
        sensor_id,
    )

    current_value = sensor_average(
        current,
        sensor_id,
    )

    if previous_value is None or current_value is None:

        difference = None

    else:

        difference = current_value - previous_value

    return {

        "previous": previous_value,

        "current": current_value,

        "difference": difference,

    }


# ==========================================================
# Public Comparisons
# ==========================================================

def fps(
    previous: Session,
    current: Session,
):
    """
    Compare average FPS.
    """

    return compare_sensor(
        previous,
        current,
        "fps",
    )


def cpu_temperature(
    previous: Session,
    current: Session,
):
    """
    Compare CPU temperature.
    """

    return compare_sensor(
        previous,
        current,
        "cpu_temp",
    )


def cpu_usage(
    previous: Session,
    current: Session,
):
    """
    Compare CPU usage.
    """

    return compare_sensor(
        previous,
        current,
        "cpu_usage",
    )


def gpu_temperature(
    previous: Session,
    current: Session,
):
    """
    Compare GPU temperature.
    """

    return compare_sensor(
        previous,
        current,
        "gpu_temp",
    )


def gpu_usage(
    previous: Session,
    current: Session,
):
    """
    Compare GPU usage.
    """

    return compare_sensor(
        previous,
        current,
        "gpu_usage",
    )


def memory_used(
    previous: Session,
    current: Session,
):
    """
    Compare physical memory used.
    """

    return compare_sensor(
        previous,
        current,
        "memory_used",
    )


def memory_available(
    previous: Session,
    current: Session,
):
    """
    Compare physical memory available.
    """

    return compare_sensor(
        previous,
        current,
        "memory_available",
    )


def memory_load(
    previous: Session,
    current: Session,
):
    """
    Compare physical memory load.
    """

    return compare_sensor(
        previous,
        current,
        "memory_load",
    )