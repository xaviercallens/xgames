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
import os


class BombermanGame:
    """Main game class that handles the game loop and rendering."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Trump Man (Prouts Man) - Educational Game")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        
        # Game state
        self.game_state = GameState(GRID_SIZE)
        
        # Create players
        self.human_player = self.game_state.add_player(1, 1, GREEN, "Player")
        self.ai_player = self.game_state.add_player(
            GRID_SIZE - 2, GRID_SIZE - 2, RED, "AI"
        )
        
        # Load AI training stats
        self.ai_stats = self._load_ai_stats()
        
        # Create AI agent (priority: PPO > DQN > Simple)
        ppo_model_path = os.path.join(os.path.dirname(__file__), "models", "ppo_agent.pth")
        dqn_model_path = os.path.join(os.path.dirname(__file__), "models", "rl_agent.pth")
        
        if os.path.exists(ppo_model_path):
            print(f"🤖 Using PPO Agent (Advanced RL)")
            if self.ai_stats:
                print(f"   Level: {self.ai_stats.get('current_level', 'Unknown')}")
                print(f"   Training: {self._format_time(self.ai_stats.get('total_training_time', 0))}")
                print(f"   Win Rate: {self.ai_stats.get('win_rate', 0):.1f}%")
            self.ai_agent = PPOAgent(self.ai_player, model_path=ppo_model_path, training=False)
            self.ai_type = "PPO"
        elif os.path.exists(dqn_model_path):
            print(f"🤖 Using DQN Agent (Deep Q-Learning)")
            self.ai_agent = RLAgent(self.ai_player, model_path=dqn_model_path, training=False)
            self.ai_type = "DQN"
        else:
            print(f"🤖 Using Simple Heuristic Agent")
            print(f"   💡 Train advanced AI: ./quick_train_agent.py")
            self.ai_agent = SimpleAgent(self.ai_player)
            self.ai_type = "Simple"
        
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
            self.human_player.move(dx, dy, self.game_state.grid, TILE_SIZE, self.game_state)
            self.human_player.update(dt)  # Update animation
        
        # Update AI
        if self.ai_player.alive:
            action = self.ai_agent.update(dt, self.game_state)
            if action:
                ai_dx, ai_dy, place_bomb = action
                self.ai_player.move(ai_dx, ai_dy, self.game_state.grid, TILE_SIZE, self.game_state)
                if place_bomb:
                    self.game_state.place_bomb(self.ai_player)
            self.ai_player.update(dt)  # Update animation
        
        # Update game state
        self.game_state.update(dt)
    
    def render(self):
        """Render the game."""
        self.screen.fill(BLACK)
        
        # Draw grid
        self._draw_grid()
        
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
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        if self.game_state.winner:
            text = f"{self.game_state.winner.name} Wins!"
            color = self.game_state.winner.color
        else:
            text = "Draw!"
            color = WHITE
        
        text_surf = self.big_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(text_surf, text_rect)
        
        # Restart text
        restart_surf = self.font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(restart_surf, restart_rect)
    
    def _restart_game(self):
        """Restart the game."""
        self.game_state = GameState(GRID_SIZE)
        self.human_player = self.game_state.add_player(1, 1, GREEN, "Player")
        self.ai_player = self.game_state.add_player(
            GRID_SIZE - 2, GRID_SIZE - 2, RED, "AI"
        )
        self.ai_agent = SimpleAgent(self.ai_player)
        self._load_sprites()  # Reload sprites
    
    def run(self):
        """Main game loop."""
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
