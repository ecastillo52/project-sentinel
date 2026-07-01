# core/scanner.py

from pathlib import Path

from core.database import record_exists


def get_new_logs(folder):

    logs = sorted(folder.glob("*.CSV"))

    return [

        log

        for log in logs

        if not record_exists(log)

    ]