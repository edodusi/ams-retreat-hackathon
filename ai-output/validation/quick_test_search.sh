#!/bin/bash
echo "==================================="
echo "Quick Search Test"
echo "==================================="
echo ""

# Test if server is running
echo "1. Checking server..."
HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
if [ -z "$HEALTH" ]; then
    echo "❌ Server not running. Start with:"
    echo "   DEBUG=true python -m uvicorn backend.main:app --reload"
    exit 1
fi
echo "✅ Server is running"
echo ""

echo "2. Testing search query..."
echo "Query: 'find all marketing stories'"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "find all marketing stories", "conversation_history": []}')

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool

echo ""
echo "3. Analyzing response..."

# Check for results
if echo "$RESPONSE" | grep -q '"results"'; then
    if echo "$RESPONSE" | grep -q '"stories"'; then
        STORY_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('results', {}).get('stories', [])))" 2>/dev/null || echo "0")
        echo "✅ Results field present"
        echo "✅ Stories array present"
        echo "   Story count: $STORY_COUNT"
        
        if [ "$STORY_COUNT" -gt 0 ]; then
            echo ""
            echo "First story fields:"
            echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); story=data['results']['stories'][0]; print(f'  - body: {len(story.get(\"body\", \"\"))} chars'); print(f'  - name: {story.get(\"name\", \"N/A\")}'); print(f'  - slug: {story.get(\"slug\", \"N/A\")}'); print(f'  - story_id: {story.get(\"story_id\", \"N/A\")}');" 2>/dev/null
        fi
    else
        echo "❌ Results present but no stories array"
    fi
else
    echo "❌ No results field in response"
    echo ""
    echo "Message field:"
    echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'  {data.get(\"message\", \"N/A\")}')" 2>/dev/null
fi

echo ""
echo "==================================="
echo "Check server logs for details with markers like:"
echo "  >>> PERFORMING SEARCH"
echo "  >>> SEARCH RETURNED"
echo "==================================="
