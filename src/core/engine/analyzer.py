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

This module knows how to analyze a sensor definition but
contains no health or reporting logic.
"""

import re
from typing import Any

NUMBER_PATTERN = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")

Log = dict[str, Any]
Sensor = dict[str, Any]


# ==========================================================
# Header Matching
# ==========================================================


def normalize(text: Any) -> str:
    """
    Normalize text for case-insensitive matching.
    """

    return str(text).lower().strip()


def score_header(
    header: str,
    keyword: str,
) -> int:
    """
    Score how closely a header matches a sensor keyword.
    """

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
    """
    Find the highest-scoring header.
    """

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
# Data Extraction
# ==========================================================


def extract_column(
    log: Log,
    header: str,
) -> list[str]:
    """
    Extract a column from the log.
    """

    index = log["header_map"][header]

    return [
        row[index]
        for row in log["rows"]
    ]


def clean_values(
    values: list[Any],
    value_type: str,
) -> list[Any]:
    """
    Convert raw CSV values into Python values.
    """

    cleaned = []

    if value_type == "float":

        for value in values:

            if value is None:
                continue

            match = NUMBER_PATTERN.search(
                str(value).replace(",", "")
            )

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


# ==========================================================
# Statistics
# ==========================================================


def calculate_statistics(
    numbers: list[float],
) -> dict[str, Any] | None:
    """
    Calculate descriptive statistics.
    """

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
# Analysis
# ==========================================================


def analyze_sensor(
    log: Log,
    sensor: Sensor,
) -> dict[str, Any] | None:
    """
    Analyze a sensor definition against a HWiNFO log.
    """

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

    return calculate_statistics(numbers)