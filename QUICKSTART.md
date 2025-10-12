# 🚀 Quick Start Guide - Bomberman Game

## ✅ Installation & Setup

### Option 1: Easy Launch (Recommended)
```bash
# Navigate to project directory
cd ~/CascadeProjects/windsurf-project-2

# Run the launch script
./launch_bomberman.sh
```

### Option 2: Manual Launch
```bash
# Navigate to project directory
cd ~/CascadeProjects/windsurf-project-2

# Activate virtual environment
source game_dev_env/bin/activate

# Run the game
python play_bomberman.py
```

### Option 3: Direct Python
```bash
cd ~/CascadeProjects/windsurf-project-2
source game_dev_env/bin/activate
python -m bomber_game.game_engine
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **W** or **↑** | Move Up |
| **S** or **↓** | Move Down |
| **A** or **←** | Move Left |
| **D** or **→** | Move Right |
| **Space** | Place Bomb |
| **P** | Pause/Resume |
| **R** | Restart (when game over) |
| **ESC** | Quit Game |

## 🎯 How to Play

1. **You are the GREEN player** in the top-left corner
2. **The AI is the RED player** in the bottom-right corner
3. **Move around** using WASD or Arrow keys
4. **Place bombs** with Space to destroy walls
5. **Collect power-ups** hidden under brown walls:
   - 🔴 **Red** = More bombs
   - 🟠 **Orange** = Bigger explosions
   - 🔵 **Blue** = Faster movement
6. **Avoid explosions** - they hurt you too!
7. **Defeat the AI** to win!

## 🐛 Troubleshooting

### "No module named pygame"
```bash
source game_dev_env/bin/activate
pip install pygame
```

### "No DISPLAY variable"
```bash
export DISPLAY=:0
python play_bomberman.py
```

### "GameState object has no attribute"
This has been fixed! Make sure you have the latest code:
```bash
git pull
```

### Game window doesn't appear
- Make sure you have a graphical environment
- Try: `export DISPLAY=:0`
- On remote systems, you may need X11 forwarding

### Game is slow or laggy
- Close other applications
- The game runs at 30 FPS by default
- Check your system resources

## 📝 Quick Tips

### For Your First Game:
1. **Take it slow** - Learn the controls first
2. **Watch the AI** - See how it moves
3. **Be careful** - Don't trap yourself with bombs!
4. **Collect power-ups** - They make you stronger
5. **Have fun!** - It's okay to lose at first

### Strategy Tips:
- **Corner the AI** - Trap it with bombs
- **Use walls** - Hide behind them for safety
- **Power-ups first** - Get stronger before fighting
- **Watch timers** - Bombs explode after 3 seconds
- **Escape routes** - Always have a way out

## 🎓 Learning Mode

### Explore the Code:
```bash
# Look at the player code
cat bomber_game/entities/player.py

# Check out the AI
cat bomber_game/agents/simple_agent.py

# See the game config
cat bomber_game/config.py
```

### Make Simple Changes:
```bash
# Edit configuration
nano bomber_game/config.py

# Try changing:
# - bomb_timer: 2.0 (faster explosions)
# - initial_bombs: 2 (start with more bombs)
# - initial_range: 3 (bigger explosions)
```

## 📊 Game Stats

After playing, discuss:
- How many times did you win?
- What strategies worked?
- How does the AI make decisions?
- What would make the game better?

## 🔧 Advanced Options

### Run in Debug Mode:
```bash
python play_bomberman.py --debug
```

### Change Grid Size:
Edit `bomber_game/__init__.py`:
```python
GRID_SIZE = 15  # Bigger world!
```

### Adjust AI Difficulty:
Edit `bomber_game/agents/simple_agent.py`:
```python
self.think_delay = 0.5  # Slower AI (easier)
self.think_delay = 0.1  # Faster AI (harder)
```

## 📚 Next Steps

1. **Play 5-10 games** - Get comfortable with controls
2. **Beat the AI** - Celebrate your first win!
3. **Read the code** - Start with `player.py`
4. **Make a change** - Try modifying colors or speeds
5. **Discuss** - Talk about what you learned

## 🎉 Have Fun!

Remember:
- **Learning is the goal** - Winning is just a bonus
- **Experiment freely** - You can't break anything permanently
- **Ask questions** - There are no dumb questions
- **Take breaks** - Fresh eyes solve problems better

**Ready? Let's play! 🎮**

---

## 📞 Need Help?

- Check `bomber_game/README.md` for detailed info
- Read `EDUCATION_PLAN.md` for the learning path
- See `spec.md` for complete documentation
- Ask questions and experiment!

**Happy gaming and learning! 🚀**
