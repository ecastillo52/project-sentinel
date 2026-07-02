# core/ui/menu.py

"""
Project Sentinel

Menu Controller

Coordinates the console interface and connects the UI
to Sentinel's analysis engine.

This module contains application flow only.

All printing is delegated to console.py.
"""

from core.config import INCOMING_FOLDER

from core.engine.processor import run
from core.report.renderer import render
from core.engine.reporter import print_saved_session
from core.engine.scanner import get_new_logs

from core.metadata.archive import archive_log
from core.metadata.database import add_analysis
from core.metadata.game_detector import prompt_for_game
from core.metadata.history import (
    get_session,
    print_history,
)

from .console import (
    header,
    pause,
    main_menu,
)


# ==========================================================
# Analysis
# ==========================================================

def analyze_logs():

    header()

    logs = get_new_logs(INCOMING_FOLDER)

    if not logs:

        print("\nNo new logs found.")

        pause()

        return

    print(f"\nFound {len(logs)} new log(s).\n")

    processed = 0

    for log in logs:

        print("=" * 70)
        print(f"Analyzing: {log.name}")
        print("=" * 70)

        #
        # Detect Game
        #

        game = prompt_for_game(log.name)

        #
        # Analyze
        #

        report = run(log, game)

        render(report)

        #
        # Archive
        #

        archive_path = archive_log(
            log,
            game
        )

        #
        # Save
        #

        saved = add_analysis(
            original_path=log,
            archive_path=archive_path,
            game=game,
            report=report
        )

        if saved:

            processed += 1

            print()

            print("✓ Analysis saved.")

            print(f"✓ Archived to:\n  {archive_path}")

        else:

            print("\nSession already exists.")

        print()

    print("=" * 70)
    print(f"Processed {processed} log(s).")
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
            "\nSelect a session "
            "(Enter to return): "
        ).strip()

        if choice == "":
            return

        if not choice.isdigit():

            print("\nInvalid selection.")

            pause()

            continue

        session = get_session(
            int(choice) - 1
        )

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

def run_menu():

    while True:

        header()

        main_menu()

        choice = input(
            "\nSelection: "
        ).strip()

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