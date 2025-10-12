"""
Base Entity class for all game objects.
"""

import pygame


class Entity:
    """Base class for all game entities."""
    
    def __init__(self, x, y, width, height):
        """
        Initialize entity.
        
        Args:
            x: Grid x position
            y: Grid y position
            width: Entity width in pixels
            height: Entity height in pixels
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alive = True
        
    def get_rect(self, tile_size):
        """Get pygame rect for collision detection."""
        return pygame.Rect(
            self.x * tile_size,
            self.y * tile_size,
            self.width,
            self.height
        )
    
    def update(self, dt):
        """Update entity state. Override in subclasses."""
        pass
    
    def render(self, screen, tile_size):
        """Render entity. Override in subclasses."""
        pass
