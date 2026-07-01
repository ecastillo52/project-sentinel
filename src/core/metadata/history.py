# core/history.py

"""
Project Sentinel

History Manager

Loads previously analyzed sessions.
"""

from .database import get_all_records


def list_sessions():

    return get_all_records()


def session_count():

    return len(
        list_sessions()
    )


def get_session(index):

    sessions = list_sessions()

    if index < 0:

        return None

    if index >= len(sessions):

        return None

    return sessions[index]


def print_history():

    sessions = list_sessions()

    print()
    print("=" * 70)
    print("Sentinel History")
    print("=" * 70)
    print()

    if not sessions:

        print("No sessions available.\n")
        return

    for i, session in enumerate(sessions, start=1):

        print(
            f"{i:>2}. "
            f"{session['filename']}"
        )

        print(
            f"    {session['analyzed_at']}"
        )

    print()