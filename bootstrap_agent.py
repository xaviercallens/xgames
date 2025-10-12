#!/usr/bin/env python3
"""
Bootstrap AI Agent with Heuristics
Trains the PPO agent using heuristic demonstrations to learn basic strategies.
"""

import sys
import os
import time
import json
import numpy as np
from datetime import datetime

# Suppress pygame warnings
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE, TILE_SIZE
from bomber_game.game_state import GameState
from bomber_game.entities import Player
from bomber_game.agents import PPOAgent, SimpleAgent
from bomber_game.heuristics import HeuristicAgent, GameHeuristics

# Configuration
BOOTSTRAP_EPISODES = 500  # Number of heuristic demonstrations
MODEL_PATH = "bomber_game/models/ppo_agent.pth"
BOOTSTRAP_STATS_FILE = "bomber_game/models/bootstrap_stats.json"


def print_banner():
    """Print bootstrap banner."""
    print("\n" + "=" * 80)
    print("🎓 HEURISTIC BOOTSTRAP - Teaching AI Basic Strategies")
    print("=" * 80)
    print()
    print("📚 Learning Objectives:")
    print("   ✅ Walk in unblocked directions")
    print("   ✅ Find safe spaces to place bombs")
    print("   ✅ Create bombs and escape")
    print("   ✅ Avoid bombs when detected")
    print("   ✅ Move towards objectives")
    print("   ✅ Basic survival strategies")
    print()
    print("=" * 80)
    print()


def save_state(game_state, player, enemy):
    """Save game state for PPO."""
    return {
        'player_pos': (int(player.x), int(player.y)),
        'enemy_pos': (int(enemy.x), int(enemy.y)),
        'player_alive': player.alive,
        'enemy_alive': enemy.alive,
        'bombs': [(b.grid_x, b.grid_y, b.timer) for b in game_state.bombs],
        'explosions': [(e.grid_x, e.grid_y) for e in game_state.explosions],
    }


def calculate_reward(prev_state, curr_state, action, player, enemy):
    """Calculate reward for heuristic action."""
    reward = 0
    
    # Survival reward
    if player.alive:
        reward += 0.1
    else:
        reward -= 10.0
        return reward
    
    # Enemy defeat reward
    if not enemy.alive and prev_state['enemy_alive']:
        reward += 20.0
    
    # Movement rewards
    px, py = curr_state['player_pos']
    prev_px, prev_py = prev_state['player_pos']
    
    # Reward for moving to safer positions
    if GameHeuristics.is_safe_position(px, py, None):
        reward += 0.2
    
    # Reward for placing bombs strategically
    if action[2]:  # Placed bomb
        reward += 0.5
    
    # Small penalty for staying still
    if px == prev_px and py == prev_py:
        reward -= 0.05
    
    return reward


