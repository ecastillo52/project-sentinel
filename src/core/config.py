# core/config.py

"""
Project Sentinel

Global Configuration

This module is the single source of truth for:

    • Project paths
    • Application metadata
    • Folder locations
    • Version information
    • Common helper functions

Every module should import paths from here instead of
building paths with Path(__file__).parents[x].
"""

import json
import os
import sys
from pathlib import Path


# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "Project Sentinel"

APP_VERSION = "0.7.2 - Silent Analysis"

REPORT_SCHEMA = 2

AUTHOR = "Erik Castillo"

ENGINE_NAME = "Sentinel Analysis Engine"


# ==========================================================
# Project Root
# ==========================================================

if getattr(sys, "frozen", False):
    # A packaged application must not try to write beside the bundled EXE.
    # LocalAppData is writable for normal Windows accounts and persists across
    # application upgrades.
    PROJECT_ROOT = (
        Path(os.environ.get("LOCALAPPDATA", Path.home()))
        / "Project Sentinel"
    )
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ==========================================================
# Data Folders
# ==========================================================

DATA_FOLDER = PROJECT_ROOT / "data"

CONFIG_FOLDER = DATA_FOLDER / "config"

SETTINGS_FILE = CONFIG_FOLDER / "settings.json"

DEFAULT_PATH_SETTINGS = {
    "incoming_folder": str(DATA_FOLDER / "incoming"),
    "archive_folder": str(DATA_FOLDER / "archive"),
    "processed_folder": str(DATA_FOLDER / "processed"),
    "exports_folder": str(DATA_FOLDER / "exports"),
}


def load_path_settings() -> dict[str, Path]:
    """Return configured folder paths, falling back safely to defaults."""
    values = DEFAULT_PATH_SETTINGS.copy()
    try:
        with SETTINGS_FILE.open(encoding="utf-8") as file:
            saved = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        saved = {}
    if isinstance(saved, dict):
        for key in values:
            value = saved.get(key)
            if isinstance(value, str) and value.strip():
                values[key] = value.strip()
    return {key: Path(value).expanduser() for key, value in values.items()}


def save_path_settings(paths: dict[str, Path | str]) -> dict[str, Path]:
    """Persist user-selected folder paths and create them when possible."""
    values = DEFAULT_PATH_SETTINGS.copy()
    for key in values:
        value = paths.get(key)
        if value:
            values[key] = str(Path(value).expanduser())
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(values, indent=4), encoding="utf-8")
    configured = {key: Path(value) for key, value in values.items()}
    for folder in configured.values():
        folder.mkdir(parents=True, exist_ok=True)
    return configured


_PATH_SETTINGS = load_path_settings()

INCOMING_FOLDER = _PATH_SETTINGS["incoming_folder"]
ARCHIVE_FOLDER = _PATH_SETTINGS["archive_folder"]
PROCESSED_FOLDER = _PATH_SETTINGS["processed_folder"]
EXPORTS_FOLDER = _PATH_SETTINGS["exports_folder"]


# ==========================================================
# Output Folders
# ==========================================================

REPORTS_FOLDER = PROJECT_ROOT / "reports"

IMAGES_FOLDER = PROJECT_ROOT / "images"

LOGS_FOLDER = PROJECT_ROOT / "logs"

TESTS_FOLDER = PROJECT_ROOT / "tests"


# ==========================================================
# Configuration Files
# ==========================================================


ALIASES_FILE = CONFIG_FOLDER / "game_aliases.json"


# ==========================================================
# Ensure Required Directories Exist
# ==========================================================

REQUIRED_DIRECTORIES = [

    DATA_FOLDER,

    INCOMING_FOLDER,

    ARCHIVE_FOLDER,

    PROCESSED_FOLDER,

    CONFIG_FOLDER,

    EXPORTS_FOLDER,

    REPORTS_FOLDER,

    IMAGES_FOLDER,

    LOGS_FOLDER,

]


def initialize():
    """
    Creates every required Sentinel directory.

    Safe to call multiple times.
    """

    for folder in REQUIRED_DIRECTORIES:

        folder.mkdir(
            parents=True,
            exist_ok=True
        )


# ==========================================================
# Console Helpers
# ==========================================================

LINE = "=" * 70

DIVIDER = "-" * 70


def print_header(title=APP_NAME):
    """
    Prints a standardized Sentinel header.
    """

    print()
    print(LINE)
    print(title)
    print(LINE)


def print_divider():
    """
    Prints a divider line.
    """

    print(DIVIDER)


# ==========================================================
# Version Helpers
# ==========================================================

def version_string():
    """
    Returns the formatted application version.
    """

    return f"{APP_NAME} v{APP_VERSION}"


# ==========================================================
# Startup
# ==========================================================

initialize()
