"""
Physics Demo - Demonstrates 2D physics using Pymunk.
Shows gravity, collisions, and realistic physics simulation.
"""

import pygame
import pymunk
import pymunk.pygame_util
import random
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


class PhysicsDemo:
    """Physics demonstration using Pymunk."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Physics Demo - Pymunk Example")
        self.clock = pygame.time.Clock()
        
        # Create physics space
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)  # Gravity pointing down
        
        # Physics debug drawing
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
        # Create static ground
        self.create_ground()
        
        # Game state
        self.running = True
        self.mouse_pressed = False
        
        # Font
        self.font = pygame.font.Font(None, 24)
        
    def create_ground(self):
        """Create static ground and walls."""
        # Ground
        ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        ground_shape = pymunk.Segment(ground_body, (0, SCREEN_HEIGHT), 
                                    (SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        ground_shape.friction = 0.7
        self.space.add(ground_body, ground_shape)
        
        # Left wall
        left_wall = pymunk.Segment(ground_body, (0, 0), (0, SCREEN_HEIGHT), 5)
        left_wall.friction = 0.7
        self.space.add(left_wall)
        
        # Right wall
        right_wall = pymunk.Segment(ground_body, (SCREEN_WIDTH, 0), 
                                  (SCREEN_WIDTH, SCREEN_HEIGHT), 5)
        right_wall.friction = 0.7
        self.space.add(right_wall)
        
        # Add some platforms
        platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        
        # Platform 1
        platform1 = pymunk.Segment(platform_body, (200, 450), (400, 450), 5)
        platform1.friction = 0.7
        self.space.add(platform1)
        
        # Platform 2
        platform2 = pymunk.Segment(platform_body, (500, 350), (700, 350), 5)
        platform2.friction = 0.7
        self.space.add(platform2)
        
        # Angled platform
        platform3 = pymunk.Segment(platform_body, (100, 300), (300, 200), 5)
        platform3.friction = 0.7
        self.space.add(platform3)
        
    def create_ball(self, x, y):
        """Create a bouncing ball at the given position."""
        mass = 10
        radius = random.randint(10, 25)
        
        # Create body
        body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        body.position = x, y
        
        # Create shape
        shape = pymunk.Circle(body, radius)
        shape.friction = 0.3
        shape.elasticity = 0.8  # Bounciness
        
        # Add random color
        shape.color = (random.randint(100, 255), 
                      random.randint(100, 255), 
                      random.randint(100, 255), 255)
        
        self.space.add(body, shape)
        
    def create_box(self, x, y):
        """Create a box at the given position."""
        mass = 15
        width = random.randint(20, 40)
        height = random.randint(20, 40)
        
        # Create body
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, (width, height)))
        body.position = x, y
        
        # Create shape
        vertices = [(-width/2, -height/2), (width/2, -height/2), 
                   (width/2, height/2), (-width/2, height/2)]
        shape = pymunk.Poly(body, vertices)
        shape.friction = 0.5
        shape.elasticity = 0.3
        
        # Add random color
        shape.color = (random.randint(100, 255), 
                      random.randint(100, 255), 
                      random.randint(100, 255), 255)
        
        self.space.add(body, shape)
        
    def create_explosion(self, x, y):
        """Create an explosion effect by adding multiple objects with force."""
        for _ in range(8):
            # Create small balls
            mass = 5
            radius = 8
            
            body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
            body.position = x + random.randint(-20, 20), y + random.randint(-20, 20)
            
            shape = pymunk.Circle(body, radius)
            shape.friction = 0.3
            shape.elasticity = 0.9
            shape.color = (255, random.randint(100, 255), 0, 255)  # Orange-ish
            
            # Add explosive force
            force_x = random.randint(-500, 500)
            force_y = random.randint(-800, -200)
            body.apply_impulse_at_local_point((force_x, force_y), (0, 0))
            
            self.space.add(body, shape)
            
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_pressed = True
                elif event.button == 3:  # Right click
                    self.create_explosion(event.pos[0], event.pos[1])
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # Clear all dynamic bodies
                    bodies_to_remove = []
                    for body in self.space.bodies:
                        if body.body_type == pymunk.Body.DYNAMIC:
                            bodies_to_remove.append(body)
                    
                    for body in bodies_to_remove:
                        self.space.remove(body, *body.shapes)
                        
                elif event.key == pygame.K_r:
                    # Add random objects
                    for _ in range(5):
                        x = random.randint(50, SCREEN_WIDTH - 50)
                        y = random.randint(50, 200)
                        if random.choice([True, False]):
                            self.create_ball(x, y)
                        else:
                            self.create_box(x, y)
                            
        # Continuous mouse input
        if self.mouse_pressed:
            mouse_pos = pygame.mouse.get_pos()
            if random.choice([True, False]):
                self.create_ball(mouse_pos[0], mouse_pos[1])
            else:
                self.create_box(mouse_pos[0], mouse_pos[1])
                
    def update(self):
        """Update physics simulation."""
        dt = 1.0 / FPS
        self.space.step(dt)
        
    def draw(self):
        """Draw everything to the screen."""
        self.screen.fill(BLACK)
        
        # Draw physics objects
        self.space.debug_draw(self.draw_options)
        
        # Draw UI
        instructions = [
            "Left Click/Hold: Create objects",
            "Right Click: Explosion",
            "C: Clear all objects",
            "R: Add random objects",
            f"Objects: {len(self.space.bodies) - 1}"  # -1 for static ground body
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, 10 + i * 25))
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    # Check if pymunk is available
    try:
        import pymunk
        game = PhysicsDemo()
        game.run()
    except ImportError:
        print("Pymunk is not installed. Install it with: pip install pymunk")
        print("This demo requires Pymunk for physics simulation.")
