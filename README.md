# Project Sentinel
Measure first. Improve second. Never guess.

Developer:
Erik Castillo

Started:
June 2026

Purpose:

Sentinel is a PC diagnostics application built around HWiNFO logs.

Goals:

- Analyze HWiNFO logs
- Generate health reports
- Track upgrades
- Compare hardware
- Build historical trends

# Project Sentinel

A modular system monitoring and analysis framework.

## Overview
Project Sentinel collects, processes, and displays hardware telemetry such as CPU, GPU, memory, and system performance metrics.

## Architecture
- `core/reader.py` → Extracts raw data
- `core/analyzer.py` → Processes and computes stats
- `main.py` → Controller entry point (orchestrates modules)

## Goal
A plugin-style monitoring system where modules can be added without overlap or dependency conflicts.