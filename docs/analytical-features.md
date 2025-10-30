# Analytical and Conversational Features

This document describes the analytical capabilities and conversational enhancements added to the Storyblok Voice Assistant.

## Overview

The assistant now supports:
- **Content type detection and clarification**
- **Analytical queries** (counting, pattern detection)
- **Conversational analysis flow** (analyze → confirm → list)
- **Smart filtering by content type**

---

## Features

### 1. Content Type Awareness

The assistant now understands and filters by Storyblok content types.

#### Supported Content Types
- `article` - News articles, blog articles
- `blog_post` - Blog posts
- `page` - Regular pages
- `landing_page` - Landing pages
- `post` - Generic posts
- Any custom content type in your Storyblok space

#### Examples
```
User: "Find 5 articles about marketing"
Assistant: [Searches for marketing content, filters to articles only]

User: "Show me blog posts about React"
Assistant: [Returns only blog_post content type]

User: "Find pages about our company"
Assistant: [Returns only page content type]
```

---

### 2. Clarification Requests

When a query is ambiguous, the assistant asks for clarification.

#### When Clarification Happens
- Content type is not specified or unclear
- User says "stories" without specifying the type
- Multiple interpretations are possible

#### Examples
```
User: "Find stories about marketing"
Assistant: "What type of content are you looking for? Articles, blog posts, pages, or all types?"

User: "Articles please"
Assistant: [Proceeds with article search]
```

---

### 3. Analytical Queries

The assistant can **analyze** content without immediately showing all results.

#### Action Type: `analyze`

Performs a search but presents results as analysis/statistics first.

#### Use Cases
- Counting items
- Checking if content exists
- Getting an overview before diving in

#### Examples

**Example 1: Counting**
```
User: "How many articles mention Drupal?"
Assistant: "I found 13 articles that mention Drupal. Would you like me to list them?"

User: "Yes please"
Assistant: [Shows all 13 articles with previews]
```

**Example 2: Existence Check**
```
User: "Do we have any blog posts about React?"
Assistant: "I found 8 blog posts that mention React. Would you like me to list them?"

User: "Yes"
Assistant: [Shows the 8 blog posts]
```

**Example 3: Content Type Filtering**
```
User: "How many pages mention AI?"
Assistant: "I found 5 pages that mention AI. Would you like me to list them?"

User: "Show them"
Assistant: [Displays the 5 pages]
```

---

### 4. Conversational Flow

The system maintains context across multiple turns for natural conversation.

#### Multi-Turn Examples

**Scenario 1: Analysis → List**
```
Turn 1:
User: "How many articles mention GraphQL?"
Assistant: "I found 7 articles that mention GraphQL. Would you like me to list them?"

Turn 2:
User: "Yes please"
Assistant: "Here are the articles:" [Shows 7 articles]

Turn 3:
User: "Out of those, which ones mention TypeScript?"
Assistant: "Here are the articles that mention TypeScript:" [Shows filtered subset]
```

**Scenario 2: Search → Refine**
```
Turn 1:
User: "Find 10 marketing articles"
Assistant: [Shows 10 marketing articles]

Turn 2:
User: "From these, show only the ones about social media"
Assistant: [Shows filtered articles about social media]
```

**Scenario 3: Clarify → Search**
```
Turn 1:
User: "Find content about Next.js"
Assistant: "What type of content are you looking for? Articles, blog posts, pages, or all types?"

Turn 2:
User: "Blog posts"
Assistant: [Shows blog posts about Next.js]
```

---

## API Response Structure

### Analysis Response

When `action: "analyze"` is performed:

```json
{
  "message": "I found 13 articles that mention Drupal. Would you like me to list them?",
  "action": "analyze",
  "results": null,
  "analysis": {
    "description": "Analyzed drupal (article)",
    "count": 13,
    "search_term": "drupal",
    "content_type": "article",
    "analysis_type": "count"
  }
}
```

### List Response

When user confirms listing (`action: "list_analyzed"`):

```json
{
  "message": "Here are the articles:",
  "action": "list_analyzed",
  "results": {
    "stories": [
      {
        "story_id": 123,
        "name": "Getting Started with Drupal",
        "slug": "getting-started-drupal",
        "body": "...",
        "content_type": "article",
        "full_story": { ... }
      }
    ],
    "total": 13
  },
  "analysis": null
}
```

---

## Frontend Display

### Analysis Display

The frontend shows analysis results in a blue info box:

```
┌─────────────────────────────────────┐
│ 📊 Analysis Results                 │
│ 13 articles                         │
│ Matching: drupal                    │
└─────────────────────────────────────┘
```

### Story Cards

Each story now displays:
- **Title** (large, bold)
- **Content Type Badge** (if available) - purple badge showing type
- **Body Preview** (truncated to 200 chars)
- **Full Story Preview** (if fetched from API)
- **Metadata** (slug, story ID)

