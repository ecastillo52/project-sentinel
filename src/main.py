# main.py

"""
Project Sentinel

Main Entry Point
"""

from pathlib import Path

from core.processor import run
from core.reporter import print_report
from core.database import add_analysis
from core.scanner import get_new_logs


RAW_FOLDER = Path("data/raw")


def main():

    print()
    print("=" * 70)
    print("Project Sentinel")
    print("=" * 70)
    print()

    new_logs = get_new_logs(RAW_FOLDER)

    if not new_logs:

        print("✓ No new logs found.")
        return

    print(f"Found {len(new_logs)} new log(s).\n")

    processed = 0

    for log in new_logs:

        print("=" * 70)
        print(f"Analyzing: {log.name}")
        print("=" * 70)

        report = run(log)

        print_report(report)

        add_analysis(log, report)

        processed += 1

        print()
        print("✓ Analysis saved.")
        print()

    print("=" * 70)
    print(f"Completed. Processed {processed} new log(s).")
    print("=" * 70)


if __name__ == "__main__":
    main()