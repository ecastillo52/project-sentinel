# core/report/builder.py

"""
Project Sentinel

Report Builder

Constructs Report objects from completed analysis.
"""

from __future__ import annotations

from typing import Any

from core.engine.sensors import get_all_sensors
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
        analysis: dict[str, dict[str, Any] | None],
        health: dict[str, str],
        machine: dict[str, Any],
    ) -> Report:
        """
        Build a complete Report object.
        """

        sensors: dict[str, Sensor] = {}

        # --------------------------------------------------
        # Build Sensor Models
        # --------------------------------------------------

        for definition in get_all_sensors():

            sensor_id = definition["id"]

            analysis_entry = analysis.get(sensor_id) or {}
            stats = analysis_entry.get("stats") or {}

            sensors[sensor_id] = Sensor(
                id=sensor_id,
                name=definition["display"],
                display=definition["display"],
                category=definition.get("category", "Other"),
                description=definition.get("description", ""),

                current=stats.get("current"),
                minimum=stats.get("minimum"),
                maximum=stats.get("maximum"),
                average=stats.get("average"),

                unit=definition.get("unit", ""),
                status=health.get(sensor_id, "UNKNOWN"),
            )

        # --------------------------------------------------
        # Build Report
        # --------------------------------------------------

        report = Report(
            sensors=sensors,
            health=health,
            metadata={
                "machine": machine,
            },
        )

        # --------------------------------------------------
        # Generate Summary
        # --------------------------------------------------

        report.summary = build_summary(
            report.to_dict()
        )

        return report