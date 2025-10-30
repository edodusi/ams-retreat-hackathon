# Voice-Enabled Content Discovery for Storyblok
## Hackathon Project Specifications

**Project Name:** Storyblok Voice Assistant  
**Date:** October 30, 2025

---

## 🎯 Project Overview

Accessible voice-powered AI agent for discovering Storyblok content through natural conversation using AWS Bedrock and Storyblok Strata.

**Value:** Enable users (especially those with disabilities) to find content through voice rather than traditional UI, making content discovery fully accessible.

**Target Users:** Content editors with visual/motor disabilities, and anyone preferring voice interaction  
**Accessibility:** WCAG 2.1 Level AA compliant

---

## 🎨 User Journey

1. **Initiation:** User opens the interface and activates voice input
2. **Query:** User speaks their content search request (e.g., "Find all marketing articles published last month")
3. **Processing:** AI agent interprets the request and queries Storyblok Strata
4. **Response:** System presents results via voice and visual display
5. **Iteration:** User refines their search through follow-up questions
6. **Action:** User selects content or continues refining

---

## ✨ Key Features

### 1. Voice Interface
- Real-time speech-to-text and text-to-speech
- Push-to-talk activation
- Multi-turn conversation support
- Visual transcript display

### 2. AI Models (AWS Bedrock)
- **Conversation Agent:** `anthropic.claude-sonnet-4-5-v1:0` (latest, best reasoning & context)
- **Speech-to-Text:** Web Speech API (browser native)
- **Text-to-Speech:** Web Speech API (browser native)
- **Region:** us-east-1

### 3. Content Search (Storyblok Strata)
- Semantic search via `vsearches` endpoint
- **Client Options:**
  - Direct HTTP calls with httpx/fetch
  - storyblok-js-client (use `endpoint` param to set custom base URL)
- **Parameters:** `term`, `limit`, `offset`
- Returns metadata-rich results

### 4. Accessible UI
- **Layout:** Chat-like interface similar to ChatGPT (conversation-oriented)
- **Message bubbles:** User messages (right), agent responses (left)
- **Story previews:** Display title and description in card/box format within agent responses
- High contrast, large typography, minimal layout
- Full keyboard navigation with focus indicators
- ARIA labels and semantic HTML
- Screen reader compatible
- Touch-friendly controls (44x44px min)

### 5. Iterative Refinement
- Conversation history display (scrollable chat)
- Natural follow-up questions
- Voice-based result filtering
- Story previews update dynamically with each refinement

---

## 🏗️ Technical Architecture

### System Components

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │ (Voice/Keyboard)
       ▼
┌─────────────────────────────────┐
│   Frontend Application          │
│   - Voice Input/Output          │
│   - Accessible UI Components    │
│   - Conversation Display        │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Backend API/Middleware        │
│   - Request orchestration       │
│   - Session management          │
│   - Response formatting         │
└──────┬──────────────────────────┘
       │
       ├──────────────────┐
       ▼                  ▼
┌──────────────┐   ┌──────────────┐
│ AWS Bedrock  │   │  Storyblok   │
│   (Claude)   │   │    Strata    │
└──────────────┘   └──────────────┘
```

### Tech Stack

**Frontend:**
- **Framework:** Alpine.js (lightweight, declarative)
- **Voice:** Web Speech API (native browser support)
- **Styling:** Tailwind CSS with accessibility focus
- **UI Pattern:** Chat interface (ChatGPT-like) with message bubbles and story preview cards
- **Template:** HTML5 with semantic markup

**Backend:**
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **HTTP Client:** httpx for async requests

**APIs:**
- **AWS Bedrock:** Converse API via HTTPS
- **Storyblok Strata:** REST API via storyblok-js-client (with custom endpoint)

---

## 🔐 Configuration

See `.env.example` for required environment variables. Copy to `.env` and fill with your credentials.

---

## 📋 API Integration Examples

### AWS Bedrock (Python)
```python
import httpx

url = f"https://bedrock-runtime.{region}.amazonaws.com/model/anthropic.claude-sonnet-4-5-v1:0/converse"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AWS_BEARER_TOKEN_BEDROCK}"
}
body = {
    "messages": [{"role": "user", "content": [{"text": query}]}]
}
response = await httpx.post(url, headers=headers, json=body)
```

### Storyblok Strata (Python with httpx)
```python
url = f"{STORYBLOK_API_BASE}/v1/spaces/{STORYBLOK_SPACE_ID}/vsearches"
headers = {
    "Content-Type": "application/json",
    "Authorization": STORYBLOK_TOKEN
}
params = {"term": search_term, "limit": 10, "offset": 0}
response = await httpx.get(url, headers=headers, params=params)
```

### Storyblok Strata (JavaScript with storyblok-js-client)
```javascript
import StoryblokClient from 'storyblok-js-client';

// Initialize client with custom endpoint for Strata
const Storyblok = new StoryblokClient({
  accessToken: process.env.STORYBLOK_TOKEN,
  endpoint: 'https://api-staging-d1.storyblok.com'
});

