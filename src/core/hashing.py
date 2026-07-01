# core/hashing.py

import hashlib


def file_hash(path):
    """
    Returns the SHA-256 hash of a file.
    """

    sha = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)

    return sha.hexdigest()