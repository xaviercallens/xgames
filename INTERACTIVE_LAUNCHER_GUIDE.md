# Interactive Launcher Guide

**New interactive launcher with game mode selection!**

---

## 🚀 Quick Start

### Launch Interactive Menu
```bash
./launch_bomberman_interactive.sh
```

You'll see:
```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     💨 PROUTMAN - Interactive Launcher 🎮                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Select Game Mode:

1) Single Player (1v1)
   └─ You vs 1 AI opponent
   └─ Choose AI difficulty from menu

2) Multiplayer (1v1, 1v2, or 1v3)
   └─ You vs 1-3 AI opponents
   └─ Configure each AI individually

3) Quick Start (Default: 1v1 Intermediate)
   └─ Skip menus, start immediately

0) Exit

Enter your choice [0-3]:
```

---

## 🎮 Game Modes

### 1. Single Player (1v1)
**What happens:**
1. Game launches with splash screen
2. AI selection menu appears
3. Choose one AI opponent from list:
   - 🌱 Beginner Bot (10% WR)
   - 🎯 Intermediate Bot (35% WR)
   - 🤖 Advanced Bot (PPO) (20% WR)
   - 🎭 Hybrid Bot (40% WR)
   - 👑 Expert Bot (Best)
4. Game starts with your selected AI

**Best for:**
- Classic Bomberman experience
- Testing specific AI types
- Learning the game

**Controls in menu:**
- ↑/↓ or W/S - Select AI
- ENTER/SPACE - Confirm
- ESC - Use default (Beginner)

---

### 2. Multiplayer (1v1, 1v2, or 1v3)
**What happens:**
1. Game launches with splash screen
2. Player selection menu appears
3. **Step 1:** Choose number of AI opponents (0-3)
   ```
   🎯 0 AI Opponents (Practice Mode)
   🤖 1 AI Opponent (2 Total Players)
   🤖🤖 2 AI Opponents (3 Total Players)
   🤖🤖🤖 3 AI Opponents (4 Total Players)
   ```

4. **Step 2:** Configure each AI opponent
   ```
   AI Opponent 1:  ◀ Intermediate (35% WR) ▶
   AI Opponent 2:  ◀ Hybrid (40% WR) ▶
   AI Opponent 3:  ◀ Advanced (PPO) (20% WR) ▶
   ```

5. Game starts with configured opponents

**Best for:**
- Challenging gameplay
- Multiple opponents
- Strategic battles
- Chaos mode

**Controls in menu:**
- **Step 1:**
  - ↑/↓ or W/S - Select number
  - ENTER/SPACE - Confirm
  - ESC - Cancel

- **Step 2:**
  - ↑/↓ or W/S - Select opponent
  - ←/→ or A/D - Change AI type
  - ENTER/SPACE - Start game
  - ESC - Go back

---

### 3. Quick Start
**What happens:**
- Skips all menus
- Starts immediately with:
  - 1 Human Player
  - 1 Intermediate AI (35% WR)
- No configuration needed

**Best for:**
- Quick games
- Testing
- When you know what you want

---

## 📊 AI Types Available

| AI Type | Win Rate | Description | Best For |
|---------|----------|-------------|----------|
| **Beginner** | 10% | Basic heuristics | Learning |
| **Intermediate** | 35% | Smart A* pathfinding | Balanced play |
| **Advanced (PPO)** | 20% | Deep RL trained | See AI learning |
| **Hybrid** | 40% | Heuristics + RL | Best challenge |
| **Expert (Best)** | Varies | Best checkpoint | Maximum difficulty |

---

## 🎯 Recommended Configurations

### For Beginners
```
Mode: Single Player
AI: Beginner Bot (10% WR)
```

### For Intermediate Players
```
Mode: Single Player
AI: Intermediate Bot (35% WR)

OR

Mode: Multiplayer
Opponents: 1
AI 1: Intermediate (35% WR)
```

### For Advanced Players
```
Mode: Single Player
AI: Hybrid Bot (40% WR)

OR

Mode: Multiplayer
Opponents: 2
AI 1: Intermediate (35% WR)
AI 2: Hybrid (40% WR)
```

