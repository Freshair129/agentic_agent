---
description: Protocol for performing complex system refactors with high autonomy.
---

# Autonomous Refactor Protocol (v9.4.3)

Use this workflow when performing large-scale structural changes or module deconstructions.

## 1. Chain of Command

- **Architect (LLM)**: Responsible for high-level planning, task breakdown, and final verification of worker output.
- **Worker (LLM Sub-agent)**: Responsible for batch file edits and unit testing.
- **User**: Final approval authority for each major phase.

## 2. Refactor Lifecycle (Cycle: Plan -> Code -> Verify -> Summarize)

1. **Plan**: Identify target systems and define interfaces ($I-Prefix$ ABCs) first.
2. **Code**:
   - Perform Batch Edits to maintain consistency across interdependent files.
   - Follow **GSD (Goal-State Driven)** standards: 100% type hinting and robust I/O.
3. **Verify**:
   - Run terminal commands to check syntax and logic.
   - **Self-Healing**: If a bug is found, attempt a fix at least 3 times before requesting user intervention.
4. **Summarize**: Update the mission/task document immediately upon successful verification.

## 3. Core Technical Laws

- **Decoupling**: Implement the **Resonance Bus** pattern for inter-system communication.
- **Persistence**: Ensure the **MSP Engine** (Subconscious Listener) latches state snapshots automatically.
- **Versioning**: Apply the **Independent Versioning** mapping (Legacy 8->1, 9->2).

## 4. Safety Constraints

- **PhysioCore**: Never touch unless explicitly unlocked by the User.
- **SSOT**: The Mission Document is the highest law. If code conflicts with the plan, follow the plan.

// turbo-all
