#!/bin/bash

# Storyblok Voice Assistant - Startup Script
# This script starts both the backend server and opens the frontend

set -e

echo "🚀 Starting Storyblok Voice Assistant..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and configure it"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Environment ready"
echo ""

# Start the backend server
echo "🌐 Starting backend server on http://localhost:8000..."
echo "📱 Frontend will be available at http://localhost:8000/frontend/index.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Change to project root and run uvicorn
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload