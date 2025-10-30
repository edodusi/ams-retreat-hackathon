# Storyblok Voice Assistant - User Guide

Quick reference guide for using the analytical and conversational features.

## Quick Start

### Basic Search
```
"Find marketing articles"
"Show me 5 blog posts about technology"
"Search for pages about our company"
```

### Analytical Queries
```
"How many articles mention Drupal?"
"Do we have any blog posts about React?"
"How many pages discuss AI?"
```

### Content Type Specific
```
"Find articles about web development"
"Show me blog posts about design"
"Get pages about our services"
```

---

## Conversational Patterns

### Pattern 1: Analyze → List
Ask for a count first, then view the results.

```
You: "How many articles mention GraphQL?"
Assistant: "I found 7 articles that mention GraphQL. Would you like me to list them?"

You: "Yes please"
Assistant: [Shows all 7 articles with previews]
```

### Pattern 2: Search → Refine
Search broadly, then narrow down.

```
You: "Find 10 marketing articles"
Assistant: [Shows 10 marketing articles]

You: "Out of those, which ones mention social media?"
Assistant: [Shows filtered subset]

You: "Show me the one about Instagram"
Assistant: [Shows specific article]
```

### Pattern 3: Clarify → Search
When unclear, the assistant asks for clarification.

```
You: "Find stories about JavaScript"
Assistant: "What type of content are you looking for? Articles, blog posts, pages, or all types?"

You: "Articles"
Assistant: [Shows articles about JavaScript]
```

### Pattern 4: Multi-Step Analysis
Combine analysis with refinement.

```
You: "How many articles do we have?"
Assistant: "I found 150 articles. Would you like me to list them?"

You: "How many mention React?"
Assistant: "I found 23 articles that mention React. Would you like me to list them?"

You: "Yes"
Assistant: [Shows 23 React articles]

You: "From these, show ones published this year"
Assistant: [Shows filtered results]
```

---

## Content Types

The assistant understands these content types:

| Type | Description | Example Query |
|------|-------------|---------------|
| `article` | News articles, blog articles | "Find articles about AI" |
| `blog_post` | Blog posts | "Show me blog posts about design" |
| `page` | Regular pages | "Get pages about our team" |
| `landing_page` | Landing pages | "Find landing pages for campaigns" |
| `post` | Generic posts | "Show posts about updates" |

### Automatic Detection
The assistant detects content types from your query:
- "Find **articles**" → filters to article type
- "Show **blog posts**" → filters to blog_post type
- "Get **pages**" → filters to page type

---

## Tips & Tricks

### Be Specific About Quantity
```
✓ "Find the first 5 articles"
✓ "Show me 3 blog posts"
✓ "Get 10 pages"
```

### Use Natural Language
```
✓ "How many articles mention Drupal?"
✓ "Do we have blog posts about React?"
✓ "Show me articles from this year"
```

### Combine Filters
```
✓ "Find 5 articles about marketing"
  → Type: article, Topic: marketing, Limit: 5

✓ "How many blog posts mention Vue?"
  → Type: blog_post, Topic: Vue, Action: count
```

### Progressive Refinement
```
1. "Find 20 articles about web development"
2. "Out of those, which mention React?"
3. "Show me the ones about TypeScript"
4. "Give me the most recent one"
```

---

## Understanding Responses

### Analysis Response
Shows count without listing items:
```
┌─────────────────────────────────┐
│ 📊 Analysis Results             │
│ 13 articles                     │
│ Matching: drupal                │
└─────────────────────────────────┘

"Would you like me to list them?"
```

### Search Response
Shows actual results:
```
┌─────────────────────────────────────────┐
│ 📄 Getting Started with Drupal         │
│ [article]                               │
│ This comprehensive guide covers...      │
│ /blog/getting-started-drupal            │
│ ID: 123456                              │
└─────────────────────────────────────────┘
```

### Clarification Response
Asks for more information:
```
"What type of content are you looking for? 
Articles, blog posts, pages, or all types?"
```

---

## Voice Commands

All text queries work with voice input!

### Clear Pronunciation
- Speak clearly and at normal pace
- Pause briefly between phrases
- Use natural language

### Examples
```
🎤 "How many articles mention Drupal"
🎤 "Find five blog posts about React"
🎤 "Show me pages about AI"
🎤 "Yes please list them"
```

---

## Common Workflows

### Workflow 1: Content Audit
```
1. "How many articles do we have?"
2. "How many mention [specific topic]?"
3. "Show me those articles"
4. Review and note which need updates
```

