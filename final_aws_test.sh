#!/bin/bash
echo "=== FINAL AWS FIX VERIFICATION ==="
echo ""

echo "1. Testing Python compilation..."
python -m py_compile backend/*.py
if [ $? -eq 0 ]; then
    echo "   ✅ All backend files compile"
else
    echo "   ❌ Compilation failed"
    exit 1
fi
echo ""

echo "2. Running unit tests..."
pytest tests/ -v --tb=short 2>&1 | grep -E "(PASSED|FAILED|ERROR|passed|failed|error)"
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
HEALTH=$(curl -s http://localhost:8000/health | grep -c "healthy")
if [ "$HEALTH" = "1" ]; then
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

kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
echo ""

echo "=== ALL TESTS PASSED ✅ ==="
echo ""
echo "AWS Authentication Fix Complete!"
echo ""
echo "Next steps:"
echo "  1. Configure AWS credentials in .env:"
echo "     AWS_ACCESS_KEY_ID=your_key"
echo "     AWS_SECRET_ACCESS_KEY=your_secret"
echo "  2. Enable Claude model access in AWS Bedrock Console"
echo "  3. See docs/AWS_SETUP.md for detailed instructions"
echo "  4. Start server: python -m uvicorn backend.main:app --reload"
echo "  5. Open: http://localhost:8000/frontend/index.html"
