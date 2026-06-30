# core/reader.py

from pathlib import Path
import csv

def load_hwinfo_log(file_path):

    with open(file_path, newline="", encoding="cp1252") as file:
        reader = list(csv.reader(file))

    headers = [h.strip() for h in reader[0]]
    rows = reader[1:]

    header_map = {}

    for i, header in enumerate(headers):
        header_map[header] = i

    log = {
        "headers": headers,
        "rows": rows,
        "header_map": header_map,
        "filename": Path(file_path).name,
        "filepath": str(file_path),
        "sample_count": len(rows),
    }

    return log
