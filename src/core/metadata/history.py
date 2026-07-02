# core/metadata/history.py

"""
Project Sentinel

History Manager

Responsible for browsing previously analyzed Sentinel sessions.
"""

from core.metadata.database import get_all_sessions


HEADER = "=" * 70
DIVIDER = "-" * 70


# ==========================================================
# Session Queries
# ==========================================================

def get_sessions():
    """
    Return every stored Session.
    """

    return get_all_sessions()


def get_session(index):
    """
    Return a Session by list index.
    """

    sessions = get_sessions()

    if 0 <= index < len(sessions):
        return sessions[index]

    return None


def get_sessions_for_game(game):
    """
    Return every session for a specific game.
    """

    return [

        session

        for session in get_sessions()

        if session.game.lower() == game.lower()

    ]


def get_games():
    """
    Return every stored game.
    """

    return sorted({

        session.game

        for session in get_sessions()

    })


# ==========================================================
# Tree Builder
# ==========================================================

def build_history_tree():
    """
    Build a grouped history structure.
    """

    tree = {}

    for session in get_sessions():

        tree.setdefault(
            session.game,
            []
        ).append(session)

    for sessions in tree.values():

        sessions.sort(
            key=lambda s: s.session_number
        )

    return dict(
        sorted(tree.items())
    )


# ==========================================================
# Printing
# ==========================================================

def _print_session(index, session):

    print(
        f"{index:>2}. "
        f"Session {session.session_number}"
    )

    print(
        f"    {session.date.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(
        f"    {session.filename}"
    )

    print()


def print_history():

    tree = build_history_tree()

    print(HEADER)
    print("Sentinel History")
    print(HEADER)
    print()

    if not tree:

        print("No saved sessions.\n")
        return

    index = 1

    for game, sessions in tree.items():

        print(game)
        print(DIVIDER)

        for session in sessions:

            _print_session(
                index,
                session
            )

            index += 1