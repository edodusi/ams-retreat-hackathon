# Dynamic Result Limit Feature

## Overview
The Storyblok Voice Assistant now intelligently extracts the number of results requested by users from their natural language queries. Instead of always returning 10 results, the system understands phrases like "first 5 articles" or "show me 3 posts" and limits results accordingly.

## Feature Description

### Problem
Previously, all searches returned a fixed number of results (default: 10), regardless of what the user actually requested. If a user asked for "the first 5 marketing articles," they would still receive 10 results.

### Solution
The AI model (Claude) now:
1. Analyzes the user's query for numerical indicators
2. Extracts the desired result limit
3. Passes this limit to the Storyblok search API
4. Returns exactly the number of results requested

## Usage Examples

### Explicit Limits

#### Example 1: Specific Number
**User Query:** "find the first 5 articles about marketing"

**System Behavior:**
- Extracts search term: "marketing articles"
- Extracts limit: 5
- Returns exactly 5 results

#### Example 2: Show Me Pattern
**User Query:** "show me 3 blog posts about technology"

**System Behavior:**
- Extracts search term: "blog posts technology"
- Extracts limit: 3
- Returns exactly 3 results

#### Example 3: Get Pattern
**User Query:** "get 20 stories about design"

**System Behavior:**
- Extracts search term: "stories design"
- Extracts limit: 20
- Returns exactly 20 results

#### Example 4: Top N Pattern
**User Query:** "show me the top 7 posts about AI"

**System Behavior:**
- Extracts search term: "posts AI"
- Extracts limit: 7
- Returns exactly 7 results

### Default Behavior

**User Query:** "find marketing articles"

**System Behavior:**
- Extracts search term: "marketing articles"
- No explicit limit found
- Defaults to limit: 10
- Returns up to 10 results

## Supported Patterns

The system recognizes various ways users express result limits:

| Pattern | Example Query | Extracted Limit |
|---------|--------------|-----------------|
| "first X" | "find the first 5 articles" | 5 |
| "show me X" | "show me 8 stories" | 8 |
| "get X" | "get 15 blog posts" | 15 |
| "X items" | "I need 12 items about tech" | 12 |
| "top X" | "show the top 3 results" | 3 |
| "X results" | "give me 7 results" | 7 |
| No number | "find marketing posts" | 10 (default) |

## Technical Implementation

### Architecture Flow

```
User Query
    ↓
Claude AI (Bedrock)
    ↓
Extract: {term, limit, action}
    ↓
Backend API (main.py)
    ↓
Storyblok Client
    ↓
Storyblok Strata API (with limit param)
    ↓
Return N results
```

### Code Changes

#### 1. Bedrock Client (`backend/bedrock_client.py`)

**Updated System Prompt:**
```python
"""
When a user asks to search for content:
1. Extract the key search terms from their query
2. Extract the number of results if specified
3. Return JSON: {"action": "search", "term": "...", "limit": 10, "response": "..."}

Examples:
- "find all marketing stories" 
  → {"action": "search", "term": "marketing", "limit": 10, ...}
  
- "find the first 5 articles about marketing" 
  → {"action": "search", "term": "marketing articles", "limit": 5, ...}
"""
```

**Response Structure:**
```python
{
    "action": "search",
    "term": "marketing",
    "limit": 5,  # NEW: extracted from user query
    "response": "Here are 5 marketing articles:"
}
```

#### 2. Main API (`backend/main.py`)

**Extract and Use Limit:**
```python
search_term = claude_response.get("term")
search_limit = claude_response.get("limit", 10)  # Default to 10

logger.info(f"Search with term: '{search_term}', limit: {search_limit}")

search_results = await storyblok_client.search(
    term=search_term, 
    limit=search_limit  # Pass extracted limit
)
```

#### 3. Storyblok Client (`backend/storyblok_client.py`)

No changes needed - already supports `limit` parameter:
```python
async def search(
    self,
    term: str,
    limit: Optional[int] = None,  # Already supported
    offset: int = 0
) -> SearchResults:
```

## Configuration

