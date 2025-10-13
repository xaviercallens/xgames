"""
Player Selection Menu - Choose number of players and AI opponents
"""

import pygame
from . import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, RED, BLUE, YELLOW


class PlayerSelector:
    """
    Menu for selecting number of human players and AI opponents.
    Supports 1-4 total players (1 human + 0-3 AI).
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.header_font = pygame.font.Font(None, 40)
        self.text_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 255, 100)
        self.text_color = (255, 255, 255)
        self.highlight_color = (100, 200, 255)
        self.button_color = (60, 60, 100)
        self.button_hover_color = (80, 80, 140)
        self.selected_color = (100, 255, 100)
        
        # Player configuration
        self.num_ai_opponents = 1  # Default: 1 AI opponent
        self.selected_index = 0
        
        # AI type options
        self.ai_types = [
            {'name': 'Beginner', 'type': 'simple', 'win_rate': 10, 'color': GREEN},
            {'name': 'Intermediate', 'type': 'heuristic', 'win_rate': 35, 'color': YELLOW},
            {'name': 'Advanced (PPO)', 'type': 'ppo', 'win_rate': 20, 'color': RED},
            {'name': 'Hybrid', 'type': 'hybrid', 'win_rate': 40, 'color': (255, 150, 255)},
        ]
        
        # Selected AI types for each opponent
        self.ai_selections = [0, 0, 0]  # Indices into ai_types for each AI opponent
        
    def show(self):
        """
        Show player selection menu.
        
        Returns:
            Dictionary with player configuration or None if cancelled
        """
        clock = pygame.time.Clock()
        running = True
        step = 0  # 0 = select number, 1 = select AI types
        
        while running:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if step == 1:
                            step = 0  # Go back to number selection
                        else:
                            return None  # Cancel
                    
                    if step == 0:  # Number selection
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.num_ai_opponents = max(0, self.num_ai_opponents - 1)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.num_ai_opponents = min(3, self.num_ai_opponents + 1)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if self.num_ai_opponents > 0:
                                step = 1  # Move to AI type selection
                                self.selected_index = 0
                            else:
                                # No AI opponents, return immediately
                                return self._create_config()
                    
                    elif step == 1:  # AI type selection
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.selected_index = max(0, self.selected_index - 1)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.selected_index = min(self.num_ai_opponents - 1, self.selected_index + 1)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            current = self.ai_selections[self.selected_index]
                            self.ai_selections[self.selected_index] = max(0, current - 1)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            current = self.ai_selections[self.selected_index]
                            self.ai_selections[self.selected_index] = min(len(self.ai_types) - 1, current + 1)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            return self._create_config()
            
            # Render
            if step == 0:
                self._render_number_selection()
            else:
                self._render_ai_type_selection()
            
            pygame.display.flip()
        
        return None
    
    def _render_number_selection(self):
        """Render the number of opponents selection screen."""
        self.screen.fill(self.bg_color)
        
        # Title
        title = self.title_font.render("🎮 Multiplayer Setup", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.header_font.render("Select Number of AI Opponents", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 120))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Options
        y_start = 200
        y_spacing = 80
        
        for i in range(4):
            y = y_start + i * y_spacing
            
            # Highlight selected
            if i == self.num_ai_opponents:
                pygame.draw.rect(self.screen, self.selected_color, 
                               (self.width // 2 - 250, y - 30, 500, 60), 3)
            
            # Option text
            if i == 0:
                text = f"0 AI Opponents (Practice Mode)"
                icon = "🎯"
            else:
                text = f"{i} AI Opponent{'s' if i > 1 else ''} ({i+1} Total Players)"
                icon = "🤖" * i
            
            option_text = self.text_font.render(f"{icon} {text}", True, 
                                               self.selected_color if i == self.num_ai_opponents else self.text_color)
            option_rect = option_text.get_rect(center=(self.width // 2, y))
            self.screen.blit(option_text, option_rect)
        
        # Instructions
        instructions = [
            "↑/↓ or W/S - Select",
            "ENTER or SPACE - Confirm",
            "ESC - Cancel"
        ]
        
        y = self.height - 120
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.highlight_color)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 30
    
    def _render_ai_type_selection(self):
        """Render the AI type selection screen."""
        self.screen.fill(self.bg_color)
        
        # Title
        title = self.title_font.render("🤖 Configure AI Opponents", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.header_font.render(f"Select AI Type for Each Opponent", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 120))
        self.screen.blit(subtitle, subtitle_rect)
        
        # AI opponent configurations
        y_start = 200
        y_spacing = 100
        
        for i in range(self.num_ai_opponents):
            y = y_start + i * y_spacing
            
            # Highlight selected opponent
            if i == self.selected_index:
                pygame.draw.rect(self.screen, self.selected_color, 
                               (50, y - 40, self.width - 100, 80), 3)
            
            # Opponent label
            label = self.text_font.render(f"AI Opponent {i+1}:", True, 
                                         self.selected_color if i == self.selected_index else self.text_color)
            self.screen.blit(label, (80, y - 20))
            
            # AI type selector
            ai_type = self.ai_types[self.ai_selections[i]]
            
            # Left arrow
            left_arrow = self.text_font.render("◀", True, 
                                              self.highlight_color if i == self.selected_index else self.text_color)
            self.screen.blit(left_arrow, (350, y - 20))
            
            # AI type name with color
            type_text = self.text_font.render(f"{ai_type['name']} ({ai_type['win_rate']}% WR)", 
                                             True, ai_type['color'])
            type_rect = type_text.get_rect(center=(self.width // 2, y))
            self.screen.blit(type_text, type_rect)
            
            # Right arrow
            right_arrow = self.text_font.render("▶", True, 
                                               self.highlight_color if i == self.selected_index else self.text_color)
            self.screen.blit(right_arrow, (self.width - 400, y - 20))
        
        # Instructions
        instructions = [
            "↑/↓ or W/S - Select Opponent",
            "←/→ or A/D - Change AI Type",
            "ENTER or SPACE - Start Game",
            "ESC - Go Back"
        ]
        
        y = self.height - 150
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.highlight_color)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 30
    
    def _create_config(self):
        """Create player configuration dictionary."""
        config = {
            'num_human_players': 1,
            'num_ai_opponents': self.num_ai_opponents,
            'total_players': 1 + self.num_ai_opponents,
            'ai_configs': []
        }
        
        # Add AI configurations
        for i in range(self.num_ai_opponents):
            ai_type = self.ai_types[self.ai_selections[i]]
            config['ai_configs'].append({
                'index': i,
                'name': f"AI {i+1}",
                'type': ai_type['type'],
                'type_name': ai_type['name'],
                'win_rate': ai_type['win_rate'],
                'color': ai_type['color'],
            })
        
        return config
