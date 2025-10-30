# Debugging Search Issue - Stories Not Showing

## Problem
When asking "find all marketing stories", the assistant responds with:
"I'm searching for marketing stories in the Storyblok content. Here's what I found:"

But no story previews are displayed.

## Possible Causes

### 1. Claude Not Returning Proper JSON Format
**Symptom:** Claude responds conversationally but doesn't trigger search action

**Check:**
```bash
# Enable DEBUG mode and check logs
DEBUG=true python -m uvicorn backend.main:app --reload

# Look for these log lines:
# - "Raw Claude response: ..."
# - "Parsed action: ..., term: ..."
# - ">>> PERFORMING SEARCH with term: ..."
```

**Fix Applied:** Updated system prompt to be more explicit about JSON format

### 2. Search Returns Empty Results
**Symptom:** Search is performed but returns 0 stories

**Check logs for:**
```
>>> SEARCH RETURNED 0 stories (total: 0)
```

**Possible reasons:**
- Invalid Storyblok credentials
- No matching content in space
- Wrong space ID
- Strata API not enabled

### 3. Search Error Not Displayed
**Symptom:** Search fails with error but error message not shown to user

**Check logs for:**
```
>>> STORYBLOK SEARCH ERROR: ...
```

### 4. Frontend Not Displaying Results
**Symptom:** Backend returns results but frontend doesn't show them

**Debug in Browser Console:**
```javascript
// Add to frontend/index.html after line 497:
console.log('API Response:', data);
console.log('Has results?', !!data.results);
if (data.results) {
    console.log('Stories count:', data.results.stories?.length || 0);
    console.log('First story:', data.results.stories?.[0]);
}
```

## Step-by-Step Debug Process

### Step 1: Check Backend Logs

Start server with DEBUG mode:
```bash
DEBUG=true python -m uvicorn backend.main:app --reload
```

### Step 2: Make a Test Request

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "find all marketing stories", "conversation_history": []}'
```

### Step 3: Check Log Output

Look for these key markers:

```
INFO - Received conversation request: 'find all marketing stories'
INFO - Raw Claude response: {"action": "search", ...
INFO - Parsed action: search, term: marketing
INFO - >>> PERFORMING SEARCH with term: 'marketing'
INFO - >>> SEARCH RETURNED 5 stories (total: 5)
INFO - >>> RESULTS ATTACHED TO RESPONSE: 5 stories
INFO - >>> SUCCESS: Found 5 results with full previews
INFO - >>> FINAL RESPONSE: message length=XX, has_results=True
INFO - >>> RETURNING 5 stories in response
```

### Step 4: Identify Where It Fails

**If you see:**
- ✅ "Parsed action: search" → Claude is working correctly
- ❌ "Parsed action: chat" → Claude not returning JSON properly

**If you see:**
- ✅ "PERFORMING SEARCH" → Search is being triggered
- ❌ "NO SEARCH PERFORMED" → Search action not being executed

**If you see:**
- ✅ "SEARCH RETURNED 5 stories" → Storyblok is working
- ❌ "SEARCH RETURNED 0 stories" → No results from Storyblok
- ❌ "STORYBLOK SEARCH ERROR" → API error

**If you see:**
- ✅ "RETURNING 5 stories in response" → Backend is correct
- Check frontend if stories still don't appear

## Quick Fixes

### Fix 1: Force Search Action

Test if search works when forced:

```bash
DEBUG=true curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "search for: marketing", "conversation_history": []}'
```

### Fix 2: Test Storyblok Directly

```bash
DEBUG=true curl "http://localhost:8000/api/test-storyblok?term=marketing"
```

Expected response:
```json
{
  "status": "success",
  "results": {
    "stories": [...],
    "total": 5
  }
}
```

### Fix 3: Check Frontend Console

Open browser DevTools (F12) → Console tab

Look for:
- API response object
- Any JavaScript errors
- Stories array length

## Common Issues & Solutions

### Issue: Claude Returns Text Instead of JSON

**Example response:**
```
"I'm searching for marketing stories..."
```

**Solution:** The new system prompt should fix this. If it persists:
1. Check if Claude model supports JSON mode
2. Try adding explicit examples in prompt
3. Consider using a different Claude model

### Issue: Empty Results from Storyblok

**Check:**
1. Storyblok credentials valid: `echo $STORYBLOK_TOKEN`
2. Space ID correct: `echo $STORYBLOK_SPACE_ID`
3. Content exists in space
4. Strata API enabled for space

**Test:**
```bash
# Test with Storyblok API directly
curl -H "Authorization: YOUR_TOKEN" \
  "https://api-staging-d1.storyblok.com/v1/spaces/YOUR_SPACE/vsearches?term=marketing"
```

### Issue: Stories Schema Mismatch

If you see validation errors:
```
ValidationError: Field 'body' required
```

Check that Strata API is returning new schema format.

## Enhanced Logging Applied

The following improvements have been made:

### Backend (`backend/bedrock_client.py`):
- ✅ Log raw Claude response
- ✅ Log parsed action and term
- ✅ Better JSON parse error messages

### Backend (`backend/main.py`):
- ✅ Log action, term, and message length
- ✅ Log ">>> PERFORMING SEARCH" marker
- ✅ Log search results count
- ✅ Log full story fetch progress
- ✅ Log final response details
- ✅ Log why search wasn't performed

### System Prompt:
- ✅ More explicit JSON format requirements
- ✅ Example responses
- ✅ "CRITICAL" instructions for search action

## Testing the Fix

Run this complete test:

```bash
# 1. Start server with debug logging
DEBUG=true python -m uvicorn backend.main:app --reload &
SERVER_PID=$!

# 2. Wait for server to start
sleep 3

# 3. Test search
echo "Testing search..."
curl -s -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "find all marketing stories", "conversation_history": []}' \
  | python3 -m json.tool

# 4. Kill server
kill $SERVER_PID
```

Check the output for:
- `"results"` field present
- `"stories"` array with items
- Each story has: `body`, `cursor`, `name`, `slug`, `story_id`

## Next Steps

1. ✅ Enhanced logging added
2. ✅ Improved system prompt
3. ⏭️ Test with actual query
4. ⏭️ Check logs for specific failure point
5. ⏭️ Apply targeted fix based on logs

## Contact

If issue persists after these changes, provide:
1. Complete server logs from a test request
2. Browser console output
3. curl response from test endpoint
