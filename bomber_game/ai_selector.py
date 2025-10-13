"""
AI Opponent Selector - Choose AI difficulty and type before game starts.
"""

import pygame
import json
import os
from pathlib import Path


class AISelector:
    """
    AI Opponent Selection Menu.
    Shows available AI opponents with stats and allows user to choose.
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.header_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Colors
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 255, 100)
        self.text_color = (255, 255, 255)
        self.highlight_color = (100, 200, 255)
        self.button_color = (60, 60, 100)
        self.button_hover_color = (80, 80, 140)
        self.selected_color = (100, 255, 100)
        
        # AI Options
        self.ai_options = self._load_ai_options()
        self.selected_index = 0
        self.hovered_index = -1
        
        # Button positions
        self.button_rects = []
        self._calculate_button_positions()
        
    def _load_ai_options(self):
        """Load available AI opponents with their stats."""
        models_dir = Path(__file__).parent / "models"
        stats_file = models_dir / "training_stats.json"
        history_file = models_dir / "game_history.json"
        
        # Load training stats
        training_stats = {}
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    training_stats = json.load(f)
            except:
                pass
        
        # Load game history
        game_history = {}
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    game_history = json.load(f)
            except:
                pass
        
        # Define AI options
        options = []
        
        # 1. Beginner AI (Simple Heuristic)
        options.append({
            'name': 'Beginner Bot',
            'type': 'simple',
            'level': 'Beginner',
            'description': 'Basic AI for learning the game',
            'icon': '🌱',
            'win_rate': 10.0,
            'games_played': game_history.get('total_games', 0),
            'ai_wins': game_history.get('ai_wins', 0),
            'human_wins': game_history.get('human_wins', 0),
            'model_path': None,
            'color': (100, 255, 100),
        })
        
        # 2. Intermediate AI (Improved Heuristic)
        options.append({
            'name': 'Intermediate Bot',
            'type': 'heuristic',
            'level': 'Intermediate',
            'description': 'Smart rule-based AI with A* pathfinding',
            'icon': '🎯',
            'win_rate': 35.0,
            'games_played': game_history.get('total_games', 0),
            'ai_wins': game_history.get('ai_wins', 0),
            'human_wins': game_history.get('human_wins', 0),
            'model_path': None,
            'color': (255, 200, 100),
        })
        
        # 3. Advanced AI (PPO Trained)
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
                'description': f'Deep RL trained on {episodes:,} games (Recent: {recent_win_rate:.0f}% WR)',
                'icon': '🤖',
                'win_rate': recent_win_rate,
                'games_played': episodes,
                'ai_wins': training_stats.get('total_wins', 0),
                'human_wins': episodes - training_stats.get('total_wins', 0),
                'model_path': str(ppo_model),
                'color': (255, 100, 100),
            })
        
        # 4. Hybrid AI (Heuristics + RL) - NEW!
        if ppo_model.exists():
            options.append({
                'name': '🎭 Hybrid Bot (NEW!)',
                'type': 'hybrid',
                'level': 'Expert',
                'description': 'Combines heuristics + RL (Adaptive, ~40% WR)',
                'icon': '🎭',
                'win_rate': 40.0,
                'games_played': episodes,
                'ai_wins': 0,
                'human_wins': 0,
                'model_path': str(ppo_model),
                'color': (255, 150, 255),
                'hybrid_mode': 'adaptive',
            })
        
        # 5. Expert AI (Best Model)
        best_model = models_dir / "best_model.pth"
        if best_model.exists():
            options.append({
                'name': 'Expert Bot (Best)',
                'type': 'ppo_best',
                'level': 'Expert',
                'description': 'The strongest trained AI',
                'icon': '👑',
                'win_rate': training_stats.get('win_rate', 0.3),
                'games_played': training_stats.get('total_episodes', 0),
                'ai_wins': training_stats.get('total_wins', 0),
                'human_wins': training_stats.get('total_episodes', 0) - training_stats.get('total_wins', 0),
                'model_path': str(best_model),
                'color': (200, 100, 255),
            })
        
        # 6. Pretrained AI (Bootstrap)
        pretrained_model = models_dir / "ppo_agent_pretrained.pth"
        if pretrained_model.exists():
            options.append({
                'name': 'Trained Bot (Bootstrap)',
                'type': 'ppo_pretrained',
                'level': 'Intermediate',
                'description': 'AI bootstrapped with heuristics',
                'icon': '🎓',
                'win_rate': 25.0,
                'games_played': 1000,
                'ai_wins': 250,
                'human_wins': 750,
                'model_path': str(pretrained_model),
                'color': (100, 200, 255),
            })
        
        return options
    
    def _calculate_button_positions(self):
        """Calculate button positions for each AI option."""
        self.button_rects = []
        
        button_width = 600
        button_height = 120
        start_y = 150
        spacing = 20
        
        for i in range(len(self.ai_options)):
            x = (self.width - button_width) // 2
            y = start_y + i * (button_height + spacing)
            self.button_rects.append(pygame.Rect(x, y, button_width, button_height))
    
    def handle_events(self, event):
        """Handle user input."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            self.hovered_index = -1
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.hovered_index = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_index = i
                        return True  # Selection made
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.ai_options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.ai_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return True  # Selection confirmed
            elif event.key == pygame.K_ESCAPE:
                return None  # Cancel
        
        return False
    
    def draw(self):
        """Draw the AI selection menu."""
        self.screen.fill(self.bg_color)
        
        # Title
        title = self.title_font.render("🎮 Choose Your Opponent", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.text_font.render("Select AI difficulty level", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 110))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw AI options
        for i, (option, rect) in enumerate(zip(self.ai_options, self.button_rects)):
            self._draw_ai_option(option, rect, i)
        
        # Instructions
        instructions = [
            "Use ↑↓ arrows or mouse to select",
            "Press ENTER or click to confirm",
            "Press ESC to use default"
        ]
        
        y = self.height - 80
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.text_color)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 25
        
        pygame.display.flip()
    
    def _draw_ai_option(self, option, rect, index):
        """Draw a single AI option button."""
        # Determine button color
        if index == self.selected_index:
            color = self.selected_color
            border_width = 4
        elif index == self.hovered_index:
            color = self.button_hover_color
            border_width = 3
        else:
            color = self.button_color
            border_width = 2
        
        # Draw button background
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, option['color'], rect, border_width, border_radius=10)
        
        # Icon and name
        icon_name = f"{option['icon']} {option['name']}"
        name_text = self.header_font.render(icon_name, True, self.text_color)
        name_rect = name_text.get_rect(left=rect.left + 20, top=rect.top + 15)
        self.screen.blit(name_text, name_rect)
        
        # Level badge
        level_text = self.small_font.render(option['level'], True, self.text_color)
        level_bg = pygame.Rect(rect.right - 120, rect.top + 15, 100, 30)
        pygame.draw.rect(self.screen, option['color'], level_bg, border_radius=5)
        level_rect = level_text.get_rect(center=level_bg.center)
        self.screen.blit(level_text, level_rect)
        
        # Description
        desc_text = self.text_font.render(option['description'], True, self.text_color)
        desc_rect = desc_text.get_rect(left=rect.left + 20, top=rect.top + 50)
        self.screen.blit(desc_text, desc_rect)
        
        # Stats
        if option['games_played'] > 0:
            human_wr = (option['human_wins'] / option['games_played']) * 100
            stats_text = f"Win Rate: {option['win_rate']:.1f}% | Your Record: {human_wr:.0f}% ({option['human_wins']}/{option['games_played']})"
        else:
            stats_text = f"Expected Win Rate: {option['win_rate']:.1f}%"
        
        stats = self.small_font.render(stats_text, True, self.text_color)
        stats_rect = stats.get_rect(left=rect.left + 20, top=rect.top + 85)
        self.screen.blit(stats, stats_rect)
    
    def get_selected_ai(self):
        """Get the selected AI configuration."""
        return self.ai_options[self.selected_index]
    
    def show(self):
        """Show the AI selection menu and return selected AI."""
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                result = self.handle_events(event)
                if result is True:
                    return self.get_selected_ai()
                elif result is None:
                    return None  # Use default
            
            self.draw()
