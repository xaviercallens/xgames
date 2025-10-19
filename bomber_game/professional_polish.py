"""
Professional Polish System for PROUTMAN.
Elevates game to AAA-quality standards with polished UI, animations, and effects.
"""

import pygame
import math
import time
from typing import Tuple, Optional, List


class ParticleSystem:
    """Advanced particle effects system."""
    
    def __init__(self):
        """Initialize particle system."""
        self.particles = []
        self.max_particles = 500
    
    def emit(self, x: float, y: float, particle_type: str, count: int = 10):
        """
        Emit particles.
        
        Args:
            x: X position
            y: Y position
            particle_type: 'explosion', 'dust', 'spark', 'heal', 'collect'
            count: Number of particles
        """
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            
            angle = (360 / count) * _ if count > 1 else 0
            speed = 5.0 + (hash(_) % 30) / 10.0
            
            particle = {
                'x': x,
                'y': y,
                'vx': math.cos(math.radians(angle)) * speed,
                'vy': math.sin(math.radians(angle)) * speed,
                'type': particle_type,
                'lifetime': 1.0,
                'max_lifetime': 1.0,
                'size': 3,
                'color': self._get_particle_color(particle_type),
            }
            self.particles.append(particle)
    
    def _get_particle_color(self, particle_type: str) -> Tuple[int, int, int]:
        """Get color for particle type."""
        colors = {
            'explosion': (255, 150, 0),
            'dust': (150, 150, 150),
            'spark': (255, 255, 0),
            'heal': (0, 255, 100),
            'collect': (100, 200, 255),
        }
        return colors.get(particle_type, (255, 255, 255))
    
    def update(self, dt: float):
        """Update particles."""
        for particle in self.particles[:]:
            particle['lifetime'] -= dt
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 5.0 * dt  # Gravity
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def render(self, screen, tile_size: int):
        """Render particles."""
        for particle in self.particles:
            progress = 1.0 - (particle['lifetime'] / particle['max_lifetime'])
            alpha = int(255 * (1.0 - progress))
            
            pixel_x = int(particle['x'] * tile_size)
            pixel_y = int(particle['y'] * tile_size)
            size = max(1, int(particle['size'] * (1.0 - progress)))
            
            color = particle['color']
            pygame.draw.circle(screen, color, (pixel_x, pixel_y), size)


class ScreenShakeEffect:
    """Screen shake effect for explosions and impacts."""
    
    def __init__(self):
        """Initialize screen shake."""
        self.intensity = 0.0
        self.duration = 0.0
        self.max_duration = 0.0
    
    def trigger(self, intensity: float = 5.0, duration: float = 0.2):
        """
        Trigger screen shake.
        
        Args:
            intensity: Shake intensity in pixels
            duration: Duration in seconds
        """
        self.intensity = intensity
        self.duration = duration
        self.max_duration = duration
    
    def update(self, dt: float):
        """Update screen shake."""
        if self.duration > 0:
            self.duration -= dt
        else:
            self.intensity = 0.0
    
    def get_offset(self) -> Tuple[int, int]:
        """Get screen shake offset."""
        if self.intensity <= 0:
            return 0, 0
        
        progress = self.duration / self.max_duration
        offset_x = int((hash(time.time() * 1000) % 2 - 1) * self.intensity * progress)
        offset_y = int((hash(time.time() * 1000 + 1) % 2 - 1) * self.intensity * progress)
        
        return offset_x, offset_y


