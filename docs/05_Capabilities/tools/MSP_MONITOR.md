# 🏥 AuthDoc: MSP Monitor Utility

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/tools/msp_monitor.py`

## 1. Overview
The MSP Monitor is a diagnostic tool designed to track the health and capacity of the [Memory & Soul Passport](file:///e:/The%20Human%20Algorithm/T2/agent/docs/04_Systems/memory_n_soul_passport/msp_overview.md) system.

## 2. Core Responsibilities
- **Capacity Tracking**: Monitors the size of `.jsonl` archives and triggers cleanup alerts.
- **Entry Validation**: Performs periodic sampling of episodic records to ensure schema compliance.
- **Performance Diagnostics**: Measures the latency of memory retrieval and persistence operations.

## 3. Code Mapping
- `tools/msp_monitor.py`: Implementation of the monitor logic.
