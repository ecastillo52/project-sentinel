# core/metadata/game_detector.py

"""
Project Sentinel

Game Detection

Responsible for identifying games from filenames
and remembering user-defined aliases.
"""

import json

from core.config import ALIASES_FILE


# ==========================================================
# Internal Helpers
# ==========================================================

def _ensure_alias_file():
    """
    Ensure the alias database exists.
    """

    ALIASES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not ALIASES_FILE.exists():

        with open(
            ALIASES_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump({}, f, indent=4)


# ==========================================================
# Alias Storage
# ==========================================================

def load_aliases():
    """
    Load all known filename aliases.

    Returns
    -------
    dict
        Mapping of filename keyword -> game name.
    """

    _ensure_alias_file()

    try:

        with open(
            ALIASES_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except json.JSONDecodeError:

        return {}


def save_aliases(aliases):
    """
    Save aliases in alphabetical order.
    """

    _ensure_alias_file()

    aliases = dict(
        sorted(
            aliases.items(),
            key=lambda item: item[0]
        )
    )

    with open(
        ALIASES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            aliases,
            f,
            indent=4
        )


# ==========================================================
# Detection
# ==========================================================

def detect_game(filename):
    """
    Attempt to identify a game from a filename.

    Parameters
    ----------
    filename : str

    Returns
    -------
    str | None
        Detected game name or None.
    """

    filename = filename.lower()

    for keyword, game in load_aliases().items():

        if keyword.lower() in filename:

            return game

    return None


# ==========================================================
# Learning
# ==========================================================

def learn_alias(keyword, game):
    """
    Teach Sentinel a new filename keyword.
    """

    keyword = keyword.strip().lower()
    game = game.strip()

    aliases = load_aliases()

    aliases[keyword] = game

    save_aliases(aliases)


# ==========================================================
# User Interaction
# ==========================================================

def prompt_for_game(filename):
    """
    Prompt the user to identify an unknown game.

    If a matching alias already exists, it is returned
    immediately without prompting.
    """

    detected = detect_game(filename)

    if detected:

        return detected

    print()
    print("=" * 70)
    print("Unknown Game")
    print("=" * 70)
    print(filename)
    print()

    game = input(
        "Game name: "
    ).strip()

    if not game:

        game = "Unknown"

    keyword = input(
        f"Keyword to remember [{game}]: "
    ).strip()

    if not keyword:

        keyword = game

    learn_alias(
        keyword,
        game
    )

    print()
    print(f'✓ Learned "{keyword}" → "{game}"')
    print()

    return game