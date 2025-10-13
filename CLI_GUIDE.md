# Bomberman CLI Guide

**Unified command-line interface for all game features**

---

## 🚀 Quick Start

### Interactive Menu (Easiest)
```bash
./bomberman
```
or
```bash
./bomberman menu
```

### Direct Commands
```bash
./bomberman play              # Single player
./bomberman play --multi      # Multiplayer
./bomberman train             # Quick training
./bomberman monitor           # Monitor progress
```

---

## 📋 All Commands

### Play Commands

#### Single Player (1v1)
```bash
./bomberman play
```
- Classic 1v1 mode
- Choose AI from menu
- 5 difficulty levels

#### Multiplayer (1v1, 1v2, or 1v3)
```bash
./bomberman play --multi
```
- Configure 0-3 AI opponents
- Individual AI type selection
- Strategic gameplay

#### Hybrid AI Mode
```bash
./bomberman play --hybrid
```
- Play against Hybrid AI
- Choose strategy mode
- Best AI performance

#### Interactive Launcher
```bash
./bomberman play --interactive
```
- Full interactive menu
- Choose game mode
- Configure everything

---

### Training Commands

#### Quick Training (100 episodes)
```bash
./bomberman train
```
- Fast training session
- ~5 minutes
- Good for testing

#### Overnight Training (10,000 episodes)
```bash
./bomberman train --overnight
```
- Long training session
- ~8 hours
- Target 40-55% win rate

#### Bootstrap Training (Heuristics)
```bash
./bomberman train --bootstrap
```
- Train with expert demonstrations
- Learn from heuristics
- 500 episodes

#### Custom Training
```bash
./bomberman train --episodes 1000
```
- Specify episode count
- Flexible duration
- Any number you want

---

### Monitoring Commands

#### Monitor Training Progress
```bash
./bomberman monitor
```
- Real-time training stats
- Win rate graphs
- Episode progress

#### View Statistics
```bash
./bomberman stats
```
- Complete training history
- Performance metrics
- Session details

---

### Utility Commands

#### Test Game Setup
```bash
./bomberman test
```
- Verify installation
- Check dependencies
- Test game launch

#### Test Training Setup
```bash
./bomberman test-train
```
- Verify training system
- Check models
- Test AI agents

#### Create Pretrained Model
```bash
./bomberman pretrain
```
- Generate bootstrap model
- Use heuristics
- Quick start for training

#### Reset AI Training
```bash
./bomberman reset
```
- Delete all training progress
- Start from scratch
- Requires confirmation

---

## 🎮 Interactive Menu

### Launch Menu
```bash
./bomberman
```
or
```bash
./bomberman menu
```

### Menu Options
```
╔════════════════════════════════════════════════════════════════╗
║     💨 BOMBERMAN CLI - Unified Command Interface 🎮       ║
╚════════════════════════════════════════════════════════════════╝

🎮 PLAY MODES:
  1. Single Player (1v1)
  2. Multiplayer (1v1, 1v2, or 1v3)
  3. Hybrid AI Mode
  4. Interactive Launcher

🤖 TRAINING:
  5. Quick Training (100 episodes)
  6. Overnight Training (10,000 episodes)
  7. Bootstrap Training (Heuristics)
  8. Custom Training (specify episodes)
  9. Monitor Training Progress
 10. View Training Statistics

🔧 UTILITIES:
 11. Test Game Setup
 12. Test Training Setup
 13. Create Pretrained Model
 14. Reset AI Training

  0. Exit

Enter your choice [0-14]:
```

---

## 📊 Command Reference

| Command | Description | Duration |
|---------|-------------|----------|
| `bomberman play` | Single player | Until quit |
| `bomberman play --multi` | Multiplayer | Until quit |
| `bomberman play --hybrid` | Hybrid AI | Until quit |
| `bomberman play --interactive` | Interactive launcher | Until quit |
| `bomberman train` | Quick training | ~5 min |
| `bomberman train --overnight` | Overnight training | ~8 hours |
| `bomberman train --bootstrap` | Bootstrap | ~5 min |
| `bomberman train --episodes N` | Custom training | Varies |
| `bomberman monitor` | Monitor training | Until quit |
| `bomberman stats` | View statistics | Instant |
| `bomberman test` | Test setup | ~10 sec |
| `bomberman test-train` | Test training | ~30 sec |
| `bomberman pretrain` | Create model | ~5 min |
| `bomberman reset` | Reset training | Instant |
| `bomberman menu` | Interactive menu | Until quit |

