# core/reader.py

"""
Project Sentinel

HWiNFO Reader

Responsible only for loading HWiNFO CSV logs.

Returns a normalized log object for the Analyzer.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class Reader:
    """
    Loads HWiNFO CSV logs.
    """

    def read(
        self,
        file_path: str | Path,
    ) -> dict[str, Any]:
        """
        Load a HWiNFO CSV log.

        Returns
        -------
        dict
            Normalized log object.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        try:
            csv_rows = self._read_csv(
                path,
                "utf-8",
            )

        except UnicodeDecodeError:

            csv_rows = self._read_csv(
                path,
                "cp1252",
            )

        if not csv_rows:
            raise ValueError(
                "CSV file is empty."
            )

        headers = [
            header.strip()
            for header in csv_rows[0]
        ]

        rows = [
            row
            for row in csv_rows[1:]
            if self._is_sample_row(row)
        ]

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
            "sample_count": len(rows),
        }

    # ======================================================
    # Internal
    # ======================================================

    @staticmethod
    def _read_csv(
        path: Path,
        encoding: str,
    ) -> list[list[str]]:
        """
        Read a CSV using the specified encoding.
        """

        with path.open(
            newline="",
            encoding=encoding,
        ) as file:

            return list(
                csv.reader(file)
            )

    @staticmethod
    def _is_sample_row(row: list[str]) -> bool:
        """
        Keep timestamped data rows and ignore HWiNFO footer metadata.
        """

        if len(row) < 2:
            return False

        date = row[0].strip().lower()
        time = row[1].strip().lower()

        if not date or not time:
            return False

        return date != "date" and time != "time"