class TransitionEffect:
    """Smooth transition effects between screens."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize transition."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.progress = 0.0
        self.duration = 0.5
        self.transition_type = 'fade'  # 'fade', 'slide', 'wipe'
    
    def start(self, transition_type: str = 'fade', duration: float = 0.5):
        """Start transition."""
        self.active = True
        self.progress = 0.0
        self.duration = duration
        self.transition_type = transition_type
    
    def update(self, dt: float) -> bool:
        """
        Update transition.
        
        Returns:
            True if transition is complete
        """
        if not self.active:
            return False
        
        self.progress += dt / self.duration
        
        if self.progress >= 1.0:
            self.active = False
            self.progress = 1.0
            return True
        
        return False
    
    def render(self, screen):
        """Render transition effect."""
        if not self.active and self.progress < 1.0:
            return
        
        if self.transition_type == 'fade':
            self._render_fade(screen)
        elif self.transition_type == 'slide':
            self._render_slide(screen)
        elif self.transition_type == 'wipe':
            self._render_wipe(screen)
    
    def _render_fade(self, screen):
        """Render fade transition."""
        alpha = int(255 * self.progress)
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(alpha)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
    
    def _render_slide(self, screen):
        """Render slide transition."""
        offset = int(self.screen_width * self.progress)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, offset, self.screen_height))
    
    def _render_wipe(self, screen):
        """Render wipe transition."""
        wipe_y = int(self.screen_height * self.progress)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.screen_width, wipe_y))


class UIPolish:
    """Professional UI polish and styling."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize UI polish."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.Font(None, 48)
        self.font_large = pygame.font.Font(None, 32)
        self.font_normal = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # UI colors
        self.primary_color = (100, 200, 50)
        self.secondary_color = (255, 200, 0)
        self.accent_color = (255, 100, 100)
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
    
    def draw_button(self, screen, x: int, y: int, width: int, height: int,
                   text: str, hovered: bool = False):
        """
        Draw professional button.
        
        Args:
            screen: Pygame screen
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button text
            hovered: Whether button is hovered
        """
        # Button background
        color = self.secondary_color if hovered else self.primary_color
        pygame.draw.rect(screen, color, (x, y, width, height), border_radius=8)
        
        # Button border
        border_color = (255, 255, 255) if hovered else (150, 150, 150)
        pygame.draw.rect(screen, border_color, (x, y, width, height), 3, border_radius=8)
        
        # Shadow effect
        shadow_rect = pygame.Rect(x + 2, y + 2, width, height)
        pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=8)
        
        # Text
        text_surf = self.font_normal.render(text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surf, text_rect)
    
    def draw_panel(self, screen, x: int, y: int, width: int, height: int,
                  title: str = "", alpha: int = 200):
        """
        Draw professional panel.
        
        Args:
            screen: Pygame screen
            x: X position
            y: Y position
            width: Panel width
            height: Panel height
            title: Panel title
            alpha: Transparency (0-255)
        """
        # Panel background with alpha
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        panel_surface.fill((20, 20, 30, alpha))
        screen.blit(panel_surface, (x, y))
        
        # Panel border
        pygame.draw.rect(screen, self.primary_color, (x, y, width, height), 3)
        
        # Title bar
        if title:
            title_height = 40
            pygame.draw.rect(screen, self.primary_color, (x, y, width, title_height))
            
            title_surf = self.font_large.render(title, True, self.text_color)
            title_rect = title_surf.get_rect(center=(x + width // 2, y + title_height // 2))
            screen.blit(title_surf, title_rect)
    
    def draw_stat_bar(self, screen, x: int, y: int, width: int, height: int,
                     value: float, max_value: float, label: str = "", color=None):
        """
        Draw professional stat bar.
        
        Args:
            screen: Pygame screen
            x: X position
            y: Y position
            width: Bar width
            height: Bar height
            value: Current value
            max_value: Maximum value
            label: Bar label
            color: Bar color
        """
        if color is None:
            color = self.primary_color
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2)
        
        # Fill
        fill_width = int(width * (value / max_value))
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
        
        # Text
        if label:
            text_surf = self.font_small.render(label, True, self.text_color)
            text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
            screen.blit(text_surf, text_rect)
    
    def draw_shadow_text(self, screen, text: str, x: int, y: int,
                        font=None, color=None):
        """
        Draw text with shadow effect.
        
        Args:
            screen: Pygame screen
            text: Text to draw
            x: X position
            y: Y position
            font: Font to use
            color: Text color
        """
        if font is None:
            font = self.font_normal
        if color is None:
            color = self.text_color
        
        # Shadow
        shadow_surf = font.render(text, True, self.shadow_color)
        screen.blit(shadow_surf, (x + 2, y + 2))
        
        # Text
        text_surf = font.render(text, True, color)
        screen.blit(text_surf, (x, y))


class AnimationController:
    """Advanced animation controller for smooth transitions."""
    
    def __init__(self):
        """Initialize animation controller."""
        self.animations = {}
        self.active_animations = []
    
    def create_animation(self, name: str, duration: float, easing: str = 'linear'):
        """
        Create animation.
        
        Args:
            name: Animation name
            duration: Duration in seconds
            easing: 'linear', 'ease_in', 'ease_out', 'ease_in_out'
        """
        self.animations[name] = {
            'duration': duration,
            'easing': easing,
            'elapsed': 0.0,
            'active': False,
        }
    
    def start_animation(self, name: str):
        """Start animation."""
        if name in self.animations:
            self.animations[name]['active'] = True
            self.animations[name]['elapsed'] = 0.0
            self.active_animations.append(name)
    
    def update(self, dt: float):
        """Update animations."""
        for anim_name in self.active_animations[:]:
            anim = self.animations[anim_name]
            anim['elapsed'] += dt
            
            if anim['elapsed'] >= anim['duration']:
                anim['active'] = False
                self.active_animations.remove(anim_name)
    
    def get_progress(self, name: str) -> float:
        """
        Get animation progress (0.0 to 1.0).
        
        Args:
            name: Animation name
            
        Returns:
            Progress value
        """
        if name not in self.animations:
            return 0.0
        
        anim = self.animations[name]
        progress = min(1.0, anim['elapsed'] / anim['duration'])
        
        # Apply easing
        if anim['easing'] == 'ease_in':
            progress = progress ** 2
        elif anim['easing'] == 'ease_out':
            progress = 1.0 - (1.0 - progress) ** 2
        elif anim['easing'] == 'ease_in_out':
            if progress < 0.5:
                progress = 2 * progress ** 2
            else:
                progress = 1.0 - 2 * (1.0 - progress) ** 2
        
        return progress


class CameraSystem:
    """Professional camera system with smooth following."""
    
    def __init__(self, screen_width: int, screen_height: int, world_width: int, world_height: int):
        """
        Initialize camera.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            world_width: World width
            world_height: World height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.smoothing = 0.1  # Camera smoothing factor
    
    def follow(self, target_x: float, target_y: float):
        """
        Set camera target.
        
        Args:
            target_x: Target X position
            target_y: Target Y position
        """
        self.target_x = target_x
        self.target_y = target_y
    
    def update(self, dt: float):
        """Update camera."""
        # Smooth follow
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing
        
        # Clamp to world bounds
        self.x = max(0, min(self.x, self.world_width - self.screen_width))
        self.y = max(0, min(self.y, self.world_height - self.screen_height))
    
    def get_offset(self) -> Tuple[int, int]:
        """Get camera offset for rendering."""
        return int(-self.x), int(-self.y)


class LightingSystem:
    """Dynamic lighting effects."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize lighting."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lights = []
    
    def add_light(self, x: float, y: float, radius: float, color: Tuple[int, int, int],
                 intensity: float = 1.0, duration: float = 0.0):
        """
        Add light source.
        
        Args:
            x: X position
            y: Y position
            radius: Light radius
            color: Light color
            intensity: Light intensity (0.0-1.0)
            duration: Duration (0 = permanent)
        """
        light = {
            'x': x,
            'y': y,
            'radius': radius,
            'color': color,
            'intensity': intensity,
            'duration': duration,
            'elapsed': 0.0,
        }
        self.lights.append(light)
    
    def update(self, dt: float):
        """Update lights."""
        for light in self.lights[:]:
            if light['duration'] > 0:
                light['elapsed'] += dt
                if light['elapsed'] >= light['duration']:
                    self.lights.remove(light)
    
    def render(self, screen):
        """Render lighting effects."""
        for light in self.lights:
            # Create light surface
            light_surface = pygame.Surface((int(light['radius'] * 2), int(light['radius'] * 2)), pygame.SRCALPHA)
            
            # Draw radial gradient
            for i in range(int(light['radius']), 0, -1):
                alpha = int(255 * light['intensity'] * (1.0 - i / light['radius']))
                color = (*light['color'], alpha)
                pygame.draw.circle(light_surface, color, (int(light['radius']), int(light['radius'])), i)
            
            # Blit to screen
            screen.blit(light_surface, (int(light['x'] - light['radius']), int(light['y'] - light['radius'])))


class ProfessionalPolishManager:
    """Main professional polish manager."""
    
    def __init__(self, screen_width: int, screen_height: int, grid_size: int, tile_size: int):
        """Initialize polish manager."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.tile_size = tile_size
        
        # Initialize all systems
        self.particles = ParticleSystem()
        self.screen_shake = ScreenShakeEffect()
        self.transition = TransitionEffect(screen_width, screen_height)
        self.ui = UIPolish(screen_width, screen_height)
        self.animation = AnimationController()
        self.camera = CameraSystem(screen_width, screen_height, grid_size * tile_size, grid_size * tile_size)
        self.lighting = LightingSystem(screen_width, screen_height)
    
    def update(self, dt: float):
        """Update all polish systems."""
        self.particles.update(dt)
        self.screen_shake.update(dt)
        self.transition.update(dt)
        self.animation.update(dt)
        self.camera.update(dt)
        self.lighting.update(dt)
    
    def render(self, screen):
        """Render all polish effects."""
        # Screen shake offset
        shake_x, shake_y = self.screen_shake.get_offset()
        
        # Render particles
        self.particles.render(screen, self.tile_size)
        
        # Render lighting
        self.lighting.render(screen)
        
        # Render transition
        self.transition.render(screen)
    
    def trigger_explosion(self, x: float, y: float):
        """Trigger explosion effects."""
        self.particles.emit(x, y, 'explosion', 20)
        self.screen_shake.trigger(intensity=8.0, duration=0.3)
    
    def trigger_collect(self, x: float, y: float):
        """Trigger collect effects."""
        self.particles.emit(x, y, 'collect', 10)
        self.lighting.add_light(x, y, 2.0, (100, 200, 255), intensity=0.8, duration=0.5)
    
    def trigger_damage(self, x: float, y: float):
        """Trigger damage effects."""
        self.particles.emit(x, y, 'spark', 15)
        self.screen_shake.trigger(intensity=5.0, duration=0.2)
