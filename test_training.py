#!/usr/bin/env python3
"""
Quick test to verify training setup works before overnight run
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE, TILE_SIZE
from bomber_game.game_state import GameState
from bomber_game.agents import PPOAgent
from bomber_game.heuristics_improved import ImprovedHeuristicAgent

print("🧪 Testing training setup...")

# Create game state
print("1. Creating game state...")
game_state = GameState(GRID_SIZE)
agent_player = game_state.add_player(1, 1, (0, 255, 0), "PPO Agent")
enemy_player = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, (255, 0, 0), "Heuristic")
print("   ✅ Game state created")

# Create agents
print("2. Creating agents...")
agent = PPOAgent(agent_player, training=True)
enemy_agent = ImprovedHeuristicAgent(enemy_player)
print("   ✅ Agents created")

# Test one episode
print("3. Running test episode...")
for step in range(10):
    # Get actions
    agent_action = agent.choose_action(game_state)
    enemy_action = enemy_agent.choose_action(game_state)
    
    # Execute actions
    agent_player.move(*agent_action[:2], game_state.grid, TILE_SIZE, game_state)
    if agent_action[2]:
        game_state.place_bomb(agent_player)
    
    enemy_player.move(*enemy_action[:2], game_state.grid, TILE_SIZE, game_state)
    if enemy_action[2]:
        game_state.place_bomb(enemy_player)
    
    # Update game
    from bomber_game import FPS
    game_state.update(1/FPS)
    
    if not agent_player.alive or not enemy_player.alive:
        break

print("   ✅ Episode completed")

# Test game state recreation
print("4. Testing game state reset...")
game_state = GameState(GRID_SIZE)
agent_player = game_state.add_player(1, 1, (0, 255, 0), "PPO Agent")
enemy_player = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, (255, 0, 0), "Heuristic")
agent.player = agent_player
enemy_agent.player = enemy_player
print("   ✅ Reset works")

print("\n🎉 All tests passed! Ready for overnight training.")
print("\n🚀 Start training with:")
print("   ./quick_train.sh")
print("   or")
print("   ./start_overnight_training.sh")
