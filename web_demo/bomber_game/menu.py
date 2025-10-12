"""
Menu and splash screen for Proutman game.
"""

import pygame
import os
from . import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, BROWN


class MenuScreen:
    """Splash screen and menu for Proutman."""
    
    def __init__(self, screen):
        """Initialize menu screen."""
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
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
