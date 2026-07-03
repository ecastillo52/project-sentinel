# core/models/report.py

"""
Project Sentinel

Report Model

Represents the complete results of one analysis session.

This model replaces the nested report dictionaries used
throughout earlier Sentinel versions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.models.sensor import Sensor


@dataclass(slots=True)
class Report:
    """
    Complete analysis report.
    """

    summary: dict[str, Any] = field(default_factory=dict)

    health: dict[str, Any] = field(default_factory=dict)
    # NOTE:
    # This is legacy/derived metadata.
    # Sensor.status is the authoritative health source.health: dict[str, Any] = field(default_factory=dict)
    # # NOTE:
    # # This is legacy/derived metadata.
    # # Sensor.status is the authoritative health source.

    sensors: dict[str, Sensor | dict[str, Any]] = field(
        default_factory=dict
    )

    warnings: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the report into a serializable dictionary.
        """

        sensors: dict[str, Any] = {}

        for sensor_id, sensor in self.sensors.items():

            if isinstance(sensor, Sensor):
                sensors[sensor_id] = sensor.to_dict()
            else:
                sensors[sensor_id] = sensor

        return {
            "summary": self.summary,
            "health": self.health,
            "sensors": sensors,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Report":
        """
        Create a Report from serialized data.
        """

        sensors: dict[str, Sensor | dict[str, Any]] = {}

        for sensor_id, sensor_data in data.get(
            "sensors",
            {},
        ).items():

            if (
                isinstance(sensor_data, dict)
                and "name" in sensor_data
                and "status" in sensor_data
            ):
                # Sensor.from_dict() now restores:
                # id
                # display
                # category
                # description
                # current
                # minimum
                # maximum
                # average
                # unit
                # status
                sensors[sensor_id] = Sensor.from_dict(
                    sensor_data
                )
            else:
                sensors[sensor_id] = sensor_data

        return cls(
            summary=data.get("summary", {}),
            health=data.get("health", {}),
            sensors=sensors,
            warnings=data.get("warnings", []),
            recommendations=data.get(
                "recommendations",
                [],
            ),
            metadata=data.get("metadata", {}),
        )

    # ======================================================
    # Convenience Properties
    # ======================================================

    @property
    def health_score(self) -> int | None:
        """
        Return overall health score if present.

        This is optional metadata and may not exist.
        """

        if not isinstance(self.health, dict):
            return None

        score = self.health.get("score")

        if isinstance(score, (int, float)):
            return int(score)

        return None

    @property
    def passed(self) -> bool:
        return not self.warnings

    @property
    def sensor_count(self) -> int:
        return len(self.sensors)

    @property
    def failed_sensors(self) -> list[Sensor]:
        """
        Return every sensor whose health status is not
        considered healthy.
        """

        return [
            sensor
            for sensor in self.sensors.values()
            if (
                isinstance(sensor, Sensor)
                and sensor.status.upper() not in {
                    "PASS",
                    "GOOD",
                }
            )
        ]

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def recommendation_count(self) -> int:
        return len(self.recommendations)

    # ======================================================
    # Helpers
    # ======================================================

    def add_warning(
        self,
        message: str,
    ) -> None:
        self.warnings.append(message)

    def add_recommendation(
        self,
        message: str,
    ) -> None:
        self.recommendations.append(message)

    # ======================================================
    # Display
    # ======================================================

    def __len__(self) -> int:
        return len(self.sensors)

    def __bool__(self) -> bool:
        return bool(self.sensors)

    def __repr__(self) -> str:
        return (
            f"Report("
            f"sensors={len(self.sensors)}, "
            f"warnings={len(self.warnings)}, "
            f"score={self.health_score})"
        )