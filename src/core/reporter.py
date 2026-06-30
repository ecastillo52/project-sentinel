# core/reporter.py

def format_sensor(name, sensor):
    """
    Formats a single sensor block.
    """

    stats = sensor["stats"]

    if stats is None:
        return f"{name}: No data"

    return (
        f"{sensor['display']}\n"
        f"Min: {stats['minimum']} {sensor['unit']}\n"
        f"Max: {stats['maximum']} {sensor['unit']}\n"
        f"Avg: {stats['average']} {sensor['unit']}\n"
        + "_" * 30
    )


def print_results(results):
    """
    Prints full analysis report.
    """

    print("\n=== Project Sentinel Report ===\n")

    for name, sensor in results.items():
        print(format_sensor(name, sensor))