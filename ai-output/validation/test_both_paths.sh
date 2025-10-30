#!/bin/bash
source venv/bin/activate
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

echo "Testing /frontend/index.html..."
curl -s -I http://localhost:8000/frontend/index.html 2>&1 | head -5

echo -e "\nTesting /frontend/ ..."
curl -s -I http://localhost:8000/frontend/ 2>&1 | head -5

kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
