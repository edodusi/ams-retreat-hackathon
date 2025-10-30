# Features Documentation

## Overview

The Storyblok Voice Assistant provides voice-enabled content discovery through natural conversation. This document details all implemented features and their usage.

---

## Core Features

### 1. Voice Input (Speech-to-Text)

Enable users to search for content using their voice instead of typing.

**Capabilities:**
- Real-time speech recognition using Web Speech API
- Continuous listening with interim results display
- Visual feedback during recording
- Automatic message sending when speech ends

**How to Use:**
1. Click the microphone button (blue circle)
2. Speak your query clearly
3. The system displays your words as you speak
4. Speech automatically stops and sends when you finish

**Browser Support:**
- ✅ Google Chrome 90+
- ✅ Microsoft Edge 90+
- ✅ Safari 14.1+
- ❌ Firefox (limited support)

**Example Queries:**
- "Find all marketing articles"
- "Show me blog posts about technology"
- "I need content about product launches"

**Accessibility:**
- Large, touch-friendly button (min 44x44px)
- Clear visual indication when recording (red pulsing)
- ARIA labels for screen readers
- Keyboard accessible (Tab + Enter)

---

### 2. Voice Output (Text-to-Speech)

Hear the assistant's responses read aloud automatically.

**Capabilities:**
- Automatic text-to-speech for all responses
- Natural, conversational speech synthesis
- Only reads the conversational part (not metadata)

**How It Works:**
- After the assistant responds, the message is automatically spoken
- Result counts and technical details are visual-only
- Clean, natural reading voice

**Configuration:**
- Uses browser's default voice
- Standard speech rate (1.0)
- Normal pitch and volume

**Accessibility:**
- Enables hands-free operation
- Critical for visually impaired users
- Can be muted via browser controls

---

### 3. Natural Language Conversation

Interact with the assistant using everyday language.

**Capabilities:**
- Multi-turn conversations with context awareness
- Natural language understanding via Claude
- Intent detection (search vs. chat)
- Query refinement through follow-ups

**Conversation Types:**

**Simple Search:**
```
User: "Find articles about marketing"
Assistant: "I found 15 marketing articles..."
[Shows preview cards]
```

**Refinement:**
```
User: "Find blog posts"
Assistant: "I found 50 blog posts..."

User: "Show only recent ones"
Assistant: "Here are 12 blog posts from this month..."
[Updated results]
```

**Casual Chat:**
```
User: "Hello"
Assistant: "Hi! How can I help you search for content today?"
```

**Context Retention:**
- Maintains up to 10 previous messages
- Understands references to previous queries
- Enables iterative search refinement

---

### 4. Content Search

Semantic search powered by Storyblok Strata.

**Capabilities:**
- Semantic search (not just keyword matching)
- Natural language query interpretation
- Returns up to 10 results per query
- Rich metadata in results

**Search Parameters:**
- **Term**: Extracted from user's natural language
- **Limit**: 10 results (configurable)
- **Offset**: 0 (pagination support ready)

**Result Fields:**
- Story ID and name
- Full slug/URL path
- Title (extracted from content)
- Description (extracted, max 200 chars)
- Publication dates

**How It Works:**
1. User asks for content in natural language
2. Claude extracts key search terms
3. System queries Storyblok Strata
4. Results formatted as preview cards
5. Assistant provides conversational context

---

### 5. Story Preview Cards

Visual display of search results in an accessible format.

**Design:**
- Clean card layout with clear hierarchy
- Title in large, bold text
- Description in readable gray text
- URL path and publication date
- Hover/focus states for interactivity

**Content Displayed:**
- **Title**: Primary heading (from content or story name)
- **Description**: Brief excerpt (max 200 characters)
- **Slug**: Full URL path to the story
- **Published Date**: Human-readable date format

**Accessibility:**
- High contrast (4.5:1 minimum)
- Focus indicators on all cards
- Semantic HTML (article elements)
- ARIA labels for context
- Keyboard navigable (Tab key)

**Example Card:**
```
┌─────────────────────────────────────────┐
│ Marketing Strategy 2025                 │
│ A comprehensive guide to modern         │
│ marketing tactics and trends...         │
│                                         │
│ /blog/marketing-strategy-2025           │
│ Published: Jan 15, 2025                 │
└─────────────────────────────────────────┘
```

---

### 6. Chat-Like Interface

Familiar conversation UI similar to modern chat applications.

**Layout:**
- **User messages**: Right-aligned, blue background
- **Assistant messages**: Left-aligned, light gray background
- **Story cards**: Below assistant messages
- **Scrollable history**: Auto-scroll to latest

**Visual Design:**
- Clean, minimalist aesthetic
- High contrast for readability
- Responsive layout (desktop and mobile)
- Smooth animations and transitions

**Components:**
- Header with status indicator
- Scrollable message area
- Fixed input footer
- Welcome message for new users

---

### 7. Keyboard Navigation

Full keyboard accessibility for users who cannot use voice or mouse.

**Navigation:**
- **Tab**: Move between interactive elements
- **Enter**: Activate buttons, send messages
- **Escape**: Cancel voice recording (if active)
- **Arrow keys**: Scroll message history

