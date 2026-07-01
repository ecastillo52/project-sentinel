# main.py

"""
Project Sentinel

Main Entry Point
"""

from pathlib import Path

from core.engine.scanner import get_new_logs
from core.engine.processor import run
from core.presentation.reporter import (
    print_report,
    print_saved_session,
)
from core.metadata.database import add_analysis
from core.metadata.history import (
    print_history,
    get_session,
)


# ==========================================================
# Configuration
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"


# ==========================================================
# Menu Helpers
# ==========================================================

def header():

    print()
    print("=" * 70)
    print("Project Sentinel")
    print("=" * 70)


def pause():

    input("\nPress Enter to continue...")


# ==========================================================
# Analysis
# ==========================================================

def analyze_logs():

    header()

    new_logs = get_new_logs(RAW_FOLDER)

    if not new_logs:

        print("\nNo new logs found.")

        pause()

        return

    print(f"\nFound {len(new_logs)} new log(s).\n")

    processed = 0

    for log in new_logs:

        print("=" * 70)
        print(f"Analyzing: {log.name}")
        print("=" * 70)

        report = run(log)

        print_report(report)

        add_analysis(log, report)

        processed += 1

        print("\n✓ Analysis saved.\n")

    print("=" * 70)
    print(f"Processed {processed} new log(s).")
    print("=" * 70)

    pause()


# ==========================================================
# History
# ==========================================================

def view_history():

    while True:

        header()

        print_history()

        choice = input(
            "Select a session "
            "(Enter to return): "
        ).strip()

        if choice == "":
            return

        if not choice.isdigit():

            print("\nInvalid selection.")

            pause()

            continue

        session = get_session(int(choice) - 1)

        if session is None:

            print("\nSession not found.")

            pause()

            continue

        header()

        print_saved_session(session)

        pause()


# ==========================================================
# Main Menu
# ==========================================================

def menu():

    while True:

        header()

        print()
        print("1. Analyze New Logs")
        print("2. View Previous Reports")
        print("3. Exit")
        print()

        choice = input("Selection: ").strip()

        if choice == "1":

            analyze_logs()

        elif choice == "2":

            view_history()

        elif choice == "3":

            print("\nGoodbye.\n")

            break

        else:

            print("\nInvalid selection.")

            pause()


# ==========================================================
# Entry Point
# ==========================================================

def main():

    menu()


if __name__ == "__main__":
    main()