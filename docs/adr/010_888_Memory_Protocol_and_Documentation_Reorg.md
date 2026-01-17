# ADR 010: 8-8-8 Memory Synthesis Protocol & Documentation Reorganization
>
> **Status**: Accepted
> **Date**: 2026-01-17

## Context

As EVA v9.4.0 matures into a state-dominant informational organism, the volume of conversational data and architectural documentation has grown. This led to two challenges:

1. **Memory Efficiency**: Raw logs alone do not scale. A tiered distillation process is needed to extract long-term wisdom from short-term episodes.
2. **Navigability**: Documentation was scattered across root and subfolders, making onboarding and retrieval difficult for both humans and AI.

## Decision

1. **8-8-8 Protocol**: Implement a tiered memory structure:
   - **Consciousness**: Awareness Domain (Functional Buffer).
   - **Session**: Working Memory (Raw Logs).
   - **Core**: Short-term Memory (Summarized from 8 Sessions).
   - **Sphere**: Long-term Wisdom (Distilled from 8 Cores).
   - Each level uses the **Clean -> Summary -> Index -> Relation** synthesis pattern.

2. **Categorical Documentation**: Reorganize the `docs/` folder into a numbered hierarchy (00_Governance, 01_Philosophies, etc.) to provide a guided learning path and improve RAG performance on internal documentation.

## Consequences

- **Positive**:
  - Significant reduction in context window usage for long-term recall.
  - Clearer differentiation between active state and distilled wisdom.
  - Simplified onboarding for new developers/AI agents via `INDEX.md`.
- **Neutral**:
  - Requires automated background agents (MSP / TruthSeeker) to perform periodic synthesis tasks.
