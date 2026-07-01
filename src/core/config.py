# core/config.py

PROJECT_NAME = "\033[1mProject Sentinel\033[0m"
VERSION = "0.2.2 - Cells become a heartbeat"
DEVELOPER = "Erik Castillo"
STATUS = "Development"


def print_header():
    print(PROJECT_NAME)
    print("Version:", VERSION)
    print("Developed:", DEVELOPER)
    print("Status:", STATUS)
    print("_" * 30)

"""
Project Sentinel

Global Configuration

Every file and folder used by Sentinel should be defined here.

If the project structure changes,
this is the ONLY file that should require updates.
"""

from pathlib import Path


# ==========================================================
# Project
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
# Reports
# ==========================================================

REPORTS_FOLDER = PROJECT_ROOT / "reports"


# ==========================================================
# Database
# ==========================================================

DATABASE_FILE = (
    PROCESSED_FOLDER
    / "sentinel_db.json"
)


# ==========================================================
# Config Files
# ==========================================================

ALIASES_FILE = (
    CONFIG_FOLDER
    / "game_aliases.json"
)