# core/report/models.py

"""
Project Sentinel

Report Models

Strongly-typed representations of a completed Sentinel report.

These models are not yet used by the rendering pipeline, which
currently operates on dictionaries. They exist to document the
report schema and prepare for a future transition to typed objects.
"""

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# Session
# ==========================================================

@dataclass(slots=True)
class SessionInfo:
    game: str = "Unknown"
    log_file: str = ""
    date: str = ""


# ==========================================================
# Machine
# ==========================================================

@dataclass(slots=True)
class MachineInfo:
    cpu: str = ""
    gpu: str = ""
    ram: str = ""
    motherboard: str = ""


# ==========================================================
# Sensor
# ==========================================================

@dataclass(slots=True)
class SensorReport:
    id: str = ""

    display: str = ""
    description: str = ""

    category: str = ""
    type: str = ""

    unit: str = ""

    stats: dict[str, Any] | None = None

    status: str = ""


# ==========================================================
# Summary
# ==========================================================

@dataclass(slots=True)
class SessionSummary:
    average_fps: float | None = None

    peak_cpu_temp: float | None = None
    peak_gpu_temp: float | None = None
    peak_ram_usage: float | None = None

    overall_health: str = "Unknown"


# ==========================================================
# Report
# ==========================================================

@dataclass(slots=True)
class Report:
    session: SessionInfo = field(default_factory=SessionInfo)

    machine: MachineInfo = field(default_factory=MachineInfo)

    sensors: dict[str, SensorReport] = field(default_factory=dict)

    summary: SessionSummary = field(default_factory=SessionSummary)