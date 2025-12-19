#!/bin/bash

echo ""
echo "========================================"
echo "  Document AI Assistant"
echo "  Starting Application..."
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create a .env file with your OpenAI API key."
    echo "You can copy .env.example and add your key."
    echo ""
    echo "Or you can enter it in the web interface."
    echo ""
fi

echo "Starting Streamlit server..."
echo "Open your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
