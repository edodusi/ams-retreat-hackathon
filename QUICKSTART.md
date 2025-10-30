# Quick Start Cheatsheet 🚀

**Storyblok Voice Assistant** - Get up and running in 5 minutes!

---

## ⚡ Super Quick Start

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure (if needed)
# Edit .env file with your credentials

# 3. Run
./run.sh
# OR
python -m uvicorn backend.main:app --reload

# 4. Open browser
# http://localhost:8000/frontend/index.html
```

---

## 📋 Essential Commands

### Start Server
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests
```bash
pytest
pytest -v  # verbose
pytest --cov=backend  # with coverage
```

### Verify Setup
```bash
python3 verify_setup.py
```

### Quick Health Check
```bash
curl http://localhost:8000/health
```

---

## 🎯 Quick API Tests

### Simple Search
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find articles about marketing", "conversation_history": []}'
```

### With Conversation History
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show recent ones",
    "conversation_history": [
      {"role": "user", "content": "Find blog posts"},
      {"role": "assistant", "content": "I found 50 blog posts..."}
    ]
  }'
```

---

## 🔑 Environment Variables (Quick Reference)

```env
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=  # Optional, for temporary credentials
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-v1:0

# Storyblok
STORYBLOK_TOKEN=your_token_here
STORYBLOK_SPACE_ID=your_space_id
STORYBLOK_API_BASE=https://api-staging-d1.storyblok.com

# App
DEBUG=false
CORS_ORIGINS=["http://localhost:8000"]
```

---

## 🎤 Using the Voice Assistant

### Voice Input
1. Click microphone button (blue circle)
2. Speak: "Find articles about marketing"
3. Wait for results

### Text Input
1. Type in input field
2. Press Enter or click Send
3. View results in chat

### Keyboard Navigation
- **Tab** - Navigate elements
- **Enter** - Activate/Send
- **Arrow Keys** - Scroll messages

---

## 📊 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/conversation` | POST | Main conversation |
| `/api/test-bedrock` | GET | Test Bedrock (debug) |
| `/api/test-storyblok` | GET | Test Storyblok (debug) |

---

## 🐛 Quick Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
python -m uvicorn backend.main:app --port 8080
```

### Voice not working
- Use Chrome, Edge, or Safari (not Firefox)
- Grant microphone permissions
- Check browser console for errors

### API errors
```bash
# Check logs
tail -f logs/app.log  # if logging to file

# Test connections separately
curl http://localhost:8000/api/test-bedrock
curl http://localhost:8000/api/test-storyblok?term=test
```

### No search results
- Verify Storyblok credentials in `.env`
- Check space ID is correct
- Try broader search terms

---

## 📱 URLs

- **Frontend:** http://localhost:8000/frontend/index.html
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 🧪 Quick Test Sequence

```bash
# 1. Health
curl http://localhost:8000/health

# 2. Simple search
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find marketing articles", "conversation_history": []}'

# 3. Chat
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}'
```

---

## 📚 Documentation Links

- **[Full Setup Guide](docs/SETUP.md)** - Detailed installation
- **[API Docs](docs/API.md)** - Complete API reference
- **[Features](docs/FEATURES.md)** - All features explained
- **[cURL Tests](docs/CURL_TESTS.md)** - More test examples
- **[Specs](SPECS.md)** - Technical specifications

---

## 💡 Example Queries

**Search Examples:**
- "Find articles about marketing"
- "Show me blog posts about technology"
- "I need content about product launches"
- "Find recent articles"

**Refinement Examples:**
- "Show only recent ones"
- "From this year only"
- "Show me the most popular"
- "Filter by blog posts"

**Chat Examples:**
- "Hello"
- "What can you do?"
- "Thank you"

---

## 🎯 Project Structure (Quick View)

```
ams-retreat-hackathon/
├── backend/           # FastAPI application
│   ├── main.py       # Main app & endpoints
│   ├── config.py     # Configuration
│   ├── models.py     # Data models
│   ├── bedrock_client.py    # AWS Bedrock
│   └── storyblok_client.py  # Storyblok
├── frontend/
│   └── index.html    # Chat UI
├── tests/            # Unit tests
├── docs/             # Documentation
├── requirements.txt  # Dependencies
├── run.sh           # Startup script
└── .env             # Configuration
```

---

## ⚙️ Debug Mode

Enable for troubleshooting:

```env
# In .env
DEBUG=true
```

Then access:
- `GET /api/test-bedrock` - Test AWS connection
- `GET /api/test-storyblok?term=test` - Test Storyblok

---

## 🔧 Common Fixes

**Import errors:**
```bash
# Ensure you're in project root
cd ams-retreat-hackathon
# Activate venv
source venv/bin/activate
```

**Port in use:**
```bash
# Change port
python -m uvicorn backend.main:app --port 8080
```

**Module not found:**
```bash
pip install -r requirements.txt
```

---

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] Frontend loads in browser
- [ ] Voice button shows in UI
- [ ] Search query returns results

---

**Need more help?** See [docs/SETUP.md](docs/SETUP.md)

**Version:** 1.0.0 | **Last Updated:** October 30, 2025
