# Dynamic Limit Feature: Visual Examples

## Overview
This document provides visual examples of how the dynamic limit feature works in the Storyblok Voice Assistant.

---

## Example 1: Request Specific Number (5 Results)

### User Input
```
"Find the first 5 articles about marketing"
```

### System Processing
```
┌─────────────────────────────────────────────┐
│ 1. User Query → Claude AI                   │
│    "Find the first 5 articles about         │
│     marketing"                              │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│ 2. Claude Extracts:                         │
│    • action: "search"                       │
│    • term: "marketing articles"             │
│    • limit: 5  ◄─── EXTRACTED!              │
│    • response: "Here are 5 marketing..."    │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│ 3. Backend calls Storyblok:                 │
│    search(term="marketing", limit=5)        │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│ 4. Returns exactly 5 stories                │
└─────────────────────────────────────────────┘
```

### UI Display
```
┌───────────────────────────────────────────────────────┐
│ 🤖 Assistant                                          │
│                                                       │
│ Here are 5 marketing articles:                        │
│                                                       │
│ [Debug: Results object exists, stories count: 5]     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Marketing Strategy 2025                      │     │
│ │ A comprehensive guide to modern marketing... │     │
│ │ /blog/marketing-strategy-2025  ID: 12345    │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Social Media Best Practices                  │     │
│ │ Learn how to maximize your social media...   │     │
│ │ /blog/social-media  ID: 12346                │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Content Marketing Fundamentals               │     │
│ │ Essential tips for creating engaging...      │     │
│ │ /blog/content-marketing  ID: 12347           │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ AI in Marketing                              │     │
│ │ Exploring the future of AI-powered...        │     │
│ │ /blog/ai-marketing  ID: 12348                │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Marketing Analytics Guide                    │     │
│ │ How to measure your marketing ROI...         │     │
│ │ /blog/marketing-analytics  ID: 12349         │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Result:** ✅ Exactly 5 story cards displayed

---

## Example 2: Different Pattern - "Show me 3"

### User Input
```
"Show me 3 blog posts about technology"
```

### Claude's Response
```json
{
  "action": "search",
  "term": "blog posts technology",
  "limit": 3,
  "response": "Here are 3 blog posts about technology:"
}
```

### UI Display
```
┌───────────────────────────────────────────────────────┐
│ 🤖 Assistant                                          │
│                                                       │
│ Here are 3 blog posts about technology:               │
│                                                       │
│ [Debug: Results object exists, stories count: 3]     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Future of AI Development                     │     │
│ │ Exploring emerging trends in artificial...   │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Cloud Computing Guide                        │     │
│ │ A complete guide to modern cloud...          │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Cybersecurity Best Practices                 │     │
│ │ Protect your systems with these...           │     │
│ └─────────────────────────────────────────────┘     │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Result:** ✅ Exactly 3 story cards displayed

---

## Example 3: Default Behavior (No Limit Specified)

### User Input
```
"Find marketing articles"
```

### Claude's Response
```json
{
  "action": "search",
  "term": "marketing",
  "limit": 10,
  "response": "Here are the marketing articles I found:"
}
```

### Backend Behavior
- No explicit number in query
- Claude defaults to `limit: 10`
- Returns up to 10 results

### UI Display
```
┌───────────────────────────────────────────────────────┐
│ 🤖 Assistant                                          │
│                                                       │
│ Here are the marketing articles I found:              │
│                                                       │
│ [Debug: Results object exists, stories count: 10]    │
│                                                       │
│ ┌─────────────────────────────────────────────┐     │
│ │ Story 1                                      │     │
│ └─────────────────────────────────────────────┘     │
│ ┌─────────────────────────────────────────────┐     │
│ │ Story 2                                      │     │
│ └─────────────────────────────────────────────┘     │
│ ┌─────────────────────────────────────────────┐     │
│ │ Story 3                                      │     │
│ └─────────────────────────────────────────────┘     │
│           ... (7 more cards) ...                      │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Result:** ✅ Up to 10 story cards displayed (default)

---

## Example 4: Conversational Refinement

### Turn 1
**User:** "Find marketing articles"
**System:** Returns 10 results (default)

### Turn 2
**User:** "Show me only the first 3"
**System:** 
- Understands context (still about marketing)
- Extracts new limit: 3
- Returns 3 results

```
Conversation Flow:

