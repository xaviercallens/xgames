"""
Explosion entity for Trump Man game.
A smelly green/brown cloud!
"""

import pygame
from .entity import Entity
from ..enhanced_graphics import ProutManGraphics


class Explosion(Entity):
    """Smelly explosion from a trump (prout)!"""
    
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
        """Render smelly explosion on screen - enhanced cloud effect!"""
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Use enhanced graphics for better visuals
        ProutManGraphics.draw_enhanced_explosion(
            screen, pixel_x, pixel_y, self.timer, self.max_timer, tile_size
        )
