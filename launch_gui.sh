#!/bin/bash
# Launch Job Scraper Ultimate GUI

echo "========================================="
echo " Job Scraper Ultimate - GUI Edition"
echo "========================================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Setting up for first time..."
    echo "Creating virtual environment..."
    python3 -m venv .venv
    
    if [ $? -ne 0 ]; then
        echo "Error: Python not found. Please install Python 3.8 or later."
        exit 1
    fi
    
    echo "Installing requirements..."
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Create output directory
mkdir -p output

echo "Launching GUI..."
echo ""

python gui_app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error launching GUI. Make sure all requirements are installed."
    echo "Try running: pip install -r requirements.txt"
    read -p "Press Enter to continue..."
fi
