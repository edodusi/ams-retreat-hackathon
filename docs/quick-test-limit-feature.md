# Quick Test Guide: Dynamic Result Limit Feature

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd /Users/edodusi/Storyblok/ams-retreat-hackathon
python -m uvicorn backend.main:app --reload
```

### 2. Open the Frontend
```bash
open http://localhost:8000/frontend/index.html
```

## ✅ Test Cases

### Test 1: Request 5 Results
**Input:** "Find the first 5 articles about marketing"

**Expected:**
- ✅ Shows exactly 5 story cards
- ✅ Debug indicator: `[Debug: Results object exists, stories count: 5]`
- ✅ Backend log: `>>> PERFORMING SEARCH with term: 'marketing', limit: 5`

---

### Test 2: Request 3 Results
**Input:** "Show me 3 blog posts about technology"

**Expected:**
- ✅ Shows exactly 3 story cards
- ✅ Debug indicator shows count: 3
- ✅ Backend log: `limit: 3`

---

### Test 3: Default Behavior (10 results)
**Input:** "Find marketing articles"

**Expected:**
- ✅ Shows up to 10 story cards
- ✅ Backend log: `limit: 10`
- ✅ Default applies when no number specified

---

### Test 4: Different Patterns
Try these variations:

| Input | Expected Limit |
|-------|----------------|
| "Get 20 stories about design" | 20 |
| "Show the top 7 posts" | 7 |
| "I need 15 blog posts" | 15 |
| "Find 1 article about AI" | 1 |

---

## 🔍 Verification Checklist

### Frontend
- [ ] Correct number of story cards appear
- [ ] Debug indicator shows matching count
- [ ] Console shows: `[DEBUG] Stories length: X`

### Backend Logs
Look for these lines:
```
INFO:backend.main:Claude response - Action: search, Term: marketing, Limit: 5
INFO:backend.main:>>> PERFORMING SEARCH with term: 'marketing', limit: 5
INFO:backend.main:>>> SEARCH RETURNED 5 stories (total: 5)
```

### Browser Console
```
[DEBUG] API Response: {...}
[DEBUG] Stories count: 5
[DEBUG] Stories length: 5
```

## 🧪 API Test (curl)

### Test with 5 results:
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find the first 5 articles about marketing",
    "conversation_history": []
  }' | jq '.results.stories | length'
```

**Expected output:** `5`

### Test default (10 results):
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find marketing articles",
    "conversation_history": []
  }' | jq '.results.stories | length'
```

**Expected output:** `10` (or less if fewer available)

## ⚠️ Troubleshooting

### Issue: Always returns 10 results
**Check:**
1. Backend logs show `Limit: 10` even for "first 5" query?
2. Restart backend to reload changes
3. Verify bedrock_client.py has updated system prompt

### Issue: Wrong number of results
**Check:**
1. Storyblok might have fewer results than requested
2. Look at backend log: `>>> SEARCH RETURNED X stories`
3. This is normal - API returns what's available

### Issue: Error in Claude response
**Check:**
1. Backend logs for JSON parsing errors
2. Claude might not have returned proper JSON
3. Should fallback to default limit: 10

## 📊 Success Criteria

- ✅ "first 5" returns 5 results
- ✅ "show me 3" returns 3 results
- ✅ No explicit number returns 10 (default)
- ✅ Backend logs show correct limit
- ✅ Frontend displays correct count
- ✅ No errors in console

## 🎯 Multi-turn Conversation Test

**Turn 1:** "Find marketing articles"
- Returns: 10 results

**Turn 2:** "Show me only the first 3"
- Returns: 3 results

**Turn 3:** "Actually, give me 7"
- Returns: 7 results

Each refinement should update the result count.

---

**Time to test:** ~5 minutes  
**Status:** Feature implemented ✓