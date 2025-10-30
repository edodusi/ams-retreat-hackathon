# Storyblok Voice Assistant 🎤

Voice-enabled content discovery for Storyblok using AWS Bedrock and natural conversation.

## 🎯 Overview

An accessible, voice-powered AI assistant that enables users to search and discover Storyblok content through natural conversation. Built for accessibility with WCAG 2.1 Level AA compliance, making content discovery available to users with visual or motor disabilities.

**Key Features:**
- 🎤 Voice input and output (Web Speech API)
- 💬 Natural language conversation (AWS Bedrock Claude)
- 🔍 Semantic content search (Storyblok Strata)
- ♿ Fully accessible (keyboard navigation, screen reader compatible)
- 📱 Responsive chat-like interface

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Modern browser (Chrome, Edge, or Safari)
- AWS Bedrock access
- Storyblok account with Strata access

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd ams-retreat-hackathon
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   The `.env` file should already be configured. Verify it contains your credentials.

5. **Start the application:**
   ```bash
   ./run.sh
   ```
   
   Or manually:
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Open the frontend:**
   Navigate to `http://localhost:8000/frontend/index.html`

## 📁 Project Structure

```
ams-retreat-hackathon/
├── backend/              # FastAPI backend application
│   ├── main.py          # Main API endpoints
│   ├── bedrock_client.py # AWS Bedrock integration
│   ├── storyblok_client.py # Storyblok API client
│   └── models.py        # Data models
├── frontend/            # Frontend application
│   └── index.html       # Alpine.js voice interface
├── docs/                # 📘 End-user documentation
│   ├── SETUP.md         # Setup guide
│   ├── API.md           # API reference
│   └── FEATURES.md      # Feature documentation
├── tests/               # ✅ Automated tests (pytest)
│   ├── test_main.py     # API endpoint tests
│   ├── test_*.py        # Other test files
│   └── pytest.ini       # Test configuration
├── ai-output/           # 🤖 AI-generated artifacts
│   ├── docs/           # Change logs, debug notes, session logs
│   └── validation/     # Validation scripts & debugging tools
├── requirements.txt     # Python dependencies
├── run.sh              # Application launcher
└── README.md           # This file
```

**Note**: The `ai-output/` folder contains AI-generated documentation and validation scripts, separate from production code and real tests.

## 📖 Documentation

User-facing documentation is in the `docs/` folder (when it exists):

- **[Setup Guide](ai-output/docs/SETUP.md)** - Detailed installation and configuration
- **[API Documentation](ai-output/docs/API.md)** - Complete API reference with examples
- **[Features Guide](ai-output/docs/FEATURES.md)** - All features and usage instructions
- **[Quick Start](ai-output/docs/QUICKSTART.md)** - Quick start guide

See the [Documentation Index](ai-output/docs/README.md) for all available documentation. 
```
┌─────────────────────────────────────────┐
│         Frontend (Alpine.js)            │
│  - Voice Input/Output                   │
│  - Chat Interface                       │
│  - Accessibility Features               │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│       Backend (FastAPI)                 │
│  - Conversation Orchestration           │
│  - Request/Response Handling            │
└──────┬──────────────────┬───────────────┘
       │                  │
       ▼                  ▼
┌──────────────┐   ┌──────────────────────┐
│ AWS Bedrock  │   │  Storyblok Strata    │
│   (Claude)   │   │  (Content Search)    │
└──────────────┘   └──────────────────────┘
```

## 🎨 Usage Examples

### Voice Search
1. Click the microphone button
2. Say: "Find articles about marketing"
3. View results in preview cards
4. Refine: "Show only recent ones"

### Text Search
1. Type in the input field: "Find blog posts about technology"
2. Press Enter or click Send
3. View results
4. Continue conversation naturally

### Keyboard Navigation
- **Tab**: Navigate between elements
- **Enter**: Activate buttons, send messages
- **Arrow keys**: Scroll through messages

## 🧪 Testing

All tests are organized in the `tests/` folder. See [tests/README.md](tests/README.md) for details.

### Run Unit Tests
```bash
pytest tests/
```

### Test with Coverage
```bash
pytest --cov=backend tests/
```

