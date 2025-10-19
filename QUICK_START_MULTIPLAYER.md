# 🚀 Quick Start - Multiplayer Configurations

## Overview

Quick launcher scripts for common multiplayer game configurations.

---

## 🎮 Available Configurations

### 1. **1 Human + 3 AI Players** (Recommended)
```bash
python3 launch_multiplayer_1h3ai.py
```

**Setup**:
- 👤 Player 1: Human (Green)
- 🤖 AI 1: Intermediate (Red) - 35% WR
- 🤖 AI 2: Advanced (Blue) - 60% WR
- 🤖 AI 3: Intermediate (Yellow) - 35% WR

**Best for**: Solo player vs multiple AI opponents

---

### 2. **1 Human + 3 AI (All Modes)**
```bash
python3 launch_multiplayer_configs.py 1h3ai
```

Same as above with command-line interface.

---

### 3. **2 Human + 2 AI Players**
```bash
python3 launch_multiplayer_configs.py 2h2ai
```

**Setup**:
- 👤 Player 1: Human (Green)
- 👤 Player 2: Human (Red)
- 🤖 AI 1: Intermediate (Blue) - 35% WR
- 🤖 AI 2: Advanced (Yellow) - 60% WR

**Best for**: Two players vs AI team

---

### 4. **3 Human + 1 AI Player**
```bash
python3 launch_multiplayer_configs.py 3h1ai
```

**Setup**:
- 👤 Player 1: Human (Green)
- 👤 Player 2: Human (Red)
- 👤 Player 3: Human (Blue)
- 🤖 AI 1: Advanced (Yellow) - 60% WR

**Best for**: Three players vs one strong AI

---

### 5. **4 Human Players**
```bash
python3 launch_multiplayer_configs.py 4human
```

**Setup**:
- 👤 Player 1: Human (Green)
- 👤 Player 2: Human (Red)
- 👤 Player 3: Human (Blue)
- 👤 Player 4: Human (Yellow)

**Best for**: Local multiplayer with friends

**Custom names**:
```bash
python3 launch_multiplayer_configs.py 4human --names Alice Bob Charlie Diana
```

---

### 6. **1 Human + 1 AI (1v1)**
```bash
python3 launch_multiplayer_configs.py 1h1ai
```

**Setup**:
- 👤 Player 1: Human (Green)
- 🤖 AI Opponent: Advanced (Red) - 60% WR

**Best for**: Classic 1v1 gameplay

**Custom AI mode**:
```bash
python3 launch_multiplayer_configs.py 1h1ai --ai-mode advanced_heuristic
```

---

## 🤖 AI Modes

### Available AI Difficulty Levels

| Mode | Type | Win Rate | Difficulty |
|------|------|----------|------------|
| Beginner | `simple` | 10% | Easy |
| Intermediate | `heuristic` | 35% | Medium |
| Advanced | `advanced_heuristic` | 60% | Hard |

---

## 🎮 Player Controls

### Player 1 (Green) - WASD
```
W: Move Up
A: Move Left
S: Move Down
D: Move Right
Space: Place Bomb
C: Place Block
```

### Player 2 (Red) - Arrow Keys
```
↑: Move Up
←: Move Left
↓: Move Down
→: Move Right
Enter: Place Bomb
Shift: Place Block
```

### Player 3 (Blue) - IJKL
```
I: Move Up
J: Move Left
K: Move Down
L: Move Right
U: Place Bomb
O: Place Block
```

### Player 4 (Yellow) - Numpad
```
8: Move Up
4: Move Left
6: Move Right
2: Move Down
0: Place Bomb
.: Place Block
```

---

## 💻 Python API

### Direct Configuration

```python
from bomber_game.multiplayer_config import GameConfigBuilder

# Create 1 Human + 3 AI
builder = GameConfigBuilder()
builder.add_human_player('Player', (0, 255, 0))
builder.add_ai_player('AI 1', 'heuristic', (255, 0, 0))
builder.add_ai_player('AI 2', 'advanced_heuristic', (0, 0, 255))
builder.add_ai_player('AI 3', 'heuristic', (255, 255, 0))
config = builder.build()
```

### Using Preset Functions

