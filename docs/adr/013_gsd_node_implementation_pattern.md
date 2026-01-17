# ADR-013: GSD Node Implementation Pattern

- **Status**: Accepted
- **Decided by**: USER, Antigravity
- **Date**: 2026-01-17

## 1. Context & Problem

The "Subconscious" layer of EVA (MSP modules) was transitioning from monolithic scripts to a Module/Node hierarchy. However, the initial "Nodes" were often skeletal stubs or lacked consistent error handling and type safety. To achieve the "Elegant Truth" and "Craftsman's Soul" pillars of the EVA Constitution, a more rigorous implementation standard was needed for these logic-heavy units.

## 2. Decision: GSD (Goal-State Driven) Standard

We have adopted a strict **GSD Implementation Pattern** for all level-4 (Node) and level-5 (Component) entities.

### Key Pillars

1. **Strict Type Hinting**: 100% type annotation for all methods (inputs and outputs). No `Any` unless absolutely unavoidable for raw data pass-through.
2. **Logic-Data Separation**: Nodes must not hold complex internal state if they are intended to be interchangeable logic providers. They should resolve parameters from the central `config` during initialization.
3. **Robust I/O**: All filesystem operations must be wrapped in exception handling with fallback or failure reporting (`return False` or `Optional` results).
4. **SSOT Initialization**: Nodes must resolve their identity and parameters from the `module_definitions` section of the system's YAML config, rather than having hardcoded paths.
5. **Standardized Imports**: All external and contract imports must be placed at the top of the file to ensure clarity and support for the `Doc-to-Code` protocol.

## 3. Implementation Checklist (The "Worker's Rule")

- [ ] Does the node use the `config` object for all path resolutions?
- [ ] Are all methods type-hinted?
- [ ] Is error handling implemented for all external calls (files, bus, etc.)?
- [ ] Is the header versioned independently if it's a major logic unit?
- [ ] Does it follow the naming convention `[Name]Node`?

## 4. Consequences

- **Positive**: Higher code quality and reliability. Easier debugging of memory-related logic. Compliance with "The Craftsman's Soul" directive. Predictable behavior across different environments.
- **Negative**: Initial development time per node is slightly increased.
- **Nuance**: This pattern works in conjunction with the **Doc-to-Code** protocol to ensure that behavior is defined in documentation before it is enforced in code.
