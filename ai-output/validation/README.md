# Validation Tools

This folder contains validation scripts and debugging utilities that are separate from automated tests.

## Contents

### Validation Scripts
Shell scripts for manual testing and verification:
- `test_server.sh` - Server functionality validation
- `test_frontend.sh` - Frontend functionality validation
- `test_aws_endpoints.sh` - AWS integration validation
- `test_boto3.sh` - Boto3 client validation
- `test_analytical_features.sh` - Analytical features validation
- `final_test.sh` - Comprehensive validation suite
- `quick_test_search.sh` - Quick search functionality check

### Manual Test Files
- `test_context_fix.py` - Manual context-aware refinement validation
- `test-alpine-stories.html` - HTML page for manual Alpine.js testing

### Setup & Verification
- `check_bedrock_models.py` - AWS Bedrock model verification
- `verify_setup.py` - Setup verification script

### Fix Scripts & Patches
- `fix_frontend_xshow.sh` - Frontend display fixes
- `fix_model_id.sh` - Model ID configuration fixes
- `fix_frontend_display.patch` - Frontend patch
- `frontend_debug.patch` - Debug patch

## Usage

These scripts are meant for manual validation, debugging, and one-off checks during development. They are NOT part of the automated test suite.

For automated tests, see the `tests/` folder in the project root.

## Running Validation Scripts

```bash
# Make scripts executable if needed
chmod +x ai-output/validation/*.sh

# Run a validation script
./ai-output/validation/test_server.sh
```
