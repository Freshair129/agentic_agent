# ADR-012: Resonance Bus State Decoupling

- **Status**: Accepted
- **Decided by**: USER, Antigravity
- **Date**: 2026-01-17

## 1. Context & Problem

Previously, core systems like `PhysioCore`, `EVAMatrix`, and `ArtifactQualia` were tightly coupled through direct method calls managed by the `Orchestrator`. This created a synchronous bottleneck and made it difficult to scale or replace individual components without modifying the main orchestrator logic. Additionally, persistence (MSP) required explicit calls to save state, increasing the risk of state drift.

## 2. Decision: Decentralized Bus-Driven Architecture

We have implemented a **Subscriber-based Decoupling Pattern** using the `Resonance Bus` (v2.4.3).

### Key Decisions

1. **Autonomous Propagation**: Components no longer call each other. Instead, they publish their state snapshots to specialized bus channels (`BUS_PHYSICAL`, `BUS_PSYCHOLOGICAL`, etc.) and subscribe to relevant incoming signals.
2. **Orchestrator as Trigger**: The `Orchestrator` is demoted from a "manager" to a "trigger". It simply kicks off the first step in the chain (e.g., `PhysioCore.step()`), and the resulting signals propagate through the bus to other subscribers (Matrix, Qualia).
3. **MSP as Subconscious Listener**: The `MSP` engine now functions as a passive listener on all core bus channels. It automatically "latches" arriving state snapshots into its active state cache, ensuring continuous and automatic persistence without explicit orchestration.
4. **Interface Standard**: All communication must adhere to the `IResonanceBus` interface, ensuring a standardized payload structure (`payload` + `__metadata__`).

## 3. Implementation Details

- **Transport**: `ResonanceBus` implements `IResonanceBus`, providing `publish` and `subscribe` methods.
- **PhysioCore**: Publishes to `BUS_PHYSICAL` after every tick.
- **EVA Matrix**: Subscribes to `BUS_PHYSICAL` and publishes to `BUS_PSYCHOLOGICAL`.
- **Artifact Qualia**: Subscribes to `BUS_PSYCHOLOGICAL` and publishes to `BUS_PHENOMENOLOGICAL`.
- **MSP**: Subscribes to all and updates internal state memory.

## 4. Consequences

- **Positive**: Improved modularity and testability. Components can be run or tested in isolation by mocking bus signals. Orchestrator logic is significantly simplified. Automatic persistence reduces state management bugs.
- **Negative**: Slight overhead in signal propagation and metadata injection. Debugging signal flows requires better logging/tracing (partially addressed by the `ResonanceBus` history).
- **Nuance**: Temporal synchronization depends on the `tick_rate` of the primary trigger, but the *logic* of reaction is now decentralized.
