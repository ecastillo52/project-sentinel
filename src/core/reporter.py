# core/reporter.py

"""
Project Sentinel

Console Reporter

Responsible ONLY for displaying analysis results.
"""

from datetime import datetime


DIVIDER = "=" * 70
SECTION = "-" * 70


def _format_value(value, unit):
    """
    Format numbers consistently.
    """

    if isinstance(value, float):
        return f"{value:.2f} {unit}"

    return f"{value} {unit}"


def format_sensor(sensor):

    stats = sensor["stats"]

    if stats is None:

        return (
            f"{sensor['display']}\n"
            f"{SECTION}\n"
            f"No data found.\n"
        )

    return (
        f"{sensor['display']}\n"
        f"{SECTION}\n"
        f"Current : {_format_value(stats['current'], sensor['unit'])}\n"
        f"Minimum : {_format_value(stats['minimum'], sensor['unit'])}\n"
        f"Maximum : {_format_value(stats['maximum'], sensor['unit'])}\n"
        f"Average : {_format_value(stats['average'], sensor['unit'])}\n"
        f"Samples : {stats['samples']}\n"
        f"Status  : {sensor['status']}\n"
    )


def print_report(report):
    """
    Print a complete Sentinel analysis report.
    """

    print()
    print(DIVIDER)
    print("PROJECT SENTINEL")
    print(DIVIDER)

    print(f"File     : {report['filename']}")
    print(f"Samples  : {report['samples']}")
    print(f"Analyzed : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    current_category = None

    for sensor in report["results"].values():

        if sensor["category"] != current_category:

            current_category = sensor["category"]

            print()
            print(f"[ {current_category} ]")
            print()

        print(format_sensor(sensor))

    print(DIVIDER)