#!/bin/bash
echo "=== TESTING AWS BEDROCK CONNECTION ==="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Start the server with DEBUG mode enabled
echo "Starting server with DEBUG mode..."
DEBUG=true python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
echo "Waiting for server to start..."
sleep 5

echo ""
echo "1. Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ] && [ ! -z "$HEALTH" ]; then
    echo "$HEALTH" | python -m json.tool
    echo "   ✅ Health endpoint working!"
else
    echo "   ❌ Health endpoint failed - server may not be running"
fi
echo ""

echo "2. Testing Bedrock connection (debug endpoint)..."
echo "   Request: GET /api/test-bedrock"
echo ""
BEDROCK_RESPONSE=$(curl -s http://localhost:8000/api/test-bedrock)
if [ ! -z "$BEDROCK_RESPONSE" ]; then
    echo "$BEDROCK_RESPONSE" | python -m json.tool
else
    echo "   ❌ No response from server"
fi
echo ""

if echo "$BEDROCK_RESPONSE" | grep -q '"status": "success"'; then
    echo "   ✅ AWS Bedrock connection successful!"
elif echo "$BEDROCK_RESPONSE" | grep -q '"response"'; then
    echo "   ✅ AWS Bedrock connection successful!"
else
    echo "   ❌ AWS Bedrock connection failed"
    echo ""
    echo "   Checking error details..."
    ERROR=$(echo "$BEDROCK_RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); print(data.get('error', 'Unknown error'))" 2>/dev/null)
    if [ ! -z "$ERROR" ]; then
        echo "   Error: $ERROR"
        echo ""
        if echo "$ERROR" | grep -q "inference profile"; then
            echo "   💡 Fix: Update your .env file with:"
            echo "      BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0"
            echo "      (Use a model that supports ON_DEMAND)"
        elif echo "$ERROR" | grep -q "credentials"; then
            echo "   💡 Fix: Check your AWS credentials in .env file"
        fi
    fi
fi
echo ""

echo "3. Testing conversation endpoint with simple message..."
echo "   Request: POST /api/conversation"
echo "   Message: 'Hello, can you help me?'"
echo ""
CONV_RESPONSE=$(curl -s -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me?", "conversation_history": []}')
echo "$CONV_RESPONSE" | python -m json.tool
echo ""

if echo "$CONV_RESPONSE" | grep -q '"message"'; then
    echo "   ✅ Conversation endpoint working!"
else
    echo "   ❌ Conversation endpoint failed"
fi
echo ""

echo "4. Testing Storyblok connection (debug endpoint)..."
echo "   Request: GET /api/test-storyblok?term=test"
echo ""
STORYBLOK_RESPONSE=$(curl -s "http://localhost:8000/api/test-storyblok?term=test")
if [ ! -z "$STORYBLOK_RESPONSE" ]; then
    echo "$STORYBLOK_RESPONSE" | python -m json.tool
else
    echo "   ❌ No response from server"
fi
echo ""

if echo "$STORYBLOK_RESPONSE" | grep -q '"status": "success"'; then
    echo "   ✅ Storyblok connection successful!"
elif echo "$STORYBLOK_RESPONSE" | grep -q '"results"'; then
    echo "   ✅ Storyblok connection successful!"
else
    echo "   ❌ Storyblok connection failed"
    ERROR=$(echo "$STORYBLOK_RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); print(data.get('error', 'Unknown error'))" 2>/dev/null)
    if [ ! -z "$ERROR" ]; then
        echo "   Error: $ERROR"
    fi
fi

# Stop the server
echo ""
echo "Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo ""
echo "=== TEST COMPLETE ==="
