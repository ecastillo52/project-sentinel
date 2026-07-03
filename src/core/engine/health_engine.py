# core/engine/health_engine.py

"""
Project Sentinel

Health Engine

Evaluates analyzed sensor statistics and determines
hardware health classifications.
"""

from __future__ import annotations

from typing import Any

from .sensors import get_all_sensors

Stats = dict[str, Any] | None


class HealthEngine:
    """
    Determines health classifications for analyzed sensors.
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

    def evaluate(
        self,
        analysis: dict[str, dict[str, Any]],
    ) -> dict[str, str]:
        """
        Evaluate every analyzed sensor.
        """

        results: dict[str, str] = {}

        for sensor in get_all_sensors():

            sensor_id = sensor["id"]

            sensor_result = analysis.get(
                sensor_id
            )

            if sensor_result is None:

                results[sensor_id] = "Unknown"
                continue

            stats = sensor_result["stats"]

            evaluator = self._rules.get(
                sensor["health"]
            )

            if evaluator is None:

                results[sensor_id] = "Unknown"
                continue

            results[sensor_id] = evaluator(
                stats
            )

        return results

    # ======================================================
    # Helpers
    # ======================================================

    @staticmethod
    def average(
        stats: Stats,
    ) -> float | None:

        if stats is None:
            return None

        return stats.get(
            "average"
        )

    # ======================================================
    # CPU
    # ======================================================

    def cpu_temperature_status(
        self,
        stats: Stats,
    ) -> str:

        avg = self.average(stats)

        if avg is None:
            return "Unknown"

        if avg < 65:
            return "Excellent"

        if avg < 75:
            return "Healthy"

        if avg < 85:
            return "Warm"

        return "Critical"

    def cpu_usage_status(
        self,
        stats: Stats,
    ) -> str:

        avg = self.average(stats)

        if avg is None:
            return "Unknown"

        if avg < 70:
            return "Healthy"

        if avg < 95:
            return "Busy"

        return "Maxed"

    # ======================================================
    # GPU
    # ======================================================

    def gpu_temperature_status(
        self,
        stats: Stats,
    ) -> str:

        avg = self.average(stats)

        if avg is None:
            return "Unknown"

        if avg < 60:
            return "Excellent"

        if avg < 70:
            return "Healthy"

        if avg < 82:
            return "Warm"

        return "Critical"

    def gpu_usage_status(
        self,
        stats: Stats,
    ) -> str:

        avg = self.average(stats)

        if avg is None:
            return "Unknown"

        if avg < 85:
            return "Healthy"

        if avg < 97:
            return "Busy"

        return "Maxed"

    # ======================================================
    # Memory
    # ======================================================

    def memory_usage_status(
        self,
        stats: Stats,
    ) -> str:

        avg = self.average(stats)

        if avg is None:
            return "Unknown"

        if avg < 70:
            return "Healthy"

        if avg < 90:
            return "High"

        return "Critical"

    # ======================================================
    # Performance
    # ======================================================

    def fps_status(
        self,
        stats: Stats,
    ) -> str:

        avg = self.average(stats)

        if avg is None:
            return "Unknown"

        if avg >= 144:
            return "Excellent"

        if avg >= 120:
            return "Healthy"

        if avg >= 60:
            return "Playable"

        return "Poor"