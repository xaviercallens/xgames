"""
Bomb entity for Bomberman game.
"""

import pygame
from .entity import Entity


class Bomb(Entity):
    """Bomb that explodes after a timer."""
    
    def __init__(self, x, y, bomb_range, owner):
        """
        Initialize bomb.
        
        Args:
            x: Grid x position
            y: Grid y position
            bomb_range: Explosion range in tiles
            owner: Player who placed the bomb
        """
        super().__init__(x, y, 28, 28)
        self.grid_x = x
        self.grid_y = y
        self.bomb_range = bomb_range
        self.owner = owner
        self.timer = 3.0  # 3 seconds until explosion
        self.exploded = False
        
    def update(self, dt):
        """Update bomb timer."""
        self.timer -= dt
        if self.timer <= 0 and not self.exploded:
            self.exploded = True
            self.alive = False
            # Owner can place another bomb
            if self.owner:
                self.owner.active_bombs -= 1
    
    def render(self, screen, tile_size):
        """Render bomb on screen."""
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Bomb body
        bomb_rect = pygame.Rect(
            pixel_x + 4,
            pixel_y + 4,
            tile_size - 8,
            tile_size - 8
        )
        
        # Pulsing effect based on timer
        pulse = int((self.timer * 4) % 2)
        color = (50, 50, 50) if pulse == 0 else (80, 80, 80)
        
        pygame.draw.ellipse(screen, color, bomb_rect)
        
        # Fuse
        fuse_color = (255, 100, 0) if self.timer < 1.0 else (200, 200, 0)
        fuse_rect = pygame.Rect(pixel_x + 14, pixel_y + 2, 4, 6)
        pygame.draw.rect(screen, fuse_color, fuse_rect, border_radius=2)