**Focus Indicators:**
- Visible 3px blue outline
- 2px offset for clarity
- Applied to all interactive elements

**Text Input Alternative:**
- Full-featured text input field
- Works identically to voice input
- Submit with Enter or Send button

---

### 8. Accessibility Features

WCAG 2.1 Level AA compliant design.

**Perceivable:**
- 4.5:1 contrast ratio minimum
- 16px base font size (readable)
- Scalable text (up to 200%)
- Visual alternatives for audio (transcripts)
- Color not sole indicator

**Operable:**
- All functionality keyboard accessible
- No keyboard traps
- Large touch targets (44x44px minimum)
- Visible focus indicators
- Generous click/tap areas

**Understandable:**
- Clear, simple language
- Predictable navigation
- Consistent interaction patterns
- Error messages with guidance
- Status indicators with labels

**Robust:**
- Valid, semantic HTML5
- ARIA labels and roles
- Screen reader compatible
- Cross-browser tested
- Progressive enhancement

**Screen Reader Support:**
- All buttons properly labeled
- Role attributes for sections
- Live regions for updates (aria-live)
- Status announcements

---

### 9. Real-Time Feedback

Immediate visual and audio feedback for all actions.

**Status Indicators:**
- **Green dot**: Ready for input
- **Red dot**: Recording voice
- **Yellow dot**: Processing request

**Processing States:**
- Loading spinner during API calls
- "Thinking..." message
- Disabled inputs during processing
- Send button shows "Sending..."

**Transcript Display:**
- Real-time display of spoken words
- Interim results as you speak
- Visual confirmation before sending

**Error Handling:**
- Clear error messages
- Non-blocking notifications
- Auto-dismiss after 5 seconds
- Suggested actions for resolution

---

### 10. Multi-Turn Conversations

Context-aware conversations spanning multiple exchanges.

**How It Works:**
1. Each message pair stored in history
2. Last 10 messages sent to Claude for context
3. Claude understands references to previous queries
4. Results updated based on refinements

**Example Flow:**
```
Turn 1:
User: "Find marketing content"
Assistant: [15 results shown]

Turn 2:
User: "Only from this year"
Assistant: [8 results, filtered]

Turn 3:
User: "Show me the most recent"
Assistant: [3 results, sorted by date]
```

**Benefits:**
- Natural, human-like interaction
- Iterative refinement without repetition
- Understanding of implicit references
- Efficient search narrowing

---

## Technical Features

### API Integration

**AWS Bedrock (Claude):**
- Model: `anthropic.claude-sonnet-4-5-v1:0`
- Converse API for chat functionality
- Structured response parsing (JSON)
- Error handling and retries

**Storyblok Strata:**
- Semantic search API
- Rich metadata retrieval
- Fast response times (<1s typical)

### Performance

**Response Times:**
- Voice recognition: Instant
- API calls: 1-3 seconds typical
- Result rendering: <100ms

**Optimization:**
- Async/await for all I/O
- Efficient DOM updates
- Minimal JavaScript bundle
- CDN-hosted dependencies

### Browser Compatibility

**Fully Supported:**
- Chrome 90+
- Edge 90+
- Safari 14.1+

**Partial Support:**
- Firefox (text input only, no voice)
- Mobile browsers (iOS Safari, Chrome Android)

---

## Usage Examples

### Basic Search

1. Click microphone or type in text field
2. Say/type: "Find blog posts about technology"
3. View results in preview cards
4. Click or focus on cards for details

### Refined Search

1. Perform initial search
2. Say/type: "Show only recent ones"
3. View filtered results
4. Continue refining as needed

### Voice-Only Operation

1. Click microphone button
2. Speak your query
3. Listen to spoken response
4. Speak refinement query
5. Repeat as needed

### Keyboard-Only Operation

1. Tab to text input field
2. Type your query
3. Tab to Send button or press Enter
4. Tab through result cards
5. Use arrow keys to scroll

---

## Configuration Options

Available via environment variables:

| Setting | Default | Description |
|---------|---------|-------------|
| `MAX_CONVERSATION_HISTORY` | 10 | Messages retained for context |
| `DEFAULT_SEARCH_LIMIT` | 10 | Results per search |
| `REQUEST_TIMEOUT` | 30 | API timeout (seconds) |
| `CORS_ORIGINS` | localhost:8000 | Allowed frontend origins |

---

## Known Limitations

1. **Voice Support**: Not available in all browsers (Firefox limited)
2. **Language**: Currently English only
3. **History**: Not persisted between sessions
4. **Results**: Limited to 10 per query (pagination not in UI)
5. **Offline**: Requires internet connection

---

## Future Enhancements

Planned features for future releases:

- [ ] Multi-language support (Spanish, German, French)
- [ ] Voice customization (speed, pitch, voice selection)
- [ ] Result pagination in UI
- [ ] Search history persistence
- [ ] Export results to CSV/JSON
- [ ] Advanced filters (date range, author, tags)
- [ ] Thumbnail previews for stories
- [ ] Direct story editing links
- [ ] Collaborative sessions
- [ ] Mobile app (iOS/Android)

---

**Last Updated**: October 30, 2025  
**Version**: 1.0.0