### For Experts
```
Mode: Multiplayer
Opponents: 3
AI 1: Intermediate (35% WR)
AI 2: Advanced (PPO) (20% WR)
AI 3: Hybrid (40% WR)
```

---

## 🔧 Technical Details

### File Structure
```
launch_bomberman_interactive.sh  ← New interactive launcher
launch_bomberman.sh              ← Original launcher (single player)
play_multiplayer.sh              ← Direct multiplayer launcher
play_bomberman.py                ← Single player game
bomber_game/
  ├── multiplayer_engine.py      ← Multiplayer game engine
  ├── menu.py                    ← Menu with multiplayer support
  └── player_selector.py         ← Player selection menu
```

### Environment Variables
```bash
# Quick start mode (skip menus)
export BOMBERMAN_QUICK_START=true

# Hybrid mode (for single player)
export BOMBERMAN_HYBRID_MODE=true
export BOMBERMAN_HYBRID_STRATEGY=adaptive
```

---

## 🎮 Complete User Flow

### Single Player Flow
```
./launch_bomberman_interactive.sh
  ↓
Select: 1) Single Player
  ↓
[Splash Screen]
  ↓
[AI Selection Menu]
  ↓
Select AI: Hybrid Bot (40% WR)
  ↓
[Game Starts - 1v1]
```

### Multiplayer Flow
```
./launch_bomberman_interactive.sh
  ↓
Select: 2) Multiplayer
  ↓
[Splash Screen]
  ↓
[Player Selection - Step 1]
  ↓
Select: 2 AI Opponents
  ↓
[Player Selection - Step 2]
  ↓
Configure AI 1: Intermediate (35% WR)
Configure AI 2: Hybrid (40% WR)
  ↓
[Game Starts - 1v2]
```

### Quick Start Flow
```
./launch_bomberman_interactive.sh
  ↓
Select: 3) Quick Start
  ↓
[Game Starts Immediately - 1v1 Intermediate]
```

---

## 💡 Tips

### Menu Navigation
- Use arrow keys or WASD
- ENTER or SPACE to confirm
- ESC to go back or cancel

### Game Controls
- **WASD** or **Arrow Keys** - Move
- **SPACE** - Place bomb
- **P** - Pause
- **R** - Restart (when game over)
- **ESC** - Quit

### Strategy
- **Single Player:** Focus on learning AI patterns
- **Multiplayer:** Use chaos to your advantage
- **Quick Start:** Good for warm-up games

---

## 🐛 Troubleshooting

### Launcher won't run?
```bash
chmod +x launch_bomberman_interactive.sh
./launch_bomberman_interactive.sh
```

### Menu not showing?
- Check if virtual environment is activated
- Ensure pygame is installed:
  ```bash
  pip install pygame
  ```

### AI not working?
- Check if models exist: `bomber_game/models/ppo_agent.pth`
- Try Beginner or Intermediate AI (don't need models)

---

## 📈 Comparison: Old vs New

### Old Way
```bash
# Single player only
./launch_bomberman.sh
# AI selected automatically
```

### New Way
```bash
# Interactive menu
./launch_bomberman_interactive.sh
# Choose mode: Single or Multiplayer
# Configure AI(s) as you like
```

### Still Available
```bash
# Direct launchers
./launch_bomberman.sh        # Original single player
./play_multiplayer.sh         # Direct multiplayer
./play_hybrid.sh              # Hybrid AI mode
```

---

## ✅ Summary

**New Features:**
- ✅ Interactive launcher with mode selection
- ✅ Single player with AI selection menu
- ✅ Multiplayer with player configuration
- ✅ Quick start option
- ✅ Integrated into standard menu system

**How to Use:**
```bash
./launch_bomberman_interactive.sh
```

**Recommended:**
- First time: Option 1 (Single Player)
- For challenge: Option 2 (Multiplayer with 2-3 AI)
- Quick game: Option 3 (Quick Start)

**All game modes now accessible from one launcher!** 🎮✨

---

**Created:** 2025-10-13  
**Status:** ✅ Ready to Use  
**Modes:** Single Player, Multiplayer, Quick Start
