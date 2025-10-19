"""
Enhanced User Experience module for PROUTMAN.
Provides fluid controls, responsive feedback, and intuitive interactions.
"""

import pygame
import time
from typing import Tuple, Optional, Callable


class FluidControlSystem:
    """Manages fluid, responsive player controls."""
    
    def __init__(self):
        """Initialize control system."""
        self.key_states = {}  # Track which keys are pressed
        self.last_action_time = 0
        self.action_cooldown = 0.05  # 50ms between actions
        self.input_buffer = []  # Buffer for rapid inputs
        self.max_buffer_size = 3
        
        # Movement state
        self.current_direction = None
        self.next_direction = None
        self.is_moving = False
        
        # Action state
        self.last_bomb_time = 0
        self.last_caca_time = 0
        self.bomb_cooldown = 0.1  # 100ms cooldown
        self.caca_cooldown = 0.1
    
    def update_key_state(self, key: int, pressed: bool):
        """Update key press state."""
        self.key_states[key] = pressed
    
    def get_movement_input(self) -> Tuple[int, int]:
        """
        Get smooth movement input from key states.
        Returns (dx, dy) for movement direction.
        """
        dx, dy = 0, 0
        
        # Check for movement keys (prioritize last pressed)
        keys_pressed = [k for k, v in self.key_states.items() if v]
        
        if not keys_pressed:
            self.current_direction = None
            return 0, 0
        
        # Get the most recently pressed key
        last_key = keys_pressed[-1]
        
        # Map keys to directions
        key_map = {
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
        }
        
        if last_key in key_map:
            dx, dy = key_map[last_key]
            self.current_direction = (dx, dy)
        
        return dx, dy
    
    def should_place_bomb(self) -> bool:
        """Check if bomb should be placed (with cooldown)."""
        current_time = time.time()
        if current_time - self.last_bomb_time >= self.bomb_cooldown:
            self.last_bomb_time = current_time
            return True
        return False
    
    def should_place_caca(self) -> bool:
        """Check if caca should be placed (with cooldown)."""
        current_time = time.time()
        if current_time - self.last_caca_time >= self.caca_cooldown:
            self.last_caca_time = current_time
            return True
        return False
    
    def reset(self):
        """Reset control state."""
        self.key_states.clear()
        self.current_direction = None
        self.next_direction = None
        self.input_buffer.clear()


