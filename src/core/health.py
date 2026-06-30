# core/health.py

def cpu_temperature_status(stats):
    if stats is None:
        return "Unknown"

    avg = stats["average"]

    if avg < 75:
        return "Healthy"

    if avg < 85:
        return "Warm"

    return "Critical"


def gpu_temperature_status(stats):
    if stats is None:
        return "Unknown"

    avg = stats["average"]

    if avg < 70:
        return "Healthy"

    if avg < 82:
        return "Warm"

    return "Critical"


def cpu_usage_status(stats):
    if stats is None:
        return "Unknown"

    return "Normal"


def fps_status(stats):
    if stats is None:
        return "Unknown"

    avg = stats["average"]

    if avg >= 120:
        return "Excellent"

    if avg >= 60:
        return "Playable"

    return "Poor"