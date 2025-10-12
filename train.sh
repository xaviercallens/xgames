#!/bin/bash
################################################################################
# Training Mode Selector for Bomberman AI
# Interactive menu to choose different training modes
################################################################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Ensure virtual environment
if [ ! -d "game_dev_env" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}   Run: ./setup_terminal.sh${NC}"
    exit 1
fi

# Activate virtual environment
source game_dev_env/bin/activate

# Python executable
PYTHON="$SCRIPT_DIR/game_dev_env/bin/python"

# Clear screen
clear

# Print banner
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}                                                                    ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}     ${PURPLE}💨 PROUTMAN AI - Training Mode Selector 🤖${NC}                ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}                                                                    ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check for existing model
MODEL_PATH="bomber_game/models/ppo_agent.pth"
BOOTSTRAP_STATS="bomber_game/models/bootstrap_stats.json"
TRAINING_STATS="bomber_game/models/training_stats.json"

if [ -f "$MODEL_PATH" ]; then
    MODEL_SIZE=$(du -h "$MODEL_PATH" | cut -f1)
    echo -e "${GREEN}✅ Existing Model Found:${NC} ${MODEL_SIZE}"
    
    if [ -f "$TRAINING_STATS" ]; then
        # Extract stats using Python
        WIN_RATE=$($PYTHON -c "import json; data=json.load(open('$TRAINING_STATS')); print(f\"{data.get('total_wins', 0) / max(data.get('total_episodes', 1), 1) * 100:.1f}%\")" 2>/dev/null || echo "N/A")
        EPISODES=$($PYTHON -c "import json; print(json.load(open('$TRAINING_STATS')).get('total_episodes', 0))" 2>/dev/null || echo "0")
        LEVEL=$($PYTHON -c "import json; print(json.load(open('$TRAINING_STATS')).get('current_level', 'Unknown'))" 2>/dev/null || echo "Unknown")
        
        echo -e "${BLUE}   Episodes:${NC} ${EPISODES}"
        echo -e "${BLUE}   Win Rate:${NC} ${WIN_RATE}"
        echo -e "${BLUE}   Level:${NC} ${LEVEL}"
    fi
    echo ""
else
    echo -e "${YELLOW}⚠️  No existing model found${NC}"
    echo -e "${BLUE}   Recommendation: Start with option 1 or 2${NC}"
    echo ""
fi

# Training modes
echo -e "${PURPLE}📋 Training Modes:${NC}"
echo ""
echo -e "${GREEN}1.${NC} ${CYAN}Complete Pipeline${NC} (Recommended for first time)"
echo -e "   ${BLUE}├─${NC} Bootstrap with heuristics (500 episodes, ~5 min)"
echo -e "   ${BLUE}├─${NC} Reinforcement learning (5 min)"
echo -e "   ${BLUE}└─${NC} Total: ~10 minutes, Win Rate: 50-60%"
echo ""
echo -e "${GREEN}2.${NC} ${CYAN}Bootstrap Only${NC} (Teach basic strategies)"
echo -e "   ${BLUE}├─${NC} 500 episodes of expert demonstrations"
echo -e "   ${BLUE}├─${NC} Learn 6 core heuristics"
echo -e "   ${BLUE}└─${NC} Time: ~5 minutes, Win Rate: 30-40%"
echo ""
echo -e "${GREEN}3.${NC} ${CYAN}Quick Training${NC} (5-minute session)"
echo -e "   ${BLUE}├─${NC} Continue from existing model"
echo -e "   ${BLUE}├─${NC} ~400 episodes of reinforcement learning"
echo -e "   ${BLUE}└─${NC} Time: 5 minutes, Improves by 5-10%"
echo ""
echo -e "${GREEN}4.${NC} ${CYAN}Extended Training${NC} (15-minute session)"
echo -e "   ${BLUE}├─${NC} Deep reinforcement learning"
echo -e "   ${BLUE}├─${NC} ~1200 episodes"
echo -e "   ${BLUE}└─${NC} Time: 15 minutes, Improves by 10-20%"
echo ""
echo -e "${GREEN}5.${NC} ${CYAN}Custom Training${NC} (Configure duration)"
echo -e "   ${BLUE}├─${NC} Choose your own duration"
echo -e "   ${BLUE}├─${NC} Flexible episode count"
echo -e "   ${BLUE}└─${NC} Time: Your choice"
echo ""
echo -e "${GREEN}6.${NC} ${CYAN}Reset & Restart${NC} (Start from scratch)"
echo -e "   ${BLUE}├─${NC} Delete existing model"
echo -e "   ${BLUE}├─${NC} Run complete pipeline"
echo -e "   ${BLUE}└─${NC} Time: ~10 minutes"
echo ""
echo -e "${GREEN}7.${NC} ${CYAN}View Statistics${NC} (Check progress)"
echo -e "   ${BLUE}└─${NC} Display training history and performance"
echo ""
echo -e "${GREEN}0.${NC} ${RED}Exit${NC}"
echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Get user choice
read -p "$(echo -e ${YELLOW}Select training mode [0-7]: ${NC})" choice

echo ""

case $choice in
    1)
        echo -e "${GREEN}🚀 Starting Complete Pipeline...${NC}"
        echo ""
        ./train_with_heuristics.py
        ;;
    
    2)
        echo -e "${GREEN}🎓 Starting Bootstrap Training...${NC}"
        echo ""
        $PYTHON bootstrap_agent.py
        ;;
    
    3)
        echo -e "${GREEN}⚡ Starting Quick Training (5 minutes)...${NC}"
        echo ""
        $PYTHON quick_train_agent.py
        ;;
    
    4)
        echo -e "${GREEN}🔥 Starting Extended Training (15 minutes)...${NC}"
        echo ""
        # Temporarily modify training duration
        $PYTHON -c "
