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

from pathlib import Path


# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "Project Sentinel"

APP_VERSION = "0.4.0 - The era of Information"

AUTHOR = "Erik Castillo"

ENGINE_NAME = "Sentinel Analysis Engine"


# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ==========================================================
# Data Folders
# ==========================================================

DATA_FOLDER = PROJECT_ROOT / "data"

INCOMING_FOLDER = DATA_FOLDER / "incoming"

ARCHIVE_FOLDER = DATA_FOLDER / "archive"

PROCESSED_FOLDER = DATA_FOLDER / "processed"

CONFIG_FOLDER = DATA_FOLDER / "config"

EXPORTS_FOLDER = DATA_FOLDER / "exports"


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

DATABASE_FILE = PROCESSED_FOLDER / "sentinel_db.json"

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