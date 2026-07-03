# core/ui/menu.py

"""
Project Sentinel

Menu Controller

Coordinates the console interface.

The UI communicates only with the application container.
Business logic lives inside AnalysisService and the
database layer.
"""

from __future__ import annotations

from core.app import App
from core.engine.scanner import find_logs

from core.intelligence.engine import run as run_intelligence
from core.intelligence.renderer import (
    render as render_intelligence,
)

from core.metadata.game_detector import prompt_for_game
from core.report.renderer import render

from .console import (
    goodbye,
    header,
    main_menu,
    pause,
    prompt,
    show_analysis_start,
    show_invalid_selection,
    show_log_count,
    show_no_history,
    show_no_logs,
    show_processed,
    show_session_not_found,
)

from .game_selector import select_game


# ==========================================================
# Analysis
# ==========================================================

def analyze_logs(app: App) -> None:
    """
    Analyze every newly discovered HWiNFO log.
    """

    header()

    logs = find_logs(app.incoming_folder)

    if not logs:
        show_no_logs()
        pause()
        return

    show_log_count(len(logs))

    processed = 0

    for log in logs:

        show_analysis_start(log.name)

        game = prompt_for_game(log.name)

        session = app.analysis.analyze(
            csv_path=log,
            game=game,
        )

        if session is None:
            print(f"Skipped duplicate log: {log.name}")
            continue

        render(
            session.report,
            session=session,
        )

        processed += 1

    show_processed(processed)

    pause()


# ==========================================================
# History
# ==========================================================

def view_history(app: App) -> None:
    """
    Browse previously analyzed sessions.
    """

    while True:

        header()

        sessions = app.sessions.all()

        if not sessions:

            show_no_history()
            pause()
            return

        print("=" * 70)
        print("Sentinel History")
        print("=" * 70)
        print()

        for index, session in enumerate(
            sessions,
            start=1,
        ):

            print(
                f"{index:>2}. "
                f"{session.game} "
                f"(Session {session.session_number})"
            )

            print(f"    {session.analyzed_at}")
            print(f"    {session.filename}")
            print()

        choice = prompt(
            "Select a session (Enter to return): "
        )

        if not choice:
            return

        if not choice.isdigit():

            show_invalid_selection()
            pause()
            continue

        index = int(choice) - 1

        if index < 0 or index >= len(sessions):

            show_session_not_found()
            pause()
            continue

        session = sessions[index]

        header()

        render(
            session.report,
            session=session,
        )

        pause()


# ==========================================================
# Historical Intelligence
# ==========================================================

def historical_intelligence(app: App) -> None:
    """
    Launch the historical intelligence engine.
    """

    history = app.sessions.all()

    if not history:

        header()

        show_no_history()

        pause()

        return

    game = select_game(history)

    if game is None:
        return

    header()

    report = run_intelligence(
        sessions=history,
        game=game,
    )

    render_intelligence(report)

    pause()


# ==========================================================
# Main Menu
# ==========================================================

def run_menu(app: App) -> None:
    """
    Launch the Sentinel main menu.
    """

    while True:

        header()

        main_menu()

        choice = prompt("Selection: ")

        if choice == "1":

            analyze_logs(app)

        elif choice == "2":

            view_history(app)

        elif choice == "3":

            historical_intelligence(app)

        elif choice == "4":

            goodbye()
            break

        else:

            show_invalid_selection()
            pause()