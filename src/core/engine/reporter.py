# core/engine/reporter.py

"""
Project Sentinel

Report Renderer

Responsible for rendering analysis reports to the console.
"""

from collections import OrderedDict

from core.models.session import Session


# ==========================================================
# Helpers
# ==========================================================

def divider():

    print("-" * 70)


def heading(title):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def section(title):

    print()
    print(f"[ {title} ]")
    print()


# ==========================================================
# Sensor Rendering
# ==========================================================

def print_sensor(sensor):
    """
    Render one analyzed sensor.
    """

    stats = sensor["stats"]

    divider()

    print(sensor["display"])

    divider()

    print(
        f"Current : "
        f"{stats['current']:.2f} {sensor['unit']}"
    )

    print(
        f"Minimum : "
        f"{stats['minimum']:.2f} {sensor['unit']}"
    )

    print(
        f"Maximum : "
        f"{stats['maximum']:.2f} {sensor['unit']}"
    )

    print(
        f"Average : "
        f"{stats['average']:.2f} {sensor['unit']}"
    )

    print(
        f"Samples : "
        f"{stats['samples']}"
    )

    print(
        f"Status  : "
        f"{sensor['status']}"
    )


# ==========================================================
# Report Rendering
# ==========================================================

def print_report(report):
    """
    Render an analysis report.
    """

    heading("PROJECT SENTINEL")

    print(f"File     : {report['filename']}")
    print(f"Samples  : {report['samples']}")

    categories = OrderedDict()

    for sensor in report["results"].values():

        category = sensor["category"]

        categories.setdefault(
            category,
            []
        ).append(sensor)

    for category, sensors in categories.items():

        section(category)

        for sensor in sensors:

            print_sensor(sensor)


# ==========================================================
# Saved Sessions
# ==========================================================

def print_saved_session(session: Session):
    """
    Render a saved Sentinel session.
    """

    heading(session.game)

    print(f"Session : {session.session_number}")

    print(
        "Analyzed: "
        f"{session.date.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(f"Source  : {session.filename}")

    print(f"Archive : {session.archive}")

    print(f"Version : {session.version}")

    print(f"Engine  : {session.engine}")

    print()

    print_report(session.report)