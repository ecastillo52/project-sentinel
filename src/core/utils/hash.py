# core/utils/hash.py

"""
Project Sentinel

Hash Utilities

Provides helper functions for generating hashes used
throughout Sentinel.
"""

from __future__ import annotations

import hashlib

from pathlib import Path


def sha256(path: Path | str) -> str:
    """
    Compute the SHA-256 hash of a file.
    """

    path = Path(path)

    digest = hashlib.sha256()

    with path.open("rb") as file:

        for chunk in iter(
            lambda: file.read(8192),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()