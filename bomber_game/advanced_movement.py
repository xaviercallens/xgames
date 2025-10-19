"""
Advanced Movement System for PROUTMAN.
Provides fluid, responsive movement with improved collision detection.
Inspired by classic Bomberman movement mechanics.
"""

import pygame
import math
from typing import Tuple, Optional, List


class MovementState:
    """Tracks player movement state."""
    
    def __init__(self):
        """Initialize movement state."""
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.desired_direction = None
        self.current_direction = None
        self.is_moving = False
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.speed = 7.0  # tiles per second
        self.acceleration = 20.0
        self.deceleration = 15.0
        self.max_velocity = 7.0


class CollisionBox:
    """Represents a collision box for an entity."""
    
    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialize collision box.
        
        Args:
            x: Center X position
            y: Center Y position
            width: Box width
            height: Box height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def get_rect(self) -> pygame.Rect:
        """Get pygame rect."""
        return pygame.Rect(
            self.x - self.width / 2,
            self.y - self.height / 2,
            self.width,
            self.height
        )
    
    def collides_with(self, other: 'CollisionBox') -> bool:
        """Check collision with another box."""
        return self.get_rect().colliderect(other.get_rect())
    
    def collides_with_point(self, px: float, py: float) -> bool:
        """Check if point is inside box."""
        rect = self.get_rect()
        return rect.collidepoint(px, py)


