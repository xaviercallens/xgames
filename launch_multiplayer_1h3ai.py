#!/usr/bin/env python3
"""
Quick launcher for 1 Human + 3 AI players game.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game.multiplayer_config import (
    GameConfig, PlayerConfig, GameConfigBuilder
)


def create_1human_3ai_config(human_name='Player', ai_modes=None):
    """
    Create 1 Human + 3 AI configuration.
    
    Args:
        human_name: Name for human player
        ai_modes: List of 3 AI modes (default: mixed difficulty)
        
    Returns:
        GameConfig instance
    """
    if ai_modes is None:
        ai_modes = [
            'heuristic',              # Intermediate (35% WR)
            'advanced_heuristic',     # Advanced (60% WR)
            'heuristic'               # Intermediate (35% WR)
        ]
    
    # Player colors: Green, Red, Blue, Yellow
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    
    builder = GameConfigBuilder()
    
    # Add human player
    builder.add_human_player(human_name, colors[0])
    
    # Add 3 AI players
    for i, ai_mode in enumerate(ai_modes):
        builder.add_ai_player(f'AI {i + 1}', ai_mode, colors[i + 1])
    
    return builder.build()


def print_config(config):
    """Print configuration details."""
    print("\n" + "=" * 70)
    print("🎮 GAME CONFIGURATION: 1 Human + 3 AI Players")
    print("=" * 70)
    print()
    
    for player in config.players:
        if player.is_human():
            print(f"  👤 Player {player.player_id}: {player.name} (HUMAN)")
        else:
            print(f"  🤖 Player {player.player_id}: {player.name} (AI - {player.ai_mode})")
    
    print()
    print(f"Total Players: {config.get_player_count()}")
    print(f"Human Players: {config.get_human_count()}")
    print(f"AI Players: {config.get_ai_count()}")
    print()
    print("=" * 70)
    print()


def main():
    """Main entry point."""
    import pygame
    from bomber_game.game_engine import BombermanGame
    
    # Create configuration
    print("\n🎮 Creating 1 Human + 3 AI configuration...")
    config = create_1human_3ai_config(
        human_name='Player',
        ai_modes=[
            'heuristic',              # Intermediate Bot (35% WR)
            'advanced_heuristic',     # Advanced Bot (60% WR)
            'heuristic'               # Intermediate Bot (35% WR)
        ]
    )
    
    # Print configuration
    print_config(config)
    
    # Start game
    print("🚀 Starting game...")
    print()
    
    try:
        # Initialize pygame
        pygame.init()
        
        # Create game instance
        game = BombermanGame(show_splash=False)
        
        # Setup multiplayer game with configuration
        game.setup_multiplayer_game(config)
        
        # Run game
        game.run()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
