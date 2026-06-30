# main.py

from core.processor import run
from core.sensors import get_all_sensors
from core.analyzer import analyze_sensor
from core import health

results = []

def main():
    run()


if __name__ == "__main__":
    main()