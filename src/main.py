# main.py

from pathlib import Path

from core.processor import run
from core.reporter import print_report
from core.database import add_analysis
from core.scanner import get_new_logs


RAW_FOLDER = Path("data/raw")


def main():

    new_logs = get_new_logs(RAW_FOLDER)

    if not new_logs:

        print("No new logs found.")

        return

    print(f"Found {len(new_logs)} new log(s).\n")

    for log in new_logs:

        print("=" * 60)
        print(f"Analyzing: {log.name}")
        print("=" * 60)

        results = run(log)

        print_report(results)

        add_analysis(log, results)

        print("\nSaved to Sentinel database.\n")


if __name__ == "__main__":
    main()

processed = 0

for log in new_logs:

    ...

    processed += 1

print(f"\nProcessed {processed} new log(s).")