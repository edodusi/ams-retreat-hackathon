#!/bin/bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

echo "Testing health endpoint..."
curl -s http://localhost:8000/health | python -m json.tool

echo -e "\n\nServer started successfully!"
echo "Check logs above for any errors."

kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
