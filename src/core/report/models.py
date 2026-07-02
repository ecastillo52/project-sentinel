# core/report/models.py

from dataclasses import dataclass, field


@dataclass
class SessionInfo:
    game: str = "Unknown"
    log_file: str = ""
    date: str = ""
    duration: str = ""


@dataclass
class MachineInfo:
    cpu: str = ""
    gpu: str = ""
    ram: str = ""
    motherboard: str = ""


@dataclass
class SensorReport:
    display: str = ""
    category: str = ""
    unit: str = ""
    description: str = ""

    current: float | None = None
    average: float | None = None
    minimum: float | None = None
    maximum: float | None = None

    status: str = ""


@dataclass
class SessionSummary:
    average_fps: float | None = None

    peak_cpu_temp: float | None = None
    peak_gpu_temp: float | None = None
    peak_ram_usage: float | None = None

    overall_health: str = ""


@dataclass
class Report:
    session: SessionInfo = field(default_factory=SessionInfo)
    machine: MachineInfo = field(default_factory=MachineInfo)

    sensors: dict[str, SensorReport] = field(default_factory=dict)

    summary: SessionSummary = field(default_factory=SessionSummary)