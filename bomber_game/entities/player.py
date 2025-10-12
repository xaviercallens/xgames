"""
Player entity for Trump Man game.
"""

import pygame
from .entity import Entity
from ..assets import get_asset_manager


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
        super().__init__(x, y, 40, 40)  # Smaller hitbox for better movement
        self.grid_x = x
        self.grid_y = y
        self.color = color
        self.name = name
        
        # Position is in grid coordinates (float for smooth movement)
        self.x = float(x)
        self.y = float(y)
        
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
        
        # Animation
        self.direction = 'down'
        
        # Sprite
        self.sprite = None
        self.player_num = 1 if color == (0, 255, 0) else 2  # Green=1, Red=2
        self._load_sprite()
        
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
            # Update grid position (rounded to nearest tile)
            self.grid_x = int(round(self.x))
            self.grid_y = int(round(self.y))
    
    def _can_move_to(self, x, y, grid, tile_size, game_state=None):
        """Check if player can move to position."""
        # Use a smaller hitbox (0.35 tiles from center = 0.7 tile width)
        # This allows easier movement through tight spaces
        hitbox_size = 0.35  # Half-width of hitbox
        
        # Check corners of smaller hitbox centered on player
        corners = [
            (x - hitbox_size, y - hitbox_size),  # Top-left
            (x + hitbox_size, y - hitbox_size),  # Top-right
            (x - hitbox_size, y + hitbox_size),  # Bottom-left
            (x + hitbox_size, y + hitbox_size),  # Bottom-right
        ]
        
        for cx, cy in corners:
            gx, gy = int(cx), int(cy)
            # Check bounds
            if gx < 0 or gx >= len(grid[0]) or gy < 0 or gy >= len(grid):
                return False
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
    
    def _load_sprite(self):
        """Load player sprite."""
        try:
            assets = get_asset_manager()
            self.sprite = assets.get_player_sprite(self.player_num, (56, 56))
        except Exception as e:
            print(f"Could not load player sprite: {e}")
            self.sprite = None
    
    def render(self, screen, tile_size):
        """Render player on screen."""
        # Convert grid position to pixel position (centered on tile)
        pixel_x = int(self.x * tile_size)
        pixel_y = int(self.y * tile_size)
        
        # Use sprite if available, otherwise draw simple shape
        if self.sprite:
            # Center the sprite on the player's position
            sprite_rect = self.sprite.get_rect()
            sprite_rect.center = (pixel_x + tile_size // 2, pixel_y + tile_size // 2)
            screen.blit(self.sprite, sprite_rect)
        else:
            # Fallback to simple colored rectangle
            body_rect = pygame.Rect(
                pixel_x + 4,
                pixel_y + 4,
                self.width,
                self.height
            )
            pygame.draw.rect(screen, self.color, body_rect, border_radius=4)
            
            # Draw eyes based on direction
            eye_color = (255, 255, 255)
            if self.direction == 'down':
                pygame.draw.circle(screen, eye_color, (pixel_x + 16, pixel_y + 20), 3)
                pygame.draw.circle(screen, eye_color, (pixel_x + 32, pixel_y + 20), 3)
            elif self.direction == 'up':
                pygame.draw.circle(screen, eye_color, (pixel_x + 16, pixel_y + 12), 3)
                pygame.draw.circle(screen, eye_color, (pixel_x + 32, pixel_y + 12), 3)