### Validation Scripts
Validation and debugging scripts are in `ai-output/validation/`:

```bash
# Test server functionality
./ai-output/validation/test_server.sh

# Test frontend functionality
./ai-output/validation/test_frontend.sh

# Run comprehensive validation
./ai-output/validation/final_test.sh
```

### Test API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Conversation:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find marketing articles",
    "conversation_history": []
  }'
```

For more test examples, see [ai-output/docs/CURL_TESTS.md](ai-output/docs/CURL_TESTS.md).

## 🛠️ Tech Stack

### Frontend
- **Alpine.js** - Lightweight reactive framework
- **Tailwind CSS** - Utility-first styling
- **Web Speech API** - Voice input/output

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **httpx** - Async HTTP client

### APIs
- **AWS Bedrock** - Claude Sonnet 4.5 for conversation
- **Storyblok Strata** - Semantic content search

## ♿ Accessibility

This project is built with accessibility as a priority:

- ✅ WCAG 2.1 Level AA compliant
- ✅ Full keyboard navigation
- ✅ Screen reader compatible
- ✅ High contrast (4.5:1 minimum)
- ✅ Large touch targets (44x44px)
- ✅ ARIA labels and semantic HTML
- ✅ Focus indicators on all interactive elements

## 📊 Project Structure

```
ams-retreat-hackathon/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── bedrock_client.py    # AWS Bedrock integration
│   └── storyblok_client.py  # Storyblok Strata integration
├── frontend/
│   └── index.html           # Chat interface
├── tests/
│   ├── __init__.py
│   └── test_main.py         # Unit tests
├── docs/
│   ├── SETUP.md             # Setup guide
│   ├── API.md               # API documentation
│   └── FEATURES.md          # Features documentation
├── requirements.txt         # Python dependencies
├── run.sh                   # Startup script
├── SPECS.md                 # Project specifications
├── GUIDELINES.md            # Development guidelines
└── README.md                # This file
```

## 🔧 Configuration

Environment variables in `.env`:

| Variable | Description |
|----------|-------------|
| `AWS_REGION` | AWS region (default: us-east-1) |
| `AWS_BEARER_TOKEN_BEDROCK` | AWS Bedrock bearer token |
| `BEDROCK_MODEL_ID` | Claude model ID |
| `STORYBLOK_TOKEN` | Storyblok API token |
| `STORYBLOK_SPACE_ID` | Storyblok space ID |
| `STORYBLOK_API_BASE` | Strata API base URL |
| `DEBUG` | Enable debug mode (true/false) |
| `CORS_ORIGINS` | Allowed CORS origins |

## 🐛 Troubleshooting

**Voice not working?**
- Ensure you're using Chrome, Edge, or Safari
- Grant microphone permissions
- Check browser console for errors

**CORS errors?**
- Verify frontend origin is in `CORS_ORIGINS`
- Check that backend is running on correct port

**API connection fails?**
- Verify credentials in `.env`
- Check AWS region and token validity
- Ensure Storyblok token has correct permissions

**No search results?**
- Verify Storyblok space ID is correct
- Check that content exists in the space
- Try broader search terms

## 🚢 Deployment

For production deployment:

1. Set `DEBUG=false` in `.env`
2. Use production WSGI server (Gunicorn)
3. Configure HTTPS/SSL
4. Set appropriate CORS origins
5. Implement rate limiting
6. Set up monitoring and logging

## 🎯 MVP Goals

✅ Voice input and output
✅ Chat-like UI with message bubbles
✅ Story preview cards
✅ AWS Bedrock integration
✅ Storyblok Strata search
✅ Multi-turn conversation context
✅ Full keyboard accessibility
✅ WCAG 2.1 AA compliance

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice customization
- [ ] Search history persistence
- [ ] Advanced filtering
- [ ] Result pagination in UI
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] Mobile app

## 📝 License

This is a hackathon project for the Amsterdam Retreat 2025.

## 🙏 Acknowledgments

- AWS Bedrock for Claude AI
- Storyblok for Strata API
- Web Speech API contributors
- Alpine.js and Tailwind CSS teams

---

**Built with ❤️ for accessibility and inclusive design**

**Last Updated:** October 30, 2025  
**Version:** 1.0.0