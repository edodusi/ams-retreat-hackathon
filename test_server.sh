#!/bin/bash
source venv/bin/activate
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

echo "Testing health endpoint..."
curl -s http://localhost:8000/health | python -m json.tool

echo -e "\n\nTesting conversation endpoint..."
curl -s -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}' | python -m json.tool

kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