### Workflow 2: Topic Research
```
1. "Find articles about [topic]"
2. "How many mention [subtopic]?"
3. "Show me those"
4. "Which ones were published recently?"
```

### Workflow 3: Content Discovery
```
1. "Do we have blog posts about [topic]?"
2. "Yes, show them"
3. "Out of those, which mention [keyword]?"
4. "Give me the full details"
```

---

## Troubleshooting

### "I couldn't find any matching content"
- Try broader search terms
- Check spelling
- Try different content type
- Remove filters and search again

### "What type of content are you looking for?"
- The query was ambiguous
- Specify: articles, blog posts, pages, etc.
- Example: "Articles about React"

### Results don't match expected type
- Be more explicit: "articles only" or "just blog posts"
- Use content type in your query
- Refine results after initial search

### Count doesn't match when listed
- Content type filtering may reduce results
- This is expected behavior
- Analysis searches broadly, then filters by type

---

## Keyboard Shortcuts

- **Enter** - Send message
- **Tab** - Navigate between elements
- **Space** - Activate voice input (when focused on mic button)
- **Escape** - Stop voice recording

---

## Accessibility

### Screen Reader Support
- All interactive elements have ARIA labels
- Results announced automatically
- Clear focus indicators

### Keyboard Navigation
- Full keyboard access
- Logical tab order
- Visual focus indicators

### Voice Input/Output
- Speech-to-text for input
- Text-to-speech for responses
- Transcript display

---

## Best Practices

### 1. Start with Analysis
For large datasets, check count first:
```
"How many articles about [topic]?" → Get count
"Show them" → View results
```

### 2. Use Content Types
Be specific to get better results:
```
✓ "Find articles about React"
✗ "Find stuff about React"
```

### 3. Refine Progressively
Narrow down step by step:
```
1. Broad search
2. Filter by keyword
3. Further refinement
4. Select specific item
```

### 4. Leverage Context
The assistant remembers your conversation:
```
"Find marketing articles"
→ "Which ones mention social media?"
→ "Show me the one about Instagram"
```

---

## Examples by Use Case

### Content Manager
```
"How many articles need updating?"
"Show me articles from last year"
"Which ones mention outdated products?"
```

### Editor
```
"Find drafts about [topic]"
"Show me articles pending review"
"Which blog posts mention [keyword]?"
```

### SEO Specialist
```
"How many articles mention [keyword]?"
"Find pages with [term]"
"Show me articles about [trending topic]"
```

### Content Strategist
```
"How many blog posts do we have?"
"Which topics have the most coverage?"
"Find gaps in our content"
```

---

## Advanced Features

### Combining Multiple Filters
```
"Find 10 recent articles about marketing that mention social media"
```

### Contextual Follow-ups
```
Previous: "I found 15 articles"
You: "Show me the top 5"
```

### Natural Language Dates
```
"Articles from this year"
"Blog posts from last month"
"Recent pages"
```

---

## FAQ

**Q: Can I search multiple content types at once?**
A: Yes! Just don't specify a type, or say "all types"

**Q: How do I see full story details?**
A: Full story previews are shown automatically when available

**Q: Can I export results?**
A: Not yet - feature coming soon

**Q: Does it remember my previous searches?**
A: Yes, within the current conversation session

**Q: Can I use voice and text together?**
A: Yes! Switch between them freely

---

## Getting Help

### In-App
- Click the help icon for quick tips
- View conversation history to review past queries
- Use simple test queries to verify functionality

### Support
- Check documentation in `/docs` folder
- Review examples in this guide
- Test with simple queries first

---

**Version:** 1.2.0  
**Last Updated:** 2025-01-XX  
**Status:** Production Ready

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────┐
│ SEARCH                                           │
├──────────────────────────────────────────────────┤
│ "Find [type] about [topic]"                      │
│ "Show me [number] [type]"                        │
│ "Get [type] about [topic]"                       │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ ANALYZE                                          │
├──────────────────────────────────────────────────┤
│ "How many [type] mention [topic]?"               │
│ "Do we have [type] about [topic]?"               │
│ "Count [type] with [keyword]"                    │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ REFINE                                           │
├──────────────────────────────────────────────────┤
│ "Out of those, which mention [topic]?"           │
│ "From these, show [criteria]"                    │
│ "Filter by [keyword]"                            │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ CONFIRM                                          │
├──────────────────────────────────────────────────┤
│ "Yes please"                                     │
│ "Show them"                                      │
│ "List them"                                      │
└──────────────────────────────────────────────────┘
```

---

*Happy searching! 🚀*