"""
Statistics Panel - Right-side panel showing comprehensive game analytics.
"""

import pygame
import math


class StatsPanel:
    """
    Right-side statistics panel with real-time game analytics.
    Shows AI info, risk levels, strategy, recommendations, and performance graphs.
    """
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Fonts
        self.title_font = pygame.font.Font(None, 28)
        self.header_font = pygame.font.Font(None, 22)
        self.text_font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 16)
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.border_color = (100, 100, 150)
        self.title_color = (255, 255, 255)
        self.human_color = (100, 255, 100)
        self.ai_color = (255, 100, 100)
        self.text_color = (200, 200, 200)
        self.highlight_color = (255, 255, 100)
        
        # Graph data
        self.human_perf_history = []
        self.ai_perf_history = []
        
    def draw(self, screen, stats, game_state):
        """Draw the statistics panel."""
        # Background
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)
        
        current_y = self.y + 10
        
        # Title
        title = self.title_font.render("📊 GAME ANALYTICS", True, self.title_color)
        screen.blit(title, (self.x + 10, current_y))
        current_y += 35
        
        # Separator
        pygame.draw.line(screen, self.border_color, 
                        (self.x + 10, current_y), 
                        (self.x + self.width - 10, current_y), 2)
        current_y += 10
        
        # AI Information
        current_y = self._draw_ai_info(screen, stats, current_y)
        current_y += 10
        
        # Current Game Stats
        current_y = self._draw_current_stats(screen, stats, current_y)
        current_y += 10
        
        # Risk Levels
        current_y = self._draw_risk_levels(screen, stats, game_state, current_y)
        current_y += 10
        
        # Strategy Analysis
        current_y = self._draw_strategy(screen, stats, current_y)
        current_y += 10
        
        # Performance Scores
        current_y = self._draw_performance(screen, stats, current_y)
        current_y += 10
        
        # Historical Stats
        current_y = self._draw_history(screen, stats, current_y)
        current_y += 10
        
        # Performance Graph
        current_y = self._draw_performance_graph(screen, stats, current_y)
        current_y += 10
        
        # Recommendations
        current_y = self._draw_recommendations(screen, stats, current_y)
    
    def _draw_ai_info(self, screen, stats, y):
        """Draw AI information section."""
        header = self.header_font.render("🤖 AI OPPONENT", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        # AI Type
        ai_type = stats.ai_type
        type_text = self.text_font.render(f"Type: {ai_type}", True, self.ai_color)
        screen.blit(type_text, (self.x + 15, y))
        y += 20
        
        # AI Description
        descriptions = {
            "PPO": "Deep RL (Trained)",
            "PPO (Pretrained)": "Deep RL (Bootstrap)",
            "Improved Heuristic": "Rule-Based (Advanced)",
            "Simple": "Rule-Based (Basic)",
        }
        desc = descriptions.get(ai_type, "Unknown")
        desc_text = self.small_font.render(desc, True, self.text_color)
        screen.blit(desc_text, (self.x + 15, y))
        y += 20
        
        # AI Win Rate
        ai_win_rate = stats.get_win_rate(False)
        wr_text = self.text_font.render(f"Win Rate: {ai_win_rate:.1f}%", True, self.ai_color)
        screen.blit(wr_text, (self.x + 15, y))
        y += 25
        
        return y
    
    def _draw_current_stats(self, screen, stats, y):
        """Draw current game statistics."""
        header = self.header_font.render("📈 CURRENT GAME", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        # Game time
        game_time = int(pygame.time.get_ticks() / 1000 - stats.game_start_time + pygame.time.get_ticks() / 1000)
        time_text = self.text_font.render(f"Time: {game_time}s", True, self.text_color)
        screen.blit(time_text, (self.x + 15, y))
        y += 20
        
        # Human stats
        human_text = self.text_font.render(f"👤 Human:", True, self.human_color)
        screen.blit(human_text, (self.x + 15, y))
        y += 18
        
        stats_lines = [
            f"  Moves: {stats.human_moves}",
            f"  Bombs: {stats.human_bombs_placed}",
            f"  Power-ups: {stats.powerups_collected_human}",
            f"  Walls: {stats.walls_destroyed_human}",
        ]
        
        for line in stats_lines:
            text = self.small_font.render(line, True, self.text_color)
            screen.blit(text, (self.x + 15, y))
            y += 16
        
        y += 5
        
        # AI stats
        ai_text = self.text_font.render(f"🤖 AI:", True, self.ai_color)
        screen.blit(ai_text, (self.x + 15, y))
        y += 18
        
        stats_lines = [
            f"  Moves: {stats.ai_moves}",
            f"  Bombs: {stats.ai_bombs_placed}",
            f"  Power-ups: {stats.powerups_collected_ai}",
            f"  Walls: {stats.walls_destroyed_ai}",
        ]
        
        for line in stats_lines:
            text = self.small_font.render(line, True, self.text_color)
            screen.blit(text, (self.x + 15, y))
            y += 16
        
        y += 10
        return y
    
    def _draw_risk_levels(self, screen, stats, game_state, y):
        """Draw real-time risk levels."""
        header = self.header_font.render("⚠️ RISK LEVELS", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        # Human risk
        human_risk = stats.get_current_risk(True)
        self._draw_risk_bar(screen, "Human", human_risk, self.human_color, y)
        y += 30
        
        # AI risk
        ai_risk = stats.get_current_risk(False)
        self._draw_risk_bar(screen, "AI", ai_risk, self.ai_color, y)
        y += 35
        
        return y
    
    def _draw_risk_bar(self, screen, label, risk, color, y):
        """Draw a risk level bar."""
        # Label
        label_text = self.small_font.render(f"{label}:", True, self.text_color)
        screen.blit(label_text, (self.x + 15, y))
        
        # Risk bar
        bar_x = self.x + 70
        bar_y = y + 2
        bar_width = self.width - 90
        bar_height = 12
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Fill based on risk
        fill_width = int((risk / 100) * bar_width)
        
        # Color based on risk level
        if risk > 70:
            fill_color = (255, 50, 50)  # Red
        elif risk > 40:
            fill_color = (255, 200, 50)  # Orange
        else:
            fill_color = (50, 255, 50)  # Green
        
        if fill_width > 0:
            pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, self.border_color, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Value
        value_text = self.small_font.render(f"{risk:.0f}%", True, self.text_color)
        screen.blit(value_text, (bar_x + bar_width + 5, y))
    
    def _draw_strategy(self, screen, stats, y):
        """Draw strategy analysis."""
        header = self.header_font.render("🎯 STRATEGY", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        # Human strategy
        human_strategy = stats.get_strategy(True)
        strategy_icons = {
            "Aggressive": "⚔️",
            "Defensive": "🛡️",
            "Balanced": "⚖️"
        }
        icon = strategy_icons.get(human_strategy, "")
        
        human_text = self.text_font.render(f"Human: {icon} {human_strategy}", True, self.human_color)
        screen.blit(human_text, (self.x + 15, y))
        y += 20
        
        # AI strategy
        ai_strategy = stats.get_strategy(False)
        icon = strategy_icons.get(ai_strategy, "")
        
        ai_text = self.text_font.render(f"AI: {icon} {ai_strategy}", True, self.ai_color)
        screen.blit(ai_text, (self.x + 15, y))
        y += 25
        
        return y
    
    def _draw_performance(self, screen, stats, y):
        """Draw performance scores."""
        header = self.header_font.render("⭐ PERFORMANCE", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        # Human performance
        human_perf = stats.get_performance_score(True)
        self._draw_performance_bar(screen, "Human", human_perf, self.human_color, y)
        y += 30
        
        # AI performance
        ai_perf = stats.get_performance_score(False)
        self._draw_performance_bar(screen, "AI", ai_perf, self.ai_color, y)
        y += 35
        
        # Update history for graph
        if len(self.human_perf_history) == 0 or self.human_perf_history[-1] != human_perf:
            self.human_perf_history.append(human_perf)
            self.ai_perf_history.append(ai_perf)
            
            # Keep last 20 points
            if len(self.human_perf_history) > 20:
                self.human_perf_history.pop(0)
                self.ai_perf_history.pop(0)
        
        return y
    
    def _draw_performance_bar(self, screen, label, score, color, y):
        """Draw a performance score bar."""
        # Label
        label_text = self.small_font.render(f"{label}:", True, self.text_color)
        screen.blit(label_text, (self.x + 15, y))
        
        # Score bar
        bar_x = self.x + 70
        bar_y = y + 2
        bar_width = self.width - 90
        bar_height = 12
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Fill based on score
        fill_width = int((score / 100) * bar_width)
        
        # Color gradient based on score
        if score >= 75:
            fill_color = (50, 255, 50)  # Green
        elif score >= 50:
            fill_color = (255, 200, 50)  # Orange
        else:
            fill_color = (255, 100, 100)  # Red
        
        if fill_width > 0:
            pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, self.border_color, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Value
        value_text = self.small_font.render(f"{score:.0f}", True, self.text_color)
        screen.blit(value_text, (bar_x + bar_width + 5, y))
    
    def _draw_history(self, screen, stats, y):
        """Draw historical statistics."""
        header = self.header_font.render("📜 HISTORY", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        total_games = stats.history['total_games']
        human_wins = stats.history['human_wins']
        ai_wins = stats.history['ai_wins']
        
        # Total games
        total_text = self.text_font.render(f"Total Games: {total_games}", True, self.text_color)
        screen.blit(total_text, (self.x + 15, y))
        y += 20
        
        # Win rates
        human_wr = stats.get_win_rate(True)
        ai_wr = stats.get_win_rate(False)
        
        wr_text = self.text_font.render(f"Human: {human_wr:.1f}% | AI: {ai_wr:.1f}%", True, self.text_color)
        screen.blit(wr_text, (self.x + 15, y))
        y += 20
        
        # Win streaks
        human_streak = stats.history['human_stats']['current_win_streak']
        ai_streak = stats.history['ai_stats']['current_win_streak']
        
        if human_streak > 0:
            streak_text = self.text_font.render(f"🔥 Human Streak: {human_streak}", True, self.human_color)
            screen.blit(streak_text, (self.x + 15, y))
            y += 20
        elif ai_streak > 0:
            streak_text = self.text_font.render(f"🔥 AI Streak: {ai_streak}", True, self.ai_color)
            screen.blit(streak_text, (self.x + 15, y))
            y += 20
        
        # Trend
        human_trend = stats.get_recent_trend(True)
        trend_text = self.small_font.render(f"Trend: {human_trend}", True, self.text_color)
        screen.blit(trend_text, (self.x + 15, y))
        y += 25
        
        return y
    
    def _draw_performance_graph(self, screen, stats, y):
        """Draw performance graph over time."""
        if len(self.human_perf_history) < 2:
            return y
        
        header = self.header_font.render("📊 PERFORMANCE", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        # Graph area
        graph_x = self.x + 15
        graph_y = y
        graph_width = self.width - 30
        graph_height = 60
        
        # Background
        pygame.draw.rect(screen, (30, 30, 40), (graph_x, graph_y, graph_width, graph_height))
        pygame.draw.rect(screen, self.border_color, (graph_x, graph_y, graph_width, graph_height), 1)
        
        # Draw grid lines
        for i in range(5):
            grid_y = graph_y + (i * graph_height // 4)
            pygame.draw.line(screen, (50, 50, 60), 
                           (graph_x, grid_y), 
                           (graph_x + graph_width, grid_y), 1)
        
        # Draw data
        if len(self.human_perf_history) > 1:
            # Human line
            self._draw_graph_line(screen, self.human_perf_history, 
                                 graph_x, graph_y, graph_width, graph_height, 
                                 self.human_color)
            
            # AI line
            self._draw_graph_line(screen, self.ai_perf_history, 
                                 graph_x, graph_y, graph_width, graph_height, 
                                 self.ai_color)
        
        y += graph_height + 10
        return y
    
    def _draw_graph_line(self, screen, data, x, y, width, height, color):
        """Draw a line graph."""
        if len(data) < 2:
            return
        
        points = []
        for i, value in enumerate(data):
            px = x + (i / (len(data) - 1)) * width
            py = y + height - (value / 100) * height
            points.append((px, py))
        
        if len(points) > 1:
            pygame.draw.lines(screen, color, False, points, 2)
    
    def _draw_recommendations(self, screen, stats, y):
        """Draw gameplay recommendations."""
        header = self.header_font.render("💡 TIPS", True, self.highlight_color)
        screen.blit(header, (self.x + 10, y))
        y += 25
        
        recommendations = stats.get_recommendations()
        
        # Show top 3 recommendations
        for i, rec in enumerate(recommendations[:3]):
            # Wrap text if too long
            if len(rec) > 25:
                words = rec.split()
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line + word) < 25:
                        current_line += word + " "
                    else:
                        lines.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    lines.append(current_line.strip())
                
                for line in lines:
                    text = self.small_font.render(line, True, self.text_color)
                    screen.blit(text, (self.x + 15, y))
                    y += 16
            else:
                text = self.small_font.render(rec, True, self.text_color)
                screen.blit(text, (self.x + 15, y))
                y += 18
            
            y += 5
        
        return y
