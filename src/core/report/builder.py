# core/report/builder.py

from __future__ import annotations


from core.engine.recommendation import (
    generate as build_recommendations,
)
from core.engine.summary import build_summary

from core.models.report import Report
from core.models.sensor import Sensor


class ReportBuilder:
    """
    Builds Report models from completed analysis.
    """

    def build(
        self,
        *,
        sensors: list[Sensor],
        machine: dict,
    ) -> Report:
        """
        Build a complete Report object from Sensor objects.
        """

        # Convert list → dict (for easy lookup)
        sensor_map: dict[str, Sensor] = {
            sensor.id: sensor for sensor in sensors
        }

        # --------------------------------------------------
        # Build Report
        # --------------------------------------------------

        report = Report(
            sensors=sensor_map,
            health={
                sensor.id: sensor.status
                for sensor in sensors
            },
            metadata={
                "machine": machine,
            },
        )

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        report.summary = build_summary(report)

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        report.recommendations = (
            build_recommendations(report)
        )

        return report