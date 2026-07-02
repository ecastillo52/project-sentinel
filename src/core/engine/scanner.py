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


def find_logs(
    folder: str | Path,
    recursive: bool = False,
) -> list[Path]:
    """
    Find every supported log file.
    """

    folder = Path(folder)

    iterator = (
        folder.rglob("*")
        if recursive
        else folder.iterdir()
    )

    return sorted(
        file
        for file in iterator
        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        )
    )


def get_new_logs(
    folder: str | Path,
) -> list[Path]:
    """
    Return only logs that have not yet been recorded.
    """

    return [
        log
        for log in find_logs(folder)
        if not record_exists(log)
    ]