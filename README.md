# Project Sentinel

**Measure first. Improve second. Never guess.**

Project Sentinel is a Windows desktop application for turning HWiNFO CSV logs
into clear PC performance and hardware-health reports. It keeps game sessions,
shows game-level trends over time, and makes it easier to spot regressions after
driver, settings, or hardware changes.

> Sentinel is designed for analysing saved HWiNFO logs. It does not currently
> read live sensor data or control HWiNFO.

## What it does

- Analyses CPU, GPU, RAM, and FPS telemetry through the Sentinel engine.
- Assigns health statuses to the collected sensor data.
- Archives each processed source CSV and stores a session record locally.
- Shows a desktop report with current, average, minimum, maximum, and health
  data for every captured sensor.
- Groups sessions by game, with game-level averages and trend charts for FPS,
  CPU/GPU temperature, CPU/GPU usage, and RAM usage.
- Lets you browse stored sessions and compare two sessions side by side.

## Requirements

- Windows
- Python 3.10 or newer
- [HWiNFO](https://www.hwinfo.com/) configured to create CSV sensor logs

## Install

Clone the repository and open a PowerShell terminal in the project folder:

```powershell
git clone <your-repository-url>
cd Sentinel
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents virtual-environment activation, run the following once
for your user account, then reopen the terminal:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Run Sentinel

With the virtual environment active and the terminal in the repository root:

```powershell
python .\src\main.py
```

The desktop application opens directly; no console menu is required.

### Launch by double-clicking

After installing the requirements, double-click `Sentinel.pyw` in the project
root. Windows launches it with Python without opening a console window. You can
right-click the file and choose **Send to > Desktop (create shortcut)** for a
desktop shortcut.

## Share Sentinel with other people

For a normal Windows installation, build the release once on a development
machine, then send the resulting `release\Sentinel-Setup.exe` to the person
using Sentinel. They only need to double-click the installer and follow the
wizard; it creates Start Menu and optional desktop shortcuts. They do **not**
need Python, a virtual environment, or any Python packages.

To create that installer:

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php) on the development
   machine.
2. From the repository root with the development virtual environment active,
   run `./build-release.ps1`. It creates the app and installer automatically.
3. Send `release\Sentinel-Setup.exe` to the recipient.

The recipient still needs HWiNFO to create the CSV logs that Sentinel analyses.

## Typical workflow

1. In HWiNFO, start sensor logging and save the session as a CSV file.
2. Copy the CSV into `data/incoming`.
3. Start Sentinel and select **Analyze Latest Log**.
4. Click **Scan folder**, select the log, then choose **Analyze selected**.
5. Confirm or enter the game name.
6. Sentinel analyses the file, archives the source CSV, and saves the session.
7. Open **Performance Overview** and choose a game to see all of its sessions,
   aggregate sensor values, and performance trends.

Sentinel detects duplicate source files using a SHA-256 hash. Re-analysing the
same log loads its existing session instead of creating a duplicate.

## Desktop pages

| Page | Purpose |
| --- | --- |
| **Performance Overview** | Game-level summary, transposed sensor report, and per-session trend graphs. |
| **Analyze Latest Log** | Finds CSV files in `data/incoming` and sends the selected file to the analysis service. |
| **History** | Lists all recorded sessions; double-click a row to open that game's overview. |
| **Compare Sessions** | Compares average FPS, temperatures, usage, and RAM values between two saved sessions. |
| **Settings** | Displays the active Sentinel storage locations. Persistent editable settings are planned. |

## Data locations

The application creates and uses these folders in the repository:

```text
data/
|-- incoming/     # Place new HWiNFO CSV logs here
|-- archive/      # Source CSVs after successful analysis, organised by game
|-- processed/    # Saved Sentinel session records (JSON)
|-- config/       # Game-name aliases and future settings
`-- exports/      # Generated exports
```

**Important:** a successfully analysed CSV is moved from `data/incoming` to
`data/archive/<game>/`. Keep an original copy elsewhere if you need one.

## Project structure

```text
src/
|-- main.py                 # Desktop application entry point
`-- core/
    |-- engine/             # CSV reader, metric analysis, health rules
    |-- services/           # Analysis workflow coordination
    |-- database/           # Local session persistence and queries
    |-- archive/            # CSV archive and session creation
    |-- models/             # Session, report, and sensor data models
    `-- ui/desktop.py       # PySide6 desktop interface
```

The interface does not perform analysis itself. Its data flow is:

```text
Desktop UI -> AnalysisService -> Engine -> Session database
```

## Current status and next steps

Sentinel currently provides desktop log analysis, archived session history,
game-level trend charts, and session comparison. Planned work includes editable
saved settings, automatic folder monitoring, richer charting, and Windows
packaging with PyInstaller.

## Developer

Created by Erik Castillo. Started June 2026.
