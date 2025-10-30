# Search Issue Fix - Summary

## Problem Reported
When asking "find all marketing stories", the assistant responds but no story previews are displayed.

## Fixes Applied

### 1. Enhanced Claude System Prompt (`backend/bedrock_client.py`)

**Changes:**
- Added explicit "IMPORTANT: You MUST respond ONLY with valid JSON" instruction
- Added concrete example for "find all marketing stories" query
- Added "CRITICAL" note to always use search action for find/search queries
- Clarified response field should be brief

**Why:** Claude might be responding conversationally instead of returning proper JSON format with search action.

### 2. Enhanced Logging (`backend/bedrock_client.py` + `backend/main.py`)

**Added logs:**
- Raw Claude response (first 200 chars)
- Parsed action and search term
- ">>> PERFORMING SEARCH" marker
- Search results count
- Full story fetch progress
- Final response details
- Reason when search is NOT performed

**Why:** To identify exactly where the flow breaks.

### 3. Created Debug Tools

**Files:**
- `DEBUGGING_SEARCH_ISSUE.md` - Complete debugging guide
- `quick_test_search.sh` - Quick test script
- `frontend/debug_patch.txt` - Frontend logging instructions

## How to Diagnose

### Step 1: Start Server with Debug Logging

```bash
DEBUG=true python -m uvicorn backend.main:app --reload
```

### Step 2: Run Test Script

```bash
./quick_test_search.sh
```

### Step 3: Check Server Logs

Look for these markers in order:

```
✅ Raw Claude response: {"action": "search", ...
✅ Parsed action: search, term: marketing
✅ >>> PERFORMING SEARCH with term: 'marketing'
✅ >>> SEARCH RETURNED 5 stories (total: 5)
✅ >>> SUCCESS: Found 5 results with full previews
✅ >>> RETURNING 5 stories in response
```

**If any marker is missing**, that's where the issue is.

## Common Scenarios

### Scenario A: Claude Not Returning JSON

**Symptoms:**
```
Raw Claude response: I'm searching for marketing stories...
Parsed action: chat, term: None
>>> NO SEARCH PERFORMED - Action: chat
```

**Solution:** The enhanced prompt should fix this. If not, may need to:
- Try different phrasing in query
- Check if Claude model supports JSON mode
- Consider structured output mode

### Scenario B: Search Returns Empty

**Symptoms:**
```
>>> PERFORMING SEARCH with term: 'marketing'
>>> SEARCH RETURNED 0 stories (total: 0)
```

**Solution:** Check Storyblok:
```bash
DEBUG=true curl "http://localhost:8000/api/test-storyblok?term=marketing"
```

### Scenario C: Search Error

**Symptoms:**
```
>>> STORYBLOK SEARCH ERROR: Connection timeout
```

**Solution:** Check:
- Storyblok credentials in `.env`
- Space ID is correct
- Network connectivity
- API endpoint URL

### Scenario D: Backend Works, Frontend Doesn't

**Symptoms:**
- Logs show ">>> RETURNING 5 stories in response"
- But frontend doesn't display them

**Solution:** Check browser console (F12) for:
- JavaScript errors
- API response structure
- Stories array

## Test Commands

### Test 1: Direct API Call

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "find all marketing stories", "conversation_history": []}' \
  | python3 -m json.tool
```

Expected: `"results"` field with `"stories"` array

### Test 2: Storyblok Directly

```bash
DEBUG=true curl "http://localhost:8000/api/test-storyblok?term=marketing"
```

Expected: `"status": "success"` with stories

### Test 3: Force Search

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "search: marketing", "conversation_history": []}'
```

## What to Share If Issue Persists

1. **Server logs** from a test request (with DEBUG=true)
2. **Script output** from `./quick_test_search.sh`
3. **Browser console** output (if frontend issue)
4. **Test endpoint result**: `curl http://localhost:8000/api/test-storyblok?term=marketing`

## Next Steps

1. Run `./quick_test_search.sh` with server running
2. Check which marker is missing in logs
3. Use DEBUGGING_SEARCH_ISSUE.md for detailed troubleshooting
4. Share specific logs if issue continues

## Files Modified

- ✅ `backend/bedrock_client.py` - Enhanced prompt + logging
- ✅ `backend/main.py` - Enhanced logging
- ✅ `DEBUGGING_SEARCH_ISSUE.md` - Debug guide
- ✅ `quick_test_search.sh` - Test script
- ✅ `SEARCH_FIX_SUMMARY.md` - This file

---

**The enhanced logging will pinpoint exactly where the issue occurs!**
