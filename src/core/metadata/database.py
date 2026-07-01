# core/database.py

"""
Project Sentinel

Database Layer

Responsible for storing and retrieving analyzed sessions.
"""

import json
import uuid

from datetime import datetime
from pathlib import Path

from .hashing import file_hash
from core.config import DATABASE_FILE


# ==========================================================
# Internal Helpers
# ==========================================================

def _ensure_database():
    """
    Ensure the Sentinel database exists.
    """

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DATABASE_FILE.exists():

        DATABASE_FILE.write_text(
            "[]",
            encoding="utf-8"
        )


# ==========================================================
# Database I/O
# ==========================================================

def load_database():

    _ensure_database()

    try:

        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        return []


def save_database(database):

    _ensure_database()

    with open(
        DATABASE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            database,
            f,
            indent=4
        )


def clear_database():

    save_database([])


# ==========================================================
# Queries
# ==========================================================

def get_all_records():

    return sorted(
        load_database(),
        key=lambda record: record["analyzed_at"],
        reverse=True
    )


def get_record(record_id):

    for record in load_database():

        if record["id"] == record_id:
            return record

    return None


def get_record_by_hash(hash_value):

    for record in load_database():

        if record["hash"] == hash_value:
            return record

    return None


def record_exists(file_path):
    """
    Returns True if a file with the same SHA-256
    already exists in the database.
    """

    try:

        file_hash_value = file_hash(file_path)

    except FileNotFoundError:

        return False

    return get_record_by_hash(
        file_hash_value
    ) is not None


# ==========================================================
# Record Builder
# ==========================================================

def create_record(
    *,
    original_path,
    archive_path,
    game,
    report
):
    """
    Build one Sentinel session record.

    The archived file becomes the canonical copy.
    """

    archive_path = Path(archive_path)

    return {

        "id": str(uuid.uuid4()),

        "game": game,

        "hash": file_hash(archive_path),

        "filename": Path(original_path).name,

        "archive_path": str(
            archive_path.resolve()
        ),

        "analyzed_at": datetime.now().isoformat(
            timespec="seconds"
        ),

        "report": report

    }


# ==========================================================
# Insert
# ==========================================================

def insert_record(record):

    database = load_database()

    database.append(record)

    save_database(database)


def add_analysis(
    *,
    original_path,
    archive_path,
    game,
    report
):
    """
    Save one completed Sentinel analysis.

    Returns
    -------
    bool
        True if inserted.
        False if this archived file already exists.
    """

    archive_path = Path(archive_path)

    archive_hash = file_hash(archive_path)

    if get_record_by_hash(archive_hash):

        return False

    record = create_record(
        original_path=original_path,
        archive_path=archive_path,
        game=game,
        report=report
    )

    insert_record(record)

    return True