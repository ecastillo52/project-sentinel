# core/analyzer.py

import re

NUMBER_PATTERN = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")


# ==========================================================
# HEADER MATCHING ENGINE
# ==========================================================

def normalize(text):
    return str(text).lower().strip()


def score_header(header, keyword):

    h = normalize(header)
    k = normalize(keyword)

    if k not in h:
        return 0

    score = 5

    if "avg" in h:
        score += 2

    if "package" in h:
        score += 3

    if "total" in h:
        score += 1

    if "core" in h:
        score -= 2

    if "thread" in h:
        score -= 2

    return score


def find_best_match(log, keyword):

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
# DATA EXTRACTION
# ==========================================================

def extract_column(log, header):

    index = log["header_map"][header]

    return [
        row[index]
        for row in log["rows"]
    ]


def clean_values(values, value_type):

    cleaned = []

    if value_type == "float":

        for value in values:

            if value is None:
                continue

            text = str(value).replace(",", "")

            match = NUMBER_PATTERN.search(text)

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
# STATISTICS
# ==========================================================

def calculate_statistics(numbers):

    if not numbers:
        return None

    return {

        "current": numbers[-1],

        "minimum": min(numbers),

        "maximum": max(numbers),

        "average": round(sum(numbers) / len(numbers), 2),

        "samples": len(numbers)

    }


# ==========================================================
# ANALYSIS
# ==========================================================

def analyze_sensor(log, keyword, value_type="float"):

    header = find_best_match(log, keyword)

    if header is None:
        return None

    values = extract_column(log, header)

    numbers = clean_values(values, value_type)

    return calculate_statistics(numbers)