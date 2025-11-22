#!/bin/bash
# Quick start script for FastAPI server

echo "🔍 Starting AI Hallucination Meter API..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Please create .env file with your API keys"
    echo "   See .env.example for reference"
    echo ""
fi

# Run FastAPI
python app/api.py

