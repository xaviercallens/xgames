#!/bin/bash
# Quick launcher for overnight training
# Usage: ./start_overnight_training.sh

set -e

echo "=================================="
echo "🌙 OVERNIGHT TRAINING LAUNCHER"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# Check PyTorch
if ! python3 -c "import torch" 2>/dev/null; then
    echo "⚠️  PyTorch not found. Installing..."
    pip3 install torch
fi

# Create output directory
mkdir -p bomber_game/models/checkpoints
mkdir -p bomber_game/models/plots

# Ask user for training mode
echo "Select training mode:"
echo "1) Quick test (1 hour, 1000 episodes)"
echo "2) Overnight (8 hours, 10000 episodes) [DEFAULT]"
echo "3) Weekend (48 hours, 50000 episodes)"
echo "4) Custom"
echo ""
read -p "Choice [1-4] (default: 2): " choice
choice=${choice:-2}

case $choice in
    1)
        EPISODES=1000
        HOURS=1
        echo "📊 Quick test mode: 1000 episodes, 1 hour"
        ;;
    2)
        EPISODES=10000
        HOURS=8
        echo "🌙 Overnight mode: 10000 episodes, 8 hours"
        ;;
    3)
        EPISODES=50000
        HOURS=48
        echo "📅 Weekend mode: 50000 episodes, 48 hours"
        ;;
    4)
        read -p "Episodes: " EPISODES
        read -p "Hours: " HOURS
        echo "⚙️  Custom mode: $EPISODES episodes, $HOURS hours"
        ;;
    *)
        EPISODES=10000
        HOURS=8
        echo "🌙 Default overnight mode: 10000 episodes, 8 hours"
        ;;
esac

# Update config in training script
sed -i "s/^TOTAL_EPISODES = .*/TOTAL_EPISODES = $EPISODES/" overnight_training.py
sed -i "s/^TRAINING_HOURS = .*/TRAINING_HOURS = $HOURS/" overnight_training.py

echo ""
echo "✅ Configuration updated"
echo ""

# Ask for execution mode
echo "Select execution mode:"
echo "1) Foreground (see output, can't close terminal)"
echo "2) Background with nohup (recommended)"
echo "3) Screen session (persistent)"
echo "4) tmux session (persistent)"
echo ""
read -p "Choice [1-4] (default: 2): " exec_choice
exec_choice=${exec_choice:-2}

echo ""

case $exec_choice in
    1)
        echo "🚀 Starting training in foreground..."
        echo "💡 Press Ctrl+C to stop (will save checkpoint)"
        echo ""
        sleep 2
        python3 overnight_training.py
        ;;
    2)
        echo "🚀 Starting training in background..."
        nohup python3 overnight_training.py > training_output.log 2>&1 &
        PID=$!
        echo "✅ Training started (PID: $PID)"
        echo ""
        echo "📊 Monitor progress:"
        echo "   python3 monitor_training.py"
        echo ""
        echo "📝 View logs:"
        echo "   tail -f training_output.log"
        echo "   tail -f bomber_game/models/training_log.txt"
        echo ""
        echo "🛑 Stop training:"
        echo "   kill $PID"
        echo ""
        
        # Ask if user wants to start monitor
        read -p "Start monitor now? [y/N]: " start_monitor
        if [[ $start_monitor =~ ^[Yy]$ ]]; then
            sleep 2
            python3 monitor_training.py
        fi
        ;;
    3)
        echo "🚀 Starting screen session..."
        screen -dmS bomberman_training python3 overnight_training.py
        echo "✅ Screen session started: bomberman_training"
        echo ""
        echo "📊 Attach to session:"
        echo "   screen -r bomberman_training"
        echo ""
        echo "💡 Detach from session: Ctrl+A then D"
        echo ""
        ;;
    4)
        echo "🚀 Starting tmux session..."
        tmux new-session -d -s training "python3 overnight_training.py"
        echo "✅ tmux session started: training"
        echo ""
        echo "📊 Attach to session:"
        echo "   tmux attach -t training"
        echo ""
        echo "💡 Detach from session: Ctrl+B then D"
        echo ""
        ;;
esac

echo "=================================="
echo "✅ Training launched successfully!"
echo "=================================="
