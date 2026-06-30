# core/processor.py

for sensor in get_all_sensors():

    stats = analyze_sensor(
        log,
        sensor["keyword"]
    )

    status_function = getattr(
        health,
        sensor["health"]
    )

    status = status_function(stats)

    results.append({
        "sensor": sensor,
        "stats": stats,
        "status": status,
    })