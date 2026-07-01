# core/reporter.py

"""
Project Sentinel

Console Reporter
"""

from datetime import datetime


DIVIDER = "=" * 70
SECTION = "-" * 70


def _value(value, unit):

    if isinstance(value, float):

        return f"{value:.2f} {unit}"

    return f"{value} {unit}"


def format_sensor(sensor):

    stats = sensor["stats"]

    if stats is None:

        return (
            f"{sensor['display']}\n"
            f"{SECTION}\n"
            "No data available.\n"
        )

    return (
        f"{sensor['display']}\n"
        f"{SECTION}\n"
        f"Current : {_value(stats['current'], sensor['unit'])}\n"
        f"Minimum : {_value(stats['minimum'], sensor['unit'])}\n"
        f"Maximum : {_value(stats['maximum'], sensor['unit'])}\n"
        f"Average : {_value(stats['average'], sensor['unit'])}\n"
        f"Samples : {stats['samples']}\n"
        f"Status  : {sensor['status']}\n"
    )


def print_report(report):

    print()

    print(DIVIDER)
    print("PROJECT SENTINEL")
    print(DIVIDER)

    print(f"File     : {report['filename']}")
    print(f"Samples  : {report['samples']}")
    print(
        f"Generated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    current_category = None

    for sensor in report["results"].values():

        if sensor["category"] != current_category:

            current_category = sensor["category"]

            print()
            print(f"[ {current_category} ]")
            print()

        print(
            format_sensor(sensor)
        )

    print(DIVIDER)


def print_saved_session(session):
    """
    Display a previously saved Session.
    """

    print_report(session.report)