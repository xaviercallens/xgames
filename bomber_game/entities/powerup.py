"""
PowerUp entity for Bomberman game.
"""

import pygame
from .entity import Entity


class PowerUp(Entity):
    """Power-up that enhances player abilities."""
    
    TYPES = {
        0: {'name': 'Bomb+', 'color': (255, 100, 100)},
        1: {'name': 'Fire+', 'color': (255, 150, 0)},
        2: {'name': 'Speed+', 'color': (100, 200, 255)},
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
        """Render power-up on screen."""
        import math
        
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Floating effect
        float_y = int(math.sin(self.float_offset) * 3)
        
        # Get power-up properties
        props = self.TYPES.get(self.powerup_type, self.TYPES[0])
        color = props['color']
        
        # Draw power-up
        center_x = pixel_x + tile_size // 2
        center_y = pixel_y + tile_size // 2 + float_y
        
        # Outer glow
        glow_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 100), (tile_size // 2, tile_size // 2), 14)
        screen.blit(glow_surf, (pixel_x, pixel_y + float_y))
        
        # Main body
        pygame.draw.circle(screen, color, (center_x, center_y), 10)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 10, 2)
        
        # Icon based on type
        if self.powerup_type == 0:  # Bomb+
            pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), 6)
        elif self.powerup_type == 1:  # Fire+
            points = [
                (center_x, center_y - 6),
                (center_x + 4, center_y + 2),
                (center_x - 4, center_y + 2),
            ]
            pygame.draw.polygon(screen, (255, 255, 0), points)
        elif self.powerup_type == 2:  # Speed+
            pygame.draw.polygon(screen, (255, 255, 255), [
                (center_x - 6, center_y),
                (center_x + 6, center_y),
                (center_x, center_y - 6),
            ])