---

## Action Types

The system now supports these action types:

| Action | Description | Triggers Results | Triggers Analysis |
|--------|-------------|------------------|-------------------|
| `search` | Search for new content | ✅ Yes | ❌ No |
| `analyze` | Analyze content (count) | ❌ No | ✅ Yes |
| `list_analyzed` | List previously analyzed results | ✅ Yes | ❌ No |
| `refine` | Filter previous results | ✅ Yes | ❌ No |
| `clarify` | Ask for clarification | ❌ No | ❌ No |
| `chat` | General conversation | ❌ No | ❌ No |

---

## Session Management

### Context Storage

The system maintains three types of context per session:

1. **`conversation_contexts`** - Stores previous search results for refinement
2. **`conversation_analyses`** - Stores analysis data for follow-up listing
3. **Session key** - Stable hash based on first user message

### Context Lifecycle

```
1. User asks analytical question
   → System performs search
   → Results stored in conversation_contexts
   → Analysis data stored in conversation_analyses

2. User confirms listing
   → System retrieves from conversation_contexts
   → Displays stored results

3. User refines results
   → System filters conversation_contexts
   → Updates context with filtered results
```

---

## Implementation Details

### Backend Changes

**File: `backend/models.py`**
- Added `content_type` field to `StoryResult`
- Added `action` and `analysis` fields to `ConversationResponse`

**File: `backend/bedrock_client.py`**
- Enhanced system prompt with analytical and clarification actions
- Added support for `analyze`, `clarify`, and `list_analyzed` actions
- Improved content type extraction logic

**File: `backend/storyblok_client.py`**
- Added `content_type` parameter to search method
- Implemented client-side content type filtering
- Enhanced full story fetching to include content type

**File: `backend/main.py`**
- Added `conversation_analyses` storage
- Implemented action routing for `analyze`, `clarify`, `list_analyzed`
- Enhanced context management with analysis data

### Frontend Changes

**File: `frontend/index.html`**
- Added analysis display component (blue info box)
- Added content type badge to story cards
- Updated message structure to include `analysis` and `action` fields
- Enhanced example prompts to showcase analytical features

---

## Usage Patterns

### Pattern 1: Count Before List
```
"How many [content_type] mention [topic]?"
→ Shows count
→ Asks if user wants to see them
→ User confirms
→ Shows list
```

### Pattern 2: Type Clarification
```
"Find [topic]"
→ Asks for content type
→ User specifies type
→ Performs search
→ Shows results
```

### Pattern 3: Multi-Step Refinement
```
"Find [topic]"
→ Shows results
→ "Out of those, which mention [subtopic]?"
→ Shows filtered results
→ "How many are there?"
→ Shows count of filtered results
```

---

## Testing

### Test Analytical Queries

```bash
# Test count query
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "how many articles mention drupal?",
    "conversation_history": []
  }'

# Expected: Analysis response with count
```

### Test Content Type Filtering

```bash
# Test specific content type
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "find 5 articles about react",
    "conversation_history": []
  }'

# Expected: Only article content type returned
```

### Test Conversational Flow

```bash
# Step 1: Analyze
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "how many blog posts mention vue?",
    "conversation_history": []
  }'

# Step 2: List (use actual conversation history from step 1)
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "yes please show them",
    "conversation_history": [
      {"role": "user", "content": "how many blog posts mention vue?"},
      {"role": "assistant", "content": "I found 4 blog posts that mention vue. Would you like me to list them?"}
    ]
  }'
```

---

## Future Enhancements

### Planned Features
- **Date range analysis** - "How many articles published this month?"
- **Trend analysis** - "What topics are trending?"
- **Comparison** - "Compare articles about React vs Vue"
- **Aggregations** - "Show me the most popular content types"
- **Author analysis** - "How many articles by author X?"

### Potential Improvements
- Redis/database for persistent session storage
- More sophisticated content type detection
- Natural language date parsing
- Export analysis results
- Visualization of analysis data

---

## Troubleshooting

### Issue: Content Type Not Detected
**Cause:** Content type not returned by Storyblok API
**Solution:** Ensure full story details are fetched; content_type comes from full story data

### Issue: Analysis Count Doesn't Match List
**Cause:** Content type filtering happens after search
**Solution:** This is expected; filtering reduces the count to match criteria

### Issue: Context Lost Between Turns
**Cause:** Session key changed or context expired
**Solution:** Ensure conversation history includes first user message for stable session key

---

## Best Practices

1. **Be specific about content type** when possible
2. **Use analysis for large result sets** before listing all items
3. **Maintain conversation history** for context-aware refinement
4. **Ask for clarification** when user intent is unclear
5. **Provide conversational feedback** at each step

---

**Last Updated:** 2025-01-XX  
**Version:** 1.2.0  
**Status:** ✅ Production Ready