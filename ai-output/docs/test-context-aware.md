# Quick Test Guide: Context-Aware Refinement

## 🎯 Goal
Test that the system can filter previous search results based on follow-up questions.

## 🚀 Setup

```bash
# Start backend
python -m uvicorn backend.main:app --reload

# Open frontend in browser
open http://localhost:8000/frontend/index.html
```

## ✅ Test Scenario 1: Basic Refinement

### Step 1: Initial Search
**Input:**
```
find 10 marketing stories
```

**Expected:**
- ✅ 10 story cards appear
- ✅ Debug indicator: `[Debug: Results object exists, stories count: 10]`
- ✅ Backend log shows: `Stored 10 stories in session context`

### Step 2: Filter by Keyword
**Input:**
```
out of those stories, give me the one which mentions omnichannel
```

**Expected:**
- ✅ Shows only stories containing "omnichannel"
- ✅ Backend log shows: `Action: refine, Filter: omnichannel`
- ✅ Backend log shows: `Filtered from 10 to X stories`
- ✅ Story count is less than 10

**Verification:**
- Read the displayed story titles/content
- Confirm "omnichannel" appears in at least one story
- If 0 results, try different keywords like "marketing", "strategy", "social"

---

## ✅ Test Scenario 2: Multiple Refinements

### Step 1: Initial Search
**Input:**
```
find blog posts about technology
```

**Expected:** ~10 technology blog posts

### Step 2: First Refinement
**Input:**
```
from these, show me only the ones about AI
```

**Expected:**
- ✅ Subset of original results
- ✅ Action: refine
- ✅ Filter applied: "AI"

### Step 3: Second Refinement
**Input:**
```
which one mentions machine learning?
```

**Expected:**
- ✅ Further filtered subset
- ✅ Progressive refinement working
- ✅ Context maintained through multiple turns

---

## ✅ Test Scenario 3: New Search vs Refinement

### Step 1: Initial Search
**Input:**
```
find marketing articles
```

**Expected:** Marketing articles displayed

### Step 2: Refinement (should filter)
**Input:**
```
show me the ones about social media
```

**Expected:**
- ✅ Action: refine (NOT search)
- ✅ Filters existing results
- ✅ Backend: "REFINING PREVIOUS RESULTS"

### Step 3: New Search (should start fresh)
**Input:**
```
now find blog posts about design
```

**Expected:**
- ✅ Action: search (NOT refine)
- ✅ New search performed
- ✅ Backend: "PERFORMING SEARCH"
- ✅ Context replaced with new results

---

## 🔍 Backend Log Verification

### Successful Refinement Logs
```
INFO: Received conversation request: 'out of those stories...'
INFO: >>> Found 10 previous results in session context
INFO: Claude response - Action: refine, Filter: omnichannel
INFO: >>> REFINING PREVIOUS RESULTS with filter: 'omnichannel'
INFO: >>> Filtered from 10 to 1 stories
INFO: >>> REFINEMENT SUCCESSFUL: Returning 1 filtered stories
```

### New Search Logs
```
INFO: Received conversation request: 'find marketing stories'
INFO: Claude response - Action: search, Term: marketing, Limit: 10
INFO: >>> PERFORMING SEARCH with term: 'marketing', limit: 10
INFO: >>> SEARCH RETURNED 10 stories (total: 10)
INFO: >>> Stored 10 stories in session context for refinement
```

---

## 🧪 Browser Console Verification

Open DevTools Console (F12) and look for:

### Search Action
```javascript
[DEBUG] API Response: {message: "...", results: {...}}
[DEBUG] Stories count: 10
```

### Refine Action
```javascript
[DEBUG] API Response: {message: "...", results: {...}}
[DEBUG] Stories count: 1  // Less than original 10
```

---

## 🐛 Troubleshooting

### Issue: Always does new search instead of refining

**Check:**
1. Conversation history is being sent in requests
2. Backend logs show "Found X previous results"
3. User query uses refinement keywords: "out of those", "from these", "which one"

**Fix:**
- Make sure to include conversation_history in API calls
- Session key depends on recent conversation history

### Issue: "No previous results available"

**Check:**
1. Initial search successfully stored results
2. Backend log shows: "Stored X stories in session context"

**Fix:**
- Ensure first query is a search action that returns results
- Context is stored per session based on conversation hash

### Issue: Refinement returns 0 results

**Possible causes:**
- Filter term doesn't match any story content
- Try broader keywords
- Check story titles in initial results

**Example:**
- ❌ "which mention xyz123abc" (unlikely to match)
- ✅ "which mention marketing" (common word)

---

## 📋 Quick Checklist

Test each of these patterns:

- [ ] "find X" → "out of those, show Y" (basic refinement)
- [ ] "search X" → "from these, which mention Z" (keyword filter)
- [ ] "get X stories" → "filter by Y" → "show Z" (multiple refinements)
- [ ] "find X" → "refine" → "now find Y" (new search after refine)
- [ ] Check backend logs show correct action types
- [ ] Verify story counts decrease during refinement
- [ ] Confirm new searches replace context

---

## 🎉 Success Criteria

All tests pass if:
- ✅ Refinement queries filter existing results (don't search again)
- ✅ Backend correctly identifies "search" vs "refine" actions
- ✅ Story counts match expectations
- ✅ Multiple refinements work in sequence
- ✅ New searches replace context appropriately
- ✅ No errors in backend logs or browser console

---

## 🚨 Known Patterns to Test

### Refinement Keywords (should trigger "refine")
- "out of those"
- "from these"
- "which one(s)"
- "filter by"
- "only the ones"
- "show me the"

### New Search Keywords (should trigger "search")
- "now find"
- "search for"
- "get me"
- "show articles about" (new topic)

---

## 📊 API Testing (curl)

### Test 1: Search + Refine
```bash
# Initial search
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find 10 marketing stories",
    "conversation_history": []
  }' > response1.json

# Check: Should have 10 stories
cat response1.json | jq '.results.stories | length'

# Refinement (include history)
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "out of those, which mention social media",
    "conversation_history": [
      {"role": "user", "content": "find 10 marketing stories"},
      {"role": "assistant", "content": "Here are 10 marketing stories"}
    ]
  }' > response2.json

# Check: Should have <= 10 stories (filtered)
cat response2.json | jq '.results.stories | length'
```

### Expected Results
```bash
# response1.json
10

# response2.json
3  # (or however many match "social media")
```

---

**Time to Complete:** 5-10 minutes  
**Complexity:** Medium  
**Status:** Feature Ready ✅