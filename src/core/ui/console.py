# core/ui/console.py

"""
Project Sentinel

Console UI

Responsible for all terminal output.

This module intentionally contains no business logic.
It only draws menus, headers, messages, and waits
for user input.

As Sentinel grows, every print statement should migrate
here so the rest of the application never worries about
terminal formatting.
"""

# ==========================================================
# Constants
# ==========================================================

WIDTH = 70

TITLE = "Project Sentinel"


# ==========================================================
# Helpers
# ==========================================================

def divider():

    print("=" * WIDTH)


def blank():

    print()


# ==========================================================
# Layout
# ==========================================================

def header(title=TITLE):
    """
    Draw a standard Sentinel header.
    """

    blank()

    divider()

    print(title)

    divider()


def section(title):
    """
    Draw a section divider.
    """

    blank()

    print("-" * WIDTH)

    print(title)

    print("-" * WIDTH)


# ==========================================================
# Menus
# ==========================================================

def main_menu():
    """Print the main menu."""

    print("1. Analyze New Logs")
    print("2. View Previous Reports")
    print("3. Historical Intelligence")
    print("4. Exit")


def prompt(message):

    return input(f"\n{message}").strip()


def pause():

    input("\nPress Enter to continue...")


# ==========================================================
# Status Messages
# ==========================================================

def show_no_logs():

    print("\nNo new logs found.")


def show_log_count(count):

    print(f"\nFound {count} new log(s).\n")


def show_analysis_start(filename):

    divider()

    print(f"Analyzing: {filename}")

    divider()


def show_saved(archive_path):

    print()

    print("✓ Analysis saved.")

    print()

    print("Archived to:")

    print(f"  {archive_path}")

    print()


def show_duplicate():

    print("\nLog already exists in database.\n")


def show_invalid_selection():

    print("\nInvalid selection.")


def show_session_not_found():

    print("\nSession not found.")


def show_processed(count):

    divider()

    print(f"Processed {count} log(s).")

    divider()


def goodbye():

    print("\nGoodbye.\n")