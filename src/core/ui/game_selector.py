# core/ui/game_selector.py

"""
Project Sentinel

Game Selector

Displays a menu of games contained within the
Sentinel history database.

Returns the selected game name.

This module performs no analysis.
"""

from collections import Counter

from core.models.session import Session


# ==========================================================
# Public API
# ==========================================================

def select_game(
    history: list[Session],
) -> str | None:
    """
    Display the available games and return the user's
    selected game.

    Returns
    -------
    str | None
        Selected game name or None if cancelled.
    """

    games = game_counts(history)

    if not games:

        print("No historical sessions found.")
        return None

    print("=" * 54)
    print("Choose a Game")
    print("=" * 54)
    print()

    names = sorted(games.keys())

    for index, game in enumerate(names, start=1):

        count = games[game]

        session_text = (
            "session"
            if count == 1
            else "sessions"
        )

        print(
            f"{index}. "
            f"{game} "
            f"({count} {session_text})"
        )

    print()

    selection = input(
        "Selection (Enter to return): "
    ).strip()

    if selection == "":
        return None

    try:
        selection = int(selection)

    except ValueError:

        print("\nInvalid selection.")
        return None

    if not 1 <= selection <= len(names):

        print("\nInvalid selection.")
        return None

    return names[selection - 1]


# ==========================================================
# Helpers
# ==========================================================

def game_counts(
    history: list[Session],
) -> dict[str, int]:
    """
    Return a mapping of game names to the number of
    recorded sessions.
    """

    return dict(
        Counter(
            session.game
            for session in history
        )
    )