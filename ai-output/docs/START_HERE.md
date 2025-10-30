# 🚀 START HERE - Quick Start Guide

**Storyblok Voice Assistant** - Get started in 60 seconds!

---

## ✅ Current Status

**ALL SYSTEMS READY** - The application is fully functional and all tests pass (8/8).

- ✅ Server starts successfully
- ✅ All endpoints working
- ✅ Frontend accessible
- ✅ Error handling verified
- ✅ Python 3.9 compatible
- ✅ All configuration issues fixed

---

## 🎯 What You Need

Your `.env` file is already configured, but you need to ensure these credentials are valid:

1. **AWS_ACCESS_KEY_ID** - Your AWS access key ID
2. **AWS_SECRET_ACCESS_KEY** - Your AWS secret access key
3. **STORYBLOK_TOKEN** - Your Storyblok API token
4. **STORYBLOK_SPACE_ID** - Your Storyblok space ID

---

## 🏃 Quick Start (3 Steps)

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Start the Server

```bash
python -m uvicorn backend.main:app --reload
```

You should see:
```
INFO:     Starting Storyblok Voice Assistant...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Open the Frontend

Open your browser to:
```
http://localhost:8000/frontend/index.html
```

---

## 🧪 Quick Test

### Test the API

```bash
# In a new terminal (keep server running)
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"Storyblok Voice Assistant","version":"1.0.0"}
```

### Test a Search

```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find articles about marketing", "conversation_history": []}'
```

---

## 🎤 Using the Application

### Voice Input
1. Click the **blue microphone button**
2. Say: "Find articles about marketing"
3. Listen to the response and view results

### Text Input
1. Type in the input field: "Find blog posts about technology"
2. Press **Enter** or click **Send**
3. View results in the chat

### Refine Your Search
- "Show only recent ones"
- "From this year only"
- "Show me the most popular"

---

## 🔍 If Something Doesn't Work

### AWS Bedrock Returns Error
This is **expected** if credentials aren't configured yet.

**Fix:**
1. Open `.env` file
2. Update `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with valid credentials
3. Ensure you've enabled Claude model access in AWS Bedrock Console
4. Restart the server

**See [docs/AWS_SETUP.md](docs/AWS_SETUP.md) for detailed AWS configuration**

### Storyblok Search Returns Error
**Fix:**
1. Verify `STORYBLOK_TOKEN` in `.env`
2. Verify `STORYBLOK_SPACE_ID` is correct
3. Restart the server

### Voice Input Not Working
- Use **Chrome, Edge, or Safari** (not Firefox)
- Grant microphone permissions when prompted
- Check browser console for errors

---

## 📚 Documentation

- **[README.md](README.md)** - Full project overview
- **[QUICKSTART.md](QUICKSTART.md)** - Command reference
- **[docs/SETUP.md](docs/SETUP.md)** - Detailed setup
- **[docs/API.md](docs/API.md)** - API documentation
- **[docs/FEATURES.md](docs/FEATURES.md)** - Feature guide
- **[FIXES_APPLIED.md](FIXES_APPLIED.md)** - Issues that were fixed

---

## 🎯 Example Queries

**Search Examples:**
- "Find articles about marketing"
- "Show me blog posts about technology"
- "I need content about product launches"

**Refinement Examples:**
- "Show only recent ones"
- "From this year only"
- "Filter by blog posts"

**Chat Examples:**
- "Hello"
- "What can you help me with?"
- "Thank you"

---

## ✅ Verification Checklist

Run this to verify everything:

```bash
# Run all tests
pytest tests/ -v

# Or run the comprehensive test
source venv/bin/activate && ./final_test.sh
```

All 8 tests should pass:
```
============================== 8 passed in 0.39s ===============================
```

---

## 🚨 Known Expected Behaviors

1. **"Unable to locate credentials"** when AWS credentials missing → Normal, configure credentials
2. **"Access denied to Bedrock"** → Configure IAM permissions and enable model access
3. **Voice not available in Firefox** → Use Chrome, Edge, or Safari instead

---

## 🎉 You're Ready!

The application is **fully functional**. Once you configure your credentials:

1. Start the server: `python -m uvicorn backend.main:app --reload`
2. Open: `http://localhost:8000/frontend/index.html`
3. Try: "Find articles about marketing"
4. Enjoy! 🎤

---

**Need help?** 
- AWS Setup: [docs/AWS_SETUP.md](docs/AWS_SETUP.md)
- General Setup: [docs/SETUP.md](docs/SETUP.md)
- Recent Fixes: [AWS_CREDENTIALS_FIX.md](AWS_CREDENTIALS_FIX.md)

**Last Updated:** October 30, 2025 | **Version:** 1.0.0 MVP | **Status:** ✅ Ready