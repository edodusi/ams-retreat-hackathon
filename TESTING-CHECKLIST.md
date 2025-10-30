# Testing Checklist for Context-Aware Refinement Fix

## 🎯 Your Exact Test Case

### Queries to Test:
1. **"find the articles that mention the drupal migration"**
2. **"of those, get 2 articles that mention the CLI"**

---

## ✅ Pre-Test Setup

- [ ] Backend is running: `python -m uvicorn backend.main:app --reload`
- [ ] Frontend is open: `http://localhost:8000/frontend/index.html`
- [ ] Backend logs are visible in terminal
- [ ] Browser console is open (F12)

---

## 📋 Test Steps

### Step 1: Initial Search
- [ ] Type in chat: `find the articles that mention the drupal migration`
- [ ] Press Enter
- [ ] Wait for response

**Expected Results:**
- [ ] Story cards appear (should be ~10)
- [ ] Backend log shows: `>>> Session key: [some hash]`
- [ ] Backend log shows: `>>> Stored X stories in session '[hash]' for refinement`
- [ ] No errors in console

**If Step 1 Fails:**
- Check Storyblok connection
- Verify API credentials
- Try simpler query: "find marketing articles"

---

### Step 2: Refinement Query
- [ ] Type in chat: `of those, get 2 articles that mention the CLI`
- [ ] Press Enter
- [ ] Wait for response

**Expected Results:**
- [ ] Backend log shows: `>>> Session key: [SAME hash as Step 1]` ⚠️ CRITICAL!
- [ ] Backend log shows: `>>> Found X previous results in session context`
- [ ] Backend log shows: `>>> REFINING PREVIOUS RESULTS with filter: 'CLI'`
- [ ] Backend log shows: `>>> Filtered from X to Y stories`
- [ ] Story cards appear (fewer than Step 1, or 0 if no match)
- [ ] Message does NOT say "don't have access to previous results"

**If Step 2 Fails:**
- Check if session keys match (most important!)
- Verify conversation_history is being sent
- Check backend logs for error messages

---

## 🔍 Backend Log Verification

### What You Should See:

```
# Request 1
INFO: Received conversation request: 'find the articles that mention...'
INFO: >>> Session key: abc123def456...  ⬅️ Note this key
INFO: >>> Conversation history messages: 0
INFO: >>> No previous results found for session: abc123def456...
INFO: Claude response - Action: search, Term: drupal migration, Limit: 10
INFO: >>> PERFORMING SEARCH with term: 'drupal migration', limit: 10
INFO: >>> SEARCH RETURNED 10 stories (total: 10)
INFO: >>> Stored 10 stories in session 'abc123def456...' for refinement
INFO: >>> Session contexts now has 1 sessions

# Request 2
INFO: Received conversation request: 'of those, get 2 articles...'
INFO: >>> Session key: abc123def456...  ⬅️ MUST BE SAME AS ABOVE!
INFO: >>> Conversation history messages: 2
INFO: >>> Found 10 previous results in session context  ⬅️ KEY LINE!
INFO: Claude response - Action: refine, Filter: CLI, Limit: 2
INFO: >>> REFINING PREVIOUS RESULTS with filter: 'CLI'
INFO: >>> Current session key: abc123def456...
INFO: >>> Has previous results: True
INFO: >>> Filtering 10 stories for term: 'CLI'
INFO: >>> Filtered from 10 to X stories
INFO: >>> REFINEMENT SUCCESSFUL: Returning X filtered stories
```

---

## ❌ Common Issues & Solutions

### Issue 1: "don't have access to previous results"
**Cause:** Session keys don't match
**Check:**
- Compare session keys in logs from both requests
- Should be identical

**Debug:**
```bash
# In backend logs, look for:
grep "Session key:" [log_file]
# Both lines should show same hash
```

### Issue 2: Session key changes between requests
**Cause:** Fix didn't apply correctly
**Solution:**
```bash
# Verify the fix is in place
grep -A 3 "Use only the FIRST user message" backend/main.py
# Should show: user_messages[0]
```

### Issue 3: Action is "search" instead of "refine"
**Cause:** Claude didn't detect refinement intent
**Check:**
- User query must have refinement keywords: "of those", "from these", "which"
- Backend log shows: `Action: search` instead of `Action: refine`

**Try:**
- Use more explicit refinement language: "out of those stories..."
- Make sure first query returned results to refine

### Issue 4: 0 results after refinement
**Not a bug!** This means:
- Filter worked correctly
- No stories matched "CLI" in the previous results
- This is expected if the term doesn't appear in any stories

**To verify it's working:**
- Try a more common filter term: "content", "article", "blog"
- Should return some results

---

## 🎉 Success Criteria

All must be true for the fix to be working:

### Critical ✅
- [x] Session key is IDENTICAL in both requests
- [x] Backend says "Found X previous results in session context"
- [x] Action in Request 2 is "refine" (not "search")
- [x] NO message about "don't have access to previous results"

### Nice to Have ✅
- [x] Filtered results are subset of original
- [x] Filter respects the limit (2 articles)
- [x] Results contain the filter term if possible

---

## 🧪 Additional Test Cases

### Test 3: Multiple Refinements
```
1. "find marketing articles"
2. "of those, which mention social media"
3. "from those, show the one about Instagram"
```

**Expected:** Each refinement filters the previous set

### Test 4: New Search After Refinement
```
1. "find marketing articles"
2. "of those, show 5"
3. "now find technology articles"  ⬅️ Should be NEW search
```

**Expected:** Request 3 does NEW search, not refinement

### Test 5: No Results Available
```
1. "hello, how are you?"  ⬅️ No search
2. "of those, show me one"  ⬅️ Tries to refine
```

**Expected:** Message: "I don't have access to previous results. Please start with a search first."

---

## 📊 Quick Automated Test

Run this if manual testing is taking too long:

```bash
python3 test_context_fix.py
```

**Expected Output:**
```
============================================================
Testing Context-Aware Refinement Fix
============================================================

📤 Request 1: Initial search
✅ Response 1: 10 stories returned
   Message: Here are articles about drupal migration...
   First story: [Story Title]

📤 Request 2: Refinement query
✅ Response 2: 2 stories returned
   Message: Here are 2 articles that mention CLI...

✅ REFINEMENT SUCCESSFUL!
   Filtered from 10 to 2 stories
   1. [Story Title 1]
   2. [Story Title 2]

============================================================
Test Complete
============================================================
```

---

## 📝 Report Results

After testing, please report:

1. **Did it work?** Yes / No
2. **Session keys matched?** Yes / No  
3. **Found previous results?** Yes / No
4. **Any error messages?**
5. **Backend logs** (copy relevant lines)

---

**Next Steps:**
- [ ] Test with your exact queries
- [ ] Verify backend logs
- [ ] Try additional test cases
- [ ] Report results

Good luck! 🚀