---

## 💡 Usage Examples

### For Beginners
```bash
# Test everything works
./bomberman test

# Play single player
./bomberman play
# Select: Beginner Bot

# Try quick training
./bomberman train
```

### For Intermediate Players
```bash
# Play multiplayer
./bomberman play --multi
# Select: 1 AI Opponent
# Choose: Intermediate

# Train for better AI
./bomberman train --episodes 500

# Monitor progress
./bomberman monitor
```

### For Advanced Players
```bash
# Play against hybrid AI
./bomberman play --hybrid
# Select: Adaptive mode

# Overnight training
./bomberman train --overnight

# View statistics
./bomberman stats
```

### For Developers
```bash
# Test everything
./bomberman test
./bomberman test-train

# Create pretrained model
./bomberman pretrain

# Custom training
./bomberman train --episodes 2000

# Reset and start over
./bomberman reset
```

---

## 🔧 Advanced Usage

### Environment Variables
```bash
# Quick start mode
export BOMBERMAN_QUICK_START=true
./bomberman play

# Hybrid mode
export BOMBERMAN_HYBRID_MODE=true
export BOMBERMAN_HYBRID_STRATEGY=adaptive
./bomberman play
```

### Chaining Commands
```bash
# Test, then play
./bomberman test && ./bomberman play

# Train, then monitor
./bomberman train --episodes 500 &
sleep 10
./bomberman monitor
```

### Background Training
```bash
# Train in background
nohup ./bomberman train --overnight > training.log 2>&1 &

# Monitor later
./bomberman monitor
```

---

## 🎯 Workflow Examples

### First Time Setup
```bash
# 1. Test installation
./bomberman test

# 2. Play to understand game
./bomberman play

# 3. Try quick training
./bomberman train

# 4. Play against trained AI
./bomberman play
```

### Regular Training Workflow
```bash
# 1. Check current stats
./bomberman stats

# 2. Run training session
./bomberman train --episodes 1000

# 3. Monitor progress
./bomberman monitor

# 4. Test improved AI
./bomberman play
```

### Development Workflow
```bash
# 1. Test setup
./bomberman test
./bomberman test-train

# 2. Create pretrained model
./bomberman pretrain

# 3. Bootstrap training
./bomberman train --bootstrap

# 4. Continue training
./bomberman train --episodes 2000

# 5. Verify results
./bomberman stats
```

---

## 🐛 Troubleshooting

### Command Not Found
```bash
# Make executable
chmod +x bomberman

# Run with explicit path
./bomberman
```

### Virtual Environment Warning
```bash
# Activate virtual environment first
source .venv/bin/activate

# Then run commands
./bomberman play
```

### Permission Denied
```bash
# Fix permissions
chmod +x bomberman
chmod +x *.sh

# Try again
./bomberman
```

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Test setup
./bomberman test
```

---

## 📈 Comparison: Old vs New

### Old Way
```bash
# Multiple different scripts
./launch_bomberman.sh
./play_multiplayer.sh
./play_hybrid.sh
./start_overnight_training.sh
python monitor_training.py
python test_setup.py
# ... and many more
```

### New Way
```bash
# One unified CLI
./bomberman play
./bomberman play --multi
./bomberman play --hybrid
./bomberman train --overnight
./bomberman monitor
./bomberman test
# Everything in one place!
```

---

## ✅ Benefits

### Unified Interface
- One command for everything
- Consistent syntax
- Easy to remember

### Interactive Menu
- User-friendly
- No need to remember commands
- Guided workflow

### Flexible
- Direct commands for automation
- Interactive menu for exploration
- Both approaches supported

### Well-Documented
- Built-in help (`--help`)
- Clear examples
- Comprehensive guide

---

## 🎉 Summary

**One CLI to rule them all!**

### Quick Commands
```bash
./bomberman              # Interactive menu
./bomberman play         # Play game
./bomberman train        # Train AI
./bomberman monitor      # Monitor training
./bomberman --help       # Show help
```

### All Features Accessible
- ✅ All game modes
- ✅ All training options
- ✅ All utilities
- ✅ Interactive menu
- ✅ Direct commands

### Easy to Use
- Simple syntax
- Clear help text
- Comprehensive examples
- Interactive fallback

**Everything you need in one command!** 🎮✨

---

**Created:** 2025-10-13  
**Status:** ✅ Ready to Use  
**Command:** `./bomberman`
