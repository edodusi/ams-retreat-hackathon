# Schema Update Summary

**Date:** January 2025  
**Version:** 1.1.0  
**Status:** ✅ Complete - All tests passing (8/8)

---

## Overview

Updated the Storyblok Voice Assistant to use the new Strata API schema and added automatic full story preview fetching.

---

## New Strata API Schema

```json
{
  "body": "string",
  "cursor": 0,
  "name": "Story Title",
  "slug": "path/to/story",
  "story_id": 12345
}
```

### Field Mapping (Old → New)

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `id` | `story_id` | Renamed for clarity |
| `full_slug` | `slug` | Simplified |
| `title` | `name` | Use name directly |
| `content` | `body` | Now plain text instead of object |
| `description` | _(removed)_ | Generate from body preview |
| `published_at` | _(removed)_ | Available in `full_story` |
| _(new)_ | `cursor` | For pagination |
| _(new)_ | `full_story` | Auto-fetched complete story data |

---

## Key Changes

### Backend

1. **`backend/models.py`** - Updated `StoryResult` to new schema
2. **`backend/storyblok_client.py`** - Added `get_story_by_id()` method
3. **`backend/main.py`** - Auto-fetch full story for each search result
4. **`tests/test_main.py`** - Updated test fixtures

### Frontend

1. **`frontend/index.html`** - Updated story cards to display:
   - Story name and body preview (truncated to 200 chars)
   - Full story preview box when available
   - Slug and story_id
   - Publication date from full_story

### Documentation

1. **`docs/openapi.yaml`** - Updated schema definitions
2. **`docs/API.md`** - Updated response examples
3. **`docs/SCHEMA_UPDATE.md`** - Complete migration guide

### New Features

- **GET `/api/story/{story_id}`** - Fetch complete story by ID
- **Auto-preview** - Search results automatically include full story data
- **Graceful degradation** - Basic preview works even if full fetch fails

---

## Enhanced Preview Feature

When user searches for content:

1. ✅ Query Strata API (gets basic fields)
2. ✅ Auto-fetch full story for each result
3. ✅ Return combined data with `full_story` field
4. ✅ Display rich preview with metadata

**Benefits:**
- Better context for users
- Access to publication dates, full content structure
- No extra frontend work needed
- Parallel fetching for performance

---

## Testing

```bash
# Run all tests
source venv/bin/activate
pytest tests/ -v

# Result: 8/8 passing ✅
```

**Manual test:**
```bash
# Search with auto-preview
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find marketing articles", "conversation_history": []}'

# Get specific story
curl http://localhost:8000/api/story/12345
```

---

## Migration Guide

### Python Code

```python
# OLD
story.id              # → story.story_id
story.full_slug       # → story.slug
story.title           # → story.name
story.description     # → story.body[:200]
story.published_at    # → story.full_story.published_at

# NEW - Access full story data
story.full_story.content
story.full_story.published_at
```

### JavaScript/Frontend

```javascript
// OLD
story.id              // → story.story_id
story.full_slug       // → story.slug
story.title           // → story.name

// NEW - Access full story
story.full_story?.content
story.full_story?.published_at
```

---

## Response Example

```json
{
  "message": "I found 2 marketing articles.",
  "results": {
    "stories": [
      {
        "body": "A comprehensive guide to modern marketing...",
        "cursor": 0,
        "name": "Marketing Strategy 2025",
        "slug": "blog/marketing-strategy-2025",
        "story_id": 12345,
        "full_story": {
          "id": 12345,
          "name": "Marketing Strategy 2025",
          "content": { ... },
          "published_at": "2025-01-15T10:00:00Z"
        }
      }
    ],
    "total": 2
  }
}
```

---

## Files Modified

**Backend (5 files):**
- `backend/models.py` - New schema
- `backend/storyblok_client.py` - Added get_story_by_id()
- `backend/main.py` - Auto-fetch logic + new endpoint
- `tests/test_main.py` - Updated fixtures
- `backend/config.py` - No changes needed

**Frontend (1 file):**
- `frontend/index.html` - Updated story cards + CSS

**Documentation (3 files):**
- `docs/openapi.yaml` - Updated schema
- `docs/API.md` - Updated examples
- `docs/SCHEMA_UPDATE.md` - Full migration guide

---

## Backward Compatibility

⚠️ **Breaking Changes** - This is a major schema update:
- Field names changed
- Data structure different
- Clients must be updated

**No automatic migration available.**

---

## Next Steps

1. ✅ Update backend - COMPLETE
2. ✅ Update frontend - COMPLETE
3. ✅ Update tests - COMPLETE (8/8 passing)
4. ✅ Update documentation - COMPLETE
5. ⏭️ Test with real Strata API
6. ⏭️ Deploy to staging
7. ⏭️ Update client applications

---

## Related Documentation

- **[SCHEMA_UPDATE.md](docs/SCHEMA_UPDATE.md)** - Complete migration guide
- **[API.md](docs/API.md)** - Updated API reference
- **[openapi.yaml](docs/openapi.yaml)** - OpenAPI specification

---

**Questions?** See [SCHEMA_UPDATE.md](docs/SCHEMA_UPDATE.md) for detailed migration guide.

**Status:** ✅ Ready for testing with real API