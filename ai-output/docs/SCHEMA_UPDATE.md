# Strata API Schema Update

**Date:** January 2025  
**Status:** ✅ Complete  
**Version:** 1.1.0

---

## Overview

The Storyblok Voice Assistant has been updated to use the new Strata API schema. This document outlines the changes made to support the updated story structure.

---

## New Story Schema

The Strata API now returns stories with the following simplified schema:

```json
{
  "body": "string",
  "cursor": 0,
  "name": "Story Title",
  "slug": "path/to/story",
  "story_id": 12345
}
```

### Schema Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | string | Yes | Story body/content as plain text |
| `cursor` | number | Yes | Cursor position for pagination |
| `name` | string | Yes | Story name/title |
| `slug` | string | Yes | Story slug/path (without leading slash) |
| `story_id` | number | Yes | Unique Storyblok story identifier |

---

## Changes Made

### Backend Updates

#### 1. **Models** (`backend/models.py`)

Updated `StoryResult` class to match new schema:

```python
class StoryResult(BaseModel):
    """A single story result from Storyblok Strata API."""
    body: str = Field(..., description="Story body/content as text")
    cursor: int = Field(..., description="Cursor for pagination")
    name: str = Field(..., description="Story name")
    slug: str = Field(..., description="Story slug/path")
    story_id: int = Field(..., description="Story ID")
    
    # Additional fields for full story details (when fetched)
    full_story: Optional[dict] = Field(None, description="Full story data from Storyblok API")
```

**Removed fields:**
- `id` → replaced with `story_id`
- `full_slug` → replaced with `slug`
- `content` → replaced with `body` (text format)
- `title` → now using `name` directly
- `description` → generated from `body` preview
- `created_at`, `published_at`, `first_published_at` → available in `full_story`

#### 2. **Storyblok Client** (`backend/storyblok_client.py`)

**Updated:**
- `_extract_story_info()` - Now extracts the new schema fields
- `search()` - Enhanced error handling for malformed responses

**Added:**
- `get_story_by_id(story_id)` - New method to fetch complete story details from Storyblok API

```python
async def get_story_by_id(self, story_id: int) -> Optional[dict]:
    """
    Fetch full story details by ID from Storyblok API.
    
    Args:
        story_id: The story ID to fetch
        
    Returns:
        Full story data as dict, or None if not found
    """
    url = f"{self.base_url}/v2/cdn/stories/{story_id}"
    # ... implementation
```

#### 3. **Main API** (`backend/main.py`)

**Enhanced conversation endpoint:**
- After performing a search, automatically fetches full story details for each result
- Populates `full_story` field for enhanced previews
- Gracefully handles cases where full story fetch fails

**Added new endpoint:**

```
GET /api/story/{story_id}
```

Fetches complete story details by ID, useful for:
- Loading full story on-demand from frontend
- Getting additional metadata not in search results
- Accessing complete content structure

#### 4. **Tests** (`tests/test_main.py`)

Updated mock data to match new schema:

```python
StoryResult(
    body="A comprehensive guide to modern marketing tactics...",
    cursor=0,
    name="Marketing Strategy 2025",
    slug="blog/marketing-strategy-2025",
    story_id=1
)
```

### Frontend Updates

#### 1. **Story Card Display** (`frontend/index.html`)

Updated story card template to display new fields:

```html
<!-- Story Title -->
<h3 class="text-lg font-semibold text-gray-900 mb-2" x-text="story.name"></h3>

<!-- Story Body Preview -->
<p class="text-gray-600 mb-3 line-clamp-3"
   x-show="story.body"
   x-text="story.body.length > 200 ? story.body.substring(0, 200) + '...' : story.body">
</p>

<!-- Full Story Preview (if available) -->
<template x-if="story.full_story">
    <div class="mt-3 p-3 bg-gray-50 rounded border border-gray-200">
        <p class="text-sm text-gray-700 mb-2">
            <strong>Full Preview:</strong>
        </p>
        <p class="text-sm text-gray-600"
           x-show="story.full_story.content"
           x-text="JSON.stringify(story.full_story.content).substring(0, 150) + '...'">
        </p>
        <p class="text-xs text-gray-500 mt-2"
           x-show="story.full_story.published_at">
            Published: <span x-text="new Date(story.full_story.published_at).toLocaleDateString()"></span>
        </p>
    </div>
</template>

<!-- Story Metadata -->
<div class="flex items-center justify-between text-sm mt-3">
    <span class="text-gray-500" x-text="'/' + story.slug"></span>
    <span class="text-blue-600 font-medium">
        ID: <span x-text="story.story_id"></span>
    </span>
</div>
```

**Key changes:**
- Using `story.name` instead of `story.title`
- Displaying `story.body` preview (truncated to 200 chars)
- Showing full story preview when available
- Using `story.slug` instead of `story.full_slug`
- Displaying `story.story_id` for reference

#### 2. **CSS Enhancements**

Added utility classes for text truncation:

```css
/* Line clamp for text truncation */
.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Story preview box */
.story-card .bg-gray-50 {
    max-height: 150px;
    overflow-y: auto;
}
```

### Documentation Updates

#### 1. **OpenAPI Specification** (`docs/openapi.yaml`)

Updated schema definitions:

