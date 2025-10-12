# 🎮 Python Game Development - Educational Project

A comprehensive game development environment featuring **Trump Man** (Prouts Man), a fully-featured educational Bomberman-style game with professional graphics, smart AI, and hilarious gameplay!

## 🌟 **Featured: Trump Man (Prouts Man) v2.1**

**A complete educational Bomberman game with:**
- 💨 **Smelly Trump Bombs** - Hilarious explosions!
- 💩 **Caca Blocks** - Strategic poop obstacles!
- 🤖 **Smart AI Opponent** - Challenging gameplay
- 🎨 **Professional Sprites** - Beautiful graphics
- 📚 **Educational Value** - Learn Python, AI, and game dev!

### **Quick Play:**
```bash
./launch_bomberman.sh
```

---

## 🎮 Development Features

- **2D Game Development**: Pygame, Arcade, Pyglet
- **3D Game Development**: Panda3D, ModernGL, Ursina
- **Physics Engines**: Pymunk (2D), PyBullet (3D)
- **Utility Modules**: Math helpers, input handling, collision detection
- **Complete Examples**: Trump Man, Space Shooter, Cube Runner

## 📁 Project Structure

```
windsurf-project-2/
├── 🎮 TRUMP MAN GAME (Featured!)
│   ├── bomber_game/              # Main game package
│   │   ├── __init__.py          # Game constants
│   │   ├── config.py            # Settings
│   │   ├── assets.py            # Asset manager
│   │   ├── game_state.py        # Game logic
│   │   ├── game_engine.py       # Main loop
│   │   ├── entities/            # Game objects
│   │   │   ├── player.py        # Player with sprites
│   │   │   ├── bomb.py          # Trump bombs
│   │   │   ├── caca.py          # Poop blocks!
│   │   │   ├── explosion.py     # Explosions
│   │   │   └── powerup.py       # Power-ups
│   │   ├── agents/              # AI system
│   │   │   └── simple_agent.py  # Smart AI
│   │   └── assets/images/       # Professional sprites
│   ├── play_bomberman.py        # Game launcher
│   ├── launch_bomberman.sh      # Quick start
│   └── 📚 Documentation/
│       ├── TRUMP_MAN_COMPLETE.md    # Complete guide
│       ├── TRUMP_MAN_V2_FEATURES.md # v2.0 features
│       ├── VISUAL_UPGRADE.md        # Sprite guide
│       └── EDUCATION_PLAN.md        # Learning path
│
├── games_2d/                # 2D examples
│   └── space_shooter.py
├── games_3d/                # 3D examples
│   └── cube_runner.py
├── utils/                   # Utilities
└── assets/                  # Shared assets
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv game_dev_env
source game_dev_env/bin/activate  # On Windows: game_dev_env\\Scripts\\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Play Trump Man! 🎮

**The Featured Educational Game:**
```bash
./launch_bomberman.sh
```

**Controls:**
- WASD or Arrows: Move
- Space: Drop Trump 💨
- C: Drop Caca 💩
- P: Pause
- R: Restart

**Read the complete guide:**
```bash
cat TRUMP_MAN_COMPLETE.md
```

---

### 3. Run Other Example Games

**2D Space Shooter (Pygame):**
```bash
python games_2d/space_shooter.py
```

**3D Cube Runner (Panda3D):**
```bash
python games_3d/cube_runner.py
```

**Original Snake Game:**
```bash
python snake_game.py
```

## 📚 Library Overview

### 2D Game Development

#### Pygame
- **Best for**: Traditional 2D games, pixel-perfect control
- **Pros**: Mature, extensive documentation, large community
- **Use cases**: Platformers, shoot-em-ups, puzzle games

#### Arcade
- **Best for**: Modern 2D games with built-in physics
- **Pros**: Modern Python practices, built-in sprite physics
- **Use cases**: Educational games, modern 2D games

#### Pyglet
- **Best for**: Performance-critical 2D games
- **Pros**: OpenGL-based, cross-platform, minimal dependencies
- **Use cases**: Real-time games, multimedia applications

### 3D Game Development

#### Panda3D
- **Best for**: Full-featured 3D games
- **Pros**: Complete game engine, built-in scene graph, physics
- **Use cases**: 3D adventures, simulations, complex 3D games

#### ModernGL
- **Best for**: Custom 3D graphics and shaders
- **Pros**: Direct OpenGL access, high performance
- **Use cases**: Graphics programming, custom renderers

#### Ursina
- **Best for**: Rapid 3D prototyping
- **Pros**: Simple API, built on Panda3D, beginner-friendly
- **Use cases**: Game jams, prototypes, educational projects

### Physics Engines

#### Pymunk (2D)
```python
import pymunk

