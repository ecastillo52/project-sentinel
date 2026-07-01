# core/database.py

"""
Project Sentinel

Database Layer

Responsible for storing and retrieving analyzed sessions.
"""

from pathlib import Path
from datetime import datetime
import json
import uuid

from .hashing import file_hash


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sentinel_db.json"
)


# ==========================================================
# Internal Helpers
# ==========================================================

def _ensure_database():

    DB_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not DB_FILE.exists():

        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


# ==========================================================
# Database
# ==========================================================

def load_database():

    _ensure_database()

    try:

        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:

        return []


def save_database(database):

    _ensure_database()

    with open(DB_FILE, "w", encoding="utf-8") as f:

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

    database = load_database()

    return sorted(
        database,
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

    return get_record_by_hash(
        file_hash(file_path)
    ) is not None


# ==========================================================
# Insert
# ==========================================================

def create_record(file_path, report):

    return {

        "id": str(uuid.uuid4()),

        "hash": file_hash(file_path),

        "filename": Path(file_path).name,

        "filepath": str(Path(file_path).resolve()),

        "analyzed_at": datetime.now().isoformat(
            timespec="seconds"
        ),

        "report": report

    }


def insert_record(record):

    database = load_database()

    database.append(record)

    save_database(database)


def add_analysis(file_path, report):

    if record_exists(file_path):
        return False

    record = create_record(
        file_path,
        report
    )

    insert_record(record)

    return True