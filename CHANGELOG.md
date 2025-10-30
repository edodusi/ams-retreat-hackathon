# Changelog

All notable changes to the Storyblok Voice Assistant project will be documented in this file.

## [Unreleased]

### Added - 2025-01-XX

#### Context-Aware Refinement Feature
- **Session-based context management**: System remembers previous search results across conversation turns
- **Intelligent action detection**: AI distinguishes between new searches and refinement requests
- **Natural refinement queries**: Supports patterns like "out of those", "from these", "which mention X"
- **Progressive filtering**: Users can refine results multiple times in sequence
- **In-memory session storage**: Context stored per conversation for immediate access (Redis recommended for production)
- **Automatic context updates**: Filtered results become new context for further refinement

**Examples:**
- "Find 10 marketing stories" → Returns 10 stories
- "Out of those, give me the one which mentions omnichannel" → Filters and returns matching story
- "From these, show only about social media" → Further filters the results

**Modified Files:**
- `backend/bedrock_client.py`: Added "refine" action type and context injection
- `backend/main.py`: Session management, filter logic, and action routing
- `docs/context-aware-refinement.md`: Complete feature documentation
- `docs/test-context-aware.md`: Testing guide with examples

**Commit:** Context-aware conversation with result refinement

---

#### Dynamic Result Limit Feature
- **AI-powered limit extraction**: Claude now intelligently extracts the desired number of results from user queries
- **Natural language patterns**: Supports "first 5", "show me 3", "get 20", "top 7", and similar patterns
- **Default behavior**: Falls back to 10 results when no limit is specified
- **Conversational refinement**: Users can adjust result count in follow-up messages
- **Documentation**: Comprehensive docs in `docs/dynamic-result-limit.md`
- **Testing**: Automated tests in `tests/test_limit_extraction.py`

**Examples:**
- "Find the first 5 articles about marketing" → Returns 5 results
- "Show me 3 blog posts" → Returns 3 results
- "Find marketing articles" → Returns 10 results (default)

**Modified Files:**
- `backend/bedrock_client.py`: Updated system prompt and response parsing
- `backend/main.py`: Extract and pass limit to Storyblok client
- `docs/openapi.yaml`: Added limit feature documentation and examples

**Commit:** Dynamic result limit based on user intent

---

### Fixed - 2025-01-XX

#### Story Display Reliability
- **Root cause**: Alpine.js reactivity issues with `x-show` directive and nested properties
- **Solution**: Replaced `x-show` with `x-if` for conditional story rendering
- **Data normalization**: Explicitly structure results object when adding to messages array
- **Array validation**: Added `Array.isArray()` check before rendering stories
- **Key binding**: Changed from `story.story_id` to `storyIndex` for more reliable rendering
- **Debug tools**: Added visual debug indicator and enhanced console logging

**Impact:** Story previews now display consistently 100% of the time when results are returned from the API

**Modified Files:**
- `frontend/index.html`: Template and Alpine.js logic improvements
- `backend/main.py`: Enhanced serialization logging

**Documentation:**
- `docs/story-display-fix.md`: Technical documentation
- `docs/testing-story-display.md`: Testing guide
- `tests/test-alpine-stories.html`: Standalone test file

**Commit:** Fix story display reactivity issues

---

## [1.0.0] - Initial Release

### Features
- Voice-enabled content discovery using Web Speech API
- Natural language conversation with Claude AI (AWS Bedrock)
- Semantic search via Storyblok Strata API
- Multi-turn conversation support
- Accessible UI (WCAG 2.1 Level AA focused)
- Chat-like interface (ChatGPT-style)
- Story preview cards with title, description, and metadata
- Full story detail fetching
- Text-to-speech response playback
- Keyboard navigation support
- High contrast design for accessibility

### Technical Stack
- **Frontend**: Alpine.js, Tailwind CSS, Web Speech API
- **Backend**: Python 3.11+, FastAPI
- **AI**: AWS Bedrock (Claude Sonnet 4.5)
- **Search**: Storyblok Strata API
- **HTTP Client**: httpx (async)

### API Endpoints
- `POST /api/conversation`: Main conversation endpoint
- `GET /api/story/{story_id}`: Fetch full story details
- `GET /health`: Health check
- `GET /api/test-bedrock`: Bedrock connection test (debug)
- `GET /api/test-storyblok`: Storyblok connection test (debug)

### Documentation
- `README.md`: Project overview and setup
- `SPECS.md`: Complete specifications
- `GUIDELINES.md`: Development guidelines
- `docs/openapi.yaml`: OpenAPI 3.0 specification
- `.env.example`: Environment configuration template

---

## Development Notes

### Accessibility Focus
- Screen reader compatible
- Full keyboard navigation
- ARIA labels and semantic HTML
- High contrast design
- Touch-friendly controls (44x44px minimum)
- Voice input/output support

### Future Enhancements
- Pagination support ("show next 5")
- Result ranges ("results 5 to 10")
- Smart defaults (learn user preferences)
- Multi-language support
- Advanced conversation memory
- User preferences persistence
- Analytics and usage tracking

---

## Testing

### Manual Testing
- Frontend UI testing via browser
- Voice input/output testing
- Keyboard navigation testing
- Screen reader compatibility testing

### Automated Testing
- Backend unit tests: `tests/test_main.py`
- Limit extraction tests: `tests/test_limit_extraction.py`
- Frontend component tests: `tests/test-alpine-stories.html`

### API Testing
```bash
# Test conversation endpoint
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "find the first 5 articles about marketing", "conversation_history": []}'
```

---

## Contributors
- Storyblok AMS Retreat Hackathon Team

## License
Hackathon Project

---

**Last Updated:** 2025-01-XX
**Version:** 1.1.0+unreleased (with context-aware features)