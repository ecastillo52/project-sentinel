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
# Constants
# ==========================================================

MENU_WIDTH = 54
INVALID_SELECTION = "\nInvalid selection."


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

    names = get_games(history)

    if not names:
        print("No historical sessions found.")
        return None

    print_menu(names, game_counts(history))

    selection = input(
        "Selection (Enter to return): "
    ).strip()

    if not selection:
        return None

    try:
        selection = int(selection)

    except ValueError:
        print(INVALID_SELECTION)
        return None

    if not 1 <= selection <= len(names):
        print(INVALID_SELECTION)
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


def get_games(
    history: list[Session],
) -> list[str]:
    """
    Return all games in alphabetical order.
    """

    return sorted(
        game_counts(history)
    )


def print_menu(
    names: list[str],
    counts: dict[str, int],
) -> None:
    """
    Display the game selection menu.
    """

    print("=" * MENU_WIDTH)
    print("Choose a Game")
    print("=" * MENU_WIDTH)
    print()

    for index, game in enumerate(names, start=1):

        count = counts[game]

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