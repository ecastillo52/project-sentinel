# core/history.py

from pathlib import Path
from core.ingest import process_file


def process_all_files(data_folder):
    """
    Processes every CSV file and stores results in database.
    """

    files = Path(data_folder).glob("*.CSV")

    processed = []

    for file in files:
        result = process_file(file)
        processed.append(result)

    return processed