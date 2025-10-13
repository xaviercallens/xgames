# Quick Reference Card

**Fast access to all game features**

---

## 🚀 Launch Commands

### Interactive Launcher (Recommended)
```bash
./launch_bomberman_interactive.sh
```
Choose from: Single Player, Multiplayer, or Quick Start

### Direct Launchers
```bash
./launch_bomberman.sh        # Original single player
./play_multiplayer.sh         # Direct to multiplayer
./play_hybrid.sh              # Hybrid AI mode
```

### Training
```bash
./start_overnight_training.sh # Train AI
python monitor_training.py    # Monitor progress
```

---

## 🎮 Game Modes

| Mode | Command | Players | AI Config |
|------|---------|---------|-----------|
| **Single Player** | Option 1 | 1v1 | Choose 1 AI |
| **Multiplayer** | Option 2 | 1v1, 1v2, 1v3 | Configure each |
| **Quick Start** | Option 3 | 1v1 | Auto (Intermediate) |

---

## 🤖 AI Types

| Type | Win Rate | Best For |
|------|----------|----------|
| Beginner | 10% | Learning |
| Intermediate | 35% | Balanced |
| Advanced (PPO) | 20% | See AI learning |
| Hybrid | 40% | Best challenge |
| Expert | Varies | Maximum difficulty |

---

## 🎯 Controls

### In-Game
- **WASD** or **Arrows** - Move
- **SPACE** - Place bomb
- **P** - Pause
- **R** - Restart
- **ESC** - Quit

### In Menus
- **↑/↓** or **W/S** - Navigate
- **←/→** or **A/D** - Change selection
- **ENTER/SPACE** - Confirm
- **ESC** - Back/Cancel

---

## 📊 Quick Setup Examples

### Beginner
```bash
./launch_bomberman_interactive.sh
→ 1 (Single Player)
→ Beginner Bot
```

### Intermediate
```bash
./launch_bomberman_interactive.sh
→ 1 (Single Player)
→ Intermediate Bot
```

### Challenge
```bash
./launch_bomberman_interactive.sh
→ 2 (Multiplayer)
→ 2 AI Opponents
→ Intermediate + Hybrid
```

### Chaos
```bash
./launch_bomberman_interactive.sh
→ 2 (Multiplayer)
→ 3 AI Opponents
→ All Hybrid
```

### Quick Game
```bash
./launch_bomberman_interactive.sh
→ 3 (Quick Start)
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `COMPLETE_FEATURE_SUMMARY.md` | Full feature documentation |
| `INTERACTIVE_LAUNCHER_GUIDE.md` | Launcher guide |
| `MULTIPLAYER_GUIDE.md` | Multiplayer details |
| `QUICK_START.md` | Quick start guide |
| `TRAINING_RESULTS.md` | Training statistics |

---

## 🐛 Troubleshooting

### Won't launch?
```bash
chmod +x *.sh
source .venv/bin/activate
pip install -r requirements.txt
```

### AI not working?
Use Beginner or Intermediate (don't need trained models)

### Performance issues?
Use fewer AI opponents or simpler AI types

---

## 💡 Pro Tips

1. **Start with Beginner** - Learn the game
2. **Try Intermediate** - Balanced challenge
3. **Test Hybrid** - Best AI performance
4. **Use Multiplayer** - More strategic
5. **Quick Start** - For fast games

---

**Everything at your fingertips!** 🎮
