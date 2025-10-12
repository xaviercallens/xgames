#!/usr/bin/env python3
"""
Bomberman Game Launcher
Educational game for learning Python, AI, and Reinforcement Learning

Controls:
- WASD or Arrow Keys: Move
- Space: Place bomb
- P: Pause
- ESC: Quit
- R: Restart (when game over)

Have fun and learn!
"""

import sys
import os

# Add bomber_game to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game.game_engine import main

if __name__ == "__main__":
    print("=" * 60)
    print("🎮 BOMBERMAN - Educational Game")
    print("=" * 60)
    print("\n📚 Learning Objectives:")
    print("  - Python programming")
    print("  - Game development with Pygame")
    print("  - AI and decision-making")
    print("  - Reinforcement Learning basics")
    print("\n🎯 Game Rules:")
    print("  - Destroy walls with bombs")
    print("  - Collect power-ups (Bomb+, Fire+, Speed+)")
    print("  - Defeat the AI opponent")
    print("  - Don't get caught in explosions!")
    print("\n🎮 Controls:")
    print("  - WASD or Arrow Keys: Move")
    print("  - Space: Place bomb")
    print("  - P: Pause")
    print("  - ESC: Quit")
    print("  - R: Restart (when game over)")
    print("\n" + "=" * 60)
    print("Starting game...\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame closed. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have pygame installed:")
        print("  pip install pygame")
        sys.exit(1)
