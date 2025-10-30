# Session Context Fix

## Problem Identified
The session key was changing between requests because it was based on ALL user messages in the conversation history.

### What Was Happening

**Request 1:**
```
User messages: ["find the articles that mention the drupal migration"]
Session key: hash("find the articles that mention the drupal migration")
→ Stores results under this key
```

**Request 2:**
```
User messages: [
  "find the articles that mention the drupal migration",
  "of those, get 2 articles that mention the CLI"
]
Session key: hash("find...drupal|of those...CLI")
→ Different key! Can't find previous results
```

## Solution
Use only the **FIRST** user message to generate the session key. This keeps the key stable throughout the entire conversation.

### Fixed Code

```python
# OLD (BROKEN)
user_messages = [msg.content for msg in conversation_history if msg.role == "user"]
session_data = "|".join(user_messages)  # Includes ALL messages
session_key = hashlib.md5(session_data.encode()).hexdigest()

# NEW (FIXED)
user_messages = [msg.content for msg in conversation_history if msg.role == "user"]
if user_messages:
    # Hash only the FIRST user message
    session_key = hashlib.md5(user_messages[0].encode()).hexdigest()
```

### Now Both Requests Use Same Key

**Request 1:**
```
First user message: "find the articles that mention the drupal migration"
Session key: f56551ec4cd77f8a30718960b67521d5
→ Stores results
```

**Request 2:**
```
First user message: "find the articles that mention the drupal migration"  
Session key: f56551ec4cd77f8a30718960b67521d5
→ Same key! Finds previous results ✅
```

## How to Test

### Option 1: Automated Test Script
```bash
# Make sure backend is running
python -m uvicorn backend.main:app --reload

# In another terminal, run the test
python3 test_context_fix.py
```

### Option 2: Manual Test via Frontend
```bash
# Start backend
python -m uvicorn backend.main:app --reload

# Open frontend
open http://localhost:8000/frontend/index.html

# Test these exact queries:
1. "find the articles that mention the drupal migration"
2. Wait for results
3. "of those, get 2 articles that mention the CLI"

# Expected: Filtered results, NOT "don't have access to previous results"
```

### Option 3: curl Test
```bash
# Request 1
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find the articles that mention the drupal migration",
    "conversation_history": []
  }' > response1.json

# Request 2 (with history)
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "of those, get 2 articles that mention the CLI",
    "conversation_history": [
      {"role": "user", "content": "find the articles that mention the drupal migration"},
      {"role": "assistant", "content": "Here are articles about drupal migration"}
    ]
  }' > response2.json

# Check response2.json for filtered results
cat response2.json | jq '.message'
# Should NOT say "don't have access to previous results"
```

## Expected Backend Logs

### Request 1 (Search):
```
INFO: Received conversation request: 'find the articles that mention...'
INFO: >>> Session key: f56551ec4cd77f8a30718960b67521d5
INFO: >>> Conversation history messages: 0
INFO: >>> No previous results found for session: f56551ec4cd77f8a30718960b67521d5
INFO: Claude response - Action: search, Term: drupal migration
INFO: >>> PERFORMING SEARCH with term: 'drupal migration', limit: 10
INFO: >>> SEARCH RETURNED 10 stories
INFO: >>> Stored 10 stories in session 'f56551ec4cd77f8a30718960b67521d5'
```

### Request 2 (Refine):
```
INFO: Received conversation request: 'of those, get 2 articles...'
INFO: >>> Session key: f56551ec4cd77f8a30718960b67521d5  ← SAME KEY!
INFO: >>> Conversation history messages: 2
INFO: >>> Found 10 previous results in session context  ← FOUND!
INFO: Claude response - Action: refine, Filter: CLI, Limit: 2
INFO: >>> REFINING PREVIOUS RESULTS with filter: 'CLI'
INFO: >>> Filtering 10 stories for term: 'CLI'
INFO: >>> Filtered from 10 to 2 stories
INFO: >>> REFINEMENT SUCCESSFUL: Returning 2 filtered stories
```

## Success Criteria

✅ Session key is SAME in both requests
✅ Backend logs show "Found X previous results in session context"  
✅ Action is "refine" (not "search")
✅ Filtered results returned
✅ NO message about "don't have access to previous results"

## What Changed

**File:** `backend/main.py`
**Lines:** ~143-152
**Change:** Session key generation now uses only first user message

---

**Status:** ✅ Fixed
**Date:** 2025-01-XX
**Tested:** Pending user verification
