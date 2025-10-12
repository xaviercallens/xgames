#!/bin/bash
################################################################################
# Terminal Setup Script for Bomberman AI Project
# Run this in each new terminal to set up the environment
################################################################################

# Colors for output
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
echo -e "${CYAN}║${NC}  ${PURPLE}💨 PROUTMAN AI - Terminal Setup${NC}                              ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "game_dev_env" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}   Creating virtual environment...${NC}"
    python3 -m venv game_dev_env
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source game_dev_env/bin/activate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1)
echo -e "${GREEN}✅ Python: ${PYTHON_VERSION}${NC}"

# Check if dependencies are installed
echo -e "${BLUE}🔍 Checking dependencies...${NC}"

# Check pygame
if python -c "import pygame" 2>/dev/null; then
    PYGAME_VERSION=$(python -c "import pygame; print(pygame.__version__)")
    echo -e "${GREEN}✅ Pygame: ${PYGAME_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠️  Pygame not found, installing...${NC}"
    pip install pygame > /dev/null 2>&1
    echo -e "${GREEN}✅ Pygame installed${NC}"
fi

# Check PyTorch
if python -c "import torch" 2>/dev/null; then
    TORCH_VERSION=$(python -c "import torch; print(torch.__version__)")
    echo -e "${GREEN}✅ PyTorch: ${TORCH_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠️  PyTorch not found, installing...${NC}"
    pip install torch > /dev/null 2>&1
    echo -e "${GREEN}✅ PyTorch installed${NC}"
fi

# Check NumPy
if python -c "import numpy" 2>/dev/null; then
    NUMPY_VERSION=$(python -c "import numpy; print(numpy.__version__)")
    echo -e "${GREEN}✅ NumPy: ${NUMPY_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠️  NumPy not found, installing...${NC}"
    pip install numpy > /dev/null 2>&1
    echo -e "${GREEN}✅ NumPy installed${NC}"
fi

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${GREEN}✅ Environment Ready!${NC}                                           ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Show available commands
echo -e "${PURPLE}📋 Available Commands:${NC}"
echo ""
echo -e "  ${GREEN}🎮 Play & Test:${NC}"
echo -e "     ${CYAN}./launch_bomberman.sh${NC}          - Play the game"
echo -e "     ${CYAN}python play_bomberman.py${NC}       - Alternative launcher"
echo ""
echo -e "  ${GREEN}🤖 Training:${NC}"
echo -e "     ${CYAN}./train.sh${NC}                     - Training mode selector"
echo -e "     ${CYAN}./train_with_heuristics.py${NC}    - Complete pipeline (10 min)"
echo -e "     ${CYAN}python bootstrap_agent.py${NC}      - Bootstrap only (5 min)"
echo -e "     ${CYAN}python quick_train_agent.py${NC}    - Quick session (5 min)"
echo ""
echo -e "  ${GREEN}🛠️  Development:${NC}"
echo -e "     ${CYAN}python create_splash.py${NC}        - Regenerate splash screen"
echo -e "     ${CYAN}./activate_env.sh${NC}              - Show environment info"
echo ""
echo -e "  ${GREEN}📚 Documentation:${NC}"
echo -e "     ${CYAN}cat README.md${NC}                  - Main documentation"
echo -e "     ${CYAN}cat QUICK_START_TRAINING.md${NC}   - Training guide"
echo -e "     ${CYAN}cat HEURISTIC_BOOTSTRAP.md${NC}    - Bootstrap details"
echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Set environment variables
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export BOMBERMAN_HOME="$SCRIPT_DIR"

# Create alias for convenience
alias train='./train.sh'
alias play='./launch_bomberman.sh'
alias bomber='cd $BOMBERMAN_HOME'

echo -e "${GREEN}💡 Tip: Use 'train' or 'play' commands for quick access!${NC}"
echo ""

# Return to original directory or stay in project
# cd - > /dev/null 2>&1 || true
