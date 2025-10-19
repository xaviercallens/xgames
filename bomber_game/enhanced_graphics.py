"""
Enhanced graphics module for PROUTMAN theme.
Provides improved visual rendering for all game entities.
"""

import pygame
import math
from typing import Tuple


class ProutManGraphics:
    """Enhanced graphics system for PROUTMAN theme."""
    
    # Color palette
    PROUT_GREEN = (100, 200, 50)      # Prout cloud green
    PROUT_YELLOW = (200, 200, 50)     # Prout yellow
    PROUT_BROWN = (139, 90, 43)       # Caca brown
    DARK_BROWN = (101, 67, 33)        # Dark caca
    STINK_GREEN = (150, 220, 100)     # Stink lines
    PLAYER_GREEN = (0, 255, 0)        # Player green
    PLAYER_RED = (255, 0, 0)          # AI player red
    
    @staticmethod
    def draw_enhanced_player(screen, pixel_x, pixel_y, color, direction='down', 
                            animation_frame=0, tile_size=56):
        """
        Draw enhanced player character with more details.
        
        Args:
            screen: Pygame surface
            pixel_x: Pixel X position (center)
            pixel_y: Pixel Y position (center)
            color: Player color (RGB tuple)
            direction: Direction player is facing
            animation_frame: Current animation frame
            tile_size: Size of tile
        """
        # Player body (rounded rectangle)
        body_width = int(tile_size * 0.6)
        body_height = int(tile_size * 0.7)
        
        body_rect = pygame.Rect(
            pixel_x - body_width // 2,
            pixel_y - body_height // 2,
            body_width,
            body_height
        )
        pygame.draw.rect(screen, color, body_rect, border_radius=8)
        
        # Add body outline
        pygame.draw.rect(screen, tuple(max(0, c - 50) for c in color), 
                        body_rect, 3, border_radius=8)
        
        # Head
        head_radius = int(tile_size * 0.25)
        head_y = pixel_y - body_height // 2 - head_radius // 2
        pygame.draw.circle(screen, color, (pixel_x, head_y), head_radius)
        pygame.draw.circle(screen, tuple(max(0, c - 50) for c in color),
                          (pixel_x, head_y), head_radius, 2)
        
        # Eyes based on direction
        eye_color = (255, 255, 255)
        eye_radius = 3
        
        if direction == 'down':
            eye_left = (pixel_x - 8, head_y + 4)
            eye_right = (pixel_x + 8, head_y + 4)
        elif direction == 'up':
            eye_left = (pixel_x - 8, head_y - 4)
            eye_right = (pixel_x + 8, head_y - 4)
        elif direction == 'left':
            eye_left = (pixel_x - 10, head_y - 2)
            eye_right = (pixel_x - 10, head_y + 2)
        else:  # right
            eye_left = (pixel_x + 10, head_y - 2)
            eye_right = (pixel_x + 10, head_y + 2)
        
        pygame.draw.circle(screen, eye_color, eye_left, eye_radius)
        pygame.draw.circle(screen, eye_color, eye_right, eye_radius)
        
        # Pupils (looking in direction)
        pupil_color = (0, 0, 0)
        pupil_radius = 1
        pygame.draw.circle(screen, pupil_color, eye_left, pupil_radius)
        pygame.draw.circle(screen, pupil_color, eye_right, pupil_radius)
        
        # Mouth
        mouth_color = (0, 0, 0)
        mouth_y = head_y + 8
        pygame.draw.line(screen, mouth_color, 
                        (pixel_x - 4, mouth_y), 
                        (pixel_x + 4, mouth_y), 2)
        
        # Animation: bobbing effect
        bob_offset = int(math.sin(animation_frame * math.pi) * 2)
        
        # Legs (simple rectangles)
        leg_width = int(tile_size * 0.15)
        leg_height = int(tile_size * 0.25)
        leg_y = pixel_y + body_height // 2 - 4 + bob_offset
        
        # Left leg
        pygame.draw.rect(screen, tuple(max(0, c - 100) for c in color),
                        (pixel_x - 10, leg_y, leg_width, leg_height))
        # Right leg
        pygame.draw.rect(screen, tuple(max(0, c - 100) for c in color),
                        (pixel_x + 5, leg_y, leg_width, leg_height))
        
        # Add shine/highlight
        shine_color = tuple(min(255, c + 80) for c in color)
        pygame.draw.circle(screen, shine_color, 
                          (pixel_x - body_width // 4, pixel_y - body_height // 4), 4)
    
    @staticmethod
    def draw_enhanced_prout(screen, pixel_x, pixel_y, timer, tile_size=56):
        """
        Draw enhanced prout (bomb) with smelly cloud effect.
        
        Args:
            screen: Pygame surface
            pixel_x: Pixel X position (center)
            pixel_y: Pixel Y position (center)
            timer: Remaining time before explosion
            tile_size: Size of tile
        """
        # Pulsing effect based on timer
        pulse = 1.0 + 0.3 * math.sin(timer * 8)
        
        # Main prout cloud (green)
        cloud_radius = int(tile_size * 0.3 * pulse)
        
        # Create surface with alpha for transparency
        surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        
        # Draw main cloud
        pygame.draw.circle(surf, (*ProutManGraphics.PROUT_GREEN, 200),
                          (tile_size // 2, tile_size // 2), cloud_radius)
        
        # Draw secondary clouds (for puffs)
        offset = int(math.sin(timer * 4) * 4)
        pygame.draw.circle(surf, (*ProutManGraphics.PROUT_YELLOW, 150),
                          (tile_size // 2 - 8 + offset, tile_size // 2 - 8), 
                          int(cloud_radius * 0.7))
        pygame.draw.circle(surf, (*ProutManGraphics.PROUT_YELLOW, 150),
                          (tile_size // 2 + 8 - offset, tile_size // 2 - 8),
                          int(cloud_radius * 0.7))
        
        screen.blit(surf, (pixel_x - tile_size // 2, pixel_y - tile_size // 2))
        
        # Draw stink lines (wavy)
        stink_color = ProutManGraphics.STINK_GREEN
        for i in range(4):
            angle = (timer * 3 + i) * math.pi / 2
            for j in range(3):
                x_offset = int(math.cos(angle + j * 0.5) * (5 + j * 3))
                y_offset = int(math.sin(angle + j * 0.5) * (5 + j * 3)) - 15
                pygame.draw.circle(screen, stink_color,
                                 (pixel_x + x_offset, pixel_y + y_offset - 15), 2)
        
        # Add brown spots (caca marks)
        if timer < 1.5:
            spot_color = ProutManGraphics.DARK_BROWN
            pygame.draw.circle(screen, spot_color, 
                             (pixel_x - 8, pixel_y + 8), 3)
            pygame.draw.circle(screen, spot_color,
                             (pixel_x + 6, pixel_y + 10), 2)
    
    @staticmethod
    def draw_enhanced_caca(screen, pixel_x, pixel_y, duration, tile_size=56):
        """
        Draw enhanced caca (poop) with more detail.
        
        Args:
            screen: Pygame surface
            pixel_x: Pixel X position (top-left)
            pixel_y: Pixel Y position (top-left)
            duration: Remaining duration
            tile_size: Size of tile
        """
        # Pulsing effect for visibility
        pulse = 1.0 + 0.1 * math.sin(duration * 3)
        
        # Create surface with alpha
        surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        
        # Draw poop piles (3 stacked)
        pile_colors = [
            (*ProutManGraphics.DARK_BROWN, 220),      # Bottom
            (*ProutManGraphics.PROUT_BROWN, 220),     # Middle
            (*ProutManGraphics.DARK_BROWN, 220),      # Top
        ]
        
        for i, color in enumerate(pile_colors):
            pile_y = tile_size - 24 - i * 12
            pile_width = int((tile_size - 16) * (1 - i * 0.15) * pulse)
            pile_height = int(14 * pulse)
            
            pile_rect = pygame.Rect(
                tile_size // 2 - pile_width // 2,
                pile_y,
                pile_width,
                pile_height
            )
            pygame.draw.ellipse(surf, color, pile_rect)
        
        screen.blit(surf, (pixel_x, pixel_y))
        
        # Draw stink lines (animated)
        stink_color = ProutManGraphics.STINK_GREEN
        offset = int(duration * 2) % 4
        
        for i in range(3):
            x_pos = pixel_x + 12 + i * 14
            y_start = pixel_y + tile_size - 48
            
            # Wavy stink line
            for j in range(3):
                y_pos = y_start - j * 6
                x_offset = int(math.sin((duration * 3 + i + j) * 0.5) * 4)
                pygame.draw.circle(screen, stink_color,
                                 (x_pos + x_offset, y_pos), 2)
        
        # Add shine
        shine_color = (160, 110, 60)
        pygame.draw.circle(screen, shine_color,
                          (pixel_x + tile_size // 2 - 8, pixel_y + tile_size - 32), 5)
    
    @staticmethod
    def draw_enhanced_explosion(screen, pixel_x, pixel_y, timer, max_timer, tile_size=56):
        """
        Draw enhanced explosion with dramatic smelly cloud effect.
        
        Args:
            screen: Pygame surface
            pixel_x: Pixel X position (top-left)
            pixel_y: Pixel Y position (top-left)
            timer: Remaining time
            max_timer: Maximum timer
            tile_size: Size of tile
        """
        # Fade out effect
        alpha = int(255 * (timer / max_timer))
        
        # Create surface with alpha
        surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        
        # Expansion effect
        expansion = 1.0 - (timer / max_timer)
        
        # Draw explosion clouds (concentric circles)
        colors = [
            (*ProutManGraphics.PROUT_GREEN, alpha),      # Outer (green)
            (*ProutManGraphics.PROUT_YELLOW, alpha),     # Middle (yellow)
            (*ProutManGraphics.PROUT_BROWN, alpha),      # Inner (brown)
        ]
        
        for i, color in enumerate(colors):
            radius = int((tile_size // 2) * (1.2 - i * 0.25 + expansion * 0.3))
            pygame.draw.circle(surf, color, (tile_size // 2, tile_size // 2), radius)
        
        screen.blit(surf, (pixel_x, pixel_y))
        
        # Draw stink particles
        stink_color = (*ProutManGraphics.STINK_GREEN, alpha)
        num_particles = 6
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * math.pi
            distance = (tile_size // 2) * (1.0 + expansion * 0.5)
            
            x = pixel_x + tile_size // 2 + int(math.cos(angle) * distance)
            y = pixel_y + tile_size // 2 + int(math.sin(angle) * distance)
            
            particle_radius = int(3 * (1 - expansion))
            if particle_radius > 0:
                pygame.draw.circle(screen, stink_color, (x, y), particle_radius)
    
    @staticmethod
    def draw_enhanced_wall(screen, pixel_x, pixel_y, tile_size=56, wall_type=1):
        """
        Draw enhanced walls with better visuals.
        
        Args:
            screen: Pygame surface
            pixel_x: Pixel X position (top-left)
            pixel_y: Pixel Y position (top-left)
            tile_size: Size of tile
            wall_type: 1 for hard wall, 2 for soft wall
        """
        if wall_type == 1:  # Hard wall
            # Dark gray with stone texture
            color = (50, 50, 50)
            pygame.draw.rect(screen, color, (pixel_x, pixel_y, tile_size, tile_size))
            
            # Add stone pattern
            pygame.draw.rect(screen, (70, 70, 70), 
                           (pixel_x, pixel_y, tile_size, tile_size), 2)
            
            # Add cracks
            pygame.draw.line(screen, (40, 40, 40),
                           (pixel_x + 10, pixel_y), 
                           (pixel_x + 10, pixel_y + tile_size), 1)
            pygame.draw.line(screen, (40, 40, 40),
                           (pixel_x, pixel_y + 10),
                           (pixel_x + tile_size, pixel_y + 10), 1)
        else:  # Soft wall (destructible)
            # Brown with wood texture
            color = (139, 90, 43)
            pygame.draw.rect(screen, color, (pixel_x, pixel_y, tile_size, tile_size))
            
            # Add wood grain
            pygame.draw.rect(screen, (101, 67, 33),
                           (pixel_x, pixel_y, tile_size, tile_size), 2)
            
            # Add shine
            pygame.draw.line(screen, (180, 120, 60),
                           (pixel_x + 5, pixel_y + 5),
                           (pixel_x + tile_size - 5, pixel_y + 5), 1)
    
    @staticmethod
    def draw_enhanced_powerup(screen, pixel_x, pixel_y, powerup_type, tile_size=56):
        """
        Draw enhanced power-up with visual distinction.
        
        Args:
            screen: Pygame surface
            pixel_x: Pixel X position (center)
            pixel_y: Pixel Y position (center)
            powerup_type: Type of power-up (0-5)
            tile_size: Size of tile
        """
        # Power-up colors and symbols
        powerup_info = {
            0: ((255, 200, 0), "💣"),      # Bomb up (yellow)
            1: ((255, 100, 0), "🔥"),      # Fire up (orange)
            2: ((100, 200, 255), "⚡"),    # Speed up (blue)
            3: ((200, 100, 255), "🛡️"),    # Shield (purple)
            4: ((255, 100, 200), "📡"),    # Remote (pink)
            5: ((100, 255, 100), "⚔️"),    # Pierce (green)
        }
        
        color, symbol = powerup_info.get(powerup_type, ((200, 200, 200), "?"))
        
        # Draw rotating square
        size = int(tile_size * 0.4)
        angle = (pygame.time.get_ticks() / 10) % 360
        
        # Create rotated square
        corners = [
            (-size // 2, -size // 2),
            (size // 2, -size // 2),
            (size // 2, size // 2),
            (-size // 2, size // 2),
        ]
        
        # Rotate corners
        import math as m
        rad = m.radians(angle)
        rotated = []
        for x, y in corners:
            rx = x * m.cos(rad) - y * m.sin(rad)
            ry = x * m.sin(rad) + y * m.cos(rad)
            rotated.append((pixel_x + rx, pixel_y + ry))
        
        pygame.draw.polygon(screen, color, rotated)
        pygame.draw.polygon(screen, tuple(max(0, c - 100) for c in color), rotated, 2)
        
        # Add pulsing glow
        glow_radius = int(size * 0.6 * (1 + 0.3 * math.sin(pygame.time.get_ticks() / 200)))
        pygame.draw.circle(screen, color, (pixel_x, pixel_y), glow_radius, 1)
