"""
Caca (poop) entity for Trump Man game.
A blocking obstacle that players can place!
"""

import pygame
from .entity import Entity
from ..enhanced_graphics import ProutManGraphics


class Caca(Entity):
    """Caca (poop) that blocks movement - funny obstacle!"""
    
    def __init__(self, x, y, owner):
        """
        Initialize caca.
        
        Args:
            x: Grid x position
            y: Grid y position
            owner: Player who placed the caca
        """
        super().__init__(x, y, 56, 56)
        self.grid_x = x
        self.grid_y = y
        self.owner = owner
        self.duration = 5.0  # Lasts 5 seconds before disappearing
        
    def update(self, dt):
        """Update caca timer."""
        self.duration -= dt
        if self.duration <= 0:
            self.alive = False
    
    def render(self, screen, tile_size):
        """Render caca on screen - enhanced poop pile!"""
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Use enhanced graphics for better visuals
        ProutManGraphics.draw_enhanced_caca(
            screen, pixel_x, pixel_y, self.duration, tile_size
        )
