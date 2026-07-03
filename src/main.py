# main.py

"""
Project Sentinel

Main Entry Point
"""

from core.app import App
from core.ui.menu import run_menu


def main() -> None:
    """
    Launch Project Sentinel.
    """

    app = App()

    run_menu(app)


if __name__ == "__main__":
    main()