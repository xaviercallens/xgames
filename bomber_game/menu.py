"""
Menu and splash screen for Proutman game with multiplayer support.
"""

import pygame
import os
import json
from pathlib import Path
from . import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, BROWN


class MenuScreen:
    """Splash screen and menu for Proutman."""
    
    def __init__(self, screen):
        """Initialize menu screen."""
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # AI selection options
        self.ai_options = self._load_ai_options()
        self.selected_ai_index = 0
        
        # Load splash image
        self.splash_image = None
        splash_path = os.path.join(os.path.dirname(__file__), 
                                   "assets", "images", "proutman_splash.jpg")
        if os.path.exists(splash_path):
            try:
                self.splash_image = pygame.image.load(splash_path)
                # Scale to fit screen while maintaining aspect ratio
                img_rect = self.splash_image.get_rect()
                scale = min(SCREEN_WIDTH / img_rect.width, 
                           SCREEN_HEIGHT / img_rect.height)
                new_width = int(img_rect.width * scale)
                new_height = int(img_rect.height * scale)
                self.splash_image = pygame.transform.scale(self.splash_image, 
                                                          (new_width, new_height))
            except Exception as e:
                print(f"Could not load splash image: {e}")
                self.splash_image = None
        
        # Animation
        self.pulse_timer = 0
        self.pulse_speed = 2.0
        
        # Player selector (lazy load)
        self._player_selector = None
    
    def _load_ai_options(self):
        """Load available AI options."""
        models_dir = Path(__file__).parent / "models"
        stats_file = models_dir / "training_stats.json"
        
        # Load training stats
        training_stats = {}
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    training_stats = json.load(f)
            except:
                pass
        
        options = [
            {
                'name': 'Beginner Bot',
                'type': 'simple',
                'level': 'Beginner',
                'description': 'Basic AI - Easy to beat',
                'icon': '🌱',
                'win_rate': 10.0,
                'color': (100, 255, 100),
            },
            {
                'name': 'Intermediate Bot',
                'type': 'heuristic',
                'level': 'Intermediate',
                'description': 'Smart heuristic AI',
                'icon': '🎯',
                'win_rate': 35.0,
                'color': (255, 200, 100),
            },
        ]
        
        # Add PPO models if available
        ppo_model = models_dir / "ppo_agent.pth"
        if ppo_model.exists():
            # Use recent win rate (last 100 episodes) if available
            win_rates = training_stats.get('win_rates', [])
            recent_win_rate = win_rates[-1] if win_rates else training_stats.get('win_rate', 0.3)
            episodes = training_stats.get('total_episodes', 0)
            
            options.append({
                'name': 'Advanced Bot (PPO)',
                'type': 'ppo',
                'level': 'Advanced',
                'description': f'Deep RL - {episodes:,} games (Recent: {recent_win_rate:.0f}% WR)',
                'icon': '🤖',
                'win_rate': recent_win_rate,
                'color': (255, 100, 100),
                'model_path': str(ppo_model),
            })
        
        # Add Hybrid AI (Heuristics + RL) - NEW!
        if ppo_model.exists():
            options.append({
                'name': '🎭 Hybrid Bot (NEW!)',
                'type': 'hybrid',
                'level': 'Expert',
                'description': 'Heuristics + RL (Adaptive, ~40% WR)',
                'icon': '🎭',
                'win_rate': 40.0,
                'color': (255, 150, 255),
                'model_path': str(ppo_model),
                'hybrid_mode': 'adaptive',
            })
        
        # Add expert model if available
        best_model = models_dir / "best_model.pth"
        if best_model.exists():
            options.append({
                'name': 'Expert Bot (Best)',
                'type': 'ppo_best',
                'level': 'Expert',
                'description': 'Strongest trained AI',
                'icon': '👑',
                'win_rate': training_stats.get('win_rate', 0.3),
                'color': (200, 100, 255),
                'model_path': str(best_model),
            })
        
        return options
        
    def show_splash(self, duration=3.0):
        """
        Show splash screen for a duration.
        
        Args:
            duration: How long to show splash (seconds)
            
        Returns:
            True if user wants to skip, False otherwise
        """
        clock = pygame.time.Clock()
        elapsed = 0
        
        while elapsed < duration:
            dt = clock.tick(60) / 1000.0
            elapsed += dt
            self.pulse_timer += dt
            
            # Check for skip
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return False  # Skip splash
            
            # Draw splash
            self.screen.fill(BLACK)
            
            if self.splash_image:
                # Center splash image
                img_rect = self.splash_image.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                )
                self.screen.blit(self.splash_image, img_rect)
                
                # Pulsing "Press any key" text
                pulse = abs(pygame.math.Vector2(0, 1).rotate(
                    self.pulse_timer * 360 * self.pulse_speed).y)
                alpha = int(128 + 127 * pulse)
                
                skip_text = self.font_small.render("Press any key to start...", 
                                                   True, WHITE)
                skip_text.set_alpha(alpha)
                skip_rect = skip_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                )
                self.screen.blit(skip_text, skip_rect)
            else:
                # Fallback text splash
                self._draw_text_splash()
            
            pygame.display.flip()
        
        return False
    
    def _draw_text_splash(self):
        """Draw text-based splash screen."""
        # Title
        title = self.font_large.render("💨 PROUTMAN 💨", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("L'aventure Codée!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Caca decorations
        caca_emoji = self.font_large.render("💩", True, BROWN)
        self.screen.blit(caca_emoji, (100, 300))
        self.screen.blit(caca_emoji, (SCREEN_WIDTH - 150, 300))
        self.screen.blit(caca_emoji, (150, 450))
        self.screen.blit(caca_emoji, (SCREEN_WIDTH - 200, 450))
        
        # Description
        desc_lines = [
            "Pour Apprendre à Coder et S'Amuser!",
            "Création de Jeu & Apprentissage Renforcé",
            "",
            "💨 Drop Prouts (Trumps) to destroy walls",
            "💩 Place Cacas to block enemies",
            "🎯 Collect power-ups and defeat AI"
        ]
        
        y = 320
        for line in desc_lines:
            text = self.font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 35
        
        # Pulsing start text
        pulse = abs(pygame.math.Vector2(0, 1).rotate(
            self.pulse_timer * 360 * self.pulse_speed).y)
        alpha = int(128 + 127 * pulse)
        
        start_text = self.font_medium.render("Press any key to start...", 
                                            True, GREEN)
        start_text.set_alpha(alpha)
        start_rect = start_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        )
        self.screen.blit(start_text, start_rect)
    
    def show_menu(self):
        """
        Show main menu.
        
        Returns:
            'start' to start game, 'quit' to quit
        """
        clock = pygame.time.Clock()
        selected = 0  # 0 = Start, 1 = Quit
        
        while True:
            dt = clock.tick(60) / 1000.0
            self.pulse_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected = 1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return 'start' if selected == 0 else 'quit'
                    elif event.key == pygame.K_ESCAPE:
                        return 'quit'
            
            # Draw menu
            self.screen.fill(BLACK)
            
            # Title
            title = self.font_large.render("💨 PROUTMAN 💨", True, GREEN)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
            
            # Menu options
            options = ["START GAME", "QUIT"]
            y = 300
            
            for i, option in enumerate(options):
                color = GREEN if i == selected else WHITE
                
                # Pulse selected option
                if i == selected:
                    pulse = abs(pygame.math.Vector2(0, 1).rotate(
                        self.pulse_timer * 360 * self.pulse_speed).y)
                    scale = 1.0 + 0.1 * pulse
                    font = pygame.font.Font(None, int(48 * scale))
                else:
                    font = self.font_medium
                
                text = font.render(option, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text, text_rect)
                
                # Arrow for selected
                if i == selected:
                    arrow = self.font_medium.render("→", True, GREEN)
                    arrow_rect = arrow.get_rect(right=text_rect.left - 20, 
                                               centery=text_rect.centery)
                    self.screen.blit(arrow, arrow_rect)
                
                y += 80
            
            # Controls hint
            hint = self.font_small.render("↑↓ to select, ENTER to confirm", 
                                         True, WHITE)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 
                                             SCREEN_HEIGHT - 50))
            self.screen.blit(hint, hint_rect)
            
            pygame.display.flip()
    
    def show_ai_selection(self):
        """Show AI selection screen after splash."""
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60) / 1000.0
            self.pulse_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_ai_index = (self.selected_ai_index - 1) % len(self.ai_options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_ai_index = (self.selected_ai_index + 1) % len(self.ai_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return self.ai_options[self.selected_ai_index]
                    elif event.key == pygame.K_ESCAPE:
                        # Use default (first option)
                        return self.ai_options[0]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Check if clicked on an option
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected_ai_index = i
                            return self.ai_options[i]
            
            self._draw_ai_selection()
            pygame.display.flip()
    
    def _draw_ai_selection(self):
        """Draw AI selection screen."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("🎮 Choose Your Opponent", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("Select AI difficulty level", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 130))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw AI options
        self.option_rects = []
        start_y = 200
        option_height = 100
        option_spacing = 20
        option_width = 600
        
        for i, option in enumerate(self.ai_options):
            y = start_y + i * (option_height + option_spacing)
            x = (SCREEN_WIDTH - option_width) // 2
            
            rect = pygame.Rect(x, y, option_width, option_height)
            self.option_rects.append(rect)
            
            # Determine colors
            if i == self.selected_ai_index:
                bg_color = (60, 60, 100)
                border_color = option['color']
                border_width = 4
                
                # Pulse effect
                pulse = abs(pygame.math.Vector2(0, 1).rotate(
                    self.pulse_timer * 360 * self.pulse_speed).y)
                glow = int(20 + 20 * pulse)
                bg_color = tuple(min(255, c + glow) for c in bg_color)
            else:
                bg_color = (40, 40, 60)
                border_color = (100, 100, 150)
                border_width = 2
            
            # Draw option box
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=10)
            
            # Icon and name
            icon_name = f"{option['icon']} {option['name']}"
            name_text = self.font_medium.render(icon_name, True, WHITE)
            name_rect = name_text.get_rect(left=rect.left + 20, top=rect.top + 15)
            self.screen.blit(name_text, name_rect)
            
            # Level badge
            level_text = self.font_tiny.render(option['level'], True, WHITE)
            level_bg = pygame.Rect(rect.right - 110, rect.top + 15, 90, 25)
            pygame.draw.rect(self.screen, option['color'], level_bg, border_radius=5)
            level_rect = level_text.get_rect(center=level_bg.center)
            self.screen.blit(level_text, level_rect)
            
            # Description
            desc_text = self.font_small.render(option['description'], True, WHITE)
            desc_rect = desc_text.get_rect(left=rect.left + 20, top=rect.top + 55)
            self.screen.blit(desc_text, desc_rect)
            
            # Win rate
            wr_text = self.font_tiny.render(f"Expected Win Rate: {option['win_rate']:.1f}%", True, (200, 200, 200))
            wr_rect = wr_text.get_rect(left=rect.left + 20, top=rect.top + 80)
            self.screen.blit(wr_text, wr_rect)
        
        # Instructions
        instructions = [
            "↑↓ or W/S to select",
            "ENTER or SPACE to confirm",
            "ESC for default (Beginner)"
        ]
        
        y = SCREEN_HEIGHT - 100
        for instruction in instructions:
            text = self.font_tiny.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 25
    
    def show_multiplayer_selection(self):
        """
        Show multiplayer player selection menu.
        
        Returns:
            Dictionary with player configuration or None if cancelled
        """
        # Lazy load player selector
        if self._player_selector is None:
            from .player_selector import PlayerSelector
            self._player_selector = PlayerSelector(self.screen)
        
        return self._player_selector.show()