// Query Strata vsearches
const response = await Storyblok.get(`spaces/${STORYBLOK_SPACE_ID}/vsearches`, {
  term: searchTerm,
  limit: 10,
  offset: 0
});
```

---

## 🔄 Conversation Flow Examples

### Example 1: Simple Search
```
User: "Find articles about marketing"

Agent: "I found 15 marketing articles. Here are the top results:

┌─────────────────────────────────────────┐
│ Marketing Strategy 2025                 │
│ A comprehensive guide to modern         │
│ marketing tactics and trends...         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Social Media Best Practices             │
│ Learn how to maximize your social       │
│ media presence with proven strategies   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Content Marketing Fundamentals          │
│ Essential tips for creating engaging    │
│ content that converts                   │
└─────────────────────────────────────────┘

Would you like me to refine these results by date, category, or author?"

User: "Show only recent ones"

Agent: "Here are 8 marketing articles from the last month:

┌─────────────────────────────────────────┐
│ Marketing Strategy 2025                 │
│ A comprehensive guide to modern         │
│ marketing tactics and trends...         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ AI in Marketing: What's Next            │
│ Exploring the future of AI-powered      │
│ marketing automation                    │
└─────────────────────────────────────────┘

Any other refinements you'd like?"
```

### Example 2: Complex Query
```
User: "I need blog posts about product launches"

Agent: "I found 23 blog posts about product launches. Here's a preview:

┌─────────────────────────────────────────┐
│ Launching Your Product Successfully     │
│ Step-by-step guide to a winning         │
│ product launch strategy                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Product Launch Checklist 2025           │
│ Don't miss these critical steps for     │
│ your next launch                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Case Study: Tech Product Launch         │
│ How we achieved 10k users in 30 days    │
│ through strategic planning              │
└─────────────────────────────────────────┘

Would you like to filter by date, author, or category?"

User: "From this year only"

Agent: "Narrowed down to 12 blog posts from 2025:

┌─────────────────────────────────────────┐
│ Product Launch Checklist 2025           │
│ Don't miss these critical steps for     │
│ your next launch                        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 2025 Launch Trends                      │
│ What's working in product launches      │
│ this year                               │
└─────────────────────────────────────────┘

Need more refinement?"
```

---

## ♿ Accessibility Requirements (WCAG 2.1 AA)

1. **Perceivable:** Text alternatives, 4.5:1 contrast, resizable text
2. **Operable:** Full keyboard access, clear focus, no traps
3. **Understandable:** 16px+ text, predictable navigation, error handling
4. **Robust:** Valid HTML, ARIA labels, screen reader tested

**Voice Specific:** Audio output, visual transcripts, text input fallback

---

## 🎯 Success Metrics

- **Accessibility:** Pass WCAG 2.1 AA automated tests
- **Voice Recognition:** >90% accuracy for common queries
- **Search Relevance:** User finds desired content in <3 iterations
- **Response Time:** <2 seconds from voice input to AI response
- **User Satisfaction:** Positive feedback from accessibility testing

---

## 🚀 Development Phases

### Phase 1: MVP (Hackathon Scope)
- [ ] Basic voice input/output
- [ ] Chat-like UI with message bubbles (user right, agent left)
- [ ] Story preview cards (title + description) in agent responses
- [ ] AWS Bedrock integration
- [ ] Storyblok Strata search integration
- [ ] Basic conversation context (2-3 turns)
- [ ] Keyboard accessibility

### Phase 2: Enhanced Features (Post-Hackathon)
- [ ] Advanced conversation memory
- [ ] Multi-language support
- [ ] Voice customization options
- [ ] Result previews and thumbnails
- [ ] User preferences persistence
- [ ] Analytics and usage tracking

### Phase 3: Production Ready
- [ ] Complete WCAG audit
- [ ] Performance optimization
- [ ] Security hardening
- [ ] User testing with disabled users
- [ ] Documentation and training materials

---

## 🔧 Technical Considerations

- **Security:** Environment variables, rate limiting, input sanitization, HTTPS only
- **Performance:** Debounce voice input, cache queries, lazy loading
- **Error Handling:** Graceful degradation, retry logic, text fallback
- **Browser Support:** Modern browsers with Web Speech API, progressive enhancement

---

## 📚 Resources

- [AWS Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [Storyblok Strata Docs](https://www.storyblok.com/docs/strata)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Alpine.js](https://alpinejs.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## 🎉 Demo Script

1. **Introduction** (30 sec)
   - Show the problem: Traditional UI barriers for disabled users
   
2. **Demo Flow** (2 min)
   - Voice search: "Find all blog posts about technology"
   - Show results with visual + audio feedback
   - Display story preview cards (title + description)
   - Refine: "Only from this year"
   - Show updated results with new preview cards
   
3. **Accessibility Showcase** (1 min)
   - Keyboard navigation demo
   - Screen reader compatibility
   - High contrast mode
   
4. **Technical Highlights** (30 sec)
   - AWS Bedrock integration
   - Storyblok Strata search
   - Real-time conversation

---

**Last Updated:** October 30, 2025  
**Status:** Ready for Development