### Default Limit
The default limit (when user doesn't specify) is **10 results**.

To change the default, modify the system prompt in `backend/bedrock_client.py`:
```python
# Change "limit": 10 to your desired default
{"action": "search", "term": "...", "limit": 10, "response": "..."}
```

Or update the fallback in `backend/main.py`:
```python
search_limit = claude_response.get("limit", 10)  # Change 10 to your default
```

### Maximum Limit
The Storyblok API may have its own maximum limit. Check the API documentation or implement validation:

```python
# In backend/main.py
MAX_LIMIT = 50
search_limit = min(claude_response.get("limit", 10), MAX_LIMIT)
```

## Testing

### Manual Testing

1. **Start the application:**
```bash
python -m uvicorn backend.main:app --reload
```

2. **Test various queries:**

| Test Case | Query | Expected Limit |
|-----------|-------|----------------|
| Explicit 5 | "find the first 5 articles about marketing" | 5 |
| Explicit 3 | "show me 3 blog posts" | 3 |
| Explicit 20 | "get 20 stories" | 20 |
| Default | "find marketing articles" | 10 |
| Single | "find 1 article about AI" | 1 |

3. **Verify in logs:**
```
INFO:backend.main:Claude response - Action: search, Term: marketing, Limit: 5
INFO:backend.main:>>> PERFORMING SEARCH with term: 'marketing', limit: 5
INFO:backend.main:>>> SEARCH RETURNED 5 stories (total: 5)
```

4. **Verify in UI:**
- Story cards displayed should match requested limit
- Debug indicator shows correct count

### Automated Testing

Run the test suite:
```bash
pytest tests/test_limit_extraction.py -v
```

**Test Coverage:**
- ✅ Explicit limit extraction (5, 3, 20, etc.)
- ✅ Default limit when not specified
- ✅ Various patterns (first, show me, get, top)
- ✅ Edge cases (1 result, large numbers)

### API Testing with curl

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find the first 5 articles about marketing",
    "conversation_history": []
  }' | jq '.results.stories | length'
```

**Expected output:** `5`

## Debugging

### Check Claude's Response

Enable debug logging to see what Claude extracts:
```python
logger.info(f"Raw Claude response: {claude_response}")
```

Look for:
```json
{
  "action": "search",
  "term": "marketing",
  "limit": 5,  ← Should match user's request
  "response": "Here are 5 marketing articles:"
}
```

### Common Issues

#### Issue: Always Returns 10 Results
**Symptoms:** Limit extraction not working

**Diagnosis:**
1. Check backend logs for: `Limit: X`
2. If always shows `Limit: 10`, Claude may not be extracting correctly

**Solution:**
- Ensure Bedrock client has updated system prompt
- Check that Claude is returning valid JSON with limit field
- Verify `search_limit` is being passed to `storyblok_client.search()`

#### Issue: Limit Not in Claude Response
**Symptoms:** KeyError or missing 'limit' in response

**Diagnosis:**
```python
# In backend/bedrock_client.py, line ~181
logger.info(f"Parsed response: {parsed_response}")
# Check if 'limit' key exists
```

**Solution:**
- System prompt may not be clear enough
- Add fallback: `parsed_response.get("limit", 10)`

## Conversational Refinement

The limit feature also works in multi-turn conversations:

**Turn 1:**
- User: "find marketing articles"
- System: Returns 10 results (default)

**Turn 2:**
- User: "show me only the first 3"
- System: Returns 3 results with same search term

**Turn 3:**
- User: "actually, give me 7"
- System: Returns 7 results

The AI maintains context and understands refinement requests.

## Accessibility Considerations

### Voice Input
The feature works seamlessly with voice input:
- "Find the first five articles" → Recognized as limit: 5
- "Show me three posts" → Recognized as limit: 3

### Screen Readers
- Story count is announced correctly
- Debug indicator shows actual count: "Results object exists, stories count: 5"

## Future Enhancements

### Potential Improvements
1. **Pagination:** "Show me the next 5 results"
2. **Ranges:** "Show me results 5 to 10"
3. **Relative limits:** "Show me fewer results" (reduce by 50%)
4. **Smart defaults:** Learn user's preferred limit over time

### API Rate Limiting
Consider implementing:
```python
# Prevent abuse with very large limits
if search_limit > 100:
    search_limit = 100
    logger.warning(f"Limit capped at 100 (requested: {search_limit})")
```

## Related Files
- `backend/bedrock_client.py` - AI model integration and limit extraction
- `backend/main.py` - API endpoint using the limit
- `backend/storyblok_client.py` - Search with limit parameter
- `tests/test_limit_extraction.py` - Automated tests

---

**Date:** 2025-01-XX  
**Status:** Implemented  
**Priority:** Medium (user experience enhancement)