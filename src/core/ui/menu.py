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
from core.engine.scanner import get_new_logs

from core.history.loader import load_history

from core.intelligence.engine import run as run_intelligence
from core.intelligence.renderer import render as render_intelligence

from core.metadata.archive import archive_log
from core.metadata.database import add_analysis
from core.metadata.game_detector import prompt_for_game
from core.metadata.history import (
    get_session,
    print_history,
)

from core.report.renderer import render

from .console import (
    goodbye,
    header,
    main_menu,
    pause,
    prompt,
    show_analysis_start,
    show_duplicate,
    show_invalid_selection,
    show_log_count,
    show_no_history,
    show_no_logs,
    show_processed,
    show_saved,
    show_session_not_found,
)

from .game_selector import select_game


# ==========================================================
# Analysis
# ==========================================================

def analyze_logs():

    header()

    logs = get_new_logs(INCOMING_FOLDER)

    if not logs:
        show_no_logs()
        pause()
        return

    show_log_count(len(logs))

    processed = 0

    for log in logs:

        show_analysis_start(log.name)

        game = prompt_for_game(log.name)

        report = run(log, game)

        render(report)

        archive_path = archive_log(
            log,
            game,
        )

        saved = add_analysis(
            original_path=log,
            archive_path=archive_path,
            game=game,
            report=report,
        )

        if saved:

            processed += 1

            show_saved(archive_path)

        else:

            show_duplicate()

    show_processed(processed)

    pause()


# ==========================================================
# History
# ==========================================================

def view_history():

    while True:

        header()

        print_history()

        choice = prompt(
            "Select a session (Enter to return): "
        )

        if not choice:
            return

        if not choice.isdigit():

            show_invalid_selection()

            pause()

            continue

        session = get_session(
            int(choice) - 1
        )

        if session is None:

            show_session_not_found()

            pause()

            continue

        header()

        render(
            session.report,
            session=session,
        )

        pause()


# ==========================================================
# Historical Intelligence
# ==========================================================

def historical_intelligence():

    history = load_history()

    if not history:

        header()

        show_no_history()

        pause()

        return

    game = select_game(history)

    if game is None:
        return

    header()

    report = run_intelligence(game)

    render_intelligence(report)

    pause()


# ==========================================================
# Main Menu
# ==========================================================

def run_menu():

    while True:

        header()

        main_menu()

        choice = prompt("Selection: ")

        if choice == "1":

            analyze_logs()

        elif choice == "2":

            view_history()

        elif choice == "3":

            historical_intelligence()

        elif choice == "4":

            goodbye()

            break

        else:

            show_invalid_selection()

            pause()