# core/metadata/game_detector.py

"""
Project Sentinel

Game Detection
"""

import json

from core.config import ALIASES_FILE


# ==========================================================
# Alias Storage
# ==========================================================

def load_aliases():

    if not ALIASES_FILE.exists():

        ALIASES_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(ALIASES_FILE, "w") as f:
            json.dump({}, f, indent=4)

    with open(ALIASES_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_aliases(data):

    with open(ALIASES_FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ==========================================================
# Detection
# ==========================================================

def detect_game(filename):

    aliases = load_aliases()

    lower = filename.lower()

    for keyword, game in aliases.items():

        if keyword in lower:"""
Project Sentinel

Game Detection

Responsible for identifying games from filenames
and remembering user-defined aliases.
"""

import json

from core.config import ALIASES_FILE


# ==========================================================
# Alias Storage
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

        with open(ALIASES_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)


def load_aliases():

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
    Attempt to identify a game from the filename.
    """

    filename = filename.lower()

    aliases = load_aliases()

    for keyword, game in aliases.items():

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
# User Prompt
# ==========================================================

def prompt_for_game(filename):
    """
    Ask the user to identify an unknown game.
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
        "Keyword to remember "
        f"[{game}]: "
    ).strip()

    if not keyword:

        keyword = game

    learn_alias(
        keyword,
        game
    )

    print(f'\n✓ Learned "{keyword}" → "{game}"\n')

    return game