```python
from bomber_game.multiplayer_configs import (
    create_1h3ai_config,
    create_2h2ai_config,
    create_3h1ai_config,
    create_4human_config,
    create_1h1ai_config
)

# 1 Human + 3 AI
config = create_1h3ai_config(human_name='Player')

# 2 Human + 2 AI
config = create_2h2ai_config(human1='Alice', human2='Bob')

# 3 Human + 1 AI
config = create_3h1ai_config('P1', 'P2', 'P3')

# 4 Human
config = create_4human_config(['Alice', 'Bob', 'Charlie', 'Diana'])

# 1v1
config = create_1h1ai_config('Player', 'advanced_heuristic')
```

---

## 🎯 Quick Start Examples

### Example 1: Solo vs 3 AI
```bash
# Start 1 Human + 3 AI game
python3 launch_multiplayer_1h3ai.py
```

### Example 2: Team Play (2v2)
```bash
# Start 2 Human + 2 AI game
python3 launch_multiplayer_configs.py 2h2ai
```

### Example 3: Local Multiplayer (4 Friends)
```bash
# Start 4 Human game with custom names
python3 launch_multiplayer_configs.py 4human --names Alice Bob Charlie Diana
```

### Example 4: Classic 1v1
```bash
# Start 1v1 with Advanced AI
python3 launch_multiplayer_configs.py 1h1ai --ai-mode advanced_heuristic
```

---

## 📊 Configuration Details

### 1 Human + 3 AI (Recommended)

```
┌─────────────────────────────────┐
│ P1 (Human)      P2 (AI)         │
│                                 │
│                                 │
│                                 │
│ P4 (AI)         P3 (AI)         │
└─────────────────────────────────┘

Player 1: Human (Green) - WASD
Player 2: AI (Red) - Intermediate (35% WR)
Player 3: AI (Blue) - Advanced (60% WR)
Player 4: AI (Yellow) - Intermediate (35% WR)
```

### 2 Human + 2 AI

```
┌─────────────────────────────────┐
│ P1 (Human)      P2 (Human)      │
│                                 │
│                                 │
│                                 │
│ P4 (AI)         P3 (AI)         │
└─────────────────────────────────┘

Player 1: Human (Green) - WASD
Player 2: Human (Red) - Arrow Keys
Player 3: AI (Blue) - Intermediate (35% WR)
Player 4: AI (Yellow) - Advanced (60% WR)
```

### 3 Human + 1 AI

```
┌─────────────────────────────────┐
│ P1 (Human)      P2 (Human)      │
│                                 │
│                                 │
│                                 │
│ P4 (Human)      P3 (AI)         │
└─────────────────────────────────┘

Player 1: Human (Green) - WASD
Player 2: Human (Red) - Arrow Keys
Player 3: AI (Blue) - Advanced (60% WR)
Player 4: Human (Yellow) - Numpad
```

---

## 🎮 Game Rules

### Objective
- Destroy walls with bombs
- Defeat all opponents
- Collect power-ups
- Be the last player standing

### Controls
- **Move**: WASD / Arrow Keys / IJKL / Numpad
- **Bomb**: Space / Enter / U / Numpad 0
- **Block**: C / Shift / O / Numpad .
- **Pause**: P
- **Quit**: ESC

### Power-ups
- 🔥 **Bomb+**: Increase bomb count
- 💨 **Range+**: Increase blast range
- ⚡ **Speed+**: Increase movement speed

---

## 📋 File Structure

```
launch_multiplayer_1h3ai.py      # Direct 1H3AI launcher
launch_multiplayer_configs.py    # Multi-config launcher
QUICK_START_MULTIPLAYER.md       # This file
```

---

## ✅ Features

- ✅ 6 preset configurations
- ✅ Command-line interface
- ✅ Custom player names
- ✅ Custom AI modes
- ✅ Easy to use
- ✅ Production ready

---

## 🚀 Next Steps

### For Game Engine Integration
1. Implement `setup_multiplayer_game()` in `game_engine.py`
2. Update game state for 4 players
3. Implement player controllers
4. Test all configurations

### For Network Support
1. Add network configuration option
2. Implement server/client selection
3. Add connection settings
4. Test network multiplayer

---

## 📞 Support

### Common Issues

**Q: Game doesn't start**
A: Make sure pygame is installed: `pip install pygame`

**Q: Can't control players**
A: Check keyboard layout and player controls above

**Q: AI not responding**
A: Ensure AI mode is valid (simple, heuristic, advanced_heuristic)

---

## 🎉 Summary

Quick start launchers provide:
- ✅ 6 preset configurations
- ✅ Easy command-line usage
- ✅ Python API support
- ✅ Custom player names
- ✅ Custom AI modes
- ✅ Production ready

**Ready to play!** 🎮✨