import sys
sys.path.insert(0, '.')
from quick_train_agent import quick_train

# Monkey patch duration
import bomber_game.agents.ppo_agent as ppo
original_duration = 5 * 60
new_duration = 15 * 60

# Run with extended duration
import quick_train_agent
quick_train_agent.TRAINING_DURATION = new_duration
quick_train_agent.quick_train()
"
        ;;
    
    5)
        echo -e "${GREEN}⚙️  Custom Training Configuration${NC}"
        echo ""
        read -p "$(echo -e ${YELLOW}Enter duration in minutes [1-60]: ${NC})" duration
        
        if [[ "$duration" =~ ^[0-9]+$ ]] && [ "$duration" -ge 1 ] && [ "$duration" -le 60 ]; then
            echo ""
            echo -e "${GREEN}🎯 Starting ${duration}-minute training session...${NC}"
            echo ""
            
            $PYTHON -c "
import sys
sys.path.insert(0, '.')
import quick_train_agent

# Set custom duration
quick_train_agent.TRAINING_DURATION = $duration * 60
quick_train_agent.quick_train()
"
        else
            echo -e "${RED}❌ Invalid duration. Please enter a number between 1 and 60.${NC}"
        fi
        ;;
    
    6)
        echo -e "${YELLOW}⚠️  Reset & Restart${NC}"
        echo ""
        read -p "$(echo -e ${RED}This will delete your existing model. Continue? [y/N]: ${NC})" confirm
        
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            echo ""
            echo -e "${BLUE}🗑️  Removing existing model...${NC}"
            rm -f bomber_game/models/ppo_agent.pth
            rm -f bomber_game/models/*.json
            echo -e "${GREEN}✅ Model deleted${NC}"
            echo ""
            echo -e "${GREEN}🚀 Starting fresh training...${NC}"
            echo ""
            ./train_with_heuristics.py
        else
            echo -e "${YELLOW}❌ Reset cancelled${NC}"
        fi
        ;;
    
    7)
        echo -e "${GREEN}📊 Training Statistics${NC}"
        echo ""
        
        if [ -f "$TRAINING_STATS" ]; then
            echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
            $PYTHON << 'PYEOF'
import json
from datetime import datetime

with open('bomber_game/models/training_stats.json', 'r') as f:
    stats = json.load(f)

print("📈 Overall Statistics:")
print(f"   Total Episodes: {stats.get('total_episodes', 0)}")
print(f"   Total Wins: {stats.get('total_wins', 0)}")
print(f"   Total Losses: {stats.get('total_losses', 0)}")
win_rate = stats.get('total_wins', 0) / max(stats.get('total_episodes', 1), 1) * 100
print(f"   Win Rate: {win_rate:.1f}%")
print(f"   Current Level: {stats.get('current_level', 'Unknown')}")

if 'total_training_time' in stats:
    hours = stats['total_training_time'] // 3600
    minutes = (stats['total_training_time'] % 3600) // 60
    print(f"   Training Time: {int(hours)}h {int(minutes)}m")

if 'last_updated' in stats:
    print(f"   Last Updated: {stats.get('last_updated', 'Unknown')}")

if 'training_sessions' in stats and stats['training_sessions']:
    print("\n📅 Recent Sessions:")
    for i, session in enumerate(stats['training_sessions'][-5:], 1):
        date = session.get('date', 'Unknown')[:19]
        episodes = session.get('episodes', 0)
        wins = session.get('wins', 0)
        win_rate = wins / max(episodes, 1) * 100
        print(f"   {i}. {date} - {episodes} episodes, {win_rate:.1f}% wins")
PYEOF
            echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
        else
            echo -e "${YELLOW}⚠️  No training statistics found${NC}"
        fi
        
        echo ""
        
        if [ -f "$BOOTSTRAP_STATS" ]; then
            echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
            $PYTHON << 'PYEOF'
import json

with open('bomber_game/models/bootstrap_stats.json', 'r') as f:
    stats = json.load(f)

print("🎓 Bootstrap Statistics:")
print(f"   Episodes: {stats.get('bootstrap_episodes', 0)}")
print(f"   Wins: {stats.get('total_wins', 0)}")
print(f"   Win Rate: {stats.get('win_rate', 0):.1f}%")
print(f"   Avg Reward: {stats.get('avg_reward', 0):.2f}")

if 'strategies_learned' in stats:
    print("\n✅ Strategies Learned:")
    for strategy in stats['strategies_learned']:
        print(f"   ✓ {strategy}")
PYEOF
            echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
        fi
        
        echo ""
        read -p "$(echo -e ${YELLOW}Press Enter to continue...${NC})"
        ;;
    
    0)
        echo -e "${BLUE}👋 Goodbye!${NC}"
        exit 0
        ;;
    
    *)
        echo -e "${RED}❌ Invalid choice. Please select 0-7.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}✅ Training Complete!${NC}"
echo ""
echo -e "${PURPLE}Next Steps:${NC}"
echo -e "  ${CYAN}./launch_bomberman.sh${NC}  - Test your AI"
echo -e "  ${CYAN}./train.sh${NC}             - Train more"
echo -e "  ${CYAN}./train.sh${NC} (option 7)  - View statistics"
echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""