class ResponsiveFeedbackSystem:
    """Provides visual and audio feedback for player actions."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize feedback system."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.feedback_events = []  # List of active feedback events
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 32)
    
    def add_feedback(self, feedback_type: str, position: Tuple[int, int], 
                     message: str = "", duration: float = 1.0):
        """
        Add visual feedback event.
        
        Args:
            feedback_type: 'damage', 'collect', 'bomb', 'caca', 'heal'
            position: (x, y) screen position
            message: Optional text to display
            duration: How long to show feedback
        """
        event = {
            'type': feedback_type,
            'position': list(position),
            'message': message,
            'duration': duration,
            'elapsed': 0,
            'created_time': time.time()
        }
        self.feedback_events.append(event)
    
    def update(self, dt: float):
        """Update feedback events."""
        current_time = time.time()
        self.feedback_events = [
            e for e in self.feedback_events
            if current_time - e['created_time'] < e['duration']
        ]
    
    def render(self, screen):
        """Render all feedback events."""
        for event in self.feedback_events:
            self._render_feedback(screen, event)
    
    def _render_feedback(self, screen, event: dict):
        """Render individual feedback event."""
        feedback_type = event['type']
        x, y = event['position']
        message = event['message']
        
        # Calculate alpha based on remaining duration
        current_time = time.time()
        elapsed = current_time - event['created_time']
        progress = elapsed / event['duration']
        alpha = int(255 * (1 - progress))
        
        # Create surface with alpha
        feedback_surface = pygame.Surface((100, 40), pygame.SRCALPHA)
        
        # Color based on type
        colors = {
            'damage': (255, 0, 0),      # Red
            'collect': (0, 255, 0),     # Green
            'bomb': (255, 200, 0),      # Yellow
            'caca': (139, 90, 43),      # Brown
            'heal': (0, 255, 255),      # Cyan
        }
        
        color = colors.get(feedback_type, (255, 255, 255))
        color_with_alpha = (*color, alpha)
        
        # Draw background
        pygame.draw.rect(feedback_surface, color_with_alpha, 
                        (0, 0, 100, 40), border_radius=5)
        
        # Draw text if provided
        if message:
            text_surf = self.font.render(message, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(50, 20))
            feedback_surface.blit(text_surf, text_rect)
        
        # Draw to screen with floating effect
        float_offset = int(progress * 30)  # Float up as it fades
        screen.blit(feedback_surface, (x - 50, y - 20 - float_offset))


class TutorialOverlay:
    """Provides in-game tutorial and hints."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize tutorial system."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 28)
        
        self.tutorial_steps = [
            {
                'title': 'Welcome to PROUTMAN!',
                'text': 'Use WASD or Arrow Keys to move around the board',
                'duration': 5.0,
                'position': (screen_width // 2, screen_height // 4)
            },
            {
                'title': 'Place Prouts!',
                'text': 'Press SPACE to place smelly prout bombs (💨)',
                'duration': 5.0,
                'position': (screen_width // 2, screen_height // 4)
            },
            {
                'title': 'Place Cacas!',
                'text': 'Press C to place poop obstacles (💩)',
                'duration': 5.0,
                'position': (screen_width // 2, screen_height // 4)
            },
            {
                'title': 'Collect Power-ups!',
                'text': 'Walk over rotating squares to get power-ups ⭐',
                'duration': 5.0,
                'position': (screen_width // 2, screen_height // 4)
            },
            {
                'title': 'Defeat the AI!',
                'text': 'Use your prouts to destroy walls and defeat the AI opponent',
                'duration': 5.0,
                'position': (screen_width // 2, screen_height // 4)
            },
        ]
        
        self.current_step = 0
        self.step_start_time = 0
        self.show_tutorial = True
    
    def update(self, dt: float):
        """Update tutorial state."""
        if not self.show_tutorial or self.current_step >= len(self.tutorial_steps):
            return
        
        elapsed = time.time() - self.step_start_time
        if elapsed > self.tutorial_steps[self.current_step]['duration']:
            self.current_step += 1
            self.step_start_time = time.time()
    
    def render(self, screen):
        """Render tutorial overlay."""
        if not self.show_tutorial or self.current_step >= len(self.tutorial_steps):
            return
        
        step = self.tutorial_steps[self.current_step]
        
        # Semi-transparent background
        overlay = pygame.Surface((self.screen_width, 100), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Title
        title_surf = self.big_font.render(step['title'], True, (255, 200, 0))
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 25))
        screen.blit(title_surf, title_rect)
        
        # Text
        text_surf = self.font.render(step['text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.screen_width // 2, 55))
        screen.blit(text_surf, text_rect)
        
        # Progress indicator
        progress = (self.current_step + 1) / len(self.tutorial_steps)
        progress_width = int(self.screen_width * progress)
        pygame.draw.rect(screen, (0, 255, 0), (0, 95, progress_width, 5))
    
    def skip(self):
        """Skip tutorial."""
        self.show_tutorial = False
    
    def reset(self):
        """Reset tutorial."""
        self.current_step = 0
        self.step_start_time = time.time()
        self.show_tutorial = True


class HelpPanel:
    """Displays contextual help and controls."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize help panel."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 14)
        self.visible = True
        
        self.controls = [
            ('WASD / Arrows', 'Move'),
            ('SPACE', 'Place Prout (💨)'),
            ('C', 'Place Caca (💩)'),
            ('P', 'Pause'),
            ('R', 'Record'),
            ('S', 'Save Stats'),
            ('ESC', 'Stats Screen'),
            ('H', 'Toggle Help'),
        ]
    
    def render(self, screen):
        """Render help panel."""
        if not self.visible:
            return
        
        # Panel background
        panel_width = 200
        panel_height = len(self.controls) * 20 + 20
        panel_x = self.screen_width - panel_width - 10
        panel_y = 10
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (0, 0, 0), panel_rect)
        pygame.draw.rect(screen, (100, 200, 50), panel_rect, 2)
        
        # Title
        title = self.font.render('Controls', True, (100, 200, 50))
        screen.blit(title, (panel_x + 10, panel_y + 5))
        
        # Controls list
        for i, (key, action) in enumerate(self.controls):
            y = panel_y + 25 + i * 20
            
            # Key
            key_surf = self.small_font.render(key, True, (255, 200, 0))
            screen.blit(key_surf, (panel_x + 10, y))
            
            # Action
            action_surf = self.small_font.render(action, True, (200, 200, 200))
            screen.blit(action_surf, (panel_x + 80, y))
    
    def toggle(self):
        """Toggle visibility."""
        self.visible = not self.visible


class GameStateIndicator:
    """Shows current game state and player status."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize state indicator."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
    
    def render(self, screen, game_state, player, ai_player):
        """Render game state indicator."""
        # Background
        bg_height = 80
        bg_rect = pygame.Rect(0, self.screen_height - bg_height, 
                             self.screen_width, bg_height)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.line(screen, (100, 200, 50), (0, self.screen_height - bg_height),
                        (self.screen_width, self.screen_height - bg_height), 2)
        
        y = self.screen_height - 70
        
        # Player status
        if player.alive:
            player_text = f"🟢 Player: Prouts:{player.max_bombs} Cacas:{player.max_cacas} Range:{player.bomb_range}"
            color = (0, 255, 0)
        else:
            player_text = "🟢 Player: DEAD"
            color = (255, 0, 0)
        
        player_surf = self.font.render(player_text, True, color)
        screen.blit(player_surf, (10, y))
        
        # AI status
        y += 25
        if ai_player.alive:
            ai_text = f"🔴 AI: Prouts:{ai_player.max_bombs} Cacas:{ai_player.max_cacas} Range:{ai_player.bomb_range}"
            color = (255, 0, 0)
        else:
            ai_text = "🔴 AI: DEAD"
            color = (100, 100, 100)
        
        ai_surf = self.font.render(ai_text, True, color)
        screen.blit(ai_surf, (10, y))
        
        # Game time
        y += 25
        game_time = int(time.time() - game_state.start_time) if hasattr(game_state, 'start_time') else 0
        time_text = f"⏱️  Time: {game_time}s"
        time_surf = self.small_font.render(time_text, True, (200, 200, 200))
        screen.blit(time_surf, (self.screen_width - 150, y))


class InputHintSystem:
    """Provides context-sensitive input hints."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize hint system."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 18)
        self.hints = []
        self.hint_duration = 3.0
    
    def add_hint(self, text: str, hint_type: str = 'info'):
        """
        Add a hint message.
        
        Args:
            text: Hint text
            hint_type: 'info', 'warning', 'success', 'error'
        """
        hint = {
            'text': text,
            'type': hint_type,
            'created_time': time.time(),
            'duration': self.hint_duration
        }
        self.hints.append(hint)
    
    def update(self, dt: float):
        """Update hints."""
        current_time = time.time()
        self.hints = [
            h for h in self.hints
            if current_time - h['created_time'] < h['duration']
        ]
    
    def render(self, screen):
        """Render hints."""
        for i, hint in enumerate(self.hints):
            self._render_hint(screen, hint, i)
    
    def _render_hint(self, screen, hint: dict, index: int):
        """Render individual hint."""
        current_time = time.time()
        elapsed = current_time - hint['created_time']
        progress = elapsed / hint['duration']
        alpha = int(255 * (1 - progress))
        
        # Color based on type
        colors = {
            'info': (100, 200, 255),
            'warning': (255, 200, 0),
            'success': (0, 255, 100),
            'error': (255, 0, 100),
        }
        
        color = colors.get(hint['type'], (200, 200, 200))
        
        # Create surface with alpha
        text_surf = self.font.render(hint['text'], True, color)
        
        # Position (stack vertically)
        y = 20 + index * 30
        
        # Draw with fade effect
        text_surf.set_alpha(alpha)
        screen.blit(text_surf, (20, y))


class UserExperienceManager:
    """Main UX manager coordinating all UX systems."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize UX manager."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize all UX systems
        self.controls = FluidControlSystem()
        self.feedback = ResponsiveFeedbackSystem(screen_width, screen_height)
        self.tutorial = TutorialOverlay(screen_width, screen_height)
        self.help = HelpPanel(screen_width, screen_height)
        self.state_indicator = GameStateIndicator(screen_width, screen_height)
        self.hints = InputHintSystem(screen_width, screen_height)
        
        # Settings
        self.show_tutorial = True
        self.show_help = True
        self.show_hints = True
    
    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            self.controls.update_key_state(event.key, True)
            
            # Handle special keys
            if event.key == pygame.K_h:
                self.help.toggle()
            elif event.key == pygame.K_ESCAPE:
                self.tutorial.skip()
        
        elif event.type == pygame.KEYUP:
            self.controls.update_key_state(event.key, False)
    
    def update(self, dt: float):
        """Update all UX systems."""
        self.feedback.update(dt)
        self.tutorial.update(dt)
        self.hints.update(dt)
    
    def render(self, screen, game_state=None, player=None, ai_player=None):
        """Render all UX elements."""
        if self.show_tutorial:
            self.tutorial.render(screen)
        
        if self.show_help:
            self.help.render(screen)
        
        if self.show_hints:
            self.hints.render(screen)
        
        self.feedback.render(screen)
        
        if game_state and player and ai_player:
            self.state_indicator.render(screen, game_state, player, ai_player)
    
    def get_movement_input(self) -> Tuple[int, int]:
        """Get movement input."""
        return self.controls.get_movement_input()
    
    def should_place_bomb(self) -> bool:
        """Check if bomb should be placed."""
        return self.controls.should_place_bomb()
    
    def should_place_caca(self) -> bool:
        """Check if caca should be placed."""
        return self.controls.should_place_caca()
    
    def add_feedback(self, feedback_type: str, position: Tuple[int, int],
                     message: str = "", duration: float = 1.0):
        """Add visual feedback."""
        self.feedback.add_feedback(feedback_type, position, message, duration)
    
    def add_hint(self, text: str, hint_type: str = 'info'):
        """Add hint message."""
        self.hints.add_hint(text, hint_type)
    
    def reset(self):
        """Reset UX state."""
        self.controls.reset()
        self.tutorial.reset()
        self.hints.hints.clear()
