# Testing Guide: Story Display Fix

## Overview
This guide helps you verify that the story display fix is working correctly in the Storyblok Voice Assistant.

## Quick Test

### 1. Start the Application
```bash
# Terminal 1: Start backend
cd /Users/edodusi/Storyblok/ams-retreat-hackathon
python -m uvicorn backend.main:app --reload

# Terminal 2: Open frontend
open http://localhost:8000/frontend/index.html
```

### 2. Perform a Search Query
1. Open the browser console (F12 or Cmd+Option+I)
2. In the Voice Assistant interface, type or speak: "Find stories about marketing"
3. Press Enter or click the send button

### 3. Verify Display
**Expected Results:**
- ✅ Text response from the assistant appears
- ✅ Story preview cards appear below the text response
- ✅ Each card shows:
  - Story title (bold)
  - Body preview (truncated to 200 chars)
  - Slug and Story ID at the bottom
- ✅ Debug indicator shows: `[Debug: Results object exists, stories count: X]`

**If Stories Don't Appear:**
- Check browser console for `[DEBUG]` messages
- Verify `Has results?` is `true`
- Verify `Stories is array?` is `true`
- Verify `Stories length:` is greater than 0

## Detailed Console Debugging

When you make a search request, you should see these console messages:

```
[DEBUG] API Response: {message: "...", results: {...}}
[DEBUG] Has results? true
[DEBUG] Stories count: 2
[DEBUG] First story: {body: "...", cursor: 1, name: "...", ...}
[DEBUG] Pushing message to array: {role: "assistant", content: "...", results: {...}}
[DEBUG] Has results in message? true
[DEBUG] Has stories in results? true
[DEBUG] Stories is array? true
[DEBUG] Stories length: 2
[DEBUG] First story structure: {body: "...", cursor: 1, ...}
[DEBUG] Messages array length: 2
[DEBUG] Last message: {role: "assistant", content: "...", results: {...}}
[DEBUG] Last message has results? true
[DEBUG] Last message stories count: 2
```

## Backend Logs

Check the backend logs for search operations:

```
INFO:backend.main:>>> PERFORMING SEARCH with term: 'marketing'
INFO:backend.storyblok_client:Searching Storyblok for: 'marketing' (limit=10, offset=0)
INFO:backend.main:>>> SEARCH RETURNED 2 stories (total: 2)
INFO:backend.main:>>> RESULTS ATTACHED TO RESPONSE: 2 stories
INFO:backend.main:>>> SUCCESS: Found 2 results with full previews
INFO:backend.main:>>> FINAL RESPONSE: message length=45, has_results=True
INFO:backend.main:>>> RETURNING 2 stories in response
INFO:backend.main:>>> Serialized response keys: dict_keys(['message', 'results', 'conversation_id'])
INFO:backend.main:>>> Serialized results keys: dict_keys(['stories', 'total'])
INFO:backend.main:>>> Serialized stories count: 2
```

## Standalone Alpine.js Test

To test the template logic in isolation:

```bash
open tests/test-alpine-stories.html
```

**Test Actions:**
1. Click "Load Test Data (2 stories)" - should display 2 story cards
2. Click "Load Empty Results" - should show "No stories found"
3. Click "Load No Results (null)" - should show only message, no story section
4. Check Debug Info section for live reactive state

## Common Issues and Solutions

### Issue: Stories in console but not on screen
**Solution:** Already fixed! The template now uses:
- `x-if` instead of `x-show` for better reactivity
- Explicit `Array.isArray()` check
- Normalized data structure when pushing to messages array

### Issue: Debug indicator shows 0 stories but backend returns data
**Symptoms:**
- Console shows `[DEBUG] Stories count: 2` from API
- But shows `stories count: 0` in the message
- Debug indicator shows `[Debug: ... stories count: 0]`

**Diagnosis:**
```javascript
// Check in console:
console.log(app.messages[app.messages.length - 1].results.stories);
// Should return an array, not undefined
```

**Solution:** Check that the data structure is properly normalized when adding the message (line 517-522 in index.html).

### Issue: Template condition fails
**Symptoms:**
- Data is present but cards don't render
- No visible errors in console

**Check:**
```javascript
// In browser console, check the last message:
let lastMsg = app.messages[app.messages.length - 1];
console.log('Has results:', !!lastMsg.results);
console.log('Is array:', Array.isArray(lastMsg.results?.stories));
console.log('Has length:', lastMsg.results?.stories?.length > 0);
```

All three should be `true` for stories to display.

## Testing Different Scenarios

### Test 1: Successful Search
**Query:** "Find marketing articles"
**Expected:** Text response + story cards

### Test 2: No Results Found
**Query:** "asdfqwerzxcv123456"
**Expected:** Text response + message about no results

### Test 3: Conversation Without Search
**Query:** "Hello, how are you?"
**Expected:** Text response only, no story section

### Test 4: Refinement Query
1. First: "Find blog posts"
2. Then: "Show only recent ones"
**Expected:** Each response shows updated story cards

## Manual API Test

Test the backend endpoint directly:

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find stories about marketing",
    "conversation_history": []
  }' | jq
```

**Verify JSON Structure:**
```json
{
  "message": "I found several stories about marketing...",
  "results": {
    "stories": [
      {
        "body": "...",
        "cursor": 1,
        "name": "Story Title",
        "slug": "story-slug",
        "story_id": 12345,
        "full_story": null
      }
    ],
    "total": 1
  },
  "conversation_id": null
}
```

## Success Criteria

All of the following should be true:
- [ ] Story cards appear visually in the UI
- [ ] Debug indicator shows correct story count
- [ ] Console logs show proper data flow
- [ ] Backend logs confirm stories were returned
- [ ] Standalone test file works correctly
- [ ] Multiple searches show updated results each time
- [ ] Empty results handled gracefully
- [ ] Chat-only messages (no search) work without errors

## Performance Check

**Response Time:**
- Search query → Assistant response: < 3 seconds
- Story cards appear: Immediately with response
- No flickering or delayed rendering

**Memory:**
- No memory leaks after 10+ searches
- Console errors: 0
- Messages array grows appropriately

## Accessibility Check

With screen reader enabled:
- [ ] Story cards are announced as "article"
- [ ] Each card has proper aria-label with story name
- [ ] Region labeled as "Search results"
- [ ] Keyboard navigation works (Tab through cards)

---

**Last Updated:** 2025-01-XX  
**Related Files:**
- `frontend/index.html` - Main implementation
- `tests/test-alpine-stories.html` - Standalone test
- `docs/story-display-fix.md` - Technical documentation