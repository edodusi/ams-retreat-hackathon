# API Documentation

Complete API reference for the Storyblok Voice Assistant backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, authentication is handled via environment variables for AWS Bedrock and Storyblok. No user authentication is required for API endpoints.

---

## Endpoints

### Health Check

#### `GET /`

Root endpoint returning service health status.

**Response**

```json
{
  "status": "healthy",
  "service": "Storyblok Voice Assistant",
  "version": "1.0.0"
}
```

**Status Codes**
- `200 OK` - Service is healthy

---

#### `GET /health`

Dedicated health check endpoint.

**Response**

```json
{
  "status": "healthy",
  "service": "Storyblok Voice Assistant",
  "version": "1.0.0"
}
```

**Status Codes**
- `200 OK` - Service is healthy

---

### Conversation

#### `POST /api/conversation`

Main conversation endpoint for processing user messages and searching content.

**Request Body**

```json
{
  "message": "Find articles about marketing",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you?"
    }
  ]
}
```

**Request Schema**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | User's message/query (min length: 1) |
| `conversation_history` | array | No | Previous conversation messages for context |
| `conversation_history[].role` | string | Yes | Either "user" or "assistant" |
| `conversation_history[].content` | string | Yes | Message content |

**Response**

```json
{
  "message": "I found 15 marketing articles. Here are the top results:",
  "results": {
    "stories": [
      {
        "id": 12345,
        "name": "Marketing Strategy 2025",
        "full_slug": "blog/marketing-strategy-2025",
        "title": "Marketing Strategy 2025",
        "description": "A comprehensive guide to modern marketing tactics and trends",
        "content": {...},
        "created_at": "2025-01-01T10:00:00Z",
        "published_at": "2025-01-15T10:00:00Z",
        "first_published_at": "2025-01-15T10:00:00Z"
      }
    ],
    "total": 15
  },
  "conversation_id": null
}
```

**Response Schema**

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | Assistant's conversational response |
| `results` | object or null | Search results if a search was performed |
| `results.stories` | array | Array of story objects |
| `results.total` | integer | Total number of results |
| `conversation_id` | string or null | Conversation session ID (future use) |

**Story Object Schema**

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique story identifier |
| `name` | string | Story name |
| `full_slug` | string | Complete URL slug/path |
| `title` | string or null | Display title extracted from content |
| `description` | string or null | Brief description (max 200 chars) |
| `content` | object or null | Raw story content object |
| `created_at` | string or null | ISO 8601 timestamp of creation |
| `published_at` | string or null | ISO 8601 timestamp of publication |
| `first_published_at` | string or null | ISO 8601 timestamp of first publication |

**Status Codes**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid request body
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - External service (Bedrock/Storyblok) unavailable

**Example Requests**

Simple search:
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find blog posts about technology",
    "conversation_history": []
  }'
```

With conversation history:
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show only recent ones",
    "conversation_history": [
      {
        "role": "user",
        "content": "Find blog posts about technology"
      },
      {
        "role": "assistant",
        "content": "I found 23 technology blog posts."
      }
    ]
  }'
```

---

### Debug Endpoints

The following endpoints are only available when `DEBUG=true` in the environment configuration.

#### `GET /api/test-bedrock`

Test AWS Bedrock connection.

**Response**

Success:
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

Error:
```json
{
  "status": "error",
  "error": "Connection timeout"
}
```

**Status Codes**
- `200 OK` - Test completed (check status field)
- `404 Not Found` - Debug mode disabled

---

#### `GET /api/test-storyblok`

Test Storyblok Strata connection.

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `term` | string | No | "test" | Search term to test |

**Response**

Success:
```json
{
  "status": "success",
  "results": {
    "stories": [...],
    "total": 5
  }
}
```

Error:
```json
{
  "status": "error",
  "error": "Authentication failed"
}
```

**Status Codes**
- `200 OK` - Test completed (check status field)
- `404 Not Found` - Debug mode disabled

**Example**

```bash
curl "http://localhost:8000/api/test-storyblok?term=marketing"
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "Brief error message",
  "detail": "Detailed error information",
  "status_code": 500
}
```

### Common Error Scenarios

**Validation Error (422)**
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

**Service Unavailable (503)**
```json
{
  "error": "Service unavailable",
  "detail": "Unable to connect to AI service: Connection timeout",
  "status_code": 503
}
```

**Internal Server Error (500)**
```json
{
  "error": "Internal server error",
  "detail": "An unexpected error occurred",
  "status_code": 500
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, implement rate limiting to prevent abuse.

---

## CORS Configuration

By default, the API allows requests from:
- `http://localhost:8000`
- `http://127.0.0.1:8000`

Configure additional origins via the `CORS_ORIGINS` environment variable.

---

## Conversation Flow

The conversation endpoint implements a multi-turn conversation flow:

1. **User sends message** with optional conversation history
2. **System processes with Claude** (AWS Bedrock)
3. **Claude determines action**:
   - `search`: Extract search term and query Storyblok
   - `chat`: Respond conversationally without search
4. **System returns response** with message and optional results
5. **Client adds messages to history** for next turn

### Best Practices

- **Keep history manageable**: Limit to last 10 messages (automatically enforced)
- **Handle errors gracefully**: Check for null results
- **Progressive enhancement**: Work without conversation history if needed

---

## Integration Examples

### JavaScript (Fetch API)

```javascript
async function sendMessage(message, history = []) {
  const response = await fetch('http://localhost:8000/api/conversation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      conversation_history: history
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}
```

### Python (httpx)

```python
import httpx

async def send_message(message: str, history: list = None):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8000/api/conversation',
            json={
                'message': message,
                'conversation_history': history or []
            }
        )
        response.raise_for_status()
        return response.json()
```

### cURL

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "message": "Find marketing articles",
  "conversation_history": []
}
EOF
```

---

## OpenAPI Specification

The full OpenAPI 3.0 specification is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **JSON Schema**: http://localhost:8000/openapi.json

---

## Configuration

API behavior can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_CONVERSATION_HISTORY` | 10 | Maximum messages to retain in history |
| `DEFAULT_SEARCH_LIMIT` | 10 | Default number of search results |
| `REQUEST_TIMEOUT` | 30 | API request timeout in seconds |
| `DEBUG` | false | Enable debug endpoints and verbose logging |

---

## Performance Considerations

- **Response Time**: Typically 1-3 seconds for search requests
- **Timeout**: 30 seconds default (configurable)
- **Payload Size**: Keep conversation history reasonable (<10 messages)
- **Concurrent Requests**: FastAPI handles async requests efficiently

---

## Security Notes

- API tokens stored in environment variables
- HTTPS recommended for production
- No user data persistence (stateless)
- CORS restrictions enforced
- Input validation on all endpoints

---

## Future Enhancements

Planned API improvements:

- [ ] User authentication and session management
- [ ] Rate limiting per user/IP
- [ ] Caching for common queries
- [ ] WebSocket support for real-time updates
- [ ] Pagination for large result sets
- [ ] Advanced filtering options
- [ ] Result sorting capabilities

---

**Last Updated**: October 30, 2025  
**API Version**: 1.0.0