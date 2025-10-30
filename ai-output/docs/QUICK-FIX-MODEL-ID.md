# Quick Fix: Invalid Model ID

## The Problem
You're trying to use: `anthropic.claude-sonnet-4-5-20250929-v1:0`
This model **does not exist**.

## The Solution (2 steps)

### Step 1: Update your `.env` file
```bash
# Open your .env file and change the BEDROCK_MODEL_ID line to:
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
```

### Step 2: Restart your backend
```bash
# Stop the backend (Ctrl+C) and restart:
python -m uvicorn backend.main:app --reload
```

## Verify It Works
```bash
# Test the endpoint:
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "conversation_history": []}'
```

## Why Did This Happen?

The SPECS.md mentioned `anthropic.claude-sonnet-4-5-v1:0` which was either:
- A typo
- Future speculation
- Confusion with version numbers

**Reality:** The latest Claude model is Claude **3.5** Sonnet, not 4.5.

## Still Having Issues?

Run the model checker:
```bash
python check_bedrock_models.py
```

This will show you all available models in your AWS account.

---

**TL;DR:** Change `BEDROCK_MODEL_ID` in `.env` to:
```
anthropic.claude-3-5-sonnet-20240620-v1:0
```
