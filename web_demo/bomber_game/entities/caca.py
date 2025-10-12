"""
Caca (poop) entity for Trump Man game.
A blocking obstacle that players can place!
"""

import pygame
from .entity import Entity


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
        """Render caca on screen - brown poop pile!"""
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Draw poop pile (brown with highlights)
        # Base of poop
        base_color = (101, 67, 33)  # Dark brown
        highlight_color = (139, 90, 43)  # Lighter brown
        
        # Bottom pile
        bottom_rect = pygame.Rect(
            pixel_x + 8,
            pixel_y + tile_size - 24,
            tile_size - 16,
            20
        )
        pygame.draw.ellipse(screen, base_color, bottom_rect)
        
        # Middle pile
        middle_rect = pygame.Rect(
            pixel_x + 12,
            pixel_y + tile_size - 36,
            tile_size - 24,
            18
        )
        pygame.draw.ellipse(screen, highlight_color, middle_rect)
        
        # Top pile (smaller)
        top_rect = pygame.Rect(
            pixel_x + 16,
            pixel_y + tile_size - 46,
            tile_size - 32,
            14
        )
        pygame.draw.ellipse(screen, base_color, top_rect)
        
        # Add stink lines (green wavy lines)
        stink_color = (100, 150, 50)
        import math
        offset = int(self.duration * 2) % 4
        
        for i in range(3):
            x_pos = pixel_x + 16 + i * 12
            y_start = pixel_y + tile_size - 48
            # Wavy stink line
            for j in range(3):
                y_pos = y_start - j * 6
                x_offset = int(math.sin((self.duration * 3 + i + j) * 0.5) * 3)
                pygame.draw.circle(screen, stink_color, 
                                 (x_pos + x_offset, y_pos), 2)
        
        # Add shine/highlight
        shine_color = (160, 110, 60)
        pygame.draw.circle(screen, shine_color, 
                         (pixel_x + tile_size // 2 - 8, pixel_y + tile_size - 32), 4)
