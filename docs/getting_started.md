# Getting Started with Python Game Development

## Quick Setup

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Or install manually:**
   ```bash
   pip install -r requirements.txt
   ```

## Your First Game

### Option 1: Modify Existing Games

Start by modifying one of the example games:

- **`snake_game.py`** - Your existing Turtle-based Snake game
- **`games_2d/space_shooter.py`** - Pygame space shooter
- **`games_3d/cube_runner.py`** - Panda3D 3D runner
- **`examples/simple_platformer.py`** - Physics-based platformer
- **`examples/physics_demo.py`** - Interactive physics simulation

### Option 2: Create a New Game

1. **Choose your framework:**
   - **Pygame**: Best for 2D games, lots of tutorials
   - **Panda3D**: Full 3D engine, more complex but powerful
   - **Arcade**: Modern 2D framework with built-in physics

2. **Use the utility modules:**
   ```python
   from utils.game_math import Vector2D, circle_collision
   from utils.input_handler import InputManager, Keys
   ```

3. **Follow the game structure:**
   ```python
   class MyGame:
       def __init__(self):
           # Initialize game
           pass
           
       def handle_events(self):
           # Handle input
           pass
           
       def update(self):
           # Update game logic
           pass
           
       def draw(self):
           # Render graphics
           pass
           
       def run(self):
           # Main game loop
           while self.running:
               self.handle_events()
               self.update()
               self.draw()
   ```

## Game Development Concepts

### 1. Game Loop
Every game needs a main loop that:
- Handles input
- Updates game state
- Renders graphics
- Controls timing (FPS)

### 2. Sprites and Objects
- Use classes for game entities (Player, Enemy, Bullet)
- Inherit from framework sprite classes when possible
- Separate data from behavior

### 3. Collision Detection
```python
# Circle collision
if circle_collision(pos1, radius1, pos2, radius2):
    # Handle collision
    
# Rectangle collision (Pygame)
if sprite1.rect.colliderect(sprite2.rect):
    # Handle collision
```

### 4. Game States
Organize your game into states:
- Menu
- Playing
- Paused
- Game Over

### 5. Asset Management
- Keep assets organized in the `assets/` folder
- Load assets once at startup
- Use appropriate formats (PNG for sprites, WAV for sounds)

## Common Patterns

### Player Movement
```python
# Pygame example
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player.x -= player.speed
if keys[pygame.K_RIGHT]:
    player.x += player.speed
```

### Sprite Groups (Pygame)
```python
# Create groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Add sprites
all_sprites.add(player)
enemies.add(enemy)

# Update and draw
all_sprites.update()
all_sprites.draw(screen)

# Check collisions
hits = pygame.sprite.spritecollide(player, enemies, False)
```

### Basic AI
```python
# Simple enemy AI
def update_enemy(enemy, player):
    # Move towards player
    if player.x > enemy.x:
        enemy.x += enemy.speed
    else:
        enemy.x -= enemy.speed
```

## Debugging Tips

1. **Print debug info:**
   ```python
   print(f"Player position: {player.x}, {player.y}")
   print(f"FPS: {clock.get_fps()}")
   ```

2. **Draw debug shapes:**
   ```python
   # Pygame - draw collision rectangles
   pygame.draw.rect(screen, RED, player.rect, 2)
   ```

3. **Use a debugger:**
   - Set breakpoints in your IDE
   - Step through code to find issues

## Performance Tips

1. **Limit object creation in game loop**
2. **Use sprite groups for batch operations**
3. **Optimize image formats and sizes**
4. **Profile your code to find bottlenecks**
5. **Use object pooling for frequently created objects**

## Next Steps

1. **Complete a simple game** (Pong, Breakout, or Asteroids)
2. **Add sound effects and music**
3. **Implement game states and menus**
4. **Learn about game design patterns**
5. **Experiment with different genres**

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Panda3D Manual](https://docs.panda3d.org/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [Real Python Game Tutorial](https://realpython.com/pygame-a-primer/)

Happy game development! 🎮
