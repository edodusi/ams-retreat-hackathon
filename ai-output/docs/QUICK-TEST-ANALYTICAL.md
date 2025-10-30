# Quick Test Guide: Analytical Features

Fast testing guide for the new analytical and conversational features.

## Prerequisites

```bash
# Start the server
cd ams-retreat-hackathon
source venv/bin/activate
python -m uvicorn backend.main:app --reload
```

Server should be running at `http://localhost:8000`

---

## Quick Tests

### 1. Analytical Query (Count)

**Query:** "How many articles mention Drupal?"

**Expected:**
- Action: `analyze`
- Response: "I found X articles that mention Drupal. Would you like me to list them?"
- Analysis box showing count
- No results displayed yet

**cURL Test:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "how many articles mention drupal?",
    "conversation_history": []
  }'
```

---

### 2. List Analyzed Results

**Query:** "Yes please"

**Expected:**
- Action: `list_analyzed`
- Shows all previously analyzed results
- Story cards with content type badges

**cURL Test:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "yes please show them",
    "conversation_history": [
      {"role": "user", "content": "how many articles mention drupal?"},
      {"role": "assistant", "content": "I found 13 articles that mention Drupal. Would you like me to list them?"}
    ]
  }'
```

---

### 3. Content Type Filtering

**Query:** "Find 5 articles about React"

**Expected:**
- Action: `search`
- Content type: `article`
- Limit: 5
- Only articles returned

**cURL Test:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find 5 articles about react",
    "conversation_history": []
  }'
```

---

### 4. Clarification Request

**Query:** "Find stories about JavaScript"

**Expected:**
- Action: `clarify`
- Response: "What type of content are you looking for? Articles, blog posts, pages, or all types?"
- No results yet

**cURL Test:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find stories about javascript",
    "conversation_history": []
  }'
```

---

### 5. Search with Refinement

**Step 1 - Search:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find 10 articles about web development",
    "conversation_history": []
  }'
```

**Step 2 - Refine:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "from these, show me only the ones about React",
    "conversation_history": [
      {"role": "user", "content": "find 10 articles about web development"},
      {"role": "assistant", "content": "Here are the web development articles I found:"}
    ]
  }'
```

---

## UI Testing

### Open Browser
Navigate to: `http://localhost:8000/frontend/`

### Test Scenarios

**Scenario 1: Analytical Flow**
1. Type or speak: "How many blog posts mention Vue?"
2. Wait for count
3. Type or speak: "Yes show them"
4. Verify results display

**Scenario 2: Content Type**
1. Type: "Find 5 articles about marketing"
2. Check that content type badges show "article"
3. Verify only 5 results (or fewer if less available)

**Scenario 3: Clarification**
1. Type: "Find content about Node.js"
2. Wait for clarification question
3. Type: "Articles"
4. Verify articles are returned

---

## Automated Test Script

Run the comprehensive test script:

```bash
cd ams-retreat-hackathon
chmod +x test_analytical_features.sh
./test_analytical_features.sh
```

This runs 5+ test scenarios automatically.

---

## Unit Tests

```bash
source venv/bin/activate
python -m pytest tests/test_analytical_features.py -v
```

**Expected:** All 18 tests pass ✅

---

## Verification Checklist

- [ ] Analytical queries return count with confirmation question
- [ ] "Yes please" lists the analyzed results
- [ ] Content type badges appear on story cards
- [ ] Content type filtering works (e.g., "articles only")
- [ ] Clarification requests appear when needed
- [ ] Analysis box shows statistics before results
- [ ] Refinement works on previous results
- [ ] Session context preserved across turns
- [ ] All unit tests pass

---

## Troubleshooting

### No Results Found
- Try broader search terms
- Check if content exists in your Storyblok space
- Verify API credentials are correct

### Content Type Not Shown
- Full story details needed for content_type
- Check Storyblok API response includes content_type field

### Analysis Not Stored
- Verify conversation history includes first message
- Check session key generation in logs
- Look for ">>> Stored X stories in session" log message

### Wrong Action Type
- Check Claude's response parsing in logs
- Verify system prompt is being used
- Look for JSON parsing errors

---

## Expected Log Messages

```
>>> Session key: abc123def456
>>> ANALYZING with term: 'drupal', type: 'article'
>>> ANALYSIS FOUND 13 stories
>>> Stored 13 stories in session 'abc123def456' for refinement
>>> ANALYSIS COMPLETE: 13 results stored for potential listing
```

---

## Quick Debugging

### Enable Debug Logs
Check `backend/main.py` log level is set to INFO:
```python
logging.basicConfig(level=logging.INFO)
```

### Check Response Structure
```bash
curl http://localhost:8000/api/conversation \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "how many articles?", "conversation_history": []}' \
  | jq '.'
```

Look for:
- `action` field
- `analysis` object (if analyze action)
- `results` array (if search/list action)

---

## Success Indicators

✅ Analysis shows count before listing  
✅ Content type badges visible  
✅ Clarification questions appear  
✅ "Yes please" triggers listing  
✅ Refinement filters results  
✅ All tests pass  

---

**Total Test Time:** ~5 minutes  
**Test Coverage:** All major features  

Happy testing! 🚀