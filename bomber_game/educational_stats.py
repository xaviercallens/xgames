"""
Educational Statistics Screen - Detailed RL learning statistics.
Shows educational information about reinforcement learning progress.
"""

import pygame
import json
from pathlib import Path


class EducationalStatsScreen:
    """
    Educational statistics screen showing detailed RL information.
    Activated by pressing ESC or E key during gameplay.
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 56)
        self.header_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Colors
        self.bg_color = (15, 15, 25)
        self.title_color = (255, 255, 100)
        self.header_color = (100, 200, 255)
        self.text_color = (255, 255, 255)
        self.highlight_color = (100, 255, 100)
        self.warning_color = (255, 100, 100)
        
        # Scroll
        self.scroll_offset = 0
        self.max_scroll = 0
        
    def show(self, game_stats, ai_agent, game_state):
        """Show the educational statistics screen."""
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                        return 'resume'
                    elif event.key == pygame.K_r:
                        return 'restart'
                    elif event.key == pygame.K_q:
                        return 'quit'
                    elif event.key == pygame.K_UP:
                        self.scroll_offset = max(0, self.scroll_offset - 30)
                    elif event.key == pygame.K_DOWN:
                        self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll up
                        self.scroll_offset = max(0, self.scroll_offset - 30)
                    elif event.button == 5:  # Scroll down
                        self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
            
            self._draw(game_stats, ai_agent, game_state)
            pygame.display.flip()
    
    def _draw(self, game_stats, ai_agent, game_state):
        """Draw the educational statistics screen."""
        self.screen.fill(self.bg_color)
        
        # Create scrollable surface
        content_height = 2000
        content_surface = pygame.Surface((self.width, content_height))
        content_surface.fill(self.bg_color)
        
        y = 20
        
        # Title
        title = self.title_font.render("📚 Educational Statistics", True, self.title_color)
        title_rect = title.get_rect(center=(self.width // 2, y))
        content_surface.blit(title, title_rect)
        y += 70
        
        # Subtitle
        subtitle = self.text_font.render("Reinforcement Learning Progress & Analysis", True, self.text_color)
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, y))
        content_surface.blit(subtitle, subtitle_rect)
        y += 50
        
        # Section 1: Current Game State
        y = self._draw_game_state(content_surface, y, game_state)
        y += 30
        
        # Section 2: AI Agent Information
        y = self._draw_ai_info(content_surface, y, ai_agent)
        y += 30
        
        # Section 3: Learning Progress
        y = self._draw_learning_progress(content_surface, y, game_stats)
        y += 30
        
        # Section 4: Reward Function
        y = self._draw_reward_function(content_surface, y)
        y += 30
        
        # Section 5: State Representation
        y = self._draw_state_representation(content_surface, y)
        y += 30
        
        # Section 6: Performance Metrics
        y = self._draw_performance_metrics(content_surface, y, game_stats)
        y += 30
        
        # Section 7: Educational Insights
        y = self._draw_educational_insights(content_surface, y, game_stats)
        
        # Calculate max scroll
        self.max_scroll = max(0, y - self.height + 100)
        
        # Blit scrollable content
        self.screen.blit(content_surface, (0, -self.scroll_offset))
        
        # Draw fixed bottom bar
        self._draw_bottom_bar()
    
    def _draw_game_state(self, surface, y, game_state):
        """Draw current game state information."""
        header = self.header_font.render("🎮 Current Game State", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        # Count entities
        alive_players = sum(1 for p in game_state.players if p.alive)
        active_bombs = len(game_state.bombs)
        active_explosions = len(game_state.explosions)
        powerups = len(game_state.powerups)
        
        info = [
            f"Alive Players: {alive_players}/{len(game_state.players)}",
            f"Active Bombs: {active_bombs}",
            f"Active Explosions: {active_explosions}",
            f"Available Power-ups: {powerups}",
            f"Game Over: {'Yes' if game_state.game_over else 'No'}",
        ]
        
        for line in info:
            text = self.text_font.render(line, True, self.text_color)
            surface.blit(text, (70, y))
            y += 30
        
        return y
    
    def _draw_ai_info(self, surface, y, ai_agent):
        """Draw AI agent information."""
        header = self.header_font.render("🤖 AI Agent Information", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        agent_type = type(ai_agent).__name__
        
        info = [
            f"Agent Type: {agent_type}",
            f"Algorithm: {self._get_algorithm_name(agent_type)}",
        ]
        
        # Add agent-specific stats
        if hasattr(ai_agent, 'total_games'):
            info.append(f"Games Played: {ai_agent.total_games}")
        if hasattr(ai_agent, 'get_win_rate'):
            wr = ai_agent.get_win_rate() * 100
            info.append(f"Win Rate: {wr:.1f}%")
        if hasattr(ai_agent, 'get_average_reward'):
            avg_reward = ai_agent.get_average_reward()
            info.append(f"Average Reward: {avg_reward:.2f}")
        
        for line in info:
            text = self.text_font.render(line, True, self.text_color)
            surface.blit(text, (70, y))
            y += 30
        
        return y
    
    def _draw_learning_progress(self, surface, y, game_stats):
        """Draw learning progress information."""
        header = self.header_font.render("📈 Learning Progress", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        total_games = game_stats.history['total_games']
        human_wins = game_stats.history['human_wins']
        ai_wins = game_stats.history['ai_wins']
        
        human_wr = (human_wins / total_games * 100) if total_games > 0 else 0
        ai_wr = (ai_wins / total_games * 100) if total_games > 0 else 0
        
        info = [
            f"Total Training Games: {total_games}",
            f"Human Wins: {human_wins} ({human_wr:.1f}%)",
            f"AI Wins: {ai_wins} ({ai_wr:.1f}%)",
            f"Current Streak: {game_stats.history['human_stats']['current_win_streak']} (Human)",
            f"Best Streak: {game_stats.history['human_stats']['best_win_streak']} (Human)",
        ]
        
        for line in info:
            text = self.text_font.render(line, True, self.text_color)
            surface.blit(text, (70, y))
            y += 30
        
        # Learning stage
        y += 10
        stage_text = self.text_font.render("Learning Stage:", True, self.highlight_color)
        surface.blit(stage_text, (70, y))
        y += 30
        
        stage = self._determine_learning_stage(ai_wr)
        stage_desc = self.small_font.render(stage, True, self.text_color)
        surface.blit(stage_desc, (90, y))
        y += 25
        
        return y
    
    def _draw_reward_function(self, surface, y):
        """Draw reward function explanation."""
        header = self.header_font.render("🎁 Reward Function (Based on Paper)", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        desc = self.small_font.render("Event-based rewards from research paper:", True, self.text_color)
        surface.blit(desc, (70, y))
        y += 30
        
        rewards = [
            ("Valid Move", "-1", "Encourages active movement"),
            ("Invalid Move", "-5", "Penalty for illegal actions"),
            ("Kill Player", "+500", "Main objective reward"),
            ("Die", "-300", "Strong penalty for losing"),
            ("Break Wall", "+30", "Encourages exploration"),
        ]
        
        for event, reward, reason in rewards:
            # Event
            event_text = self.text_font.render(f"• {event}:", True, self.text_color)
            surface.blit(event_text, (90, y))
            
            # Reward
            color = self.highlight_color if reward.startswith('+') else self.warning_color
            reward_text = self.text_font.render(reward, True, color)
            surface.blit(reward_text, (300, y))
            
            # Reason
            reason_text = self.small_font.render(f"({reason})", True, (180, 180, 180))
            surface.blit(reason_text, (400, y))
            
            y += 28
        
        y += 10
        note = self.small_font.render("Discount Factor γ = 0.99 (values future rewards highly)", True, (200, 200, 100))
        surface.blit(note, (90, y))
        y += 25
        
        return y
    
    def _draw_state_representation(self, surface, y):
        """Draw state representation explanation."""
        header = self.header_font.render("🗺️ State Representation", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        desc = self.small_font.render("Two approaches from research paper:", True, self.text_color)
        surface.blit(desc, (70, y))
        y += 30
        
        # Complete Information
        approach1 = self.text_font.render("1. Complete Information (Full State)", True, self.highlight_color)
        surface.blit(approach1, (90, y))
        y += 30
        
        complete_info = [
            "• All tile types (free, breakable, unbreakable)",
            "• All player positions",
            "• All bomb countdowns and explosion predictions",
            "• State space: ~4.9 × 10⁴⁹ states",
            "• Requires Deep Q-Network (DQN)",
        ]
        
        for line in complete_info:
            text = self.small_font.render(line, True, self.text_color)
            surface.blit(text, (110, y))
            y += 25
        
        y += 10
        
        # 5-Tiles Information
        approach2 = self.text_font.render("2. 5-Tiles Information (Limited Vision)", True, self.highlight_color)
        surface.blit(approach2, (90, y))
        y += 30
        
        tiles_info = [
            "• Only adjacent tiles (North, East, South, West, Current)",
            "• Nearest opponent position (Manhattan distance)",
            "• Explosion countdowns for visible tiles",
            "• State space: ~10⁹ states (much smaller!)",
            "• Works with Q-Learning, Sarsa, Double Q-Learning",
            "• Best results: Sarsa with 5-tiles (from paper)",
        ]
        
        for line in tiles_info:
            text = self.small_font.render(line, True, self.text_color)
            surface.blit(text, (110, y))
            y += 25
        
        return y
    
    def _draw_performance_metrics(self, surface, y, game_stats):
        """Draw performance metrics."""
        header = self.header_font.render("📊 Performance Metrics", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        # Current game performance
        human_perf = game_stats.get_performance_score(True)
        ai_perf = game_stats.get_performance_score(False)
        
        human_risk = game_stats.get_current_risk(True)
        ai_risk = game_stats.get_current_risk(False)
        
        metrics = [
            ("Human Performance", f"{human_perf:.0f}/100", human_perf >= 70),
            ("AI Performance", f"{ai_perf:.0f}/100", ai_perf >= 70),
            ("Human Risk Level", f"{human_risk:.0f}%", human_risk < 50),
            ("AI Risk Level", f"{ai_risk:.0f}%", ai_risk < 50),
        ]
        
        for label, value, is_good in metrics:
            label_text = self.text_font.render(f"{label}:", True, self.text_color)
            surface.blit(label_text, (90, y))
            
            color = self.highlight_color if is_good else self.warning_color
            value_text = self.text_font.render(value, True, color)
            surface.blit(value_text, (400, y))
            
            y += 30
        
        return y
    
    def _draw_educational_insights(self, surface, y, game_stats):
        """Draw educational insights."""
        header = self.header_font.render("💡 Educational Insights", True, self.header_color)
        surface.blit(header, (50, y))
        y += 45
        
        insights = [
            "Key Findings from Research Paper:",
            "",
            "✓ Sarsa with 5-tiles information achieved best results",
            "✓ Complete information requires Deep Q-Network (DQN)",
            "✓ Simple Q-Learning works but struggles with large state space",
            "✓ Double Q-Learning reduces maximization bias",
            "✓ Reward engineering is critical for learning success",
            "✓ Discount factor γ=0.99 works best for Bomberman",
            "",
            "Learning Process:",
            "• Early: Agent learns valid moves and wall breaking",
            "• Middle: Agent learns to avoid bombs and chase opponents",
            "• Advanced: Agent develops strategic bomb placement",
            "• Expert: Agent masters timing and positioning",
            "",
            "Training Recommendations:",
            "• Start with 10,000 episodes per generation",
            "• Evaluate every 100 episodes",
            "• Use ε-greedy exploration (ε=0.1 to 0.01)",
            "• Monitor win rate and average reward",
        ]
        
        for line in insights:
            if line.startswith("✓"):
                text = self.small_font.render(line, True, self.highlight_color)
            elif line.startswith("•"):
                text = self.small_font.render(line, True, (200, 200, 200))
            elif line == "":
                y += 10
                continue
            elif line.endswith(":"):
                text = self.text_font.render(line, True, self.header_color)
            else:
                text = self.small_font.render(line, True, self.text_color)
            
            surface.blit(text, (70, y))
            y += 25
        
        return y
    
    def _draw_bottom_bar(self):
        """Draw fixed bottom instruction bar."""
        bar_rect = pygame.Rect(0, self.height - 60, self.width, 60)
        pygame.draw.rect(self.screen, (30, 30, 50), bar_rect)
        pygame.draw.line(self.screen, self.header_color, (0, self.height - 60), (self.width, self.height - 60), 2)
        
        instructions = "ESC/E: Resume Game  |  R: Restart  |  Q: Quit  |  ↑↓: Scroll"
        text = self.text_font.render(instructions, True, self.text_color)
        text_rect = text.get_rect(center=(self.width // 2, self.height - 30))
        self.screen.blit(text, text_rect)
    
    def _get_algorithm_name(self, agent_type):
        """Get algorithm name from agent type."""
        if 'PPO' in agent_type:
            return "Proximal Policy Optimization (PPO)"
        elif 'Heuristic' in agent_type:
            return "Rule-Based Heuristic (A* Pathfinding)"
        elif 'Simple' in agent_type:
            return "Random/Simple Agent"
        else:
            return "Unknown"
    
    def _determine_learning_stage(self, win_rate):
        """Determine learning stage based on win rate."""
        if win_rate < 10:
            return "🌱 Early Learning - Agent is learning basic moves"
        elif win_rate < 25:
            return "📚 Intermediate - Agent understands game mechanics"
        elif win_rate < 40:
            return "🎯 Advanced - Agent developing strategies"
        elif win_rate < 60:
            return "💪 Expert - Agent plays competitively"
        else:
            return "🏆 Master - Agent has mastered the game"
