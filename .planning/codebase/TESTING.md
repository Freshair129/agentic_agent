# Testing Patterns

**Analysis Date:** 2026-01-18

## Test Framework

**Runner:**
- `unittest` (Python standard library)
- Config: No pytest config detected

**Assertion Library:**
- `unittest.TestCase` assertions

**Run Commands:**
```bash
python -m pytest tests/                    # Run all tests (if pytest installed)
python -m pytest {module}/tests/           # Run module tests
python {module}/tests/test_{module}_init.py   # Run single test file
```

## Test File Organization

**Location:**
- Co-located with modules: `{module}/tests/`
- Root-level tests: `tests/`

**Naming:**
- Pattern: `test_{module}_init.py`
- Examples:
  - `physio_core/tests/test_physio_core_init.py`
  - `eva_matrix/tests/test_eva_matrix_init.py`
  - `memory_n_soul_passport/tests/test_msp_init.py`

**Structure:**
```
{module}/
├── {module}.py
├── configs/
├── schema/
└── tests/
    └── test_{module}_init.py
```

## Test Structure

**Suite Organization:**
```python
import unittest
from pathlib import Path

class Test{Module}Initialization(unittest.TestCase):

    def test_initialization(self):
        """Test basic module initialization"""
        # Setup
        # Execute
        # Assert
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
```

**Patterns:**
- Single test class per file (initialization focus)
- Test methods: `test_{functionality}()`
- Docstrings for test descriptions
- Try/except for error tolerance (placeholder tests)

## Mocking

**Framework:** None detected (manual mocking)

**Patterns:**
```python
# Manual mocking with None
physio = PhysioController(
    endocrine_cfg_path=str(config_path),
    msp=None,  # Mock MSP dependency
    bus=None   # Mock Resonance Bus
)
```

**What to Mock:**
- External dependencies: MSP, Resonance Bus
- Config paths: Use Path resolution

**What NOT to Mock:**
- Module internals
- YAML config files (use real files)

## Fixtures and Factories

**Test Data:**
```python
# Path resolution for config files
root_path = Path(__file__).parent.parent.parent
base_config = root_path / "{module}" / "configs"
```

**Location:**
- No centralized fixtures detected
- Test data embedded in test files

## Coverage

**Requirements:** None enforced

**View Coverage:**
```bash
# If pytest-cov installed
python -m pytest --cov={module} {module}/tests/
```

## Test Types

**Unit Tests:**
- Scope: Module initialization
- Approach: Basic smoke tests (`assertIsNotNone`)
- Current state: Placeholder tests (error-tolerant)

**Integration Tests:**
- Scope: Not detected
- Approach: Would require full system boot

**E2E Tests:**
- Not detected

## Common Patterns

**Path Resolution:**
```python
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
```

**Error Tolerance:**
```python
try:
    result = Module()
    self.assertIsNotNone(result)
    print("[SUCCESS] Initialized.")
except Exception as e:
    print(f"[FAILURE] {e}")
    pass  # Don't fail test (placeholder)
```

## Test Coverage Status

**Current Coverage:**
- Modules tested: 11 modules have `test_*_init.py`
- Test depth: Shallow (initialization only)
- Mocking: Minimal (None for dependencies)

**Modules with Tests:**
- `physio_core/tests/test_physio_core_init.py`
- `eva_matrix/tests/test_eva_matrix_init.py`
- `memory_n_soul_passport/tests/test_msp_init.py`
- `artifact_qualia/tests/test_artifact_qualia_init.py`
- `capabilities/services/agentic_rag/tests/test_agentic_rag_init.py`
- `orchestrator/tests/test_orchestrator_init.py`
- Plus 5 more

**Modules without Tests:**
- `genesis_knowledge_system/` (no tests detected)
- `operation_system/` (no tests detected)
- Individual services/tools (partial coverage)

## Test Execution

**Manual Execution:**
```bash
# Run single module test
cd physio_core/tests
python test_physio_core_init.py

# Run with unittest discovery
python -m unittest discover -s tests/ -p "test_*.py"
```

**Automated:**
- No CI/CD detected
- No pre-commit hooks for tests

---

*Testing analysis: 2026-01-18*
