"""
Explosion entity for Bomberman game.
"""

import pygame
from .entity import Entity


class Explosion(Entity):
    """Explosion from a bomb."""
    
    def __init__(self, x, y):
        """
        Initialize explosion.
        
        Args:
            x: Grid x position
            y: Grid y position
        """
        super().__init__(x, y, 32, 32)
        self.grid_x = x
        self.grid_y = y
        self.timer = 0.5  # Duration in seconds
        self.max_timer = 0.5
        
    def update(self, dt):
        """Update explosion timer."""
        self.timer -= dt
        if self.timer <= 0:
            self.alive = False
    
    def render(self, screen, tile_size):
        """Render explosion on screen."""
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Fade out effect
        alpha = int(255 * (self.timer / self.max_timer))
        
        # Create explosion colors (orange to yellow)
        colors = [
            (255, 100, 0, alpha),   # Orange
            (255, 200, 0, alpha),   # Yellow-orange
            (255, 255, 0, alpha),   # Yellow
        ]
        
        # Draw multiple circles for explosion effect
        for i, color in enumerate(colors):
            radius = int((tile_size // 2) * (1 - i * 0.2))
            center = (pixel_x + tile_size // 2, pixel_y + tile_size // 2)
            
            # Create surface with alpha
            surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (tile_size // 2, tile_size // 2), radius)
            screen.blit(surf, (pixel_x, pixel_y))
