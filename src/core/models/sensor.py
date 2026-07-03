# core/models/sensor.py

"""
Project Sentinel

Sensor Model

Represents one analyzed HWiNFO sensor.

Every subsystem operates on Sensor objects instead of
nested dictionaries.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Sensor:
    """
    Represents one analyzed sensor.
    """

    # ======================================================
    # Identity
    # ======================================================

    id: str = ""

    name: str = ""
    display: str = ""
    category: str = ""
    description: str = ""

    # ======================================================
    # Statistics
    # ======================================================

    current: float | int | None = None
    minimum: float | int | None = None
    maximum: float | int | None = None
    average: float | int | None = None

    unit: str = ""

    # ======================================================
    # Health
    # ======================================================

    health_rule: str = ""

    status: str = "UNKNOWN"

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict:
        """
        Serialize this Sensor into a dictionary.
        """

        return {
            "id": self.id,
            "name": self.name,
            "display": self.display,
            "category": self.category,
            "description": self.description,
            "current": self.current,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "average": self.average,
            "unit": self.unit,
            "health_rule": self.health_rule,
            "status": self.status,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "Sensor":
        """
        Construct a Sensor from a serialized dictionary.
        """

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            display=data.get(
                "display",
                data.get("name", ""),
            ),
            category=data.get(
                "category",
                "Other",
            ),
            description=data.get(
                "description",
                "",
            ),
            current=data.get("current"),
            minimum=data.get("minimum"),
            maximum=data.get("maximum"),
            average=data.get("average"),
            unit=data.get("unit", ""),
            health_rule=data.get("health_rule", ""),
            status=data.get(
                "status",
                "UNKNOWN",
            ),
        )

    # ======================================================
    # Convenience Properties
    # ======================================================

    @property
    def healthy(self) -> bool:
        """
        Determine whether this sensor passed its
        health evaluation.
        """

        return self.status.upper() in {
            "GOOD",
            "PASS",
            "HEALTHY",
            "EXCELLENT",
        }

    @property
    def has_data(self) -> bool:
        """
        Determine whether statistics were collected.
        """

        return any(
            value is not None
            for value in (
                self.current,
                self.minimum,
                self.maximum,
                self.average,
            )
        )

    @property
    def value(self) -> float | int | None:
        """
        Return the sensor's primary value.

        By convention this is the current reading.
        """

        return self.current

    # ======================================================
    # Display
    # ======================================================

    def __str__(self) -> str:
        return self.display or self.name

    def __repr__(self) -> str:
        return (
            f"Sensor("
            f"id={self.id!r}, "
            f"display={self.display!r}, "
            f"average={self.average}, "
            f"status={self.status!r}, "
            f"health_rule={self.health_rule!r})"
        )