#!/bin/bash
# JobGoblin 2.0 - Linux Launcher Script
# Quick launcher for the GUI application

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                     JOBGOBLIN 2.0 - JOB SCRAPER ULTIMATE                     ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Starting JobGoblin GUI..."
echo ""
echo "📋 Quick Setup Reminder:"
echo "   1. Get FREE API key: https://rapidapi.com"
echo "   2. Settings tab → Add RAPIDAPI_KEY"
echo "   3. Click Save → Start scraping with APIs!"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
else
    source venv/bin/activate
fi

# Check if dependencies are installed
if ! python -c "import ttkbootstrap" 2>/dev/null; then
    echo "📦 Installing missing dependencies..."
    pip install -q -r requirements.txt
fi

# Kill any existing instances
pkill -f "gui_app.py" 2>/dev/null || true
sleep 1

# Launch the GUI
echo "✨ Launching GUI application..."
python gui_app.py

# If GUI exits
echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "👋 JobGoblin closed. Thanks for using the scraper!"
echo "═══════════════════════════════════════════════════════════════════════════════"
