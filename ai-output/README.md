# AI Output

This folder contains AI-generated documentation and validation scripts that are separate from the application logic.

## Structure

- **`docs/`** - All project documentation (markdown files, specs, guides)
- **`validation/`** - Validation scripts, test utilities, and debugging tools

## Purpose

This separation ensures that:
1. Application logic (`backend/`, `frontend/`) is distinct from AI-generated artifacts
2. Automated tests (`tests/`) only contain real test files (pytest, jest, etc.)
3. Documentation and validation tools are organized but clearly separated from production code

## Contents

### docs/
Contains all project documentation including:
- API documentation
- Setup guides
- Feature documentation
- Change logs and summaries
- Architecture diagrams

### validation/
Contains validation and debugging tools including:
- Shell scripts for manual testing (*.sh)
- Verification scripts
- Debug patches
- Model checking utilities
