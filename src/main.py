# main.py

from core.config import print_header
from pathlib import Path
from core.history import process_all_files


def main():
    print_header()

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"

    print("Processing all CSV files...")
    print("_" * 30)

    results = process_all_files(data_dir)

    print(f"Processed {len(results)} files successfully.")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()