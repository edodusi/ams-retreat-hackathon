# Tests

This folder contains **ONLY** automated tests (unit tests, integration tests).

## What Belongs Here

✅ **Automated test files:**
- Python test files using pytest (test_*.py)
- JavaScript/TypeScript test files (*.test.js, *.spec.js)
- Test configuration files (pytest.ini, jest.config.js)
- Test fixtures and mock data
- `__init__.py` for Python test modules

❌ **What does NOT belong here:**
- Shell scripts for manual validation
- Verification scripts
- Debug patches
- Ad-hoc testing utilities

**Note:** All validation scripts, shell scripts, and debugging tools are in `ai-output/validation/`

## Test Files

- `test_main.py` - Main API endpoint unit tests (FastAPI TestClient)
- `test_analytical_features.py` - Analytical features unit tests
- `test_limit_extraction.py` - Limit extraction integration tests
- `pytest.ini` - Pytest configuration
- `__init__.py` - Python test package marker

## Running Tests

### Run all pytest tests:
```bash
pytest tests/
```

### Run specific test file:
```bash
pytest tests/test_main.py
```

### Run with coverage:
```bash
pytest --cov=backend tests/
```

## Guidelines

**Only automated test files belong in this folder.**

For validation scripts and debugging tools, see `ai-output/validation/`
