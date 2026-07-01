# core/hashing.py

"""
Project Sentinel

Hashing Utilities

Provides SHA-256 hashing for files and text.

Used for:

- Duplicate detection
- Session integrity
- Future report verification
"""

from pathlib import Path
import hashlib


CHUNK_SIZE = 8192


def file_hash(path):
    """
    Return the SHA-256 hash of a file.
    """

    path = Path(path)

    sha = hashlib.sha256()

    with path.open("rb") as f:

        while True:

            chunk = f.read(CHUNK_SIZE)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()


def text_hash(text):
    """
    Return the SHA-256 hash of a string.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()