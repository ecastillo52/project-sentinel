# core/database.py

import json
from pathlib import Path
from datetime import datetime


DB_FILE = Path(__file__).resolve().parents[1] / "data" / "processed" / "sentinel_db.json"


def load_database():
    if not DB_FILE.exists():
        return []

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_database(data):
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def insert_record(record):
    """
    Adds one analyzed file into the database.
    """
    db = load_database()
    db.append(record)
    save_database(db)


def get_all_records():
    return load_database()


def clear_database():
    save_database([])