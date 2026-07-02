# core/metadata/machine.py

"""
Project Sentinel

Machine Metadata

Collect hardware information for the current system.

This module is the single interface between Sentinel and the
operating system for machine metadata.

Public API
----------
get_machine_info()

Future Notes
------------
Currently optimized for Windows.

If Sentinel is ever ported to another operating system,
only this module should require modification.
"""

from subprocess import run, PIPE


# ==========================================================
# Public API
# ==========================================================

def get_machine_info():
    """
    Collect machine metadata.

    Returns
    -------
    dict
        Machine information for the current system.
    """

    return {
        "cpu": _get_cpu(),
        "gpu": _get_gpu(),
        "ram": _get_ram(),
        "motherboard": _get_motherboard(),
    }


# ==========================================================
# Hardware Queries
# ==========================================================

def _get_cpu():
    """Return the installed CPU."""

    return _run_powershell(
        "(Get-CimInstance Win32_Processor).Name"
    )


def _get_gpu():
    """Return the primary GPU."""

    return _run_powershell(
        "(Get-CimInstance Win32_VideoController | "
        "Select-Object -First 1).Name"
    )


def _get_motherboard():
    """Return motherboard manufacturer and model."""

    manufacturer = _run_powershell(
        "(Get-CimInstance Win32_BaseBoard).Manufacturer"
    )

    product = _run_powershell(
        "(Get-CimInstance Win32_BaseBoard).Product"
    )

    if manufacturer == "Unknown" and product == "Unknown":
        return "Unknown"

    return f"{manufacturer} {product}".strip()


def _get_ram():
    """Return installed system memory."""

    command = (
        "[math]::Round("
        "(Get-CimInstance Win32_ComputerSystem)"
        ".TotalPhysicalMemory / 1GB)"
    )

    ram = _run_powershell(command)

    if ram == "Unknown":
        return ram

    return f"{ram} GB"


# ==========================================================
# Helpers
# ==========================================================

def _run_powershell(command):
    """
    Execute a PowerShell command.

    Parameters
    ----------
    command : str

    Returns
    -------
    str

    Returns "Unknown" if the command fails.
    """

    try:

        result = run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                command,
            ],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            check=True,
        )

        output = result.stdout.strip()

        return output if output else "Unknown"

    except Exception:

        return "Unknown"