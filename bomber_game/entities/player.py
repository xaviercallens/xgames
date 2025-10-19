"""
Player entity for Trump Man game.
"""

import pygame
from .entity import Entity
from ..assets import get_asset_manager
from ..enhanced_graphics import ProutManGraphics


class Player(Entity):
    """Player character that can move and place bombs."""
    
    def __init__(self, x, y, color, name="Player"):
        """
        Initialize player.
        
        Args:
            x: Starting grid x position
            y: Starting grid y position
            color: Player color (RGB tuple)
            name: Player name
        """
        super().__init__(x, y, 20, 20)  # 50% smaller hitbox
        self.grid_x = x
        self.grid_y = y
        self.color = color
        self.name = name
        
        # Position is in grid coordinates (float for smooth movement)
        # Position at CENTER of grid cell for proper collision detection
        self.x = float(x) + 0.5
        self.y = float(y) + 0.5
        
        # Movement
        self.speed = 7  # tiles per second (faster)
        self.move_x = 0
        self.move_y = 0
        
        # Bomb properties
        self.max_bombs = 2  # Start with 2 bombs
        self.bomb_range = 2
        self.active_bombs = 0
        
        # Caca properties
        self.max_cacas = 3
        self.active_cacas = 0
        
        # Power-ups
        self.speed_level = 1
        self.has_shield = False
        self.has_remote_bombs = False
        self.has_pierce_bombs = False
        self.shield_hits = 0  # Number of hits shield can take
        
        # Animation
        self.direction = 'down'
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  # Seconds per frame
        
        # Sprite
        self.sprite = None
        self.player_num = 1 if color == (0, 255, 0) else 2  # Green=1, Red=2
        self._load_sprite()
        
    def update(self, dt):
        """Update player animation."""
        # Update animation timer
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2  # 2-frame animation
    
    def move(self, dx, dy, grid, tile_size, game_state=None):
        """
        Move player in given direction.
        
        Args:
            dx: X direction (-1, 0, 1)
            dy: Y direction (-1, 0, 1)
            grid: Game grid for collision
            tile_size: Size of each tile
            game_state: Optional game state for checking bombs/cacas
        """
        # Update direction
        if dx != 0:
            self.direction = 'right' if dx > 0 else 'left'
        elif dy != 0:
            self.direction = 'down' if dy > 0 else 'up'
            
        # Calculate new position (in grid coordinates)
        new_x = self.x + dx * self.speed * (1/30)  # Assuming 30 FPS
        new_y = self.y + dy * self.speed * (1/30)
        
        # Check collision with walls using smaller hitbox
        if self._can_move_to(new_x, new_y, grid, tile_size, game_state):
            self.x = new_x
            self.y = new_y
            # Update grid position (floor since we're using cell centers)
            # Position 1.5 is in grid cell 1, position 2.3 is in grid cell 2
            import math
            self.grid_x = int(math.floor(self.x))
            self.grid_y = int(math.floor(self.y))
        else:
            # Reset animation when blocked
            self.animation_frame = 0
    
    def _can_move_to(self, x, y, grid, tile_size, game_state=None):
        """Check if player can move to position."""
        # Use a 50% smaller hitbox for easier movement
        # Player centered at (1.5, 1.5) with hitbox 0.2 has corners at (1.3, 1.3) to (1.7, 1.7)
        # which all stay within grid cell (1, 1)
        hitbox_size = 0.2  # Half-width of hitbox (50% of previous 0.4)
        
        # Check corners of smaller hitbox centered on player
        corners = [
            (x - hitbox_size, y - hitbox_size),  # Top-left
            (x + hitbox_size, y - hitbox_size),  # Top-right
            (x - hitbox_size, y + hitbox_size),  # Bottom-left
            (x + hitbox_size, y + hitbox_size),  # Bottom-right
        ]
        
        for cx, cy in corners:
            # Convert to grid coordinates using floor
            # This checks which grid cell the corner is in
            import math
            gx = math.floor(cx)
            gy = math.floor(cy)
            
            # Skip corners that are out of bounds
            if gx < 0 or gx >= len(grid[0]) or gy < 0 or gy >= len(grid):
                continue
            
            # Check for walls
            if grid[gy][gx] in [1, 2]:  # Wall or soft wall
                return False
        
        # Check for bombs and cacas if game_state provided
        if game_state:
            player_grid_x = int(round(x))
            player_grid_y = int(round(y))
            
            # Check for bombs (can't walk through them)
            for bomb in game_state.bombs:
                if bomb.grid_x == player_grid_x and bomb.grid_y == player_grid_y:
                    return False
            
            # Check for cacas (can't walk through them)
            for caca in game_state.cacas:
                if caca.grid_x == player_grid_x and caca.grid_y == player_grid_y:
                    return False
        
        return True
    
    def can_place_bomb(self):
        """Check if player can place a bomb."""
        return self.active_bombs < self.max_bombs
    
    def can_place_caca(self):
        """Check if player can place a caca."""
        return self.active_cacas < self.max_cacas
    
    def add_powerup(self, powerup_type):
        """Apply power-up effect."""
        if powerup_type == 0:  # Bomb up
            self.max_bombs = min(self.max_bombs + 1, 8)
        elif powerup_type == 1:  # Fire up
            self.bomb_range = min(self.bomb_range + 1, 10)
        elif powerup_type == 2:  # Speed up
            self.speed = min(self.speed + 1, 8)
            self.speed_level += 1
        elif powerup_type == 3:  # Shield
            self.has_shield = True
            self.shield_hits = 1  # Can survive 1 hit
        elif powerup_type == 4:  # Remote detonator
            self.has_remote_bombs = True
        elif powerup_type == 5:  # Pierce bombs
            self.has_pierce_bombs = True
    
    def _load_sprite(self):
        """Load player sprite."""
        try:
            assets = get_asset_manager()
            # 50% smaller sprite: 28x28 instead of 56x56
            self.sprite = assets.get_player_sprite(self.player_num, (28, 28))
        except Exception as e:
            print(f"Could not load player sprite: {e}")
            self.sprite = None
    
    def render(self, screen, tile_size):
        """Render player on screen with smooth sub-pixel positioning."""
        # Convert grid position to pixel position with sub-pixel accuracy
        # Since player position is already at cell center (e.g., 1.5),
        # we multiply by tile_size to get exact pixel position
        pixel_x = self.x * tile_size
        pixel_y = self.y * tile_size
        
        # Use sprite if available, otherwise use enhanced graphics
        if self.sprite:
            # Center the sprite directly on the pixel position
            # Use float positioning for smooth movement
            sprite_rect = self.sprite.get_rect()
            sprite_rect.centerx = pixel_x
            sprite_rect.centery = pixel_y
            screen.blit(self.sprite, sprite_rect)
        else:
            # Use enhanced graphics for better visuals
            ProutManGraphics.draw_enhanced_player(
                screen, pixel_x, pixel_y, self.color,
                direction=self.direction,
                animation_frame=self.animation_frame,
                tile_size=tile_size
            )
