#!/bin/bash
################################################################################
# Reset AI Training - Start Fresh with Better Model
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

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${PURPLE}🔄 Reset AI Training - Start Fresh${NC}                            ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check current stats
if [ -f "bomber_game/models/training_stats.json" ]; then
    echo -e "${YELLOW}📊 Current Training Statistics:${NC}"
    python3 << 'PYEOF'
import json
try:
    with open('bomber_game/models/training_stats.json', 'r') as f:
        stats = json.load(f)
    print(f"   Episodes: {stats.get('total_episodes', 0)}")
    print(f"   Win Rate: {stats.get('total_wins', 0) / max(stats.get('total_episodes', 1), 1) * 100:.1f}%")
    print(f"   Training Time: {stats.get('total_training_time', 0) // 3600}h {(stats.get('total_training_time', 0) % 3600) // 60}m")
except:
    print("   No stats found")
PYEOF
    echo ""
fi

# Confirm reset
read -p "$(echo -e ${RED}This will delete current training progress. Continue? [y/N]: ${NC})" confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}❌ Reset cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🗑️  Removing old training data...${NC}"

# Backup old model if it exists
if [ -f "bomber_game/models/ppo_agent.pth" ]; then
    BACKUP_NAME="bomber_game/models/ppo_agent_backup_$(date +%Y%m%d_%H%M%S).pth"
    mv "bomber_game/models/ppo_agent.pth" "$BACKUP_NAME"
    echo -e "${GREEN}✅ Backed up old model to: $BACKUP_NAME${NC}"
fi

# Remove stats
rm -f bomber_game/models/training_stats.json
rm -f bomber_game/models/bootstrap_stats.json
echo -e "${GREEN}✅ Removed old statistics${NC}"

echo ""
echo -e "${BLUE}🎯 Creating fresh pretrained model...${NC}"

# Create new pretrained model
./game_dev_env/bin/python create_pretrained_model.py

# Copy to main model
cp bomber_game/models/ppo_pretrained.pth bomber_game/models/ppo_agent.pth
echo -e "${GREEN}✅ Installed fresh pretrained model${NC}"

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ AI Training Reset Complete!${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${PURPLE}📋 Next Steps:${NC}"
echo ""
echo -e "  ${GREEN}1. Train with heuristics (Recommended):${NC}"
echo -e "     ${CYAN}./train_with_heuristics.py${NC}"
echo -e "     This teaches the AI basic strategies first"
echo ""
echo -e "  ${GREEN}2. Or use training menu:${NC}"
echo -e "     ${CYAN}./train.sh${NC}"
echo -e "     Select option 1 (Complete Pipeline)"
echo ""
echo -e "  ${GREEN}3. Test the fresh AI:${NC}"
echo -e "     ${CYAN}./launch_bomberman.sh${NC}"
echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""
