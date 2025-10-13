"""
Multiplayer Game Engine - Supports 1 human + 0-3 AI opponents
"""

import pygame
import sys
from . import (GRID_SIZE, TILE_SIZE, FPS, SCREEN_WIDTH, SCREEN_HEIGHT,
               BLACK, WHITE, GRAY, DARK_GRAY, GREEN, RED, BLUE, YELLOW, BROWN)
from .game_state import GameState
from .agents import PPOAgent, HybridAgent
from .assets import get_asset_manager
from .menu import MenuScreen
from .model_selector import ModelSelector
from .player_selector import PlayerSelector
from .heuristics_improved import ImprovedHeuristicAgent
from .game_statistics import GameStatistics
from .stats_panel import StatsPanel
import os


class MultiplayerGame:
    """Game engine supporting multiple AI opponents."""
    
    # Player spawn positions for 2-4 players
    SPAWN_POSITIONS = [
        (1, 1),                    # Player 1 (Human) - Top-left
        (GRID_SIZE - 2, GRID_SIZE - 2),  # Player 2 (AI 1) - Bottom-right
        (GRID_SIZE - 2, 1),        # Player 3 (AI 2) - Top-right
        (1, GRID_SIZE - 2),        # Player 4 (AI 3) - Bottom-left
    ]
    
    PLAYER_COLORS = [GREEN, RED, BLUE, YELLOW]
    
    def __init__(self):
        """Initialize multiplayer game."""
        pygame.init()
        
        # Screen setup
        self.stats_panel_width = 300
        self.game_width = SCREEN_WIDTH
        self.total_width = SCREEN_WIDTH + self.stats_panel_width
        self.screen = pygame.display.set_mode((self.total_width, SCREEN_HEIGHT))
        pygame.display.set_caption("💨 PROUTMAN - Multiplayer Mode! 💩")
        self.clock = pygame.time.Clock()
        
        # Statistics
        self.stats = GameStatistics()
        self.stats_panel = StatsPanel(SCREEN_WIDTH, 0, self.stats_panel_width, SCREEN_HEIGHT)
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Menu system
        self.menu = MenuScreen(self.screen)
        self.player_selector = PlayerSelector(self.screen)
        
        # Game state
        self.running = True
        self.paused = False
        
        # Assets
        self.assets = get_asset_manager()
        
        # Players and AI agents (will be initialized after menu)
        self.human_player = None
        self.ai_players = []
        self.ai_agents = []
        self.player_config = None
        
    def initialize_players(self, player_config):
        """
        Initialize players based on configuration.
        
        Args:
            player_config: Dictionary from PlayerSelector
        """
        self.player_config = player_config
        self.game_state = GameState(GRID_SIZE)
        
        # Create human player
        pos = self.SPAWN_POSITIONS[0]
        self.human_player = self.game_state.add_player(
            pos[0], pos[1], self.PLAYER_COLORS[0], "Player 1"
        )
        
        # Create AI opponents
        self.ai_players = []
        self.ai_agents = []
        
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        
        for i, ai_config in enumerate(player_config['ai_configs']):
            # Create AI player
            pos = self.SPAWN_POSITIONS[i + 1]
            ai_player = self.game_state.add_player(
                pos[0], pos[1], 
                ai_config['color'],
                ai_config['name']
            )
            self.ai_players.append(ai_player)
            
            # Create AI agent based on type
            ai_type = ai_config['type']
            
            if ai_type == 'simple' or ai_type == 'heuristic':
                agent = ImprovedHeuristicAgent(ai_player)
            elif ai_type == 'ppo':
                model_path = os.path.join(models_dir, "ppo_agent.pth")
                agent = PPOAgent(ai_player, model_path=model_path, training=False)
            elif ai_type == 'hybrid':
                model_path = os.path.join(models_dir, "ppo_agent.pth")
                agent = HybridAgent(ai_player, mode='adaptive', ppo_model_path=model_path)
            else:
                agent = ImprovedHeuristicAgent(ai_player)
            
            self.ai_agents.append(agent)
            
            print(f"✅ {ai_config['name']}: {ai_config['type_name']} ({ai_config['win_rate']}% WR)")
        
        # Update statistics
        ai_info = f"{len(self.ai_agents)} AI opponents"
        self.stats.set_ai_info(ai_info, None)
        
        # Load sprites
        self._load_sprites()
    
    def _load_sprites(self):
        """Load game sprites."""
        try:
            self.wall_sprite = self.assets.get_sprite('wall')
            self.soft_wall_sprite = self.assets.get_sprite('soft_wall')
            self.bomb_sprite = self.assets.get_sprite('bomb')
            self.explosion_sprite = self.assets.get_sprite('explosion')
            self.powerup_sprites = {
                'bomb': self.assets.get_sprite('powerup_bomb'),
                'fire': self.assets.get_sprite('powerup_fire'),
                'speed': self.assets.get_sprite('powerup_speed'),
            }
        except:
            self.wall_sprite = None
            self.soft_wall_sprite = None
            self.bomb_sprite = None
            self.explosion_sprite = None
            self.powerup_sprites = {}
    
    def run(self):
        """Main game loop."""
        # Show splash
        quit_requested = self.menu.show_splash(duration=3.0)
        if quit_requested:
            pygame.quit()
            sys.exit()
        
        # Show player selection
        player_config = self.player_selector.show()
        if player_config is None:
            pygame.quit()
            sys.exit()
        
        # Initialize players
        print(f"\n{'='*70}")
        print(f"🎮 MULTIPLAYER SETUP")
        print(f"{'='*70}")
        print(f"   Total Players: {player_config['total_players']}")
        print(f"   Human Players: {player_config['num_human_players']}")
        print(f"   AI Opponents: {player_config['num_ai_opponents']}")
        print(f"{'='*70}\n")
        
        self.initialize_players(player_config)
        
        # Main game loop
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_state.game_over:
                    self.restart_game()
    
    def update(self, dt):
        """Update game state."""
        if self.game_state.game_over:
            return
        
        # Get human player input
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        place_bomb = False
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1
        
        if keys[pygame.K_SPACE]:
            place_bomb = True
        
        # Move human player
        if dx != 0 or dy != 0:
            self.human_player.move(dx, dy, self.game_state.grid, TILE_SIZE, self.game_state)
        
        if place_bomb:
            self.game_state.place_bomb(self.human_player)
        
        # Update AI agents
        for ai_player, ai_agent in zip(self.ai_players, self.ai_agents):
            if ai_player.alive:
                action = ai_agent.choose_action(self.game_state)
                dx, dy, place_bomb = action
                
                if dx != 0 or dy != 0:
                    ai_player.move(dx, dy, self.game_state.grid, TILE_SIZE, self.game_state)
                
                if place_bomb:
                    self.game_state.place_bomb(ai_player)
        
        # Update game state
        self.game_state.update(dt)
        
        # Check for game over
        alive_players = [p for p in [self.human_player] + self.ai_players if p.alive]
        if len(alive_players) <= 1:
            self.game_state.game_over = True
            if len(alive_players) == 1:
                winner = alive_players[0]
                self.game_state.winner = winner.name
            else:
                self.game_state.winner = "Draw"
    
    def render(self):
        """Render game."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw game area
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface.fill(DARK_GRAY)
        
        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                cell = self.game_state.grid[y][x]
                if cell == 1:  # Wall
                    if self.wall_sprite:
                        game_surface.blit(self.wall_sprite, rect)
                    else:
                        pygame.draw.rect(game_surface, GRAY, rect)
                elif cell == 2:  # Soft wall
                    if self.soft_wall_sprite:
                        game_surface.blit(self.soft_wall_sprite, rect)
                    else:
                        pygame.draw.rect(game_surface, BROWN, rect)
                else:
                    pygame.draw.rect(game_surface, DARK_GRAY, rect)
                
                # Grid lines
                pygame.draw.rect(game_surface, BLACK, rect, 1)
        
        # Draw power-ups
        for powerup in self.game_state.powerups:
            powerup.draw(game_surface, self.powerup_sprites.get(powerup.type))
        
        # Draw bombs
        for bomb in self.game_state.bombs:
            bomb.draw(game_surface, self.bomb_sprite)
        
        # Draw explosions
        for explosion in self.game_state.explosions:
            explosion.draw(game_surface, self.explosion_sprite)
        
        # Draw players
        self.human_player.draw(game_surface)
        for ai_player in self.ai_players:
            ai_player.draw(game_surface)
        
        # Draw game over
        if self.game_state.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            game_surface.blit(overlay, (0, 0))
            
            if self.game_state.winner:
                text = self.big_font.render(f"{self.game_state.winner} Wins!", True, WHITE)
            else:
                text = self.big_font.render("Draw!", True, WHITE)
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            game_surface.blit(text, text_rect)
            
            restart_text = self.font.render("Press R to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            game_surface.blit(restart_text, restart_rect)
        
        # Blit game surface
        self.screen.blit(game_surface, (0, 0))
        
        # Draw stats panel
        self.stats_panel.draw(self.screen, self.stats, self.human_player, 
                             self.ai_players[0] if self.ai_players else None)
        
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game with same configuration."""
        self.initialize_players(self.player_config)
        self.paused = False


def main():
    """Entry point for multiplayer game."""
    game = MultiplayerGame()
    game.run()


if __name__ == "__main__":
    main()
