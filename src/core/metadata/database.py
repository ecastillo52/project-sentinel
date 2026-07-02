# core/metadata/database.py

"""
Project Sentinel

Database Layer

Responsible for storing and retrieving analyzed sessions.
"""

import json
import uuid

from datetime import datetime
from pathlib import Path

from core.config import DATABASE_FILE
from core.models.session import Session
from .hashing import file_hash


DATABASE_VERSION = "0.2.0"


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

        save_database([])


# ==========================================================
# Database I/O
# ==========================================================

def load_database():
    """
    Returns the raw database dictionary.
    """

    _ensure_database()

    try:

        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

    except json.JSONDecodeError:

        data = None

    #
    # Brand new database
    #
    if not data:

        data = {
            "version": DATABASE_VERSION,
            "sessions": []
        }

    #
    # Legacy database (0.1.x)
    #
    elif isinstance(data, list):

        data = {
            "version": "0.1.0",
            "sessions": data
        }

    #
    # Safety
    #
    data.setdefault(
        "version",
        DATABASE_VERSION
    )

    data.setdefault(
        "sessions",
        []
    )

    return data


def save_database(sessions):
    """
    Save Session objects back to disk.
    """

    database = {

        "version": DATABASE_VERSION,

        "sessions": [

            session.to_dict()

            if isinstance(session, Session)

            else session

            for session in sessions
        ]
    }

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

def get_database_version():

    return load_database()["version"]


def get_all_sessions():
    """
    Returns Session objects.
    """

    database = load_database()

    sessions = [

        Session.from_dict(record)

        for record in database["sessions"]

    ]

    sessions.sort(
        key=lambda s: s.analyzed_at,
        reverse=True
    )

    return sessions


def get_session(session_id):

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
# Helpers
# ==========================================================

def next_session_number(game):
    """
    Determine the next session number
    for a given game.
    """

    sessions = [

        s

        for s in get_all_sessions()

        if s.game == game

    ]

    if not sessions:
        return 1

    return max(
        s.session_number
        for s in sessions
    ) + 1


# ==========================================================
# Insert
# ==========================================================

def add_analysis(
    *,
    original_path,
    archive_path,
    game,
    report
):
    """
    Save one completed Sentinel analysis.
    """

    archive_path = Path(archive_path)

    archive_hash = file_hash(
        archive_path
    )

    if get_session_by_hash(
        archive_hash
    ):
        return False

    session = Session(

        id=str(uuid.uuid4()),

        game=game,

        session_number=next_session_number(
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

        report=report,
    )

    sessions = get_all_sessions()

    sessions.append(session)

    save_database(sessions)

    return True