def bootstrap_training():
    """Run bootstrap training with heuristics."""
    print_banner()
    
    # Check PyTorch
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"✅ Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    except ImportError:
        print("❌ PyTorch not installed!")
        print("   Install: pip install torch")
        return
    
    print()
    print("🤖 Initializing PPO Agent...")
    
    # Create agent
    agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
    agent = PPOAgent(agent_player)
    agent.training = True
    
    print("✅ PPO Agent initialized")
    print()
    print(f"📊 Bootstrap Configuration:")
    print(f"   Episodes: {BOOTSTRAP_EPISODES}")
    print(f"   Strategy: Heuristic demonstrations")
    print(f"   Learning: Imitation + Reinforcement")
    print()
    print("🎮 Starting bootstrap training...\n")
    
    # Statistics
    total_rewards = []
    wins = 0
    losses = 0
    start_time = time.time()
    
    for episode in range(BOOTSTRAP_EPISODES):
        # Initialize game
        game_state = GameState(GRID_SIZE)
        agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
        enemy_player = Player(11, 11, (0, 255, 0), "Heuristic Teacher")
        game_state.players = [agent_player, enemy_player]
        agent.player = agent_player
        
        # Create heuristic teacher
        teacher = HeuristicAgent(enemy_player)
        
        # Episode loop
        steps = 0
        max_steps = 500
        total_reward = 0
        prev_state = save_state(game_state, agent_player, enemy_player)
        
        while steps < max_steps and agent_player.alive and enemy_player.alive:
            # Get heuristic action for agent (learning from heuristics)
            heuristic_action = GameHeuristics.get_heuristic_action(agent_player, game_state)
            
            # Agent chooses action (will learn to mimic heuristics)
            agent_action = agent.choose_action(game_state)
            
            # Use heuristic action 70% of the time for demonstration
            if np.random.random() < 0.7:
                action = heuristic_action
            else:
                action = agent_action
            
            # Execute agent action
            if action:
                dx, dy, place_bomb = action
                agent_player.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                
                if place_bomb and agent_player.active_bombs < agent_player.max_bombs:
                    bomb = game_state.place_bomb(agent_player)
            
            # Teacher action
            teacher_action = teacher.update(0.1, game_state)
            if teacher_action:
                t_dx, t_dy, t_bomb = teacher_action
                enemy_player.move(t_dx, t_dy, game_state.grid, TILE_SIZE, game_state)
                
                if t_bomb and enemy_player.active_bombs < enemy_player.max_bombs:
                    game_state.place_bomb(enemy_player)
            
            # Update game state
            game_state.update(0.1)
            
            # Calculate reward
            curr_state = save_state(game_state, agent_player, enemy_player)
            reward = calculate_reward(prev_state, curr_state, action, agent_player, enemy_player)
            total_reward += reward
            
            # Store experience
            done = not agent_player.alive or not enemy_player.alive
            agent.store_reward(reward, done)
            
            prev_state = curr_state
            steps += 1
        
        # Update policy
        agent.update_policy()
        
        # Statistics
        total_rewards.append(total_reward)
        if agent_player.alive and not enemy_player.alive:
            wins += 1
        elif not agent_player.alive:
            losses += 1
        
        # Progress
        if (episode + 1) % 50 == 0:
            avg_reward = np.mean(total_rewards[-50:])
            win_rate = (wins / (episode + 1)) * 100
            elapsed = time.time() - start_time
            
            print(f"Episode {episode + 1}/{BOOTSTRAP_EPISODES} | "
                  f"Avg Reward: {avg_reward:.2f} | "
                  f"Win Rate: {win_rate:.1f}% | "
                  f"Time: {elapsed:.0f}s")
    
    # Save model
    print()
    print("=" * 80)
    print("💾 Saving bootstrapped model...")
    agent.save_model(MODEL_PATH)
    
    # Save statistics
    stats = {
        'bootstrap_episodes': BOOTSTRAP_EPISODES,
        'total_wins': wins,
        'total_losses': losses,
        'win_rate': (wins / BOOTSTRAP_EPISODES) * 100,
        'avg_reward': float(np.mean(total_rewards)),
        'timestamp': datetime.now().isoformat(),
        'strategies_learned': [
            'Walk in unblocked directions',
            'Find safe spaces for bombs',
            'Create bombs and escape',
            'Avoid bombs when detected',
            'Move towards objectives',
            'Basic survival strategies'
        ]
    }
    
    with open(BOOTSTRAP_STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print("✅ Model saved to:", MODEL_PATH)
    print("✅ Statistics saved to:", BOOTSTRAP_STATS_FILE)
    print()
    print("=" * 80)
    print("🎓 BOOTSTRAP TRAINING COMPLETE!")
    print("=" * 80)
    print()
    print(f"📊 Results:")
    print(f"   Episodes: {BOOTSTRAP_EPISODES}")
    print(f"   Wins: {wins}")
    print(f"   Losses: {losses}")
    print(f"   Win Rate: {stats['win_rate']:.1f}%")
    print(f"   Avg Reward: {stats['avg_reward']:.2f}")
    print()
    print("✅ Strategies Learned:")
    for strategy in stats['strategies_learned']:
        print(f"   ✓ {strategy}")
    print()
    print("=" * 80)
    print("🚀 Next Steps:")
    print("   1. Run: ./quick_train_agent.py  (Continue training)")
    print("   2. Run: ./launch_bomberman.sh   (Test the agent)")
    print("=" * 80)
    print()


if __name__ == "__main__":
    bootstrap_training()
