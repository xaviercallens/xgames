"""
Game Recap Screen - Detailed end-game statistics and analysis.
"""

import pygame
import json
from pathlib import Path


class GameRecap:
    """
    Detailed end-game recap screen showing comprehensive statistics.
    """
    
    def __init__(self, screen, game_stats, recorder_stats, ai_info):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.game_stats = game_stats
        self.recorder_stats = recorder_stats
        self.ai_info = ai_info
        
        # Fonts
        self.title_font = pygame.font.Font(None, 56)
        self.header_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Colors
        self.bg_color = (20, 20, 40)
        self.title_color = (255, 255, 100)
        self.human_color = (100, 255, 100)
        self.ai_color = (255, 100, 100)
        self.text_color = (255, 255, 255)
        self.highlight_color = (100, 200, 255)
        self.button_color = (60, 60, 100)
        self.button_hover_color = (80, 80, 140)
        
        # Scroll offset
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Buttons
        self.buttons = {
            'continue': pygame.Rect(self.width // 2 - 250, self.height - 80, 200, 50),
            'export': pygame.Rect(self.width // 2 - 20, self.height - 80, 200, 50),
            'quit': pygame.Rect(self.width // 2 + 210, self.height - 80, 200, 50),
        }
        self.hovered_button = None
        
    def draw(self):
        """Draw the recap screen."""
        self.screen.fill(self.bg_color)
        
        # Create scrollable surface
        content_height = 1200  # Estimated content height
        content_surface = pygame.Surface((self.width, content_height))
        content_surface.fill(self.bg_color)
        
        y = 20
        
        # Title
        winner = self.game_stats.history['games'][-1]['winner'] if self.game_stats.history['games'] else None
        if winner == "Player":
            title_text = "🎉 VICTORY! 🎉"
            title_color = self.human_color
        elif winner == "AI":
            title_text = "💀 DEFEAT 💀"
            title_color = self.ai_color
        else:
            title_text = "🤝 DRAW 🤝"
            title_color = self.text_color
        
        title = self.title_font.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(self.width // 2, y))
        content_surface.blit(title, title_rect)
        y += 70
        
        # Game duration
        last_game = self.game_stats.history['games'][-1] if self.game_stats.history['games'] else {}
        duration = last_game.get('duration', 0)
        duration_text = f"Game Duration: {int(duration)}s"
        duration_surf = self.text_font.render(duration_text, True, self.text_color)
        duration_rect = duration_surf.get_rect(center=(self.width // 2, y))
        content_surface.blit(duration_surf, duration_rect)
        y += 40
        
        # Separator
        pygame.draw.line(content_surface, self.highlight_color, (50, y), (self.width - 50, y), 2)
        y += 30
        
        # Player vs AI comparison
        y = self._draw_player_comparison(content_surface, y, last_game)
        y += 30
        
        # Detailed statistics
        y = self._draw_detailed_stats(content_surface, y, last_game)
        y += 30
        
        # Historical performance
        y = self._draw_historical_stats(content_surface, y)
        y += 30
        
        # AI Information
        y = self._draw_ai_info(content_surface, y)
        y += 30
        
        # Recommendations
        y = self._draw_recommendations(content_surface, y)
        
        # Calculate max scroll
        self.max_scroll = max(0, y - self.height + 150)
        
        # Blit scrollable content
        self.screen.blit(content_surface, (0, -self.scroll_offset))
        
        # Draw fixed bottom bar
        self._draw_bottom_bar()
        
        pygame.display.flip()
    
    def _draw_player_comparison(self, surface, y, last_game):
        """Draw player vs AI comparison."""
        header = self.header_font.render("📊 Performance Comparison", True, self.highlight_color)
        header_rect = header.get_rect(center=(self.width // 2, y))
        surface.blit(header, header_rect)
        y += 50
        
        human_stats = last_game.get('human', {})
        ai_stats = last_game.get('ai', {})
        
        # Create two columns
        col_width = (self.width - 100) // 2
        left_x = 50
        right_x = 50 + col_width + 50
        
        # Human column
        human_header = self.text_font.render("👤 Human", True, self.human_color)
        surface.blit(human_header, (left_x, y))
        
        # AI column
        ai_header = self.text_font.render(f"🤖 {self.ai_info.get('name', 'AI')}", True, self.ai_color)
        surface.blit(ai_header, (right_x, y))
        y += 35
        
        # Stats comparison
        stats_to_show = [
            ('Moves', 'moves'),
            ('Bombs Placed', 'bombs'),
            ('Power-ups', 'powerups'),
            ('Walls Destroyed', 'walls'),
            ('Strategy', 'strategy'),
            ('Avg Risk', 'avg_risk'),
            ('Performance', 'performance'),
        ]
        
        for label, key in stats_to_show:
            human_val = human_stats.get(key, 0)
            ai_val = ai_stats.get(key, 0)
            
            # Format values
            if key == 'avg_risk':
                human_str = f"{human_val:.1f}%"
                ai_str = f"{ai_val:.1f}%"
            elif key == 'performance':
                human_str = f"{human_val:.0f}/100"
                ai_str = f"{ai_val:.0f}/100"
            elif key == 'strategy':
                human_str = str(human_val)
                ai_str = str(ai_val)
            else:
                human_str = str(human_val)
                ai_str = str(ai_val)
            
            # Label
            label_surf = self.small_font.render(label + ":", True, self.text_color)
            label_rect = label_surf.get_rect(left=left_x, top=y)
            surface.blit(label_surf, label_rect)
            
            # Human value
            human_surf = self.text_font.render(human_str, True, self.human_color)
            human_rect = human_surf.get_rect(right=left_x + col_width - 10, top=y)
            surface.blit(human_surf, human_rect)
            
            # AI value
            ai_surf = self.text_font.render(ai_str, True, self.ai_color)
            ai_rect = ai_surf.get_rect(right=right_x + col_width - 10, top=y)
            surface.blit(ai_surf, ai_rect)
            
            y += 28
        
        return y
    
    def _draw_detailed_stats(self, surface, y, last_game):
        """Draw detailed game statistics."""
        header = self.header_font.render("📈 Detailed Statistics", True, self.highlight_color)
        header_rect = header.get_rect(center=(self.width // 2, y))
        surface.blit(header, header_rect)
        y += 50
        
        # Recording stats
        if self.recorder_stats:
            stats = [
                f"Total Actions: {self.recorder_stats.get('total_actions', 0)}",
                f"Total Events: {self.recorder_stats.get('total_events', 0)}",
                f"Total Frames: {self.recorder_stats.get('total_frames', 0)}",
            ]
            
            for stat in stats:
                text = self.text_font.render(stat, True, self.text_color)
                text_rect = text.get_rect(left=100, top=y)
                surface.blit(text, text_rect)
                y += 30
        
        return y
    
    def _draw_historical_stats(self, surface, y):
        """Draw historical performance."""
        header = self.header_font.render("📜 Historical Performance", True, self.highlight_color)
        header_rect = header.get_rect(center=(self.width // 2, y))
        surface.blit(header, header_rect)
        y += 50
        
        total_games = self.game_stats.history['total_games']
        human_wins = self.game_stats.history['human_wins']
        ai_wins = self.game_stats.history['ai_wins']
        
        human_wr = self.game_stats.get_win_rate(True)
        ai_wr = self.game_stats.get_win_rate(False)
        
        stats = [
            f"Total Games Played: {total_games}",
            f"Human Wins: {human_wins} ({human_wr:.1f}%)",
            f"AI Wins: {ai_wins} ({ai_wr:.1f}%)",
            f"Human Win Streak: {self.game_stats.history['human_stats']['current_win_streak']}",
            f"Best Win Streak: {self.game_stats.history['human_stats']['best_win_streak']}",
        ]
        
        for stat in stats:
            text = self.text_font.render(stat, True, self.text_color)
            text_rect = text.get_rect(left=100, top=y)
            surface.blit(text, text_rect)
            y += 30
        
        # Trend
        trend = self.game_stats.get_recent_trend(True)
        trend_text = f"Recent Trend: {trend}"
        trend_surf = self.text_font.render(trend_text, True, self.highlight_color)
        trend_rect = trend_surf.get_rect(left=100, top=y)
        surface.blit(trend_surf, trend_rect)
        y += 40
        
        return y
    
    def _draw_ai_info(self, surface, y):
        """Draw AI opponent information."""
        header = self.header_font.render("🤖 AI Opponent Info", True, self.highlight_color)
        header_rect = header.get_rect(center=(self.width // 2, y))
        surface.blit(header, header_rect)
        y += 50
        
        info = [
            f"Name: {self.ai_info.get('name', 'Unknown')}",
            f"Type: {self.ai_info.get('type', 'Unknown')}",
            f"Level: {self.ai_info.get('level', 'Unknown')}",
            f"Description: {self.ai_info.get('description', 'N/A')}",
        ]
        
        for line in info:
            text = self.text_font.render(line, True, self.text_color)
            text_rect = text.get_rect(left=100, top=y)
            surface.blit(text, text_rect)
            y += 30
        
        return y
    
    def _draw_recommendations(self, surface, y):
        """Draw gameplay recommendations."""
        header = self.header_font.render("💡 Recommendations", True, self.highlight_color)
        header_rect = header.get_rect(center=(self.width // 2, y))
        surface.blit(header, header_rect)
        y += 50
        
        recommendations = self.game_stats.get_recommendations()
        
        for rec in recommendations[:5]:  # Show top 5
            # Wrap text
            words = rec.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                if len(test_line) > 70:
                    lines.append(current_line.strip())
                    current_line = word + " "
                else:
                    current_line = test_line
            
            if current_line:
                lines.append(current_line.strip())
            
            for line in lines:
                text = self.small_font.render(line, True, self.text_color)
                text_rect = text.get_rect(left=100, top=y)
                surface.blit(text, text_rect)
                y += 25
            
            y += 10
        
        return y
    
    def _draw_bottom_bar(self):
        """Draw fixed bottom bar with buttons."""
        # Background
        bar_rect = pygame.Rect(0, self.height - 100, self.width, 100)
        pygame.draw.rect(self.screen, (30, 30, 50), bar_rect)
        pygame.draw.line(self.screen, self.highlight_color, (0, self.height - 100), (self.width, self.height - 100), 2)
        
        # Buttons
        button_labels = {
            'continue': 'Continue (R)',
            'export': 'Export Data',
            'quit': 'Quit (ESC)',
        }
        
        for key, rect in self.buttons.items():
            color = self.button_hover_color if key == self.hovered_button else self.button_color
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, self.highlight_color, rect, 2, border_radius=5)
            
            label = self.text_font.render(button_labels[key], True, self.text_color)
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)
    
    def handle_events(self, event):
        """Handle user input."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            self.hovered_button = None
            for key, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    self.hovered_button = key
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = event.pos
                for key, rect in self.buttons.items():
                    if rect.collidepoint(mouse_pos):
                        return key
            
            elif event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 30)
            
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return 'continue'
            elif event.key == pygame.K_e:
                return 'export'
            elif event.key == pygame.K_ESCAPE:
                return 'quit'
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 30)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
        
        return None
    
    def show(self):
        """Show the recap screen and wait for user action."""
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                
                action = self.handle_events(event)
                if action:
                    return action
            
            self.draw()
