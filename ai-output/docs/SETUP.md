# Setup and Installation Guide

## Prerequisites

- Python 3.11 or higher
- Modern web browser with Web Speech API support (Chrome, Edge, Safari)
- AWS Bedrock access with bearer token
- Storyblok account with Strata access

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ams-retreat-hackathon
```

### 2. Create Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The `.env` file should already be configured with your credentials. Verify it contains:

```
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_BEARER_TOKEN_BEDROCK=your_bearer_token_here
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-v1:0

# Storyblok Configuration
STORYBLOK_TOKEN=your_token_here
STORYBLOK_SPACE_ID=your_space_id_here
STORYBLOK_API_BASE=https://api-staging-d1.storyblok.com

# Application Configuration
DEBUG=false
CORS_ORIGINS=["http://localhost:8000", "http://127.0.0.1:8000"]
```

## Running the Application

### Start the Backend Server

```bash
# From the project root directory
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Access the Frontend

Open your web browser and navigate to:

```
http://localhost:8000/frontend/index.html
```

Or use a simple HTTP server:

```bash
# In a new terminal, from the project root
cd frontend
python -m http.server 8000
```

Then open `http://localhost:8000/index.html`

## Verifying the Installation

### 1. Check API Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Storyblok Voice Assistant",
  "version": "1.0.0"
}
```

### 2. Test Bedrock Connection (Debug Mode)

Set `DEBUG=true` in your `.env` file, then:

```bash
curl http://localhost:8000/api/test-bedrock
```

### 3. Test Storyblok Connection (Debug Mode)

```bash
curl "http://localhost:8000/api/test-storyblok?term=test"
```

### 4. Test Conversation Endpoint

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find articles about marketing",
    "conversation_history": []
  }'
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend tests/

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

## Troubleshooting

### Issue: Voice input not working

**Solution:** Ensure you're using a supported browser (Chrome, Edge, or Safari) and have granted microphone permissions.

### Issue: CORS errors

**Solution:** Make sure the frontend is being served from an origin listed in `CORS_ORIGINS` in your `.env` file.

### Issue: Bedrock connection fails

**Solution:** 
- Verify your AWS bearer token is valid
- Check that you have access to the Bedrock model
- Ensure the AWS region is correct

### Issue: Storyblok search returns no results

**Solution:**
- Verify your Storyblok token has the correct permissions
- Check that the space ID is correct
- Ensure you're using the correct API base URL for Strata

### Issue: Module import errors

**Solution:** Make sure you're running commands from the project root directory and the virtual environment is activated.

## Browser Requirements

For full functionality, your browser should support:

- Web Speech API (Speech Recognition)
- Web Speech Synthesis API (Text-to-Speech)
- ES6+ JavaScript
- CSS Grid and Flexbox
- Fetch API

**Recommended browsers:**
- Google Chrome 90+
- Microsoft Edge 90+
- Safari 14.1+

## API Documentation

Once the server is running, visit:

- **Interactive API Docs (Swagger):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc

## Development Mode

To enable debug features and more verbose logging:

1. Set `DEBUG=true` in `.env`
2. Restart the backend server
3. Access debug endpoints:
   - `/api/test-bedrock` - Test Bedrock integration
   - `/api/test-storyblok` - Test Storyblok integration

## Production Deployment

For production deployment:

1. Set `DEBUG=false` in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up HTTPS/SSL certificates
4. Configure appropriate CORS origins
5. Implement rate limiting
6. Set up monitoring and logging

## Next Steps

- Read [FEATURES.md](./FEATURES.md) for feature documentation
- Check [API.md](./API.md) for detailed API reference
- Review [ACCESSIBILITY.md](./ACCESSIBILITY.md) for accessibility features