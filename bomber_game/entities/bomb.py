"""
Trump (Prout) entity for Trump Man game.
A smelly trump instead of a bomb!
"""

import pygame
from .entity import Entity
from ..assets import get_asset_manager
from ..enhanced_graphics import ProutManGraphics


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
            # Match player sprite size: 28x28
            self.sprite = assets.get_bomb_sprite((28, 28))
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
        """Render trump (prout) on screen - uses sprite or enhanced graphics!"""
        # Position at center of grid cell for consistency with players
        pixel_x = (self.grid_x + 0.5) * tile_size
        pixel_y = (self.grid_y + 0.5) * tile_size
        
        # Use sprite if available
        if self.sprite:
            # Center the sprite on the grid cell center
            sprite_rect = self.sprite.get_rect()
            sprite_rect.centerx = pixel_x
            sprite_rect.centery = pixel_y
            
            # Pulsing effect - scale based on timer
            if self.timer < 1.0:
                pulse_scale = 1.0 + 0.2 * (1.0 - self.timer)  # Grow as timer runs out
                scaled_sprite = pygame.transform.scale(
                    self.sprite,
                    (int(28 * pulse_scale), int(28 * pulse_scale))
                )
                scaled_rect = scaled_sprite.get_rect()
                scaled_rect.centerx = pixel_x
                scaled_rect.centery = pixel_y
                screen.blit(scaled_sprite, scaled_rect)
            else:
                screen.blit(self.sprite, sprite_rect)
        else:
            # Use enhanced graphics for better visuals
            ProutManGraphics.draw_enhanced_prout(
                screen, pixel_x, pixel_y, self.timer, tile_size
            )