┌─────────────────────────────────────────┐
│ 👤 You                                  │
│ Find marketing articles                 │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 🤖 Assistant                            │
│ Here are marketing articles:            │
│ [10 story cards displayed]              │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 👤 You                                  │
│ Show me only the first 3                │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ 🤖 Assistant                            │
│ Here are 3 marketing articles:          │
│ [3 story cards displayed]               │
└─────────────────────────────────────────┘
```

**Result:** ✅ Limit updates based on conversation

---

## Supported Patterns Reference

| Pattern | Example | Extracted Limit |
|---------|---------|-----------------|
| **first X** | "find the first 5 articles" | 5 |
| **show me X** | "show me 8 stories" | 8 |
| **get X** | "get 15 blog posts" | 15 |
| **X items** | "I need 12 items" | 12 |
| **top X** | "show the top 3" | 3 |
| **X results** | "give me 7 results" | 7 |
| **X stories** | "find 20 stories" | 20 |
| **X articles** | "show 6 articles" | 6 |
| **X posts** | "get 4 posts" | 4 |
| **No number** | "find marketing content" | 10 (default) |

---

## Backend Log Examples

### Successful Limit Extraction
```
INFO:backend.main:Claude response - Action: search, Term: marketing, Limit: 5
INFO:backend.main:>>> PERFORMING SEARCH with term: 'marketing', limit: 5
INFO:backend.storyblok_client:Searching Storyblok for: 'marketing' (limit=5, offset=0)
INFO:backend.main:>>> SEARCH RETURNED 5 stories (total: 5)
INFO:backend.main:>>> RESULTS ATTACHED TO RESPONSE: 5 stories
```

### Default Limit Applied
```
INFO:backend.main:Claude response - Action: search, Term: technology, Limit: 10
INFO:backend.main:>>> PERFORMING SEARCH with term: 'technology', limit: 10
INFO:backend.storyblok_client:Searching Storyblok for: 'technology' (limit=10, offset=0)
INFO:backend.main:>>> SEARCH RETURNED 10 stories (total: 10)
```

---

## Browser Console Output

### With Limit Extraction
```javascript
[DEBUG] API Response: {message: "Here are 5...", results: {...}}
[DEBUG] Has results? true
[DEBUG] Stories count: 5
[DEBUG] First story: {body: "...", name: "Marketing Strategy 2025", ...}
[DEBUG] Pushing message to array: {role: "assistant", ...}
[DEBUG] Stories is array? true
[DEBUG] Stories length: 5
[DEBUG] Messages array length: 2
[DEBUG] Last message stories count: 5
```

---

## Edge Cases

### Case 1: Single Result
**Input:** "Find 1 article about productivity"
**Output:** Exactly 1 story card
**Limit:** 1

### Case 2: Large Number
**Input:** "Get 100 stories"
**Output:** Up to 100 results (or maximum available)
**Limit:** 100
**Note:** May be capped by API or configuration

### Case 3: Zero Results Available
**Input:** "Find the first 10 articles about xyzabc123"
**Output:** "I couldn't find any matching content..."
**Limit:** 10 (requested, but 0 available)

---

## Before vs After Feature Implementation

### ❌ Before (Old Behavior)
```
User: "Find the first 5 articles about marketing"
System: Returns 10 results (ignored user's "5")
Issue: User request not respected
```

### ✅ After (New Behavior)
```
User: "Find the first 5 articles about marketing"
System: Returns exactly 5 results
Result: User intent understood and fulfilled
```

---

## Testing Quick Reference

### Test Command
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "find the first 5 articles about marketing", "conversation_history": []}' \
  | jq '.results.stories | length'
```

### Expected Output
```
5
```

### Verification Checklist
- [ ] Backend log shows: `Limit: 5`
- [ ] API returns 5 stories
- [ ] Frontend displays 5 cards
- [ ] Debug indicator shows: `stories count: 5`
- [ ] Console shows: `Stories length: 5`

---

**Feature Status:** ✅ Implemented and Tested  
**Documentation:** Complete  
**Last Updated:** 2025-01-XX