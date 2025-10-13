#!/bin/bash
# Interactive Bomberman Launcher - Choose game mode

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     💨 PROUTMAN - Interactive Launcher 🎮                 ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Select Game Mode:"
echo ""
echo "1) Single Player (1v1)"
echo "   └─ You vs 1 AI opponent"
echo "   └─ Choose AI difficulty from menu"
echo ""
echo "2) Multiplayer (1v1, 1v2, or 1v3)"
echo "   └─ You vs 1-3 AI opponents"
echo "   └─ Configure each AI individually"
echo ""
echo "3) Quick Start (Default: 1v1 Intermediate)"
echo "   └─ Skip menus, start immediately"
echo ""
echo "0) Exit"
echo ""
read -p "Enter your choice [0-3]: " choice

case $choice in
    1)
        echo ""
        echo "🎮 Starting Single Player Mode..."
        echo "   You will select AI difficulty from the menu"
        echo ""
        
        # Activate virtual environment if it exists
        if [ -d ".venv" ]; then
            source .venv/bin/activate
        elif [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        python play_bomberman.py
        ;;
    
    2)
        echo ""
        echo "🎮 Starting Multiplayer Mode..."
        echo "   You will configure number of opponents and their AI types"
        echo ""
        
        # Activate virtual environment if it exists
        if [ -d ".venv" ]; then
            source .venv/bin/activate
        elif [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        python -c "from bomber_game.multiplayer_engine import main; main()"
        ;;
    
    3)
        echo ""
        echo "🎮 Quick Start - 1v1 Intermediate AI"
        echo ""
        
        # Activate virtual environment if it exists
        if [ -d ".venv" ]; then
            source .venv/bin/activate
        elif [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        # Set environment variable to skip menus
        export BOMBERMAN_QUICK_START=true
        python play_bomberman.py
        ;;
    
    0)
        echo "Goodbye! 👋"
        exit 0
        ;;
    
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
