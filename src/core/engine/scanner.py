# core/scanner.py

"""
Project Sentinel

Log Scanner

Responsible ONLY for discovering new HWiNFO logs.
"""

from pathlib import Path

from ..metadata.database import record_exists

SUPPORTED_EXTENSIONS = (
    ".csv",
)


def find_logs(folder, recursive=False):
    """
    Find every supported log file.
    """

    folder = Path(folder)

    if recursive:
        iterator = folder.rglob("*")
    else:
        iterator = folder.iterdir()

    logs = []

    for file in iterator:

        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ):
            logs.append(file)

    return sorted(logs)


def get_new_logs(folder):

    return [

        log

        for log in find_logs(folder)

        if not record_exists(log)

    ]