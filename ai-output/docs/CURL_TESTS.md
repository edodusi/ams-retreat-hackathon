# cURL Testing Guide

Quick reference for testing the Storyblok Voice Assistant API with cURL commands.

## Prerequisites

- Backend server running on `http://localhost:8000`
- Environment variables configured in `.env`

## Start the Server

```bash
# From project root
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Health Check Tests

### Test Root Endpoint

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Storyblok Voice Assistant",
  "version": "1.0.0"
}
```

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Storyblok Voice Assistant",
  "version": "1.0.0"
}
```

---

## Conversation Tests

### Simple Search Query

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find articles about marketing",
    "conversation_history": []
  }'
```

**Expected Response:**
```json
{
  "message": "I found marketing articles for you...",
  "results": {
    "stories": [
      {
        "id": 12345,
        "name": "Marketing Article",
        "full_slug": "blog/marketing-article",
        "title": "Marketing Article",
        "description": "Description...",
        "published_at": "2025-01-15T10:00:00Z"
      }
    ],
    "total": 10
  },
  "conversation_id": null
}
```

### Search with Multiple Keywords

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find blog posts about technology and innovation",
    "conversation_history": []
  }'
```

### Casual Chat (No Search)

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "conversation_history": []
  }'
```

**Expected Response:**
```json
{
  "message": "Hello! I'm here to help you search for content...",
  "results": null,
  "conversation_id": null
}
```

### Multi-Turn Conversation

**First Query:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find blog posts",
    "conversation_history": []
  }'
```

**Refinement Query:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show only recent ones",
    "conversation_history": [
      {
        "role": "user",
        "content": "Find blog posts"
      },
      {
        "role": "assistant",
        "content": "I found 50 blog posts..."
      }
    ]
  }'
```

### Long Conversation History

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me the latest",
    "conversation_history": [
      {"role": "user", "content": "Find marketing content"},
      {"role": "assistant", "content": "I found 20 marketing items..."},
      {"role": "user", "content": "Filter by blog posts"},
      {"role": "assistant", "content": "Here are 12 blog posts..."},
      {"role": "user", "content": "From this year only"},
      {"role": "assistant", "content": "Here are 8 posts from 2025..."}
    ]
  }'
```

---

## Debug Tests (DEBUG=true only)

### Test Bedrock Connection

```bash
curl http://localhost:8000/api/test-bedrock
```

**Expected Response (Success):**
```json
{
  "status": "success",
  "response": {
    "action": "chat",
    "response": "Hello! I can help you search for content.",
    "raw_response": "..."
  }
}
```

**Expected Response (Error):**
```json
{
  "status": "error",
  "error": "Connection timeout"
}
```

### Test Storyblok Connection

```bash
curl "http://localhost:8000/api/test-storyblok?term=marketing"
```

**With Different Search Terms:**
```bash
# Test with "technology"
curl "http://localhost:8000/api/test-storyblok?term=technology"

# Test with "blog"
curl "http://localhost:8000/api/test-storyblok?term=blog"

# Test with default term
curl http://localhost:8000/api/test-storyblok
```

---

## Error Testing

### Missing Message Field

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_history": []
  }'
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Empty Message

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "",
    "conversation_history": []
  }'
```

**Expected Response (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Invalid JSON

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{invalid json'
```

**Expected Response (422):**
```json
{
  "detail": "Invalid JSON"
}
```

---

## Pretty Printing Responses

### Using jq (if installed)

```bash
curl -s http://localhost:8000/health | jq '.'
```

```bash
curl -s -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find marketing articles",
    "conversation_history": []
  }' | jq '.'
```

### Using Python (built-in)

```bash
curl -s http://localhost:8000/health | python -m json.tool
```

---

## Performance Testing

### Measure Response Time

```bash
curl -w "\nTime: %{time_total}s\n" \
  -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find articles",
    "conversation_history": []
  }'
```

### Verbose Output

```bash
curl -v http://localhost:8000/health
```

---

## Batch Testing Script

Create a file `test_api.sh`:

```bash
#!/bin/bash

API_BASE="http://localhost:8000"

echo "Testing Health Endpoint..."
curl -s "$API_BASE/health" | jq -r '.status'

echo -e "\nTesting Simple Search..."
curl -s -X POST "$API_BASE/api/conversation" \
  -H "Content-Type: application/json" \
  -d '{"message": "Find marketing articles", "conversation_history": []}' \
  | jq -r '.message'

echo -e "\nTesting Chat..."
curl -s -X POST "$API_BASE/api/conversation" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}' \
  | jq -r '.message'

echo -e "\nAll tests complete!"
```

Run with:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## Common Issues

### Connection Refused
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```
**Solution:** Start the backend server

### CORS Errors
Only affect browser requests, not cURL

### Authentication Errors (503)
```json
{
  "error": "Unable to connect to AI service",
  "status_code": 503
}
```
**Solution:** Check AWS Bedrock credentials in `.env`

### Storyblok Errors (503)
```json
{
  "error": "Unable to search content"
}
```
**Solution:** Check Storyblok token and space ID in `.env`

---

## Interactive API Documentation

For interactive testing with a web UI, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

**Last Updated:** October 30, 2025
## Story Retrieval Tests

### Get Full Story by ID

Fetch complete story details from Storyblok API:

```bash
curl http://localhost:8000/api/story/12345
```

**Expected Response (Success):**
```json
{
  "status": "success",
  "story": {
    "id": 12345,
    "name": "Marketing Strategy 2025",
    "full_slug": "blog/marketing-strategy-2025",
    "content": {
      "component": "article",
      "title": "Marketing Strategy 2025",
      "body": "Full article content..."
    },
    "created_at": "2025-01-01T10:00:00Z",
    "published_at": "2025-01-15T10:00:00Z",
    "first_published_at": "2025-01-15T10:00:00Z"
  }
}
```

**Expected Response (Not Found - 404):**
```json
{
  "detail": "Story with ID 99999 not found"
}
```

**Use Cases:**
- Get full story when search results don't have enough information
- Load complete content structure for display
- Access all story metadata

**Example with real ID from search:**
```bash
# First, search for stories
RESPONSE=$(curl -s -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find marketing articles", "conversation_history": []}')

# Extract first story_id (requires jq)
STORY_ID=$(echo $RESPONSE | jq -r '.results.stories[0].story_id')

# Fetch full story
curl "http://localhost:8000/api/story/${STORY_ID}"
```

---
