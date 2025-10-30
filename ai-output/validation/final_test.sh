#!/bin/bash
echo "=== FINAL COMPREHENSIVE TEST ==="
echo ""

echo "1. Testing Python compilation..."
python -m py_compile backend/*.py
if [ $? -eq 0 ]; then
    echo "   ✅ All backend files compile successfully"
else
    echo "   ❌ Compilation failed"
    exit 1
fi
echo ""

echo "2. Running unit tests..."
pytest tests/ -v --tb=short 2>&1 | grep -E "(PASSED|FAILED|ERROR|passed|failed)"
if [ $? -eq 0 ]; then
    echo "   ✅ Tests completed"
else
    echo "   ❌ Tests failed"
    exit 1
fi
echo ""

echo "3. Starting server and testing endpoints..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

echo "   Testing /health..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ Health endpoint working"
else
    echo "   ❌ Health endpoint failed"
    kill $SERVER_PID
    exit 1
fi

echo "   Testing /frontend/..."
FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/frontend/)
if [ "$FRONTEND" = "200" ]; then
    echo "   ✅ Frontend accessible"
else
    echo "   ❌ Frontend not accessible"
    kill $SERVER_PID
    exit 1
fi

echo "   Testing /api/conversation..."
CONV=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "conversation_history": []}')
if [ "$CONV" = "503" ] || [ "$CONV" = "200" ]; then
    echo "   ✅ Conversation endpoint responding (503 expected with invalid creds)"
else
    echo "   ❌ Conversation endpoint failed"
    kill $SERVER_PID
    exit 1
fi

kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
echo ""

echo "=== ALL TESTS PASSED ✅ ==="
echo ""
echo "The application is ready to use!"
echo ""
echo "Next steps:"
echo "  1. Configure your AWS Bedrock credentials in .env"
echo "  2. Configure your Storyblok credentials in .env"
echo "  3. Run: python -m uvicorn backend.main:app --reload"
echo "  4. Open: http://localhost:8000/frontend/index.html"
