# core/engine/health_engine.py

from __future__ import annotations

from core.models.sensor import Sensor


class HealthEngine:
    """
    Mutates Sensor objects with health status.
    """

    def __init__(self) -> None:
        self._rules = {
            "cpu_temperature_status": self.cpu_temperature_status,
            "cpu_usage_status": self.cpu_usage_status,
            "gpu_temperature_status": self.gpu_temperature_status,
            "gpu_usage_status": self.gpu_usage_status,
            "memory_usage_status": self.memory_usage_status,
            "fps_status": self.fps_status,
        }

    # ======================================================
    # Public
    # ======================================================

    def evaluate(self, sensors: list[Sensor]) -> list[Sensor]:
        for sensor in sensors:

            evaluator = self._rules.get(sensor.health_rule)

            if evaluator is None:
                sensor.status = "UNKNOWN"
                continue

            sensor.status = evaluator(sensor)

        return sensors

    # ======================================================
    # CPU
    # ======================================================

    def cpu_temperature_status(self, sensor: Sensor) -> str:
        avg = sensor.average

        if avg is None:
            return "UNKNOWN"
        if avg < 65:
            return "EXCELLENT"
        if avg < 75:
            return "HEALTHY"
        if avg < 85:
            return "WARM"
        return "CRITICAL"

    def cpu_usage_status(self, sensor: Sensor) -> str:
        avg = sensor.average

        if avg is None:
            return "UNKNOWN"
        if avg < 70:
            return "HEALTHY"
        if avg < 95:
            return "BUSY"
        return "MAXED"

    # ======================================================
    # GPU
    # ======================================================

    def gpu_temperature_status(self, sensor: Sensor) -> str:
        avg = sensor.average

        if avg is None:
            return "UNKNOWN"
        if avg < 60:
            return "EXCELLENT"
        if avg < 70:
            return "HEALTHY"
        if avg < 82:
            return "WARM"
        return "CRITICAL"

    def gpu_usage_status(self, sensor: Sensor) -> str:
        avg = sensor.average

        if avg is None:
            return "UNKNOWN"
        if avg < 85:
            return "HEALTHY"
        if avg < 97:
            return "BUSY"
        return "MAXED"

    # ======================================================
    # Memory
    # ======================================================

    def memory_usage_status(self, sensor: Sensor) -> str:
        avg = sensor.average

        if avg is None:
            return "UNKNOWN"
        if avg < 70:
            return "HEALTHY"
        if avg < 90:
            return "HIGH"
        return "CRITICAL"

    # ======================================================
    # Performance
    # ======================================================

    def fps_status(self, sensor: Sensor) -> str:
        avg = sensor.average

        if avg is None:
            return "UNKNOWN"
        if avg >= 144:
            return "EXCELLENT"
        if avg >= 120:
            return "HEALTHY"
        if avg >= 60:
            return "PLAYABLE"
        return "POOR"