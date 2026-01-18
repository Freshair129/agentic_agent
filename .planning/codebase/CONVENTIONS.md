# Coding Conventions

**Analysis Date:** 2026-01-18

## Naming Patterns

**Files:**
- Python modules: `snake_case.py` (`physio_core.py`, `eva_matrix.py`)
- Config files: `{Module}_configs.yaml` (PascalCase module name)
- Schemas: `{Module}_Payload_Schema_v2.json`
- Tests: `test_{module}_init.py`

**Functions:**
- `snake_case` for all functions (`clamp()`, `safe_print()`)
- Private functions: `_prefix` (`_initialize_chat()`, `_decay()`)

**Variables:**
- `snake_case` for all variables (`hormone_levels`, `body_state`)
- Constants: `UPPER_SNAKE_CASE` (implied, not enforced)

**Classes:**
- `PascalCase` for all classes (`PhysioCore`, `LLMBridge`, `EndocrineController`)
- Engine suffix common: `BloodEngine`, `ReceptorEngine`, `VitalsEngine`
- Controller suffix: `EndocrineController`, `CircadianController`

**Types:**
- `PascalCase` for custom types (follows Python typing conventions)

## Code Style

**Formatting:**
- No formal formatter detected (no Black, autopep8 config)
- Indentation: 4 spaces (Python standard)
- Line length: Not enforced (no config found)

**Linting:**
- No linter configuration found
- No `.pylintrc`, `.flake8`, or `pyproject.toml` with linting rules

**Docstrings:**
- Triple-quoted strings for module and class docs
- Format: Descriptive text, sometimes with structured sections
- Example:
  ```python
  """
  PhysioCore (Independent Version: 2.4.3)

  Role:
  - Orchestrate full physiological loop

  STRICT RULES:
  - No cognition
  - No memory
  """
  ```

## Import Organization

**Order:**
1. Standard library (`import yaml`, `import time`, `from pathlib import Path`)
2. Third-party libraries (`from typing import Dict, Any`, `import google.generativeai`)
3. Local modules (relative imports: `from .logic.endocrine import ...`)
4. Capabilities imports (`from capabilities.tools.logger import safe_print`)

**Path Aliases:**
- No path aliases detected
- Relative imports within modules: `from .logic.` pattern
- Absolute imports for cross-module: `from capabilities.tools.logger`

## Error Handling

**Patterns:**
- Try/except with structured logging
- Example pattern:
  ```python
  try:
      # operation
  except Exception as e:
      print(f"[MODULE] [ERROR] {e}")
  ```
- No custom exception hierarchy detected

**Logging:**
- Custom logger: `capabilities/tools/logger.py`
- Pattern: `from capabilities.tools.logger import safe_print` then `print = safe_print`
- Format: `[MODULE] [LEVEL] Message`
- Examples: `[PhysioCore] [INFO] Dopamine: 0.75`, `[LLM] [ERROR] Connection failed`

## Logging

**Framework:** Custom (`safe_print` wrapper)

**Patterns:**
- Structured format: `[MODULE] [LEVEL] Message`
- Levels observed: INFO, ERROR, WARNING (implied from format)
- Import: `from capabilities.tools.logger import safe_print` → `print = safe_print`

## Comments

**When to Comment:**
- Module headers (role, version, strict rules)
- Complex logic sections (YAML parsing, state transitions)
- Architectural constraints (e.g., "STRUCTURAL LOCK: DO NOT refactor")

**Inline Comments:**
- Used sparingly for clarification
- Often mark sections: `# --- Endocrine ---`, `# --- Blood ---`

## Function Design

**Size:** No strict limit (largest module is 2453 lines in MSP engine)

**Parameters:**
- Type hints used consistently (`str`, `Dict[str, Any]`, `Optional[str]`)
- Default values common: `def __init__(self, model_name: str = "gemini-2.0-flash-lite-preview-02-05")`

**Return Values:**
- Type hints for return types: `-> LLMResponse`, `-> Dict[str, float]`
- Custom response objects: `LLMResponse`, `ToolCall`

## Module Design

**Exports:**
- Classes exported via `__init__.py`
- Main classes: `PhysioCore`, `EVA_Matrix`, `LLMBridge`

**Barrel Files:**
- Not detected (no index-style re-exports)

**Structure:**
- Module-centric: Each major system is a root-level directory
- Internal structure: `Module/` or `logic/` (PhysioCore exception)
- Configs: `{module}/configs/`
- Schemas: `{module}/schema/`

## Type Hints

**Usage:**
- Extensive use of `typing` module
- Common types: `Dict`, `List`, `Any`, `Optional`, `Union`
- Custom types: `LLMResponse`, `ToolCall`

## Configuration

**Format:** YAML for all configs

**Naming:** `{Module}_configs.yaml`

**Loading:** `yaml.safe_load()` or `yaml.load()`

**Validation:** JSON Schema at module boundaries

---

*Convention analysis: 2026-01-18*
