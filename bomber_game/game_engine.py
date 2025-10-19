"""
Main game engine for Bomberman.
"""

import pygame
import sys
import os
import time
from datetime import datetime
from pathlib import Path
from . import (GRID_SIZE, TILE_SIZE, FPS, SCREEN_WIDTH, SCREEN_HEIGHT,
               BLACK, WHITE, GRAY, DARK_GRAY, GREEN, RED, BROWN)
from .game_state import GameState
from .agents import PPOAgent, HybridAgent
from .assets import get_asset_manager
from .menu import MenuScreen
from .model_selector import ModelSelector
from .player_selector import PlayerSelector
from .heuristics import HeuristicAgent
from .heuristics_improved import ImprovedHeuristicAgent
from .heuristics_intermediate import IntermediateSmartHeuristic
from .heuristics_advanced import AdvancedSmartHeuristic
from .game_statistics import GameStatistics
from .stats_panel import StatsPanel
from .educational_stats import EducationalStatsScreen
from .video_recorder import VideoRecorder
from .enhanced_graphics import ProutManGraphics


class BombermanGame:
    """Main game class that handles the game loop and rendering."""
    
    def __init__(self, show_splash=True):
        """Initialize the game."""
        pygame.init()
        
        # Screen setup with stats panel
        self.stats_panel_width = 300
        self.game_width = SCREEN_WIDTH
        self.total_width = SCREEN_WIDTH + self.stats_panel_width
        self.screen = pygame.display.set_mode((self.total_width, SCREEN_HEIGHT))
        pygame.display.set_caption("💨 PROUTMAN - L'aventure Codée! 💩")
        self.clock = pygame.time.Clock()
        
        # Statistics tracking
        self.stats = GameStatistics()
        self.stats_panel = StatsPanel(SCREEN_WIDTH, 0, self.stats_panel_width, SCREEN_HEIGHT)
        self.educational_stats = EducationalStatsScreen(self.screen)
        
        # Font
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Menu system
        self.menu = MenuScreen(self.screen)
        self.show_splash = show_splash
        
        # Video recording
        self.video_recorder = VideoRecorder(output_dir="recordings", fps=FPS)
        self.show_recording_hint = True  # Show hint on first run
        
        # Game state
        self.game_state = GameState(GRID_SIZE)
        
        # Create players
        self.human_player = self.game_state.add_player(1, 1, GREEN, "Player")
        self.ai_player = self.game_state.add_player(
            GRID_SIZE - 2, GRID_SIZE - 2, RED, "AI"
        )
        
        # Initialize AI agent (will be set in run() if splash is shown)
        self.ai_agent = None
        self.ai_type = "Improved Heuristic"
        
        # Load AI training stats
        self.ai_stats = self._load_ai_stats()
        
        # Only auto-select model if not showing splash (splash will handle selection)
        if not show_splash:
            models_dir = os.path.join(os.path.dirname(__file__), "models")
            selector = ModelSelector(models_dir)
            
            # Check if user wants hybrid mode (can be set via environment variable)
            use_hybrid = os.environ.get('BOMBERMAN_HYBRID_MODE', '').lower() in ['true', '1', 'yes']
            hybrid_mode = os.environ.get('BOMBERMAN_HYBRID_STRATEGY', 'balanced')
            
            # Select best model based on performance
            if use_hybrid:
                selection = selector.select_hybrid_mode(mode=hybrid_mode)
            else:
                selection = selector.select_best_model()
            
            # Create AI agent based on selection
            self._create_ai_agent(selection)
        
        # Game state
        self.running = True
        self.paused = False
        
        # Load assets
        self.assets = get_asset_manager()
        self.wall_sprite = None
        self._load_sprites()
    
    def _create_ai_agent(self, selection):
        """
        Create AI agent based on selection.
        
        Args:
            selection: Selection dictionary from model selector
        """
        if selection['model_path'] == 'heuristic':
            print(f"🌱 Using Improved Heuristic Agent")
            print(f"   Reason: {selection['reason']}")
            print(f"   Expected Win Rate: ~{selection['win_rate']:.1f}%")
            print(f"🧠 Using IMPROVED Heuristic Agent (Industry Best Practices)")
            print(f"   • A* pathfinding algorithm")
            print(f"   • Weighted evaluation function")
            print(f"   • Danger zone prediction")
            print(f"   • Strategic bomb placement")
            print(f"   • Performance tracking (Win Rate & Rewards)")
            print(f"\n💡 Train AI to beat heuristic: ./train.sh")
            self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
            self.ai_type = "Improved Heuristic"
            
        elif selection['model_type'] == 'ppo_pretrained':
            print(f"🎯 Using Pretrained PPO Model")
            print(f"   Reason: {selection['reason']}")
            print(f"   Expected Win Rate: ~{selection['win_rate']:.1f}%")
            self.ai_agent = PPOAgent(self.ai_player, model_path=selection['model_path'], training=False)
            self.ai_type = "PPO (Pretrained)"
            
        elif selection['model_type'] == 'ppo':
            print(f"🏆 Using Trained PPO Model")
            print(f"   Reason: {selection['reason']}")
            print(f"   Win Rate: {selection['win_rate']:.1f}%")
            self.ai_agent = PPOAgent(self.ai_player, model_path=selection['model_path'], training=False)
            self.ai_type = "PPO"
        
        elif selection['model_type'] == 'hybrid':
            print(f"🎭 Using Hybrid Agent (Heuristics + RL)")
            print(f"   Mode: {selection['mode']}")
            print(f"   Estimated Win Rate: ~{selection['win_rate']:.1f}%")
            self.ai_agent = HybridAgent(
                self.ai_player,
                mode=selection['mode'],
                ppo_model_path=selection.get('model_path')
            )
            self.ai_type = f"Hybrid ({selection['mode']})"
        
        else:
            # Fallback to heuristic agent
            print(f"🌱 Using Heuristic Agent (Fallback)")
            self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
            self.ai_type = "Heuristic"
        
        # Set AI info in statistics
        self.stats.set_ai_info(self.ai_type, selection.get('model_path'))
    
    def _load_sprites(self):
        """Load game sprites."""
        try:
            self.wall_sprite = self.assets.get_wall_sprite((TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Could not load wall sprite: {e}")
            self.wall_sprite = None
    
    def _load_ai_stats(self):
        """Load AI training statistics."""
        import json
        stats_file = os.path.join(os.path.dirname(__file__), "models", "training_stats.json")
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                    # Calculate win rate
                    total_episodes = data.get('total_episodes', 0)
                    total_wins = data.get('total_wins', 0)
                    win_rate = (total_wins / total_episodes * 100) if total_episodes > 0 else 0
                    data['win_rate'] = win_rate
                    return data
            except Exception as e:
                print(f"Could not load AI stats: {e}")
        return None
    
    def _format_time(self, seconds):
        """Format seconds to readable time."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{int(seconds)}s"
        
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Show educational statistics screen
                    action = self.educational_stats.show(self.stats, self.ai_agent, self.game_state)
                    if action == 'quit':
                        self.running = False
                    elif action == 'restart':
                        self._restart_game()
                    # else: resume game
                elif event.key == pygame.K_e:
                    # Also show educational stats with E key
                    action = self.educational_stats.show(self.stats, self.ai_agent, self.game_state)
                    if action == 'quit':
                        self.running = False
                    elif action == 'restart':
                        self._restart_game()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    if self.game_state.game_over:
                        self._restart_game()
                    else:
                        # Toggle recording when game is active
                        session_name = f"game_{self.stats.history['total_games'] + 1}"
                        is_recording = self.video_recorder.toggle_recording(session_name)
                        if is_recording:
                            self.show_recording_hint = False
                elif event.key == pygame.K_SPACE:
                    if self.human_player.alive:
                        self.game_state.place_bomb(self.human_player)
                        self.stats.record_bomb(True)
                elif event.key == pygame.K_c:
                    if self.human_player.alive:
                        self.game_state.place_caca(self.human_player)
                elif event.key == pygame.K_s:
                    # Save recording with game statistics
                    if self.video_recorder.is_recording:
                        game_stats = self._collect_game_statistics()
                        self.video_recorder.stop_recording(game_stats)
                    else:
                        # Just save statistics without recording
                        self._save_game_statistics_only()
    
    def update(self, dt):
        """Update game state."""
        if self.paused or self.game_state.game_over:
            return
        
        # Handle human player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        
        if self.human_player.alive:
            old_pos = (self.human_player.grid_x, self.human_player.grid_y)
            self.human_player.move(dx, dy, self.game_state.grid, TILE_SIZE, self.game_state)
            new_pos = (self.human_player.grid_x, self.human_player.grid_y)
            
            # Track movement
            if old_pos != new_pos:
                self.stats.record_move(True, new_pos, self.game_state)
            
            self.human_player.update(dt)  # Update animation
        
        # Update AI
        if self.ai_player.alive:
            old_pos = (self.ai_player.grid_x, self.ai_player.grid_y)
            action = self.ai_agent.update(dt, self.game_state)
            if action:
                ai_dx, ai_dy, place_bomb = action
                self.ai_player.move(ai_dx, ai_dy, self.game_state.grid, TILE_SIZE, self.game_state)
                new_pos = (self.ai_player.grid_x, self.ai_player.grid_y)
                
                # Track movement
                if old_pos != new_pos:
                    self.stats.record_move(False, new_pos, self.game_state)
                
                if place_bomb:
                    self.game_state.place_bomb(self.ai_player)
                    self.stats.record_bomb(False)
            self.ai_player.update(dt)  # Update animation
        
        # Update game state
        self.game_state.update(dt)
    
    def render(self):
        """Render the game."""
        self.screen.fill(BLACK)
        
        # Capture frame if recording
        if self.video_recorder.is_recording:
            self.video_recorder.capture_frame(self.screen)
        
        # Draw grid
        self._draw_grid()
        
        # Draw teleport doors
        if self.game_state.teleport_doors:
            self.game_state.teleport_doors.draw(self.screen, TILE_SIZE)
        
        # Draw bomb machine
        if self.game_state.bomb_machine:
            self.game_state.bomb_machine.draw(self.screen, TILE_SIZE)
        
        # Draw power-ups
        for powerup in self.game_state.powerups.values():
            powerup.render(self.screen, TILE_SIZE)
        
        # Draw cacas (poop blocks)
        for caca in self.game_state.cacas:
            caca.render(self.screen, TILE_SIZE)
        
        # Draw bombs
        for bomb in self.game_state.bombs:
            bomb.render(self.screen, TILE_SIZE)
        
        # Draw explosions
        for explosion in self.game_state.explosions:
            explosion.render(self.screen, TILE_SIZE)
        
        # Draw players
        for player in self.game_state.players:
            if player.alive:
                player.render(self.screen, TILE_SIZE)
        
        # Draw UI
        self._draw_ui()
        
        # Draw statistics panel
        self.stats_panel.draw(self.screen, self.stats, self.game_state)
        
        # Draw game over screen
        if self.game_state.game_over:
            self._draw_game_over()
        
        pygame.display.flip()
    
    def _draw_grid(self):
        """Draw the game grid."""
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE
                
                tile = self.game_state.grid[y][x]
                
                # Draw tile background with alternating pattern
                if (x + y) % 2 == 0:
                    color = (34, 139, 34)  # Forest green
                else:
                    color = (50, 205, 50)  # Lime green
                
                pygame.draw.rect(self.screen, color,
                               (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                
                # Draw walls using enhanced graphics
                if tile == 1:  # Indestructible wall
                    if self.wall_sprite:
                        self.screen.blit(self.wall_sprite, (pixel_x, pixel_y))
                    else:
                        ProutManGraphics.draw_enhanced_wall(
                            self.screen, pixel_x, pixel_y, TILE_SIZE, wall_type=1
                        )
                elif tile == 2:  # Soft wall (destructible)
                    ProutManGraphics.draw_enhanced_wall(
                        self.screen, pixel_x, pixel_y, TILE_SIZE, wall_type=2
                    )
    
    def _draw_ui(self):
        """Draw user interface."""
        ui_y = GRID_SIZE * TILE_SIZE + 5
        
        # Player stats
        if self.human_player.alive:
            player_text = f"Player: Trumps:{self.human_player.max_bombs} Cacas:{self.human_player.max_cacas} Range:{self.human_player.bomb_range}"
            text_surf = self.font.render(player_text, True, GREEN)
            self.screen.blit(text_surf, (10, ui_y))
        else:
            text_surf = self.font.render("Player: DEAD", True, RED)
            self.screen.blit(text_surf, (10, ui_y))
        
        # AI stats with training info
        if self.ai_player.alive:
            ai_text = f"AI ({self.ai_type}): Bombs:{self.ai_player.max_bombs} Range:{self.ai_player.bomb_range}"
            text_surf = self.font.render(ai_text, True, RED)
            self.screen.blit(text_surf, (10, ui_y + 25))
            
            # AI training level
            if self.ai_stats:
                level = self.ai_stats.get('current_level', 'Unknown')
                training_time = self._format_time(self.ai_stats.get('total_training_time', 0))
                win_rate = self.ai_stats.get('win_rate', 0)
                
                # Level colors
                level_colors = {
                    'Beginner': (100, 150, 255),
                    'Novice': (100, 255, 100),
                    'Intermediate': (255, 255, 100),
                    'Advanced': (255, 150, 50),
                    'Expert': (255, 50, 50),
                    'Master': (200, 100, 255),
                }
                level_color = level_colors.get(level, WHITE)
                
                level_text = f"Level: {level} | Training: {training_time} | Win Rate: {win_rate:.0f}%"
                text_surf = self.font.render(level_text, True, level_color)
                self.screen.blit(text_surf, (10, ui_y + 50))
        else:
            text_surf = self.font.render("AI: DEAD", True, GRAY)
            self.screen.blit(text_surf, (10, ui_y + 25))
        
        # Controls
        controls = "Controls: WASD=Move, Space=Trump💨, C=Caca💩, P=Pause, R=Record, S=Save Stats"
        text_surf = self.font.render(controls, True, WHITE)
        text_rect = text_surf.get_rect(right=SCREEN_WIDTH - 10, top=ui_y)
        self.screen.blit(text_surf, text_rect)
        
        # Recording status
        if self.video_recorder.is_recording:
            rec_text = self.video_recorder.get_status_text()
            rec_surf = self.font.render(rec_text, True, RED)
            rec_rect = rec_surf.get_rect(right=SCREEN_WIDTH - 10, top=ui_y + 25)
            self.screen.blit(rec_surf, rec_rect)
        elif self.show_recording_hint and not self.game_state.game_over:
            hint_text = "💡 Press R to record gameplay!"
            hint_surf = self.font.render(hint_text, True, (255, 255, 100))
            hint_rect = hint_surf.get_rect(right=SCREEN_WIDTH - 10, top=ui_y + 25)
            self.screen.blit(hint_surf, hint_rect)
    
    def _draw_game_over(self):
        """Draw game over screen with AI statistics."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        if self.game_state.winner:
            text = f"{self.game_state.winner.name} Wins!"
            color = self.game_state.winner.color
            
            # Track AI performance
            if hasattr(self.ai_agent, 'record_game_result'):
                ai_won = (self.game_state.winner == self.ai_player)
                reward = 100.0 if ai_won else -50.0
                self.ai_agent.record_game_result(ai_won, reward)
                
                # Print stats to console
                print(self.ai_agent.get_stats_string())
            
            # Save game statistics
            self.stats.finish_game(self.game_state.winner.name if self.game_state.winner else None)
        else:
            text = "Draw!"
            color = WHITE
            if hasattr(self.ai_agent, 'record_game_result'):
                self.ai_agent.record_game_result(False, 0.0)
        
        text_surf = self.big_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(text_surf, text_rect)
        
        # Show AI stats if available
        if hasattr(self.ai_agent, 'get_win_rate'):
            win_rate = self.ai_agent.get_win_rate() * 100
            avg_reward = self.ai_agent.get_average_reward()
            games = self.ai_agent.total_games
            
            stats_y = SCREEN_HEIGHT // 2 - 20
            stats_font = pygame.font.Font(None, 20)
            
            stats_lines = [
                f"AI Performance:",
                f"Win Rate: {win_rate:.1f}%",
                f"Avg Reward: {avg_reward:.1f}",
                f"Games: {games}"
            ]
            
            for i, line in enumerate(stats_lines):
                stats_surf = stats_font.render(line, True, WHITE)
                stats_rect = stats_surf.get_rect(center=(SCREEN_WIDTH // 2, stats_y + i * 25))
                self.screen.blit(stats_surf, stats_rect)
        
        # Restart text
        restart_surf = self.font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_surf, restart_rect)
    
    def _collect_game_statistics(self) -> dict:
        """Collect comprehensive game statistics for saving."""
        # Get AI info
        ai_info = {
            'type': self.ai_type,
            'model_path': getattr(self, 'ai_model_path', 'N/A'),
            'skill_level': 'Unknown'
        }
        
        # Try to get AI skill level from stats
        if self.ai_stats:
            ai_info['skill_level'] = self.ai_stats.get('current_level', 'Unknown')
        
        # Get game result
        game_result = {
            'winner': self.game_state.winner.name if self.game_state.winner else 'In Progress',
            'duration': time.time() - self.stats.game_start_time,
            'turns': self.game_state.turn_count if hasattr(self.game_state, 'turn_count') else 0
        }
        
        # Get performance statistics from history
        performance = {
            'total_games': self.stats.history['total_games'],
            'human_wins': self.stats.history['human_wins'],
            'ai_wins': self.stats.history['ai_wins'],
            'draws': self.stats.history['draws'],
            'human_win_rate': self.stats.get_win_rate(True),
            'ai_win_rate': self.stats.get_win_rate(False),
            'human_current_streak': self.stats.history['human_stats']['current_win_streak'],
            'human_best_streak': self.stats.history['human_stats']['best_win_streak'],
            'ai_current_streak': self.stats.history['ai_stats']['current_win_streak'],
            'ai_best_streak': self.stats.history['ai_stats']['best_win_streak']
        }
        
        # Get current game stats
        current_game = {
            'human': {
                'moves': self.stats.human_moves,
                'bombs': self.stats.human_bombs_placed,
                'walls': self.stats.walls_destroyed_human,
                'powerups': self.stats.powerups_collected_human,
                'near_death': self.stats.human_near_death,
                'strategy': self.stats.get_strategy(True),
                'avg_risk': self.stats.get_current_risk(True),
                'performance': self.stats.get_performance_score(True)
            },
            'ai': {
                'moves': self.stats.ai_moves,
                'bombs': self.stats.ai_bombs_placed,
                'walls': self.stats.walls_destroyed_ai,
                'powerups': self.stats.powerups_collected_ai,
                'near_death': self.stats.ai_near_death,
                'strategy': self.stats.get_strategy(False),
                'avg_risk': self.stats.get_current_risk(False),
                'performance': self.stats.get_performance_score(False)
            }
        }
        
        # Get recommendations
        recommendations = self.stats.get_recommendations()
        
        return {
            'ai_info': ai_info,
            'game_result': game_result,
            'performance': performance,
            'current_game': current_game,
            'recommendations': recommendations
        }
    
    def _save_game_statistics_only(self):
        """Save game statistics to a text file without recording."""
        # Create stats directory
        stats_dir = Path("game_stats")
        stats_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_file = stats_dir / f"game_stats_{timestamp}.txt"
        
        # Collect statistics
        game_stats = self._collect_game_statistics()
        
        # Write to file
        with open(stats_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("PROUTMAN GAMEPLAY STATISTICS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # AI Information
            ai_info = game_stats['ai_info']
            f.write("🤖 AI OPPONENT INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"AI Type:         {ai_info['type']}\n")
            f.write(f"Model Path:      {ai_info['model_path']}\n")
            f.write(f"Skill Level:     {ai_info['skill_level']}\n\n")
            
            # Game Results
            result = game_stats['game_result']
            f.write("🏆 GAME RESULT\n")
            f.write("-" * 80 + "\n")
            f.write(f"Winner:          {result['winner']}\n")
            f.write(f"Game Duration:   {result['duration']:.2f} seconds\n")
            f.write(f"Total Turns:     {result['turns']}\n\n")
            
            # Performance Statistics
            perf = game_stats['performance']
            f.write("📊 PERFORMANCE STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Games:     {perf['total_games']}\n")
            f.write(f"Human Wins:      {perf['human_wins']}\n")
            f.write(f"AI Wins:         {perf['ai_wins']}\n")
            f.write(f"Draws:           {perf['draws']}\n")
            f.write(f"Human Win Rate:  {perf['human_win_rate']:.1f}%\n")
            f.write(f"AI Win Rate:     {perf['ai_win_rate']:.1f}%\n\n")
            
            # Win streaks
            f.write("🔥 WIN STREAKS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Human Current:   {perf['human_current_streak']}\n")
            f.write(f"Human Best:      {perf['human_best_streak']}\n")
            f.write(f"AI Current:      {perf['ai_current_streak']}\n")
            f.write(f"AI Best:         {perf['ai_best_streak']}\n\n")
            
            # Current Game Stats
            current = game_stats['current_game']
            f.write("🎮 CURRENT GAME STATISTICS\n")
            f.write("-" * 80 + "\n")
            
            human = current['human']
            f.write("\nPlayer (Human):\n")
            f.write(f"  Moves:         {human['moves']}\n")
            f.write(f"  Bombs Placed:  {human['bombs']}\n")
            f.write(f"  Walls Broken:  {human['walls']}\n")
            f.write(f"  Powerups:      {human['powerups']}\n")
            f.write(f"  Near Deaths:   {human['near_death']}\n")
            f.write(f"  Strategy:      {human['strategy']}\n")
            f.write(f"  Avg Risk:      {human['avg_risk']:.1f}\n")
            f.write(f"  Performance:   {human['performance']:.1f}/100\n")
            
            ai = current['ai']
            f.write("\nAI Opponent:\n")
            f.write(f"  Moves:         {ai['moves']}\n")
            f.write(f"  Bombs Placed:  {ai['bombs']}\n")
            f.write(f"  Walls Broken:  {ai['walls']}\n")
            f.write(f"  Powerups:      {ai['powerups']}\n")
            f.write(f"  Near Deaths:   {ai['near_death']}\n")
            f.write(f"  Strategy:      {ai['strategy']}\n")
            f.write(f"  Avg Risk:      {ai['avg_risk']:.1f}\n")
            f.write(f"  Performance:   {ai['performance']:.1f}/100\n\n")
            
            # Recommendations
            f.write("💡 RECOMMENDATIONS\n")
            f.write("-" * 80 + "\n")
            for i, rec in enumerate(game_stats['recommendations'], 1):
                f.write(f"{i}. {rec}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("Generated by Proutman\n")
            f.write("=" * 80 + "\n")
        
        print(f"\n📊 Game statistics saved!")
        print(f"   📁 Location: {stats_file}")
        print(f"   💾 File: {stats_file.name}")
    
    def _restart_game(self):
        """Restart the game."""
        # Save previous game stats if game was finished
        if self.game_state.game_over and self.game_state.winner:
            self.stats.finish_game(self.game_state.winner.name)
        
        # Reset game state
        self.game_state = GameState(GRID_SIZE)
        self.human_player = self.game_state.add_player(1, 1, GREEN, "Player")
        self.ai_player = self.game_state.add_player(
            GRID_SIZE - 2, GRID_SIZE - 2, RED, "AI"
        )
        
        # Reload AI with same type
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        selector = ModelSelector(models_dir)
        selection = selector.select_best_model()
        
        if selection['model_type'] == 'ppo':
            self.ai_agent = PPOAgent(self.ai_player, model_path=selection['model_path'], training=False)
        elif selection['model_type'] == 'ppo_pretrained':
            self.ai_agent = PPOAgent(self.ai_player, model_path=selection['model_path'], training=False)
        elif selection['model_type'] == 'heuristic':
            self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
        else:
            self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
        
        # Reset statistics for new game
        self.stats = GameStatistics()
        self.stats.set_ai_info(self.ai_type, selection.get('model_path'))
        self.stats_panel.human_perf_history = []
        self.stats_panel.ai_perf_history = []
        
        self._load_sprites()  # Reload sprites
    
    def run(self):
        """Main game loop."""
        # Show splash screen
        if self.show_splash:
            quit_requested = self.menu.show_splash(duration=3.0)
            if quit_requested:
                pygame.quit()
                sys.exit()
            
            # Show AI selection menu
            selected_ai = self.menu.show_ai_selection()
            if selected_ai is None:
                pygame.quit()
                sys.exit()
            
            # Create AI agent based on selection
            print(f"\n{'='*70}")
            print(f"🎮 SELECTED OPPONENT: {selected_ai['icon']} {selected_ai['name']}")
            print(f"{'='*70}")
            print(f"   Level: {selected_ai['level']}")
            print(f"   Type: {selected_ai['type']}")
            print(f"   Expected Win Rate: {selected_ai['win_rate']:.1f}%")
            print(f"   Description: {selected_ai['description']}")
            print(f"{'='*70}\n")
            
            # Initialize AI agent based on selection
            if selected_ai['type'] == 'simple':
                self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
                self.ai_type = "Heuristic"
            elif selected_ai['type'] == 'heuristic':
                self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
                self.ai_type = "Improved Heuristic"
            elif selected_ai['type'] == 'advanced_heuristic':
                self.ai_agent = AdvancedSmartHeuristic(self.ai_player)
                self.ai_type = "Advanced Smart Heuristic"
                print(f"\n🧠 Advanced Smart Heuristic AI Initialized!")
                print(f"   Features:")
                print(f"   • Predictive bomb placement analysis")
                print(f"   • Game tree evaluation (minimax)")
                print(f"   • Strategic positioning")
                print(f"   • Opponent behavior prediction")
                print(f"   • Dynamic strategy selection (4 strategies)")
                print(f"   Expected Win Rate: {selected_ai['win_rate']:.0f}%")
            elif selected_ai['type'] == 'hybrid':
                model_path = selected_ai.get('model_path')
                hybrid_mode = selected_ai.get('hybrid_mode', 'adaptive')
                self.ai_agent = HybridAgent(self.ai_player, mode=hybrid_mode, ppo_model_path=model_path)
                self.ai_type = f"Hybrid ({hybrid_mode})"
                print(f"\n🎭 Hybrid AI Initialized!")
                print(f"   Mode: {hybrid_mode}")
                print(f"   Estimated Win Rate: {selected_ai['win_rate']:.0f}%")
            elif selected_ai['type'] == 'ppo':
                model_path = selected_ai.get('model_path')
                self.ai_agent = PPOAgent(self.ai_player, model_path=model_path, training=False)
                self.ai_type = "PPO"
            elif selected_ai['type'] == 'ppo_best':
                model_path = selected_ai.get('model_path')
                self.ai_agent = PPOAgent(self.ai_player, model_path=model_path, training=False)
                self.ai_type = "PPO (Best)"
            
            # Update statistics with selected AI
            self.stats.set_ai_info(self.ai_type, selected_ai.get('model_path'))
        
        # If AI agent not initialized yet, use default
        if self.ai_agent is None:
            self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
            self.ai_type = "Improved Heuristic"
            self.stats.set_ai_info(self.ai_type, None)
        
        # Main game loop
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game."""
    game = BombermanGame()
    game.run()


if __name__ == "__main__":
    main()
