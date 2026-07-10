# main.py

"""
Project Sentinel

Main Entry Point
"""

from core.app import App
from core.ui.desktop import run


def main() -> None:
    """
    Launch Project Sentinel.
    """

    raise SystemExit(run(App()))


if __name__ == "__main__":
    main()
