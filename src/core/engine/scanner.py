# core/engine/scanner.py

"""
Project Sentinel

Log Scanner

Responsible only for discovering HWiNFO log files.

The scanner performs no duplicate detection, validation,
or analysis. It simply locates supported log files on disk.
"""

from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTENSIONS = (
    ".csv",
)


class LogScanner:
    """
    Discovers HWiNFO log files.
    """

    def find_logs(
        self,
        folder: str | Path,
        *,
        recursive: bool = False,
    ) -> list[Path]:
        """
        Discover every supported log file.
        """

        folder = Path(folder)

        if not folder.exists():
            return []

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


# ==========================================================
# Module Singleton
# ==========================================================

_scanner = LogScanner()


# ==========================================================
# Backwards-Compatible API
# ==========================================================

def find_logs(
    folder: str | Path,
    recursive: bool = False,
) -> list[Path]:
    """
    Discover every supported log file.
    """

    return _scanner.find_logs(
        folder,
        recursive=recursive,
    )


def get_new_logs(
    folder: str | Path,
    recursive: bool = False,
) -> list[Path]:
    """
    Backwards-compatible alias.

    Duplicate detection is now handled by AnalysisService,
    so every discovered log is considered a candidate for
    analysis.
    """

    return find_logs(
        folder,
        recursive=recursive,
    )