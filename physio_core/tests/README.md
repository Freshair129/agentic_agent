# PhysioCore Tests

This directory contains unit and integration tests for the Physiological Controller.

## Test Structure (Future)

```
tests/
├── test_hpa_axis.py             # HPA stress response tests
├── test_endocrine_system.py     # Hormone secretion tests
├── test_blood_engine.py         # Transport & decay tests
├── test_receptor_engine.py      # Signal transduction tests
├── test_ans.py                  # Autonomic nervous system tests
└── test_integration.py          # Full pipeline tests
```

## Running Tests

```bash
pytest physio_core/tests/
```

---

**Status**: Tests to be implemented in future sprint.
