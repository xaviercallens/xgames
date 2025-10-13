# Multiplayer Mode Guide

**Play Bomberman with 1-4 players (1 Human + 0-3 AI Opponents)!**

---

## 🎮 How to Play Multiplayer

### Quick Start
```bash
./play_multiplayer.sh
```

### What You'll See

#### Step 1: Select Number of AI Opponents
```
🎮 Multiplayer Setup
Select Number of AI Opponents

🎯 0 AI Opponents (Practice Mode)
🤖 1 AI Opponent (2 Total Players)
🤖🤖 2 AI Opponents (3 Total Players)
🤖🤖🤖 3 AI Opponents (4 Total Players)

↑/↓ or W/S - Select
ENTER or SPACE - Confirm
ESC - Cancel
```

#### Step 2: Configure Each AI Opponent
```
🤖 Configure AI Opponents
Select AI Type for Each Opponent

AI Opponent 1:  ◀ Intermediate (35% WR) ▶
AI Opponent 2:  ◀ Hybrid (40% WR) ▶
AI Opponent 3:  ◀ Advanced (PPO) (20% WR) ▶

↑/↓ or W/S - Select Opponent
←/→ or A/D - Change AI Type
ENTER or SPACE - Start Game
ESC - Go Back
```

---

## 🎯 Game Modes

### 1. **Practice Mode** (0 AI Opponents)
- Solo play
- Practice bomb placement
- Learn the mechanics
- No competition

### 2. **1v1 Mode** (1 AI Opponent)
- Classic Bomberman
- You vs 1 AI
- Best for learning
- Choose AI difficulty

### 3. **1v2 Mode** (2 AI Opponents)
- More challenging
- Strategic gameplay
- Multiple threats
- Team dynamics

### 4. **1v3 Mode** (3 AI Opponents)
- Maximum challenge
- Chaotic battles
- Survival mode
- Expert level

---

## 🤖 AI Types Available

### 1. **Beginner** (10% WR)
- Basic AI
- Easy to beat
- Good for learning
- Predictable behavior

### 2. **Intermediate** (35% WR)
- Smart heuristics
- A* pathfinding
- Strategic placement
- Moderate challenge

### 3. **Advanced (PPO)** (20% WR)
- Deep reinforcement learning
- Trained on 4,193 games
- Adaptive behavior
- Learned tactics

### 4. **Hybrid** (40% WR) ⭐
- Combines heuristics + RL
- Adaptive decision making
- Best performance
- **Recommended for challenge**

---

## 🗺️ Spawn Positions

Players spawn in the corners of the map:

```
┌─────────────────┐
│ P1 (Human)      │  Top-left: Human Player (Green)
│                 │  
│                 │  Top-right: AI 2 (Blue)
│                 │  
│                 │  Bottom-left: AI 3 (Yellow)
│                 │  
│      AI 1 (Red) │  Bottom-right: AI 1 (Red)
└─────────────────┘
```

**Colors:**
- 🟢 Player 1 (Human) - Green
- 🔴 AI 1 - Red
- 🔵 AI 2 - Blue
- 🟡 AI 3 - Yellow

---

## 🎮 Controls

### Human Player
- **WASD** or **Arrow Keys** - Move
- **SPACE** - Place bomb
- **P** - Pause
- **ESC** - Quit
- **R** - Restart (when game over)

### AI Opponents
- Controlled automatically
- Each AI acts independently
- Different strategies based on type

---

## 🏆 Win Conditions

### Last Player Standing
- Game ends when only 1 player alive
- That player wins
- All others eliminated

### Draw
- If all players die simultaneously
- No winner declared
- Rare but possible

---

## 💡 Strategy Tips

### Against 1 AI
- Focus on power-ups
- Corner the AI
- Use walls strategically
- Trap with bombs

### Against 2 AIs
- Stay mobile
- Don't get caught between them
- Let them fight each other
- Pick off the weak one

### Against 3 AIs
- Survival is key
- Avoid center of map
- Use chaos to your advantage
- Be patient

---

## 🎯 Recommended Configurations

### For Beginners
```
1 AI Opponent: Beginner (10% WR)
```

### For Intermediate Players
```
1 AI Opponent: Intermediate (35% WR)
or
2 AI Opponents: Beginner + Intermediate
```

### For Advanced Players
```
1 AI Opponent: Hybrid (40% WR)
or
2 AI Opponents: Intermediate + Advanced (PPO)
```

### For Experts
```
3 AI Opponents: Intermediate + Advanced + Hybrid
```

---

## 📊 Difficulty Comparison

| Configuration | Difficulty | Win Rate (Estimated) |
|---------------|------------|---------------------|
| 0 AI | Practice | 100% |
| 1 Beginner | Easy | 90% |
| 1 Intermediate | Medium | 65% |
| 1 Advanced (PPO) | Medium-Hard | 80% |
| 1 Hybrid | Hard | 60% |
| 2 Intermediate | Hard | 40% |
| 2 Hybrid | Very Hard | 30% |
| 3 Mixed | Expert | 20% |
| 3 Hybrid | Insane | 10% |

---

## 🔧 Technical Details

### Files
- `bomber_game/player_selector.py` - Player selection menu
- `bomber_game/multiplayer_engine.py` - Multiplayer game engine
- `play_multiplayer.sh` - Launcher script

### Features
- Dynamic player creation
- Multiple AI agent management
- Corner spawn positions
- Independent AI decision making
- Simultaneous action execution

### Limitations
- 1 human player only (for now)
- Maximum 4 total players
- Fixed spawn positions
- Same map for all games

---

## 🎉 Example Session

```bash
$ ./play_multiplayer.sh

========================================
🎮 BOMBERMAN MULTIPLAYER MODE
========================================

Features:
  • 1 Human Player
  • 0-3 AI Opponents
  • Choose AI difficulty for each opponent
  • 4 spawn positions (corners of map)

Starting multiplayer game...

[Menu appears - select 2 AI opponents]
[Configure AI 1: Intermediate]
[Configure AI 2: Hybrid]

======================================================================
🎮 MULTIPLAYER SETUP
======================================================================
   Total Players: 3
   Human Players: 1
   AI Opponents: 2
======================================================================

✅ AI 1: Intermediate (35% WR)
✅ AI 2: Hybrid (40% WR)

[Game starts with 3 players]
```

---

## 🐛 Troubleshooting

### Game won't start?
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Try again
./play_multiplayer.sh
```

### AI not working?
- Check if models exist (`bomber_game/models/ppo_agent.pth`)
- Try using Beginner or Intermediate AI
- Restart the game

### Performance issues?
- Reduce number of AI opponents
- Use simpler AI types (Beginner/Intermediate)
- Close other applications

---

## 🚀 Future Enhancements

Potential features for future versions:
- [ ] 2-4 human players (local multiplayer)
- [ ] Network multiplayer
- [ ] Custom spawn positions
- [ ] Team modes
- [ ] Tournament mode
- [ ] AI vs AI spectator mode

---

## ✅ Summary

**Multiplayer mode is ready!**

- ✅ 1 Human + 0-3 AI opponents
- ✅ 4 AI difficulty levels
- ✅ Individual AI configuration
- ✅ Corner spawn positions
- ✅ Last player standing wins

**Play now:**
```bash
./play_multiplayer.sh
```

**Recommended:** Start with 1 Intermediate AI, then try 2 opponents!

---

**Created:** 2025-10-13  
**Status:** ✅ Ready to Play  
**Mode:** 1 Human + 0-3 AI Opponents
