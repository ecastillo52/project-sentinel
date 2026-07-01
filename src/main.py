# main.py

"""
Project Sentinel

Main Entry Point

The only responsibility of this module is to launch
the Sentinel user interface.
"""

from core.ui.menu import run_menu


def main():
    """
    Launch Sentinel.
    """

    run_menu()


if __name__ == "__main__":
    main()