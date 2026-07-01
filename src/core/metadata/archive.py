# core/metadata/archive.py

"""
Project Sentinel

Archive Manager

Responsible for moving processed logs
into the permanent archive.
"""

import shutil

from pathlib import Path

from core.config import ARCHIVE_FOLDER


def archive_log(file_path, game):
    """
    Archive a processed CSV.

    If another file with the same name already
    exists, automatically append a counter.

    Returns
    -------
    pathlib.Path
        Final archived path.
    """

    destination = ARCHIVE_FOLDER / game

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    source = Path(file_path)

    archived = destination / source.name

    counter = 2

    while archived.exists():

        archived = (
            destination
            / f"{source.stem}_{counter}{source.suffix}"
        )

        counter += 1

    shutil.move(
        str(source),
        str(archived)
    )

    return archived