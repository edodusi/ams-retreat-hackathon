# Quick Start: Test the Context Fix NOW

## ⚡ 3-Step Test (Takes 2 Minutes)

### Step 1: Start Backend
```bash
cd /Users/edodusi/Storyblok/ams-retreat-hackathon
python -m uvicorn backend.main:app --reload
```

### Step 2: Open Frontend
```bash
open http://localhost:8000/frontend/index.html
```

### Step 3: Test Your Exact Queries
```
1. Type: find the articles that mention the drupal migration
   [Press Enter, wait for results]

2. Type: of those, get 2 articles that mention the CLI
   [Press Enter]
```

---

## ✅ What You Should See

### ✅ SUCCESS = Both of these:
1. **Story cards appear** (filtered results)
2. **NO error message** about "don't have access to previous results"

### ❌ FAILURE = Either of these:
1. Error message: "I don't have access to previous results"
2. New search instead of filtering

---

## 🔍 Check Backend Logs

Look for this pattern:
```
Request 1:
>>> Session key: abc123...
>>> Stored 10 stories in session 'abc123...'

Request 2:
>>> Session key: abc123...  ← SAME KEY = GOOD!
>>> Found 10 previous results  ← FOUND = GOOD!
>>> REFINING PREVIOUS RESULTS
```

**Critical:** Session keys MUST match!

---

## 🎯 Expected Results

**Query 1:** "find the articles that mention the drupal migration"
- Returns ~10 articles about Drupal migration
- Backend stores them in session

**Query 2:** "of those, get 2 articles that mention the CLI"
- Returns 1-2 articles (or 0 if "CLI" not in any)
- Backend filters from the cached 10 articles
- NO new search performed

---

## 📊 Alternative: Run Automated Test

```bash
python3 test_context_fix.py
```

**Expected Output:**
```
✅ Response 1: 10 stories returned
✅ Response 2: 2 stories returned
✅ REFINEMENT SUCCESSFUL!
```

---

## 🐛 If It Fails

1. **Check session keys in logs** - must be identical
2. **Restart backend** - ensure latest code is loaded
3. **Verify fix applied:**
   ```bash
   grep "user_messages\[0\]" backend/main.py
   ```
   Should return a match

4. **Report:** Copy backend logs and describe what happened

---

## 📝 Report Format

After testing, reply with:

```
✅ IT WORKS! / ❌ IT FAILED

Session keys matched: YES / NO
Found previous results: YES / NO
Got filtered results: YES / NO

[Paste backend logs here if failed]
```

---

**Time Required:** 2 minutes
**Ready to test!** 🚀
