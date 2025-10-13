#!/bin/bash
# Play Bomberman with Hybrid AI (Heuristics + Reinforcement Learning)

echo "=================================="
echo "🎭 HYBRID AI MODE LAUNCHER"
echo "=================================="
echo ""
echo "Select Hybrid Strategy:"
echo "1) Heuristic Primary (80% heuristics, 20% RL)"
echo "2) Balanced (50% heuristics, 50% RL) [DEFAULT]"
echo "3) RL Primary (20% heuristics, 80% RL)"
echo "4) Adaptive (Chooses based on confidence)"
echo ""
read -p "Choice [1-4] (default: 2): " choice

case $choice in
    1)
        MODE="heuristic_primary"
        echo "🌱 Using Heuristic Primary mode"
        ;;
    3)
        MODE="rl_primary"
        echo "🤖 Using RL Primary mode"
        ;;
    4)
        MODE="adaptive"
        echo "🎯 Using Adaptive mode"
        ;;
    *)
        MODE="balanced"
        echo "⚖️  Using Balanced mode"
        ;;
esac

echo ""
echo "🎮 Starting game with Hybrid AI..."
echo "   Mode: $MODE"
echo "   Combines: Heuristics + PPO Model"
echo ""

# Set environment variables and run
export BOMBERMAN_HYBRID_MODE=true
export BOMBERMAN_HYBRID_STRATEGY=$MODE

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

python play_bomberman.py
