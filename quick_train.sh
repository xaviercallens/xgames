#!/bin/bash
# Quick training starter - no prompts, just runs
# Usage: ./quick_train.sh

echo "🌙 Starting Overnight Training..."

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Create directories
mkdir -p bomber_game/models/checkpoints bomber_game/models/plots

# Start training in background
nohup python overnight_training.py > training_output.log 2>&1 &
PID=$!

echo "✅ Training started (PID: $PID)"
echo ""
echo "📊 Monitor progress:"
echo "   python monitor_training.py"
echo ""
echo "📝 View logs:"
echo "   tail -f training_output.log"
echo ""
echo "🛑 Stop training:"
echo "   kill $PID"
echo ""
echo "💾 Save PID for later:"
echo $PID > training.pid
echo "   Saved to training.pid"
