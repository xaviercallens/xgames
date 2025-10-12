# Python Game Development Setup

A comprehensive setup for both 2D and 3D game development in Python, featuring popular libraries and complete example games.

## 🎮 Features

- **2D Game Development**: Pygame, Arcade, Pyglet
- **3D Game Development**: Panda3D, ModernGL, Ursina
- **Physics Engines**: Pymunk (2D), PyBullet (3D)
- **Utility Modules**: Math helpers, input handling, collision detection
- **Complete Examples**: Space Shooter (2D) and Cube Runner (3D)

## 📁 Project Structure

```
windsurf-project-2/
├── requirements.txt          # All dependencies
├── README.md                # This file
├── snake_game.py            # Your original Turtle game
├── games_2d/                # 2D game examples
│   ├── __init__.py
│   └── space_shooter.py     # Complete Pygame example
├── games_3d/                # 3D game examples
│   ├── __init__.py
│   └── cube_runner.py       # Complete Panda3D example
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── game_math.py         # Vector math, collision detection
│   └── input_handler.py     # Input management system
├── assets/                  # Game assets
│   ├── images/
│   ├── sounds/
│   ├── models/
│   └── textures/
├── examples/                # Additional examples
└── docs/                    # Documentation
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

### 2. Run Example Games

**2D Space Shooter (Pygame):**
```bash
python games_2d/space_shooter.py
```
- Use WASD or Arrow Keys to move
- Space to shoot
- Avoid red enemies, shoot them for points
- R to restart when game over

**3D Cube Runner (Panda3D):**
```bash
python games_3d/cube_runner.py
```
- Use A/D or Arrow Keys to move left/right
- Space to jump
- Avoid red obstacles
- R to restart when game over

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

### Documentation
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

## 🤝 Contributing

Feel free to add more examples, improve existing code, or fix bugs. This setup is designed to be a learning resource and starting point for Python game development.

## 📄 License

This project is open source and available under the MIT License.
