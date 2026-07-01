# core/metadata/database.py

"""
Project Sentinel

Database Layer

Responsible for storing and retrieving Sentinel Sessions.
"""

import json
import uuid

from datetime import datetime
from pathlib import Path

from core.config import DATABASE_FILE

from .hashing import file_hash
from ..models.session import Session


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
# Session Queries
# ==========================================================

def get_all_sessions():
    """
    Returns every session as Session objects.
    """

    sessions = [

        Session.from_dict(record)

        for record in load_database()

    ]

    return sorted(
        sessions,
        key=lambda s: s.date,
        reverse=True
    )


def get_session_by_id(session_id):

    for session in get_all_sessions():

        if session.id == session_id:
            return session

    return None


def get_session_by_hash(hash_value):

    for session in get_all_sessions():

        if session.hash == hash_value:
            return session

    return None


def record_exists(file_path):

    try:

        return (
            get_session_by_hash(
                file_hash(file_path)
            )
            is not None
        )

    except FileNotFoundError:

        return False


# ==========================================================
# Session Numbering
# ==========================================================

def get_next_session_number(game):
    """
    Returns the next session number
    for a particular game.
    """

    sessions = [

        session

        for session in get_all_sessions()

        if session.game.lower() == game.lower()

    ]

    if not sessions:

        return 1

    return max(

        session.session_number

        for session in sessions

    ) + 1


# ==========================================================
# Insert
# ==========================================================

def insert_session(session):

    database = load_database()

    database.append(
        session.to_dict()
    )

    save_database(database)


# ==========================================================
# Public API
# ==========================================================

def add_analysis(
    *,
    original_path,
    archive_path,
    game,
    report
):
    """
    Create and store a Session.

    Returns
    -------
    Session | None
    """

    archive_path = Path(archive_path)

    archive_hash = file_hash(archive_path)

    if get_session_by_hash(
        archive_hash
    ):
        return None

    session = Session(

        id=str(uuid.uuid4()),

        game=game,

        session_number=get_next_session_number(
            game
        ),

        filename=Path(
            original_path
        ).name,

        archive_path=str(
            archive_path.resolve()
        ),

        hash=archive_hash,

        analyzed_at=datetime.now().isoformat(
            timespec="seconds"
        ),

        report=report

    )

    insert_session(session)

    return session