"""
Simple Platformer - A basic 2D platformer example using Pygame.
Demonstrates gravity, jumping, platforms, and basic game mechanics.
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.game_math import Vector2D, rect_collision
from utils.input_handler import InputManager, Keys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)


class Player(pygame.sprite.Sprite):
    """Player character with physics."""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Physics
        self.velocity = Vector2D(0, 0)
        self.on_ground = False
        self.speed = 5
        
    def update(self, input_manager, platforms):
        """Update player physics and movement."""
        # Horizontal movement
        if input_manager.is_key_pressed(Keys.LEFT) or input_manager.is_key_pressed(Keys.A):
            self.velocity.x = -self.speed
        elif input_manager.is_key_pressed(Keys.RIGHT) or input_manager.is_key_pressed(Keys.D):
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
            
        # Jumping
        if (input_manager.is_key_just_pressed(Keys.SPACE) or 
            input_manager.is_key_just_pressed(Keys.UP)) and self.on_ground:
            self.velocity.y = JUMP_STRENGTH
            self.on_ground = False
            
        # Apply gravity
        self.velocity.y += GRAVITY
        
        # Move horizontally
        self.rect.x += self.velocity.x
        self.check_platform_collisions(platforms, 'horizontal')
        
        # Move vertically
        self.rect.y += self.velocity.y
        self.check_platform_collisions(platforms, 'vertical')
        
        # Keep player on screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        # Check if player fell off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            
    def check_platform_collisions(self, platforms, direction):
        """Check collisions with platforms."""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == 'horizontal':
                    if self.velocity.x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.velocity.x < 0:  # Moving left
                        self.rect.left = platform.rect.right
                        
                elif direction == 'vertical':
                    if self.velocity.y > 0:  # Falling
                        self.rect.bottom = platform.rect.top
                        self.velocity.y = 0
                        self.on_ground = True
                    elif self.velocity.y < 0:  # Jumping up
                        self.rect.top = platform.rect.bottom
                        self.velocity.y = 0
                        
    def reset_position(self):
        """Reset player to starting position."""
        self.rect.x = 100
        self.rect.y = 400
        self.velocity = Vector2D(0, 0)


class Platform(pygame.sprite.Sprite):
    """Platform that player can stand on."""
    
    def __init__(self, x, y, width, height, color=BROWN):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, width, height)


class Collectible(pygame.sprite.Sprite):
    """Collectible item for the player."""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        pygame.draw.circle(self.image, WHITE, (10, 10), 8)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation
        self.float_offset = 0
        self.original_y = y
        
    def update(self):
        """Animate the collectible."""
        self.float_offset += 0.1
        self.rect.y = self.original_y + int(5 * math.sin(self.float_offset))


class Enemy(pygame.sprite.Sprite):
    """Simple enemy that moves back and forth."""
    
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        pygame.draw.polygon(self.image, WHITE, [(12, 0), (0, 25), (25, 25)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 2
        self.direction = 1
        self.left_bound = left_bound
        self.right_bound = right_bound
        
    def update(self):
        """Move enemy back and forth."""
        self.rect.x += self.speed * self.direction
        
        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1


class SimplePlatformer:
    """Main game class."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Platformer - Pygame Example")
        self.clock = pygame.time.Clock()
        
        # Input manager
        self.input_manager = InputManager()
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Create player
        self.player = Player(100, 400)
        self.all_sprites.add(self.player)
        
        # Create level
        self.create_level()
        
        # Game state
        self.running = True
        self.score = 0
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        
    def create_level(self):
        """Create the game level with platforms and objects."""
        # Ground platforms
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # Floating platforms
        platforms_data = [
            (200, 500, 150, 20),
            (400, 400, 100, 20),
            (600, 300, 120, 20),
            (150, 350, 100, 20),
            (500, 200, 150, 20),
            (700, 450, 80, 20),
        ]
        
        for x, y, width, height in platforms_data:
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
        # Add collectibles
        collectibles_data = [
            (250, 460),
            (440, 360),
            (650, 260),
            (180, 310),
            (550, 160),
            (730, 410),
        ]
        
        for x, y in collectibles_data:
            collectible = Collectible(x, y)
            self.collectibles.add(collectible)
            self.all_sprites.add(collectible)
            
        # Add enemies
        enemies_data = [
            (200, 475, 200, 350),  # x, y, left_bound, right_bound
            (600, 275, 600, 720),
            (500, 175, 500, 650),
        ]
        
        for x, y, left, right in enemies_data:
            enemy = Enemy(x, y, left, right)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
    def handle_events(self):
        """Handle pygame events."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart_game()
                    
        # Update input manager
        self.input_manager.update(events)
        
    def check_collisions(self):
        """Check for collisions between game objects."""
        # Player-collectible collisions
        collected = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for collectible in collected:
            self.score += 10
            
        # Player-enemy collisions
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hit_enemies:
            self.player.reset_position()
            
    def update(self):
        """Update game state."""
        self.player.update(self.input_manager, self.platforms)
        self.collectibles.update()
        self.enemies.update()
        self.check_collisions()
        
    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(BLACK)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        instructions = [
            "WASD/Arrow Keys: Move",
            "Space/Up: Jump",
            "R: Restart",
            "Collect green coins, avoid red enemies!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
            self.screen.blit(text, (10, 50 + i * 25))
            
        pygame.display.flip()
        
    def restart_game(self):
        """Restart the game."""
        # Reset player
        self.player.reset_position()
        
        # Reset score
        self.score = 0
        
        # Recreate collectibles
        self.collectibles.empty()
        collectibles_data = [
            (250, 460),
            (440, 360),
            (650, 260),
            (180, 310),
            (550, 160),
            (730, 410),
        ]
        
        for x, y in collectibles_data:
            collectible = Collectible(x, y)
            self.collectibles.add(collectible)
            self.all_sprites.add(collectible)
            
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    game = SimplePlatformer()
    game.run()
