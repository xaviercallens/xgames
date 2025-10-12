"""
Main game engine for Bomberman.
"""

import pygame
import sys
from . import (GRID_SIZE, TILE_SIZE, FPS, SCREEN_WIDTH, SCREEN_HEIGHT,
               BLACK, WHITE, GRAY, DARK_GRAY, GREEN, RED, BROWN)
from .game_state import GameState
from .agents import SimpleAgent, RLAgent, PPOAgent
from .assets import get_asset_manager
from .menu import MenuScreen
from .model_selector import ModelSelector
from .heuristics import HeuristicAgent
from .heuristics_improved import ImprovedHeuristicAgent
from .game_statistics import GameStatistics
from .stats_panel import StatsPanel
import os


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
        
        # Font
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Menu system
        self.menu = MenuScreen(self.screen)
        self.show_splash = show_splash
        
        # Game state
        self.game_state = GameState(GRID_SIZE)
        
        # Create players
        self.human_player = self.game_state.add_player(1, 1, GREEN, "Player")
        self.ai_player = self.game_state.add_player(
            GRID_SIZE - 2, GRID_SIZE - 2, RED, "AI"
        )
        
        # Use intelligent model selector
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        selector = ModelSelector(models_dir)
        
        # Select best model based on performance
        selection = selector.select_best_model()
        
        # Load AI training stats
        self.ai_stats = self._load_ai_stats()
        # Create AI agent based on selection
        if selection['model_path'] == 'heuristic':
            print(f"🌱 Using Improved Heuristic Agent")
            print(f"   Reason: {selection['reason']}")
            print(f"   Expected Win Rate: ~{selection['win_rate']:.1f}%")
            if selection['model_type'] == 'heuristic':
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
            print(f"\n🧠 Model Features:")
            print(f"   • Bootstrap trained with heuristics")
            print(f"   • Ready for reinforcement learning")
            print(f"   • Strategic decision making")
            print(f"\n💡 Continue training: ./train.sh")
            self.ai_agent = PPOAgent(self.ai_player, model_path=selection['model_path'], training=False)
            self.ai_type = "PPO (Pretrained)"
            
        elif selection['model_type'] == 'ppo':
            print(f"🏆 Using Trained PPO Model")
            print(f"   Reason: {selection['reason']}")
            print(f"   Win Rate: {selection['win_rate']:.1f}%")
            
            if self.ai_stats:
                total_episodes = self.ai_stats.get('total_episodes', 0)
                total_wins = self.ai_stats.get('total_wins', 0)
                training_time = self.ai_stats.get('total_training_time', 0)
                current_level = self.ai_stats.get('current_level', 'Unknown')
                
                print(f"\n📊 Detailed Statistics:")
                print(f"   🎯 Skill Level: {current_level}")
                print(f"   🎮 Games Played: {total_episodes:,}")
                print(f"   🏆 Games Won: {total_wins:,}")
                print(f"   ⏱️  Training Time: {self._format_time(training_time)}")
                
                # Show AI strength message
                win_rate = selection['win_rate']
                if win_rate >= 50:
                    print(f"\n   ⚠️  WARNING: This AI is VERY STRONG! Good luck! 💪")
                elif win_rate >= 30:
                    print(f"\n   💪 This AI is quite skilled - prepare for a challenge!")
                elif win_rate >= 10:
                    print(f"\n   🎯 This AI is learning - you have a good chance!")
                else:
                    print(f"\n   🌱 This AI is still learning - you should win easily!")
            
            print(f"\n🧠 AI Features:")
            print(f"   • Deep Reinforcement Learning (PPO algorithm)")
            print(f"   • Trained on {self.ai_stats.get('total_episodes', 0):,} games")
            print(f"   • Learns from every game")
            print(f"   • Adapts to your strategy")
            print(f"\n💡 Train more for even better AI: ./train.sh")
            
            self.ai_agent = PPOAgent(self.ai_player, model_path=selection['model_path'], training=False)
            self.ai_type = "PPO"
        
        else:
            # Fallback to simple agent
            print(f"🤖 Using Simple Agent (Fallback)")
            self.ai_agent = SimpleAgent(self.ai_player)
            self.ai_type = "Simple"
        
        # Set AI info in statistics
        self.stats.set_ai_info(self.ai_type, selection.get('model_path'))
        
        # Game state
        self.running = True
        self.paused = False
        
        # Load assets
        self.assets = get_asset_manager()
        self.wall_sprite = None
        self._load_sprites()
    
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
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_state.game_over:
                    self._restart_game()
                elif event.key == pygame.K_SPACE:
                    if self.human_player.alive:
                        self.game_state.place_bomb(self.human_player)
                        self.stats.record_bomb(True)
                elif event.key == pygame.K_c:
                    if self.human_player.alive:
                        self.game_state.place_caca(self.human_player)
    
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
                
                # Draw tile background
                if (x + y) % 2 == 0:
                    color = (34, 139, 34)  # Forest green
                else:
                    color = (50, 205, 50)  # Lime green
                
                pygame.draw.rect(self.screen, color,
                               (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                
                # Draw walls
                if tile == 1:  # Indestructible wall
                    if self.wall_sprite:
                        self.screen.blit(self.wall_sprite, (pixel_x, pixel_y))
                    else:
                        pygame.draw.rect(self.screen, DARK_GRAY,
                                       (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                        pygame.draw.rect(self.screen, GRAY,
                                       (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 2)
                elif tile == 2:  # Soft wall
                    pygame.draw.rect(self.screen, BROWN,
                                   (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (101, 67, 33),
                                   (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE), 2)
    
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
        controls = "Controls: WASD=Move, Space=Trump💨, C=Caca💩, P=Pause"
        text_surf = self.font.render(controls, True, WHITE)
        text_rect = text_surf.get_rect(right=SCREEN_WIDTH - 10, top=ui_y)
        self.screen.blit(text_surf, text_rect)
    
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
            self.ai_agent = SimpleAgent(self.ai_player)
        
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
                self.ai_agent = SimpleAgent(self.ai_player)
                self.ai_type = "Simple"
            elif selected_ai['type'] == 'heuristic':
                self.ai_agent = ImprovedHeuristicAgent(self.ai_player)
                self.ai_type = "Improved Heuristic"
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
