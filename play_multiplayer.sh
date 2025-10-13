#!/bin/bash
# Play Bomberman in Multiplayer Mode (1 Human + 0-3 AI Opponents)

echo "========================================"
echo "🎮 BOMBERMAN MULTIPLAYER MODE"
echo "========================================"
echo ""
echo "Features:"
echo "  • 1 Human Player"
echo "  • 0-3 AI Opponents"
echo "  • Choose AI difficulty for each opponent"
echo "  • 4 spawn positions (corners of map)"
echo ""
echo "Starting multiplayer game..."
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run multiplayer game
python -c "from bomber_game.multiplayer_engine import main; main()"
