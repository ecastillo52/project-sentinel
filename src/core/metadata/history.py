# core/metadata/history.py

"""
Project Sentinel

History Manager

Responsible for browsing previously analyzed Sentinel sessions.
"""

from core.metadata.database import get_all_sessions


# ==========================================================
# Session Queries
# ==========================================================

def get_sessions():
    """
    Returns every stored Session.
    """

    return get_all_sessions()


def get_session(index):
    """
    Returns a Session by list index.
    """

    sessions = get_sessions()

    if 0 <= index < len(sessions):
        return sessions[index]

    return None


def get_sessions_for_game(game):
    """
    Returns every session for a specific game.
    """

    return [

        session

        for session in get_sessions()

        if session.game.lower() == game.lower()

    ]


def get_games():
    """
    Returns every game currently stored.
    """

    games = {

        session.game

        for session in get_sessions()

    }

    return sorted(games)


# ==========================================================
# Tree Builder
# ==========================================================

def build_history_tree():
    """
    Build a grouped history structure.

    Returns:

    {
        "Fortnite": [
            Session,
            Session,
            Session
        ],

        "StarCraft II": [
            Session
        ]
    }
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

def print_history():

    tree = build_history_tree()

    print("=" * 70)
    print("Sentinel History")
    print("=" * 70)
    print()

    if not tree:

        print("No saved sessions.\n")
        return

    index = 1

    for game, sessions in tree.items():

        print(game)
        print("-" * 70)

        for session in sessions:

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

            index += 1