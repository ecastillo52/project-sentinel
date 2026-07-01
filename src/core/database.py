# core/database.py

"""
Project Sentinel

Database Layer

Stores every completed analysis session.

Current backend:
JSON

Future backend:
SQLite
"""

import json
import uuid

from pathlib import Path
from datetime import datetime

from core.hashing import file_hash


DB_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "sentinel_db.json"
)


# ==========================================================
# BASIC DATABASE
# ==========================================================

def load_database():

    if not DB_FILE.exists():
        return []

    try:

        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:

        # Corrupted database

        return []


def save_database(data):

    DB_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(DB_FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4
        )


def clear_database():
    save_database([])


# ==========================================================
# RECORD HELPERS
# ==========================================================

def get_all_records():
    return load_database()


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

    return get_record_by_hash(
        file_hash(file_path)
    ) is not None


# ==========================================================
# INSERT
# ==========================================================

def insert_record(record):

    database = load_database()

    database.append(record)

    save_database(database)


def create_record(file_path, results):
    """
    Build a standardized Sentinel record.
    """

    return {

        "id": str(uuid.uuid4()),

        "hash": file_hash(file_path),

        "filename": Path(file_path).name,

        "filepath": str(Path(file_path).resolve()),

        "analyzed_at": datetime.now().isoformat(
            timespec="seconds"
        ),

        "results": results

    }


def add_analysis(file_path, results):

    if record_exists(file_path):
        return

    record = create_record(
        file_path,
        results
    )

    insert_record(record)