"""
Trump (Prout) entity for Trump Man game.
A smelly trump instead of a bomb!
"""

import pygame
from .entity import Entity
from ..assets import get_asset_manager


class Bomb(Entity):
    """Trump (Prout) that explodes after a timer with a smelly cloud!"""
    
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
        
        # Load sprite
        self.sprite = None
        self._load_sprite()
    
    def _load_sprite(self):
        """Load bomb sprite."""
        try:
            assets = get_asset_manager()
            self.sprite = assets.get_bomb_sprite((56, 56))
        except Exception as e:
            print(f"Could not load bomb sprite: {e}")
            self.sprite = None
        
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
        """Render trump (prout) on screen - uses sprite or fallback!"""
        pixel_x = int(self.grid_x * tile_size)
        pixel_y = int(self.grid_y * tile_size)
        
        # Use sprite if available
        if self.sprite:
            # Center the sprite
            sprite_rect = self.sprite.get_rect()
            sprite_rect.center = (pixel_x + tile_size // 2, pixel_y + tile_size // 2)
            
            # Pulsing effect - scale based on timer
            if self.timer < 1.0:
                pulse_scale = 1.0 + 0.1 * (1.0 - self.timer)  # Grow as timer runs out
                scaled_sprite = pygame.transform.scale(
                    self.sprite,
                    (int(56 * pulse_scale), int(56 * pulse_scale))
                )
                scaled_rect = scaled_sprite.get_rect(center=sprite_rect.center)
                screen.blit(scaled_sprite, scaled_rect)
            else:
                screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback: green and brown smelly cloud
            trump_rect = pygame.Rect(
                pixel_x + 4,
                pixel_y + 4,
                tile_size - 8,
                tile_size - 8
            )
            
            # Pulsing effect based on timer - alternating green and brown
            pulse = int((self.timer * 4) % 2)
            color = (100, 150, 50) if pulse == 0 else (139, 90, 43)  # Green / Brown
            
            pygame.draw.ellipse(screen, color, trump_rect)
            
            # Add stink lines
            stink_color = (150, 200, 100) if self.timer < 1.0 else (100, 150, 50)
            for i in range(3):
                offset = i * 16
                pygame.draw.line(screen, stink_color, 
                               (pixel_x + 16 + offset, pixel_y + 4),
                               (pixel_x + 14 + offset, pixel_y - 8), 2)
            
            # Add brown spots
            pygame.draw.circle(screen, (101, 67, 33), (pixel_x + 20, pixel_y + 24), 4)
            pygame.draw.circle(screen, (101, 67, 33), (pixel_x + 40, pixel_y + 32), 3)
