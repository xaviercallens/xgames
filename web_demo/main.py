#!/usr/bin/env python3
"""
Proutman - Web Version
Educational Bomberman game for browser play
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if running in browser
try:
    import platform
    RUNNING_IN_BROWSER = platform.system() == "Emscripten"
except:
    RUNNING_IN_BROWSER = False

print("=" * 60)
print("💨 PROUTMAN - Web Version 💨")
print("=" * 60)
print("\n🎮 Loading game...")
print("   Controls: WASD or Arrow Keys, SPACE for bombs!")
print("\n" + "=" * 60)

async def main():
    """Main game loop - async for web compatibility"""
    
    # Import game components
    from bomber_game.game_engine import GameEngine
    from bomber_game import GRID_SIZE, CELL_SIZE, FPS
    
    # Create game engine
    game = GameEngine()
    
    # Main game loop
    clock = game.clock
    running = True
    
    while running:
        # Handle events
        for event in game.pygame.event.get():
            if event.type == game.pygame.QUIT:
                running = False
            elif event.type == game.pygame.KEYDOWN:
                if event.key == game.pygame.K_ESCAPE:
                    running = False
                elif event.key == game.pygame.K_r and game.game_over:
                    game.restart_game()
        
        # Update game state
        if not game.paused and not game.game_over:
            game.update()
        
        # Draw everything
        game.draw()
        
        # Update display
        game.pygame.display.flip()
        clock.tick(FPS)
        
        # Yield to browser
        if RUNNING_IN_BROWSER:
            await asyncio.sleep(0)
    
    game.pygame.quit()

if __name__ == "__main__":
    if RUNNING_IN_BROWSER:
        # Run async for browser
        asyncio.run(main())
    else:
        # Run sync for desktop
        import asyncio
        asyncio.run(main())
