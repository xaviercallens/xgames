"""
Bomberman Educational Game
A project for teaching Python, AI, and Reinforcement Learning

This package contains:
- Core game engine and mechanics
- Rule-based AI agents
- Machine Learning agents
- Reinforcement Learning agents
- Educational materials and tutorials
"""

__version__ = "0.1.0"
__author__ = "Xavier Callens"
__description__ = "Educational Bomberman game for learning Python, AI, and RL"

# Game constants
GRID_SIZE = 13
TILE_SIZE = 64  # Doubled from 32 for bigger screen!
FPS = 30
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE + 64  # Extra space for UI

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Game tile types
TILE_EMPTY = 0
TILE_WALL = 1
TILE_SOFT_WALL = 2
TILE_BOMB = 3
TILE_EXPLOSION = 4
TILE_CACA = 5  # Poop block!

# Actions
ACTION_NONE = 0
ACTION_UP = 1
ACTION_DOWN = 2
ACTION_LEFT = 3
ACTION_RIGHT = 4
ACTION_BOMB = 5
ACTION_CACA = 6  # Drop caca!

ACTION_NAMES = {
    ACTION_NONE: "NONE",
    ACTION_UP: "UP",
    ACTION_DOWN: "DOWN",
    ACTION_LEFT: "LEFT",
    ACTION_RIGHT: "RIGHT",
    ACTION_BOMB: "BOMB",
    ACTION_CACA: "CACA"
}

# Power-up types
POWERUP_BOMB_UP = 0
POWERUP_FIRE_UP = 1
POWERUP_SPEED_UP = 2

POWERUP_NAMES = {
    POWERUP_BOMB_UP: "Bomb+",
    POWERUP_FIRE_UP: "Fire+",
    POWERUP_SPEED_UP: "Speed+"
}