class AdvancedMovementSystem:
    """
    Advanced movement system with smooth acceleration/deceleration.
    Prevents player from getting stuck on bombs.
    """
    
    def __init__(self, grid_size: int, tile_size: int):
        """
        Initialize movement system.
        
        Args:
            grid_size: Size of game grid
            tile_size: Size of each tile
        """
        self.grid_size = grid_size
        self.tile_size = tile_size
        
        # Movement parameters
        self.acceleration = 25.0  # Faster acceleration
        self.deceleration = 20.0  # Smooth deceleration
        self.max_speed = 8.0  # Slightly faster
        self.friction = 0.85  # Smooth friction
        
        # Collision parameters
        self.collision_buffer = 0.15  # 15% buffer for smooth movement
        self.slide_factor = 0.3  # Allow sliding along walls
        
        # Grid snapping
        self.snap_distance = 0.1  # Snap to grid when close
        self.snap_threshold = 0.05  # Threshold for snapping
    
    def update_movement(self, player, dt: float, input_dx: int, input_dy: int,
                       game_state) -> Tuple[float, float]:
        """
        Update player movement with smooth acceleration.
        
        Args:
            player: Player entity
            dt: Delta time
            input_dx: Input direction X (-1, 0, 1)
            input_dy: Input direction Y (-1, 0, 1)
            game_state: Game state for collision checking
            
        Returns:
            (new_x, new_y) position
        """
        # Get current position
        current_x = player.x
        current_y = player.y
        
        # Update desired direction
        if input_dx != 0 or input_dy != 0:
            # Normalize diagonal input
            magnitude = math.sqrt(input_dx**2 + input_dy**2)
            desired_vx = (input_dx / magnitude) * self.max_speed
            desired_vy = (input_dy / magnitude) * self.max_speed
        else:
            desired_vx = 0.0
            desired_vy = 0.0
        
        # Smooth acceleration/deceleration
        player.velocity_x = self._smooth_velocity(
            player.velocity_x, desired_vx, dt, self.acceleration, self.deceleration
        )
        player.velocity_y = self._smooth_velocity(
            player.velocity_y, desired_vy, dt, self.acceleration, self.deceleration
        )
        
        # Calculate new position
        new_x = current_x + player.velocity_x * dt
        new_y = current_y + player.velocity_y * dt
        
        # Check collisions and adjust position
        new_x, new_y = self._resolve_collisions(
            player, current_x, current_y, new_x, new_y, game_state
        )
        
        # Snap to grid when close
        new_x, new_y = self._snap_to_grid(new_x, new_y)
        
        # Update animation
        self._update_animation(player, dt, input_dx, input_dy)
        
        return new_x, new_y
    
    def _smooth_velocity(self, current: float, desired: float, dt: float,
                        accel: float, decel: float) -> float:
        """
        Smoothly transition velocity to desired value.
        
        Args:
            current: Current velocity
            desired: Desired velocity
            dt: Delta time
            accel: Acceleration rate
            decel: Deceleration rate
            
        Returns:
            New velocity
        """
        if abs(desired) > abs(current):
            # Accelerate
            current += accel * dt * (1 if desired > 0 else -1)
            current = min(abs(current), abs(desired)) * (1 if current > 0 else -1)
        else:
            # Decelerate
            if abs(current) > 0.1:
                current *= (1 - decel * dt)
            else:
                current = 0.0
        
        return current
    
    def _resolve_collisions(self, player, current_x: float, current_y: float,
                           new_x: float, new_y: float,
                           game_state) -> Tuple[float, float]:
        """
        Resolve collisions and adjust position.
        Prevents getting stuck on bombs and walls.
        
        Args:
            player: Player entity
            current_x: Current X position
            current_y: Current Y position
            new_x: Desired new X position
            new_y: Desired new Y position
            game_state: Game state for collision checking
            
        Returns:
            (adjusted_x, adjusted_y)
        """
        # Create collision box for player
        player_box = CollisionBox(new_x, new_y, 0.4, 0.4)
        
        # Check wall collisions
        if self._check_wall_collision(new_x, new_y, game_state.grid):
            # Try sliding along walls
            # Try X-only movement
            if not self._check_wall_collision(new_x, current_y, game_state.grid):
                new_y = current_y
            # Try Y-only movement
            elif not self._check_wall_collision(current_x, new_y, game_state.grid):
                new_x = current_x
            else:
                # Can't move, stay in place
                new_x = current_x
                new_y = current_y
        
        # Check bomb collisions (allow passing through with slight push)
        new_x, new_y = self._resolve_bomb_collision(
            player, new_x, new_y, game_state
        )
        
        # Check caca collisions
        if self._check_caca_collision(new_x, new_y, game_state.cacas):
            # Try sliding
            if not self._check_caca_collision(new_x, current_y, game_state.cacas):
                new_y = current_y
            elif not self._check_caca_collision(current_x, new_y, game_state.cacas):
                new_x = current_x
            else:
                new_x = current_x
                new_y = current_y
        
        return new_x, new_y
    
    def _check_wall_collision(self, x: float, y: float, grid: List[List[int]]) -> bool:
        """Check if position collides with walls."""
        # Use smaller hitbox for better movement
        hitbox_size = 0.2
        
        corners = [
            (x - hitbox_size, y - hitbox_size),
            (x + hitbox_size, y - hitbox_size),
            (x - hitbox_size, y + hitbox_size),
            (x + hitbox_size, y + hitbox_size),
        ]
        
        for cx, cy in corners:
            gx = int(math.floor(cx))
            gy = int(math.floor(cy))
            
            if gx < 0 or gx >= len(grid[0]) or gy < 0 or gy >= len(grid):
                continue
            
            if grid[gy][gx] in [1, 2]:  # Wall or soft wall
                return True
        
        return False
    
    def _resolve_bomb_collision(self, player, x: float, y: float,
                               game_state) -> Tuple[float, float]:
        """
        Resolve bomb collisions with smooth pushing.
        Prevents player from getting stuck on bombs.
        
        Args:
            player: Player entity
            x: X position
            y: Y position
            game_state: Game state
            
        Returns:
            (adjusted_x, adjusted_y)
        """
        player_box = CollisionBox(x, y, 0.4, 0.4)
        
        for bomb in game_state.bombs:
            bomb_box = CollisionBox(bomb.grid_x + 0.5, bomb.grid_y + 0.5, 0.5, 0.5)
            
            if player_box.collides_with(bomb_box):
                # Calculate push direction
                dx = x - bomb_box.x
                dy = y - bomb_box.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < 0.01:
                    distance = 0.01
                
                # Push player away from bomb
                push_distance = 0.35  # Minimum separation
                push_x = (dx / distance) * push_distance
                push_y = (dy / distance) * push_distance
                
                new_x = bomb_box.x + push_x
                new_y = bomb_box.y + push_y
                
                # Verify new position is valid
                if not self._check_wall_collision(new_x, new_y, game_state.grid):
                    return new_x, new_y
        
        return x, y
    
    def _check_caca_collision(self, x: float, y: float, cacas: List) -> bool:
        """Check collision with caca obstacles."""
        player_box = CollisionBox(x, y, 0.4, 0.4)
        
        for caca in cacas:
            caca_box = CollisionBox(caca.grid_x + 0.5, caca.grid_y + 0.5, 0.8, 0.8)
            if player_box.collides_with(caca_box):
                return True
        
        return False
    
    def _snap_to_grid(self, x: float, y: float) -> Tuple[float, float]:
        """
        Snap to grid when close for cleaner movement.
        
        Args:
            x: X position
            y: Y position
            
        Returns:
            (snapped_x, snapped_y)
        """
        # Snap X
        grid_x = round(x)
        if abs(x - grid_x) < self.snap_threshold:
            x = grid_x
        
        # Snap Y
        grid_y = round(y)
        if abs(y - grid_y) < self.snap_threshold:
            y = grid_y
        
        return x, y
    
    def _update_animation(self, player, dt: float, input_dx: int, input_dy: int):
        """Update player animation."""
        # Update direction
        if input_dx != 0:
            player.direction = 'right' if input_dx > 0 else 'left'
        elif input_dy != 0:
            player.direction = 'down' if input_dy > 0 else 'up'
        
        # Update animation frame
        player.animation_timer += dt
        if player.animation_timer >= player.animation_speed:
            player.animation_timer = 0
            player.animation_frame = (player.animation_frame + 1) % 2
    
    def get_grid_position(self, x: float, y: float) -> Tuple[int, int]:
        """Get grid position from world position."""
        return int(math.floor(x)), int(math.floor(y))
    
    def get_world_position(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        """Get world position from grid position."""
        return float(grid_x) + 0.5, float(grid_y) + 0.5


class SprintSystem:
    """
    Sprint/dash system for faster movement.
    Allows brief bursts of speed.
    """
    
    def __init__(self):
        """Initialize sprint system."""
        self.is_sprinting = False
        self.sprint_duration = 0.5  # 0.5 seconds
        self.sprint_cooldown = 1.0  # 1 second cooldown
        self.sprint_multiplier = 1.5  # 50% speed boost
        
        self.sprint_time = 0.0
        self.cooldown_time = 0.0
    
    def start_sprint(self):
        """Start sprinting if cooldown is ready."""
        if self.cooldown_time <= 0 and not self.is_sprinting:
            self.is_sprinting = True
            self.sprint_time = self.sprint_duration
    
    def update(self, dt: float) -> float:
        """
        Update sprint state.
        
        Args:
            dt: Delta time
            
        Returns:
            Speed multiplier (1.0 or sprint_multiplier)
        """
        multiplier = 1.0
        
        if self.is_sprinting:
            self.sprint_time -= dt
            multiplier = self.sprint_multiplier
            
            if self.sprint_time <= 0:
                self.is_sprinting = False
                self.cooldown_time = self.sprint_cooldown
        
        if self.cooldown_time > 0:
            self.cooldown_time -= dt
        
        return multiplier
    
    def get_sprint_progress(self) -> float:
        """Get sprint progress (0.0 to 1.0)."""
        if self.is_sprinting:
            return 1.0 - (self.sprint_time / self.sprint_duration)
        return 0.0
    
    def get_cooldown_progress(self) -> float:
        """Get cooldown progress (0.0 to 1.0)."""
        if self.cooldown_time > 0:
            return 1.0 - (self.cooldown_time / self.sprint_cooldown)
        return 0.0


class AnimationSystem:
    """
    Enhanced animation system with multiple animation states.
    Inspired by classic Bomberman sprites.
    """
    
    def __init__(self):
        """Initialize animation system."""
        self.current_animation = 'idle'
        self.frame = 0
        self.timer = 0.0
        
        # Animation definitions
        self.animations = {
            'idle': {
                'frames': 2,
                'speed': 0.15,
                'loop': True,
            },
            'walk': {
                'frames': 4,
                'speed': 0.1,
                'loop': True,
            },
            'sprint': {
                'frames': 4,
                'speed': 0.08,
                'loop': True,
            },
            'place_bomb': {
                'frames': 2,
                'speed': 0.1,
                'loop': False,
            },
            'hit': {
                'frames': 2,
                'speed': 0.1,
                'loop': False,
            },
        }
    
    def set_animation(self, animation_name: str):
        """Set current animation."""
        if animation_name in self.animations and animation_name != self.current_animation:
            self.current_animation = animation_name
            self.frame = 0
            self.timer = 0.0
    
    def update(self, dt: float) -> int:
        """
        Update animation.
        
        Args:
            dt: Delta time
            
        Returns:
            Current frame number
        """
        anim = self.animations[self.current_animation]
        self.timer += dt
        
        if self.timer >= anim['speed']:
            self.timer = 0.0
            self.frame += 1
            
            if self.frame >= anim['frames']:
                if anim['loop']:
                    self.frame = 0
                else:
                    self.frame = anim['frames'] - 1
        
        return self.frame
    
    def get_animation_progress(self) -> float:
        """Get animation progress (0.0 to 1.0)."""
        anim = self.animations[self.current_animation]
        total_time = anim['frames'] * anim['speed']
        current_time = self.frame * anim['speed'] + self.timer
        return current_time / total_time


class MovementVisualizer:
    """
    Visualizes movement state for debugging.
    Shows velocity, direction, and collision boxes.
    """
    
    def __init__(self):
        """Initialize visualizer."""
        self.show_debug = False
    
    def render_debug(self, screen, player, tile_size: int):
        """Render debug information."""
        if not self.show_debug:
            return
        
        # Convert to pixel coordinates
        pixel_x = player.x * tile_size
        pixel_y = player.y * tile_size
        
        # Draw velocity vector
        if hasattr(player, 'velocity_x') and hasattr(player, 'velocity_y'):
            vx = player.velocity_x * tile_size * 0.5
            vy = player.velocity_y * tile_size * 0.5
            
            pygame.draw.line(
                screen, (255, 0, 0),
                (pixel_x, pixel_y),
                (pixel_x + vx, pixel_y + vy),
                2
            )
        
        # Draw collision box
        box_size = int(0.4 * tile_size)
        pygame.draw.rect(
            screen, (0, 255, 0),
            (pixel_x - box_size // 2, pixel_y - box_size // 2, box_size, box_size),
            1
        )
        
        # Draw direction indicator
        direction_offset = int(0.3 * tile_size)
        if player.direction == 'up':
            pygame.draw.line(screen, (0, 0, 255), (pixel_x, pixel_y),
                           (pixel_x, pixel_y - direction_offset), 2)
        elif player.direction == 'down':
            pygame.draw.line(screen, (0, 0, 255), (pixel_x, pixel_y),
                           (pixel_x, pixel_y + direction_offset), 2)
        elif player.direction == 'left':
            pygame.draw.line(screen, (0, 0, 255), (pixel_x, pixel_y),
                           (pixel_x - direction_offset, pixel_y), 2)
        elif player.direction == 'right':
            pygame.draw.line(screen, (0, 0, 255), (pixel_x, pixel_y),
                           (pixel_x + direction_offset, pixel_y), 2)
    
    def toggle_debug(self):
        """Toggle debug visualization."""
        self.show_debug = not self.show_debug