# Create physics space
space = pymunk.Space()
space.gravity = (0, -981)  # Gravity

# Create physics body
body = pymunk.Body(1, 1666)  # mass, moment
shape = pymunk.Circle(body, 25)  # radius
space.add(body, shape)
```

#### PyBullet (3D)
```python
import pybullet as p

# Initialize physics
p.connect(p.GUI)
p.setGravity(0, 0, -9.8)

# Create collision shapes
collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[1, 1, 1])
body = p.createMultiBody(1.0, collision_shape, collision_shape)
```

## 🛠️ Development Tips

### Performance Optimization

1. **Use sprite groups** in Pygame for efficient rendering
2. **Limit object creation** in game loops
3. **Use object pooling** for frequently created/destroyed objects
4. **Profile your code** with cProfile

### Code Organization

1. **Separate game logic** from rendering
2. **Use composition** over inheritance for game objects
3. **Implement game states** (menu, playing, paused, game over)
4. **Create reusable components** for common functionality

### Asset Management

```python
# Example asset loader
class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
    
    def load_image(self, name, path):
        self.images[name] = pygame.image.load(path)
    
    def get_image(self, name):
        return self.images[name]
```

## 🎯 Next Steps

### Beginner Projects
1. **Pong** - Classic paddle game
2. **Breakout** - Brick-breaking game
3. **Tetris** - Falling blocks puzzle
4. **Platformer** - Side-scrolling jump game

### Intermediate Projects
1. **Tower Defense** - Strategic defense game
2. **RPG** - Role-playing game with stats/inventory
3. **Racing Game** - 3D racing with physics
4. **Puzzle Platformer** - Physics-based puzzles

### Advanced Projects
1. **Multiplayer Game** - Network programming
2. **Procedural Generation** - Infinite worlds
3. **AI Opponents** - Game AI and pathfinding
4. **VR Game** - Virtual reality integration

## 📖 Learning Resources

### Trump Man Documentation
- **TRUMP_MAN_COMPLETE.md** - Complete game guide
- **TRUMP_MAN_V2_FEATURES.md** - Feature details
- **VISUAL_UPGRADE.md** - Sprite integration
- **EDUCATION_PLAN.md** - Learning roadmap

### External Documentation
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Panda3D Manual](https://docs.panda3d.org/)
- [Arcade Documentation](https://api.arcade.academy/)

### Tutorials
- [Real Python Game Development](https://realpython.com/pygame-a-primer/)
- [Panda3D Tutorial](https://docs.panda3d.org/1.10/python/introduction/tutorial/index)
- [Game Development Patterns](https://gameprogrammingpatterns.com/)

### Communities
- [r/gamedev](https://reddit.com/r/gamedev)
- [Python Discord](https://discord.gg/python)
- [Pygame Community](https://www.pygame.org/wiki/about)

## 🐛 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Make sure you're in the virtual environment
pip list | grep pygame  # Check if installed
pip install --upgrade pygame  # Reinstall if needed
```

**Performance Issues:**
- Use `pygame.sprite.Group()` for batch operations
- Limit FPS with `clock.tick(60)`
- Optimize image formats (use .png for transparency, .jpg for photos)

**Audio Issues:**
```python
# Initialize pygame mixer before pygame
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()
```

## 🙏 Credits

### Trump Man Sprites
- **Source**: https://github.com/YoannHumeau/Bomberman
- **Author**: Yoann Humeau
- **License**: Open Source
- Thank you for the amazing sprites!

### Inspiration
- CoderOneHQ/bomberland repository
- Classic Bomberman games
- Educational game design principles

## 🤝 Contributing

Feel free to add more examples, improve existing code, or fix bugs. This setup is designed to be a learning resource and starting point for Python game development.

##  License

This project is open source and available under the MIT License.

---

## **Start Playing Trump Man Now!**

```bash
cd ~/CascadeProjects/windsurf-project-2
./launch_bomberman.sh
```

**Perfect for learning Python, AI, and game development while having fun!** 

---

**Happy Game Development!**
