# EVA Test Suite

**Directory**: `tests/`  
**Purpose**: Validation, unit testing, and integration testing.  
**Version**: v9.6.2

---

## 📋 Overview

The **Tests** directory contains the automated verification suite for the EVA organism. It ensures that system updates (Evolution/Growth/Healing) do not introduce regressions in core biological or cognitive functions.

---

## 📂 Structure

- **`unit/`**: Atomic tests for individual functions and classes.
- **`integration/`**: Tests focusing on the communication between systems (Bus/Registry).
- **`biological/`**: Specialized tests for hormone stability and vitals logic.
- **`cognitive/`**: Verification of memory retrieval and RAG scoring.

---

## 🚀 Running Tests

We use `pytest` as our primary testing framework.

```bash
# Run all tests
pytest tests/

# Run a specific system test
pytest tests/integration/test_physio_matrix_bus.py
```

---

## 📐 Governance

- **CI/CD Alignment**: All tests must pass before a minor or major version bump is recorded in the Registry.
- **Resonance Standard**: Integration tests must use the Resonance Bus for communication, never direct method calls.

---

*Verified Quality.*
