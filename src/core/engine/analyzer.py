# core/engine/analyzer.py

from __future__ import annotations

import re
from typing import Any, List

from .sensors import get_all_sensors
from core.models.sensor import Sensor  # <-- adjust if path differs


NUMBER_PATTERN = re.compile(
    r"-?\d+(?:,\d{3})*(?:\.\d+)?"
)

Log = dict[str, Any]
SensorDefinition = dict[str, Any]


class Analyzer:
    """
    Converts raw log data into Sensor objects with statistics.
    """

    def analyze(self, log: Log) -> list[Sensor]:
        sensors: list[Sensor] = []

        for definition in get_all_sensors():

            stats = analyze_sensor(log, definition)

            sensor = Sensor(
                id=definition["id"],
                name=definition.get("name", definition["id"]),
                display=definition["display"],
                category=definition["category"],
                description=definition["description"],
                unit=definition["unit"],
                health_rule=definition["health"],
            )

            # ✅ Map stats into fields (THIS is the key fix)
            if stats:
                if not stats:
                    continue

                sensor.current = stats.get("current")
                sensor.minimum = stats.get("minimum")
                sensor.maximum = stats.get("maximum")
                sensor.average = stats.get("average")

            sensors.append(sensor)

        return sensors


# ==========================================================
# Header Matching
# ==========================================================


def normalize(text: Any) -> str:
    return str(text).lower().strip()


def score_header(header: str, keyword: str) -> int:
    header = normalize(header)
    keyword = normalize(keyword)

    if keyword not in header:
        return 0

    score = 5

    if "avg" in header:
        score += 2
    if "package" in header:
        score += 3
    if "total" in header:
        score += 1
    if "core" in header:
        score -= 2
    if "thread" in header:
        score -= 2

    return score


def find_best_match(log: Log, keyword: str) -> str | None:
    scored = []

    for header in log["header_map"]:
        score = score_header(header, keyword)
        if score > 0:
            scored.append((score, header))

    if not scored:
        return None

    scored.sort(reverse=True)
    return scored[0][1]


# ==========================================================
# Extraction
# ==========================================================


def extract_column(log, header):
    index = log["header_map"][header]

    values = []

    for row in log["rows"]:
        if index < len(row):
            values.append(row[index])
        else:
            values.append("")

    return values


def clean_values(values: list[Any], value_type: str) -> list[Any]:
    cleaned = []

    if value_type == "float":
        for value in values:
            if value is None:
                continue

            match = NUMBER_PATTERN.search(str(value).replace(",", ""))
            if match:
                cleaned.append(float(match.group()))

    elif value_type == "bool":
        for value in values:
            text = str(value).strip().lower()

            if text == "yes":
                cleaned.append(True)
            elif text == "no":
                cleaned.append(False)

    else:
        cleaned = list(values)

    return cleaned


def transform_values(
    values: list[float],
    sensor: SensorDefinition,
) -> list[float]:
    transform = sensor.get("transform")

    if transform == "mb_to_gb":
        return [round(value / 1024, 2) for value in values]

    return values


# ==========================================================
# Statistics
# ==========================================================


def calculate_statistics(numbers: list[float]) -> dict[str, Any] | None:
    if not numbers:
        return None

    return {
        "current": numbers[-1],
        "minimum": min(numbers),
        "maximum": max(numbers),
        "average": round(sum(numbers) / len(numbers), 2),
        "samples": len(numbers),
    }


# ==========================================================
# Sensor Analysis
# ==========================================================


def analyze_sensor(log: Log, sensor: SensorDefinition) -> dict[str, Any] | None:
    header = find_best_match(log, sensor["keyword"])

    if header is None:
        return None

    values = extract_column(log, header)

    numbers = clean_values(values, sensor["value_type"])

    numbers = transform_values(numbers, sensor)

    return calculate_statistics(numbers)
