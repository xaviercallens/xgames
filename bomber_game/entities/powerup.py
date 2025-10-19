"""
PowerUp entity for Bomberman game.
"""

import pygame
from .entity import Entity
from ..enhanced_graphics import ProutManGraphics


class PowerUp(Entity):
    """Power-up that enhances player abilities."""
    
    TYPES = {
        0: {'name': 'Bomb+', 'color': (255, 100, 100), 'description': 'More bombs!'},
        1: {'name': 'Fire+', 'color': (255, 150, 0), 'description': 'Bigger explosions!'},
        2: {'name': 'Speed+', 'color': (100, 200, 255), 'description': 'Move faster!'},
        3: {'name': 'Shield', 'color': (100, 255, 100), 'description': 'Survive one hit!'},
        4: {'name': 'Remote', 'color': (255, 255, 100), 'description': 'Detonate on command!'},
        5: {'name': 'Pierce', 'color': (200, 100, 255), 'description': 'Bombs go through walls!'},
    }
    
    def __init__(self, x, y, powerup_type):
        """
        Initialize power-up.
        
        Args:
            x: Grid x position
            y: Grid y position
            powerup_type: Type of power-up (0=Bomb, 1=Fire, 2=Speed)
        """
        super().__init__(x, y, 24, 24)
        self.grid_x = x
        self.grid_y = y
        self.powerup_type = powerup_type
        self.collected = False
        self.float_offset = 0
        
    def update(self, dt):
        """Update power-up animation."""
        self.float_offset += dt * 3  # Floating animation speed
    
    def render(self, screen, tile_size):
        """Render power-up on screen with enhanced graphics."""
        import math
        
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Floating effect
        float_y = int(math.sin(self.float_offset) * 3)
        
        # Draw power-up using enhanced graphics
        center_x = pixel_x + tile_size // 2
        center_y = pixel_y + tile_size // 2 + float_y
        
        ProutManGraphics.draw_enhanced_powerup(
            screen, center_x, center_y, self.powerup_type, tile_size
        )
