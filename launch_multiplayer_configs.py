#!/usr/bin/env python3
"""
Quick launchers for various multiplayer configurations.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game.multiplayer_config import GameConfigBuilder


def create_1h3ai_config(human_name='Player'):
    """1 Human + 3 AI players."""
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    builder = GameConfigBuilder()
    builder.add_human_player(human_name, colors[0])
    builder.add_ai_player('AI 1', 'heuristic', colors[1])
    builder.add_ai_player('AI 2', 'advanced_heuristic', colors[2])
    builder.add_ai_player('AI 3', 'heuristic', colors[3])
    return builder.build()


def create_2h2ai_config(human1='Player 1', human2='Player 2'):
    """2 Human + 2 AI players."""
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    builder = GameConfigBuilder()
    builder.add_human_player(human1, colors[0])
    builder.add_human_player(human2, colors[1])
    builder.add_ai_player('AI 1', 'intermediate_heuristic', colors[2])
    builder.add_ai_player('AI 2', 'advanced_heuristic', colors[3])
    return builder.build()


def create_3h1ai_config(human1='Player 1', human2='Player 2', human3='Player 3'):
    """3 Human + 1 AI player."""
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    builder = GameConfigBuilder()
    builder.add_human_player(human1, colors[0])
    builder.add_human_player(human2, colors[1])
    builder.add_human_player(human3, colors[2])
    builder.add_ai_player('AI 1', 'advanced_heuristic', colors[3])
    return builder.build()


def create_4human_config(names=None):
    """4 Human players."""
    if names is None:
        names = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    builder = GameConfigBuilder()
    for i, name in enumerate(names[:4]):
        builder.add_human_player(name, colors[i])
    return builder.build()


def create_1h1ai_config(human_name='Player', ai_mode='advanced_heuristic'):
    """1 Human + 1 AI player (1v1)."""
    colors = [(0, 255, 0), (255, 0, 0)]
    builder = GameConfigBuilder()
    builder.add_human_player(human_name, colors[0])
    builder.add_ai_player('AI Opponent', ai_mode, colors[1])
    return builder.build()


def print_config(config, title):
    """Print configuration details."""
    print("\n" + "=" * 70)
    print(f"🎮 {title}")
    print("=" * 70)
    print()
    
    for player in config.players:
        if player.is_human():
            print(f"  👤 Player {player.player_id}: {player.name} (HUMAN)")
        else:
            print(f"  🤖 Player {player.player_id}: {player.name} (AI - {player.ai_mode})")
    
    print()
    print(f"Total: {config.get_player_count()} players " +
          f"({config.get_human_count()} human, {config.get_ai_count()} AI)")
    print("=" * 70)
    print()


def start_game(config):
    """Start game with configuration."""
    import pygame
    from bomber_game.game_engine import BombermanGame
    
    try:
        pygame.init()
        game = BombermanGame(show_splash=False)
        
        # Setup multiplayer game
        # Note: setup_multiplayer_game method needs to be implemented in game_engine.py
        # For now, we'll just print the config
        print_config(config, "GAME CONFIGURATION")
        print("🚀 Starting game...")
        print()
        
        # TODO: Implement setup_multiplayer_game in game_engine.py
        # game.setup_multiplayer_game(config)
        # game.run()
        
        print("✅ Configuration ready!")
        print("📝 Note: Game engine integration needed")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Launch multiplayer game configurations')
    parser.add_argument('config', nargs='?', default='1h3ai',
                       choices=['1h3ai', '2h2ai', '3h1ai', '4human', '1h1ai'],
                       help='Configuration to launch')
    parser.add_argument('--names', nargs='+', help='Player names')
    parser.add_argument('--ai-mode', default='advanced_heuristic',
                       choices=['simple', 'heuristic', 'advanced_heuristic'],
                       help='AI mode for 1v1')
    
    args = parser.parse_args()
    
    # Create configuration
    if args.config == '1h3ai':
        config = create_1h3ai_config()
        title = "GAME CONFIGURATION: 1 Human + 3 AI Players"
    elif args.config == '2h2ai':
        config = create_2h2ai_config()
        title = "GAME CONFIGURATION: 2 Human + 2 AI Players"
    elif args.config == '3h1ai':
        config = create_3h1ai_config()
        title = "GAME CONFIGURATION: 3 Human + 1 AI Player"
    elif args.config == '4human':
        config = create_4human_config(args.names)
        title = "GAME CONFIGURATION: 4 Human Players"
    elif args.config == '1h1ai':
        config = create_1h1ai_config(ai_mode=args.ai_mode)
        title = "GAME CONFIGURATION: 1 Human + 1 AI Player (1v1)"
    else:
        config = create_1h3ai_config()
        title = "GAME CONFIGURATION: 1 Human + 3 AI Players"
    
    # Print and start
    print_config(config, title)
    return start_game(config)


if __name__ == '__main__':
    sys.exit(main())
