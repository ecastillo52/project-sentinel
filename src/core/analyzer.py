# core/analyzer.py

# =========================
# HEADER MATCHING ENGINE
# =========================

def normalize(text):
    return text.lower().strip()


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

    if "core" in h or "thread" in h:
        score -= 2

    return score


def find_best_match(log, keyword):
    headers = log["header_map"].keys()

    scored = []

    for header in headers:
        s = score_header(header, keyword)
        if s > 0:
            scored.append((s, header))

    if not scored:
        raise ValueError(f"No match found for '{keyword}'")

    scored.sort(reverse=True)
    return scored[0][1]


# =========================
# DATA PIPELINE
# =========================

def extract_column(log, header_name):
    index = log["header_map"][header_name]
    return [row[index] for row in log["rows"]]


import re

NUMBER_PATTERN = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")

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


def calculate_statistics(numbers):
    if not numbers:
        return None

    return {
        "minimum": min(numbers),
        "maximum": max(numbers),
        "average": sum(numbers) / len(numbers),
    }


def analyze_sensor(log, keyword, value_type="float"):
    header = find_best_match(log, keyword)
    values = extract_column(log, header)
    numbers = clean_values(values, value_type)
    return calculate_statistics(numbers)


