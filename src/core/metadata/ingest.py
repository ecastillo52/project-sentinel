# core/ingest.py

"""
Project Sentinel

Ingestion Pipeline

Coordinates the complete processing of a single HWiNFO log.

Pipeline

    Detect Game
        ↓
    Analyze Log
        ↓
    Archive Log
        ↓
    Store Session
"""

from pathlib import Path

from .archive import archive_log
from .database import add_analysis
from .game_detector import prompt_for_game

from ..engine.processor import run


# ==========================================================
# Public API
# ==========================================================

def process_file(file_path):
    """
    Process one HWiNFO log from start to finish.

    Returns
    -------
    dict
        Completed Sentinel report.
    """

    file_path = Path(file_path)

    game = prompt_for_game(file_path.name)

    report = run(
        file_path,
        game=game,
    )

    archived_path = archive_log(
        file_path,
        game,
    )

    add_analysis(
        original_path=file_path,
        archive_path=archived_path,
        game=game,
        report=report,
    )

    return report