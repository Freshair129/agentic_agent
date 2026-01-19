# 🧠 AuthDoc: Engram System Service

> **Status**: DRAFT (v9.6.2 Backfill)
> **Governs**: `capabilities/services/engram_system/`

## 1. Overview
The Engram System is an O(1) high-frequency memory cache designed to store and retrieve "hot" context (emotional snapshots, salience anchors) without the overhead of full RAG or long-term storage.

## 2. Shared Responsibility
- **System Layer**: Subscribes to `BUS_PSYCHOLOGICAL` to catch high-arousal events.
- **Cache Logic**: Implements LRU (Least Recently Used) eviction for volatile state.
- **MSP Integration**: Periodically flushes engrams to the [MSP](file:///e:/The%20Human%20Algorithm/T2/agent/docs/04_Systems/memory_n_soul_passport/msp_overview.md) for permanent archival.

## 3. Code Mapping
- `engram_system/engram_controller.py`: Main service entry point.
- `engram_system/cache_logic.py`: Vector-based hot-cache implementation.
