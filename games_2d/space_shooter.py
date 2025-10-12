"""
Space Shooter - A complete 2D game example using Pygame.
Demonstrates sprites, collision detection, sound, and game states.
"""

import pygame
import random
import math
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.game_math import Vector2D, circle_collision
from utils.input_handler import InputManager, Keys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Player(pygame.sprite.Sprite):
    """Player spaceship class."""
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(GREEN)
        # Draw a simple spaceship shape
        pygame.draw.polygon(self.image, WHITE, [(15, 0), (0, 40), (30, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        
        self.speed = 5
        self.health = 100
        self.score = 0
        
    def update(self, input_manager):
        """Update player based on input."""
        # Movement
        if input_manager.is_key_pressed(Keys.LEFT) or input_manager.is_key_pressed(Keys.A):
            self.rect.x -= self.speed
        if input_manager.is_key_pressed(Keys.RIGHT) or input_manager.is_key_pressed(Keys.D):
            self.rect.x += self.speed
        if input_manager.is_key_pressed(Keys.UP) or input_manager.is_key_pressed(Keys.W):
            self.rect.y -= self.speed
        if input_manager.is_key_pressed(Keys.DOWN) or input_manager.is_key_pressed(Keys.S):
            self.rect.y += self.speed
            
        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def shoot(self):
        """Create a bullet."""
        return Bullet(self.rect.centerx, self.rect.top)


class Enemy(pygame.sprite.Sprite):
    """Enemy spaceship class."""
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        pygame.draw.polygon(self.image, WHITE, [(12, 25), (0, 0), (25, 0)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        
        self.speed = random.randint(1, 3)
        
    def update(self):
        """Move enemy down the screen."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """Bullet class."""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.speed = 7
        
    def update(self):
        """Move bullet up the screen."""
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Simple explosion effect."""
    
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        # Create simple explosion frames
        for i in range(5):
            img = pygame.Surface((30 + i * 10, 30 + i * 10))
            img.fill(YELLOW if i % 2 == 0 else RED)
            pygame.draw.circle(img, WHITE, (img.get_width()//2, img.get_height()//2), 
                             img.get_width()//2, 2)
            self.images.append(img)
            
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.frame = 0
        self.frame_rate = 5
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        """Animate explosion."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame]


class Game:
    """Main game class."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter - Pygame Example")
        self.clock = pygame.time.Clock()
        
        # Input manager
        self.input_manager = InputManager()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        
        # Player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Game state
        self.running = True
        self.game_over = False
        
        # Timing
        self.last_shot = 0
        self.shot_delay = 250  # milliseconds
        self.enemy_spawn_time = 0
        self.enemy_spawn_delay = 1000  # milliseconds
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        
    def handle_events(self):
        """Handle pygame events."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                    
        # Update input manager
        self.input_manager.update(events)
        
        # Handle shooting
        if (self.input_manager.is_key_pressed(Keys.SPACE) and 
            not self.game_over):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shot_delay:
                self.last_shot = now
                bullet = self.player.shoot()
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                
    def spawn_enemy(self):
        """Spawn a new enemy."""
        now = pygame.time.get_ticks()
        if now - self.enemy_spawn_time > self.enemy_spawn_delay:
            self.enemy_spawn_time = now
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            
    def check_collisions(self):
        """Check for collisions between game objects."""
        # Bullet-enemy collisions
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for hit in hits:
            self.player.score += 10
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            
        # Player-enemy collisions
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.player.health -= 20
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            
            if self.player.health <= 0:
                self.game_over = True
                
    def update(self):
        """Update game state."""
        if not self.game_over:
            self.player.update(self.input_manager)
            self.enemies.update()
            self.bullets.update()
            self.spawn_enemy()
            self.check_collisions()
            
        self.explosions.update()
        
    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(BLACK)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (10, 50))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            
            # Center the text
            go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            
            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def restart_game(self):
        """Restart the game."""
        # Clear all sprites
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.explosions.empty()
        
        # Create new player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Reset game state
        self.game_over = False
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
