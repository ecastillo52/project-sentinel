# core/analyzer.py

"""
Project Sentinel

Analysis Engine

Responsible for:

    Header Matching
        ↓
    Data Extraction
        ↓
    Value Cleaning
        ↓
    Statistics

This module performs sensor analysis only.

It contains no health evaluation or report construction.
"""

from __future__ import annotations

import re
from typing import Any

from .sensors import get_all_sensors

NUMBER_PATTERN = re.compile(
    r"-?\d+(?:,\d{3})*(?:\.\d+)?"
)

Log = dict[str, Any]
SensorDefinition = dict[str, Any]


class Analyzer:
    """
    Analyzes every configured sensor within a HWiNFO log.
    """

    def analyze(
        self,
        log: Log,
    ) -> dict[str, dict[str, Any]]:
        """
        Analyze every configured sensor.
        """

        results: dict[str, dict[str, Any]] = {}

        for sensor in get_all_sensors():

            stats = analyze_sensor(
                log,
                sensor,
            )

            results[sensor["id"]] = {
                "display": sensor["display"],
                "description": sensor["description"],
                "category": sensor["category"],
                "type": sensor.get("type", ""),
                "unit": sensor["unit"],
                "stats": stats,
                "health": sensor["health"],
            }

        return results


# ==========================================================
# Header Matching
# ==========================================================


def normalize(text: Any) -> str:

    return str(text).lower().strip()


def score_header(
    header: str,
    keyword: str,
) -> int:

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


def find_best_match(
    log: Log,
    keyword: str,
) -> str | None:

    scored = []

    for header in log["header_map"]:

        score = score_header(
            header,
            keyword,
        )

        if score > 0:
            scored.append(
                (score, header)
            )

    if not scored:
        return None

    scored.sort(reverse=True)

    return scored[0][1]


# ==========================================================
# Extraction
# ==========================================================


def extract_column(
    log: Log,
    header: str,
) -> list[str]:

    index = log["header_map"][header]

    return [
        row[index]
        for row in log["rows"]
    ]


def clean_values(
    values: list[Any],
    value_type: str,
) -> list[Any]:

    cleaned = []

    if value_type == "float":

        for value in values:

            if value is None:
                continue

            match = NUMBER_PATTERN.search(
                str(value).replace(",", "")
            )

            if match:
                cleaned.append(
                    float(match.group())
                )

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


# ==========================================================
# Statistics
# ==========================================================


def calculate_statistics(
    numbers: list[float],
) -> dict[str, Any] | None:

    if not numbers:
        return None

    return {
        "current": numbers[-1],
        "minimum": min(numbers),
        "maximum": max(numbers),
        "average": round(
            sum(numbers) / len(numbers),
            2,
        ),
        "samples": len(numbers),
    }


# ==========================================================
# Sensor Analysis
# ==========================================================


def analyze_sensor(
    log: Log,
    sensor: SensorDefinition,
) -> dict[str, Any] | None:

    header = find_best_match(
        log,
        sensor["keyword"],
    )

    if header is None:
        return None

    values = extract_column(
        log,
        header,
    )

    numbers = clean_values(
        values,
        sensor["value_type"],
    )

    return calculate_statistics(
        numbers,
    )