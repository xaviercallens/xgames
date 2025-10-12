#!/bin/bash
# Launch script for Bomberman game

echo "🎮 Bomberman Game Launcher"
echo "=========================="
echo ""

# Check if virtual environment exists
if [ ! -d "game_dev_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv game_dev_env"
    exit 1
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source game_dev_env/bin/activate

# Check if pygame is installed
if ! python -c "import pygame" 2>/dev/null; then
    echo "❌ Pygame not installed!"
    echo "Installing pygame..."
    pip install pygame
fi

# Check display
if [ -z "$DISPLAY" ]; then
    echo "⚠️  No DISPLAY variable set"
    echo "Setting DISPLAY=:0"
    export DISPLAY=:0
fi

echo "✓ Environment ready!"
echo ""
echo "🚀 Starting Bomberman..."
echo ""

# Run the game
python play_bomberman.py

# Deactivate on exit
deactivate
