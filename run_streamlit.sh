#!/bin/bash
# Quick start script for Streamlit UI

echo "🔍 Starting AI Hallucination Meter..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Please create .env file with your API keys"
    echo "   See .env.example for reference"
    echo ""
fi

# Run Streamlit
streamlit run app/ui.py

