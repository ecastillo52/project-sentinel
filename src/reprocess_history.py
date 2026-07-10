"""
Rebuild stored Sentinel session reports from archived CSV logs.

This updates old processed JSON files with the current reader,
analyzer, health rules, summaries, and recommendations while preserving
the original session identity and source metadata.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from core.config import PROCESSED_FOLDER
from core.database.session_store import SessionStore
from core.engine.analyzer import Analyzer
from core.engine.health_engine import HealthEngine
from core.engine.reader import Reader
from core.models.session import Session
from core.report.builder import ReportBuilder


def rebuild_session(session: Session) -> Session:
    reader = Reader()
    analyzer = Analyzer()
    health_engine = HealthEngine()
    report_builder = ReportBuilder()

    log = reader.read(session.archive)
    sensors = analyzer.analyze(log)
    sensors = health_engine.evaluate(sensors)

    machine = session.report.metadata.get("machine", {})
    session.report = report_builder.build(
        sensors=sensors,
        machine=machine,
    )

    return session


def backup_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".bak")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild processed session JSON from archived CSV logs.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write rebuilt reports back to data/processed.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .bak files when writing.",
    )
    args = parser.parse_args()

    store = SessionStore(PROCESSED_FOLDER)
    sessions = store.load_all()

    rebuilt = 0
    skipped = 0
    failed = 0

    for session in sessions:
        archive_path = session.archive

        if not archive_path.exists():
            skipped += 1
            print(f"SKIP {session.display_name}: missing {archive_path}")
            continue

        try:
            rebuilt_session = rebuild_session(session)
        except Exception as exc:
            failed += 1
            print(f"FAIL {session.display_name}: {exc}")
            continue

        rebuilt += 1

        if args.write:
            path = store.session_path(rebuilt_session.id)

            if not args.no_backup:
                backup = backup_path(path)
                if not backup.exists():
                    shutil.copy2(path, backup)

            store.save(rebuilt_session)
            print(f"WRITE {rebuilt_session.display_name}")
        else:
            print(f"DRY  {rebuilt_session.display_name}")

    mode = "write" if args.write else "dry-run"
    print()
    print(f"Mode: {mode}")
    print(f"Rebuilt: {rebuilt}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
