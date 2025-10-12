# Quick Usage Guide

## 🚀 Getting Started

### 1. Activate Your Environment
```bash
# Method 1: Use the activation script (recommended)
./activate_env.sh

# Method 2: Manual activation
source game_dev_env/bin/activate
```

### 2. Test Your Setup
```bash
python test_setup.py
```

### 3. Run Example Games

**2D Games:**
```bash
# Space Shooter (Pygame)
python games_2d/space_shooter.py
# Controls: WASD/Arrows to move, Space to shoot

# Simple Platformer
python examples/simple_platformer.py  
# Controls: WASD/Arrows to move, Space/Up to jump

# Physics Demo (Interactive)
python examples/physics_demo.py
# Controls: Left click to create objects, Right click for explosion
```

**3D Games:**
```bash
# Cube Runner (requires display)
python games_3d/cube_runner.py
# Controls: A/D to move, Space to jump
```

**Original Game:**
```bash
# Your Snake Game
python snake_game.py
# Controls: WASD to move
```

## 🛠️ Development Commands

### Install Additional Packages
```bash
source game_dev_env/bin/activate
pip install package_name
```

### Run Tests
```bash
python test_setup.py
```

### Check Installed Packages
```bash
source game_dev_env/bin/activate
pip list
```

## 📁 Project Structure

```
windsurf-project-2/
├── 🎮 games_2d/           # 2D game examples
│   └── space_shooter.py   # Complete Pygame space shooter
├── 🎲 games_3d/           # 3D game examples  
│   └── cube_runner.py     # Panda3D 3D runner
├── 📚 examples/           # Additional examples
│   ├── simple_platformer.py  # Physics platformer
│   └── physics_demo.py       # Interactive physics
├── 🛠️ utils/              # Reusable modules
│   ├── game_math.py       # Vector math, collisions
│   └── input_handler.py   # Input management
├── 🎨 assets/             # Game assets
├── 📖 docs/               # Documentation
├── 🐍 snake_game.py       # Your original game
├── ⚙️ activate_env.sh     # Environment activation
└── 🧪 test_setup.py       # Setup verification
```

## 🎯 Next Steps

### Beginner Projects
1. **Modify existing games** - Change colors, speeds, add features
2. **Create Pong** - Classic paddle game
3. **Make Breakout** - Brick-breaking game

### Intermediate Projects  
1. **Add sound effects** to existing games
2. **Create game menus** and multiple levels
3. **Build a tower defense** game

### Advanced Projects
1. **Multiplayer games** with networking
2. **Procedural generation** for infinite levels
3. **AI opponents** with pathfinding

## 🐛 Troubleshooting

### Common Issues

**"python: command not found"**
```bash
# Use python3 instead
python3 games_2d/space_shooter.py

# Or activate environment first
source game_dev_env/bin/activate
python games_2d/space_shooter.py
```

**Import errors**
```bash
# Make sure environment is activated
source game_dev_env/bin/activate

# Reinstall if needed
pip install pygame numpy pillow
```

**Display issues (for 3D games)**
```bash
# May need X11 forwarding for remote systems
export DISPLAY=:0
```

## 📚 Learning Resources

- **Pygame Tutorial**: https://realpython.com/pygame-a-primer/
- **Game Programming Patterns**: https://gameprogrammingpatterns.com/
- **Python Game Development**: Check `docs/getting_started.md`

Happy coding! 🎮
