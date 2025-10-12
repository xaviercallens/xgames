"""
Bomb Machine Entity
Automatically drops bombs at the center of the map at regular intervals.
Players have 10 seconds to escape before explosion.
"""

import pygame
import random
from .entity import Entity
from .bomb import Bomb


class BombMachine(Entity):
    """
    Bomb machine that drops bombs at the center of the map.
    Creates a dangerous zone that players must avoid.
    """
    
    def __init__(self, grid_size):
        """
        Initialize bomb machine at center of map.
        
        Args:
            grid_size: Size of the game grid
        """
        center = grid_size // 2
        super().__init__(center, center)
        self.grid_size = grid_size
        self.timer = 0
        self.interval = 10.0  # Drop bomb every 10 seconds
        self.bomb_timer = 10.0  # Bombs explode after 10 seconds
        self.bomb_range = 3  # Explosion range
        self.animation_frame = 0
        self.warning_time = 2.0  # Warning 2 seconds before drop
        self.is_warning = False
        
    def update(self, dt, game_state):
        """
        Update bomb machine and drop bombs.
        
        Args:
            dt: Delta time
            game_state: Current game state
            
        Returns:
            Bomb object if dropped, None otherwise
        """
        self.timer += dt
        self.animation_frame += dt * 2  # Animation speed
        
        # Check if warning phase
        time_until_drop = self.interval - self.timer
        self.is_warning = time_until_drop <= self.warning_time and time_until_drop > 0
        
        # Drop bomb at interval
        if self.timer >= self.interval:
            self.timer = 0
            self.is_warning = False
            
            # Create bomb at center (or near center if occupied)
            bomb_pos = self._find_drop_position(game_state)
            if bomb_pos:
                bomb = Bomb(bomb_pos[0], bomb_pos[1], self.bomb_range, self.bomb_timer)
                return bomb
                
        return None
        
    def _find_drop_position(self, game_state):
        """
        Find valid position to drop bomb (center or nearby).
        
        Args:
            game_state: Current game state
            
        Returns:
            (x, y) tuple or None
        """
        center = self.grid_size // 2
        
        # Try center first
        if game_state.grid[center][center] == 0:
            # Check if no players on center
            players_on_center = False
            for player in game_state.players:
                if int(player.x) == center and int(player.y) == center:
                    players_on_center = True
                    break
            if not players_on_center:
                return (center, center)
        
        # Try positions around center
        for radius in range(1, 3):
            positions = []
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:
                        x, y = center + dx, center + dy
                        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                            if game_state.grid[y][x] == 0:
                                positions.append((x, y))
            
            if positions:
                return random.choice(positions)
                
        return None
        
    def get_warning_message(self):
        """
        Get warning message for UI.
        
        Returns:
            String with warning or None
        """
        if self.is_warning:
            time_left = self.interval - self.timer
            return f"⚠️ BOMB DROP IN {time_left:.1f}s!"
        return None
        
    def draw(self, screen, tile_size):
        """
        Draw bomb machine at center.
        
        Args:
            screen: Pygame surface
            tile_size: Size of each tile in pixels
        """
        x = self.grid_x * tile_size
        y = self.grid_y * tile_size
        
        # Draw machine base
        machine_color = (100, 100, 100)
        if self.is_warning:
            # Flash red during warning
            flash = int(128 * abs(pygame.time.get_ticks() % 500 - 250) / 250)
            machine_color = (200 + flash, 50, 50)
            
        pygame.draw.rect(screen, machine_color, (x + 4, y + 4, tile_size - 8, tile_size - 8))
        
        # Draw machine details
        pygame.draw.rect(screen, (150, 150, 150), (x + 8, y + 8, tile_size - 16, tile_size - 16), 2)
        
        # Draw bomb symbol
        center_x = x + tile_size // 2
        center_y = y + tile_size // 2
        
        # Animated bomb icon
        pulse = int(5 * abs(self.animation_frame % 1.0 - 0.5) * 2)
        bomb_radius = 8 + pulse
        
        pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), bomb_radius)
        pygame.draw.circle(screen, (255, 100, 0), (center_x, center_y), bomb_radius - 2)
        
        # Draw fuse
        fuse_end_x = center_x - bomb_radius // 2
        fuse_end_y = center_y - bomb_radius
        pygame.draw.line(screen, (100, 50, 0), (center_x, center_y - bomb_radius), 
                        (fuse_end_x, fuse_end_y), 2)
        
        # Draw spark at fuse end (animated)
        if int(self.animation_frame * 4) % 2 == 0:
            pygame.draw.circle(screen, (255, 255, 0), (fuse_end_x, fuse_end_y), 3)
            
        # Draw timer text
        time_until_drop = self.interval - self.timer
        font = pygame.font.Font(None, 16)
        timer_text = font.render(f"{time_until_drop:.1f}s", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(center_x, y + tile_size + 10))
        
        # Draw background for text
        bg_rect = timer_rect.inflate(4, 2)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)
        screen.blit(timer_text, timer_rect)
        
        # Draw warning zone during warning
        if self.is_warning:
            # Draw danger zone indicator
            danger_radius = (self.bomb_range + 1) * tile_size
            danger_surface = pygame.Surface((danger_radius * 2, danger_radius * 2), pygame.SRCALPHA)
            
            alpha = int(50 * abs(pygame.time.get_ticks() % 500 - 250) / 250)
            pygame.draw.circle(danger_surface, (255, 0, 0, alpha), 
                             (danger_radius, danger_radius), danger_radius)
            
            screen.blit(danger_surface, 
                       (center_x - danger_radius, center_y - danger_radius))
