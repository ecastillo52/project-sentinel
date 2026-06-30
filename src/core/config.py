# config.py

PROJECT_NAME = "\033[1mProject Sentinel\033[0m"
VERSION = "0.0.2 - Let the pipeline flow!"
DEVELOPER = "Erik Castillo"
STATUS = "Development"


def print_header():
    print(PROJECT_NAME)
    print("Version:", VERSION)
    print("Developed:", DEVELOPER)
    print("Status:", STATUS)
    print("_" * 30)