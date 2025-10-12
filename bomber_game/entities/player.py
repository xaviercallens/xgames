"""
Player entity for Bomberman game.
"""

import pygame
from .entity import Entity


class Player(Entity):
    """Player character that can move and place bombs."""
    
    def __init__(self, x, y, color, name="Player"):
        """
        Initialize player.
        
        Args:
            x: Starting grid x position
            y: Starting grid y position
            color: Player color (RGB tuple)
            name: Player name
        """
        super().__init__(x, y, 28, 28)
        self.grid_x = x
        self.grid_y = y
        self.color = color
        self.name = name
        
        # Movement
        self.speed = 4  # tiles per second
        self.move_x = 0
        self.move_y = 0
        
        # Bomb properties
        self.max_bombs = 1
        self.bomb_range = 2
        self.active_bombs = 0
        
        # Power-ups
        self.speed_level = 1
        
        # Animation
        self.direction = 'down'
        
    def move(self, dx, dy, grid, tile_size):
        """
        Move player in given direction.
        
        Args:
            dx: X direction (-1, 0, 1)
            dy: Y direction (-1, 0, 1)
            grid: Game grid for collision
            tile_size: Size of each tile
        """
        if dx != 0:
            self.direction = 'right' if dx > 0 else 'left'
        elif dy != 0:
            self.direction = 'down' if dy > 0 else 'up'
            
        # Calculate new position
        new_x = self.x + dx * self.speed * (1/30)  # Assuming 30 FPS
        new_y = self.y + dy * self.speed * (1/30)
        
        # Check collision with walls
        if self._can_move_to(new_x, new_y, grid, tile_size):
            self.x = new_x
            self.y = new_y
            self.grid_x = int(self.x + 0.5)
            self.grid_y = int(self.y + 0.5)
    
    def _can_move_to(self, x, y, grid, tile_size):
        """Check if player can move to position."""
        # Check corners of player hitbox
        corners = [
            (x + 0.1, y + 0.1),
            (x + 0.9, y + 0.1),
            (x + 0.1, y + 0.9),
            (x + 0.9, y + 0.9),
        ]
        
        for cx, cy in corners:
            gx, gy = int(cx), int(cy)
            if gx < 0 or gx >= len(grid[0]) or gy < 0 or gy >= len(grid):
                return False
            if grid[gy][gx] in [1, 2]:  # Wall or soft wall
                return False
        
        return True
    
    def can_place_bomb(self):
        """Check if player can place a bomb."""
        return self.active_bombs < self.max_bombs
    
    def add_powerup(self, powerup_type):
        """Apply power-up effect."""
        if powerup_type == 0:  # Bomb up
            self.max_bombs = min(self.max_bombs + 1, 8)
        elif powerup_type == 1:  # Fire up
            self.bomb_range = min(self.bomb_range + 1, 10)
        elif powerup_type == 2:  # Speed up
            self.speed = min(self.speed + 1, 8)
            self.speed_level += 1
    
    def render(self, screen, tile_size):
        """Render player on screen."""
        pixel_x = int(self.x * tile_size)
        pixel_y = int(self.y * tile_size)
        
        # Draw player body
        body_rect = pygame.Rect(
            pixel_x + 2,
            pixel_y + 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, self.color, body_rect, border_radius=4)
        
        # Draw eyes based on direction
        eye_color = (255, 255, 255)
        if self.direction == 'down':
            pygame.draw.circle(screen, eye_color, (pixel_x + 10, pixel_y + 12), 3)
            pygame.draw.circle(screen, eye_color, (pixel_x + 22, pixel_y + 12), 3)
        elif self.direction == 'up':
            pygame.draw.circle(screen, eye_color, (pixel_x + 10, pixel_y + 8), 3)
            pygame.draw.circle(screen, eye_color, (pixel_x + 22, pixel_y + 8), 3)
        elif self.direction == 'left':
            pygame.draw.circle(screen, eye_color, (pixel_x + 8, pixel_y + 10), 3)
            pygame.draw.circle(screen, eye_color, (pixel_x + 8, pixel_y + 20), 3)
        else:  # right
            pygame.draw.circle(screen, eye_color, (pixel_x + 24, pixel_y + 10), 3)
            pygame.draw.circle(screen, eye_color, (pixel_x + 24, pixel_y + 20), 3)
