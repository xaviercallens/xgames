#!/usr/bin/env python3
"""
Trump Man (Prouts Man) Game Launcher
Educational game for learning Python, AI, and Reinforcement Learning

Drop smelly trumps (prouts) instead of bombs! 💨

Controls:
- WASD or Arrow Keys: Move
- Space: Drop a trump (prout)
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
    print("💨 TRUMP MAN (PROUTS MAN) - Educational Game 💨")
    print("=" * 60)
    print("\n📚 Learning Objectives:")
    print("  - Python programming")
    print("  - Game development with Pygame")
    print("  - AI and decision-making")
    print("  - Reinforcement Learning basics")
    print("\n🎯 Game Rules:")
    print("  - Destroy walls with smelly trumps (prouts)! 💨")
    print("  - Collect power-ups (Trump+, Smell+, Speed+)")
    print("  - Defeat the AI opponent")
    print("  - Don't get caught in the stinky clouds!")
    print("\n🎮 Controls:")
    print("  - WASD or Arrow Keys: Move")
    print("  - Space: Drop a trump (prout) 💨")
    print("  - P: Pause")
    print("  - ESC: Quit")
    print("  - R: Restart (when game over)")
    print("\n" + "=" * 60)
    print("Starting game... Get ready to smell! 💨\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame closed. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have pygame installed:")
        print("  pip install pygame")
        sys.exit(1)
