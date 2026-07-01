# core/reader.py

"""
Project Sentinel

HWiNFO Reader

Responsible ONLY for loading HWiNFO CSV logs.

Returns a normalized log object for the analyzer.
"""

from pathlib import Path
import csv


def _read_csv(path, encoding):

    with open(path, newline="", encoding=encoding) as f:
        return list(csv.reader(f))


def load_hwinfo_log(file_path):
    """
    Load a HWiNFO CSV log.

    Returns:

    {
        headers,
        header_map,
        rows,
        filename,
        filepath,
        sample_count
    }
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(path)

    # Try UTF-8 first, then Windows encoding.
    try:
        reader = _read_csv(path, "utf-8")

    except UnicodeDecodeError:
        reader = _read_csv(path, "cp1252")

    if not reader:
        raise ValueError("CSV file is empty.")

    headers = [
        header.strip()
        for header in reader[0]
    ]

    rows = reader[1:]

    header_map = {
        header: index
        for index, header in enumerate(headers)
    }

    return {

        "headers": headers,

        "header_map": header_map,

        "rows": rows,

        "filename": path.name,

        "filepath": str(path.resolve()),

        "sample_count": len(rows)

    }