```yaml
StoryResult:
  type: object
  required:
    - body
    - cursor
    - name
    - slug
    - story_id
  properties:
    body:
      type: string
      description: Story body/content as text from Strata API
    cursor:
      type: integer
      description: Cursor position for pagination
    name:
      type: string
      description: Story name/title
    slug:
      type: string
      description: Story slug/path
    story_id:
      type: integer
      description: Unique Storyblok story identifier
    full_story:
      type: object
      nullable: true
      description: Full story data fetched from Storyblok API
```

Added new endpoint documentation for `/api/story/{story_id}`.

---

## Enhanced Preview Feature

### How It Works

1. **Search Request:** User asks to search for content
2. **Strata API Call:** Backend queries Strata API with search term
3. **Results Returned:** Strata returns list of stories with basic fields (body, cursor, name, slug, story_id)
4. **Full Story Fetch:** For each result, backend automatically fetches full story details using `story_id`
5. **Enhanced Response:** Results include both Strata data and full story data in `full_story` field
6. **Preview Display:** Frontend shows both the text preview and full story metadata

### Benefits

- **Better Context:** Users see more information about each story
- **Rich Metadata:** Access to publication dates, full content structure, etc.
- **Graceful Degradation:** If full story fetch fails, basic preview still works
- **Performance:** Fetches happen in parallel during search response

### Example Response

```json
{
  "message": "I found 2 marketing articles for you.",
  "results": {
    "stories": [
      {
        "body": "A comprehensive guide to modern marketing tactics...",
        "cursor": 0,
        "name": "Marketing Strategy 2025",
        "slug": "blog/marketing-strategy-2025",
        "story_id": 12345,
        "full_story": {
          "id": 12345,
          "name": "Marketing Strategy 2025",
          "full_slug": "blog/marketing-strategy-2025",
          "content": {
            "component": "article",
            "title": "Marketing Strategy 2025",
            "intro": "Learn the latest marketing tactics..."
          },
          "published_at": "2025-01-15T10:00:00Z",
          "created_at": "2025-01-10T08:00:00Z"
        }
      }
    ],
    "total": 2
  }
}
```

---

## Testing

### Unit Tests

All tests updated and passing (8/8):

```bash
pytest tests/ -v
```

**Updated test fixtures:**
- `mock_storyblok_results` - Now uses new schema
- Added mock for `get_story_by_id` method

### Manual Testing

Test the new schema with curl:

```bash
# Search for stories (with auto-fetch of full details)
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find marketing articles", "conversation_history": []}'

# Fetch specific story by ID
curl http://localhost:8000/api/story/12345
```

### Debug Endpoint

Test Strata search directly:

```bash
DEBUG=true curl "http://localhost:8000/api/test-storyblok?term=marketing"
```

---

## Migration Guide

### For Developers

If you have custom code accessing story data, update as follows:

#### Old Schema → New Schema

```python
# OLD
story.id              → story.story_id
story.full_slug       → story.slug
story.title           → story.name
story.description     → story.body[:200]  # or use full_story data
story.content         → story.full_story.content (if available)
story.published_at    → story.full_story.published_at (if available)
```

#### Frontend (JavaScript)

```javascript
// OLD
story.id              → story.story_id
story.full_slug       → story.slug
story.title           → story.name
story.description     → story.body.substring(0, 200)

// NEW - Access full story data
story.full_story?.content
story.full_story?.published_at
```

### For API Consumers

Update your API client models to expect:
- `body` instead of `content` for text preview
- `story_id` instead of `id`
- `slug` instead of `full_slug`
- Optional `full_story` object with complete data

---

## API Endpoints

### Updated Endpoints

#### POST `/api/conversation`

**Response now includes:**
- Stories with new schema
- `full_story` field populated when available

#### GET `/api/test-storyblok` (DEBUG only)

**Response matches new schema**

### New Endpoints

#### GET `/api/story/{story_id}`

Fetch complete story details by ID.

**Parameters:**
- `story_id` (path): Story ID to fetch

**Response:**
```json
{
  "status": "success",
  "story": {
    // Complete story data from Storyblok API
  }
}
```

---

## Backward Compatibility

⚠️ **Breaking Changes:**

This update introduces breaking changes to the story schema:
- Field names have changed
- Data structure is different
- Old clients will need updates

**Migration Required:**
- Update all code accessing story data
- Update tests and fixtures
- Update documentation

---

## Future Enhancements

Potential improvements for future releases:

1. **Caching:** Cache full story data to reduce API calls
2. **Lazy Loading:** Fetch full story only when user expands preview
3. **Pagination:** Use `cursor` field for efficient pagination
4. **Field Selection:** Allow specifying which fields to fetch
5. **Batch Fetching:** Optimize multiple story fetches with batch API

---

## Troubleshooting

### Common Issues

#### Story IDs not found
- Verify story exists in Storyblok
- Check API token has correct permissions
- Ensure using correct space ID

#### Full story not loading
- Check logs for fetch errors
- Verify Storyblok API endpoint is correct
- Full story fetch failures don't break search (graceful degradation)

#### Test failures
- Ensure mock data uses new schema
- Update assertions to check new fields
- Add mock for `get_story_by_id` method

### Debug Mode

Enable detailed logging:

```bash
DEBUG=true python -m uvicorn backend.main:app --reload
```

---

## Related Documentation

- [API Documentation](API.md)
- [Features Guide](FEATURES.md)
- [OpenAPI Specification](openapi.yaml)
- [Testing Guide](CURL_TESTS.md)

---

**Questions?** Check the documentation or review the code changes in this PR.

**Last Updated:** January 2025  
**Version:** 1.1.0  
**Status:** ✅ Complete