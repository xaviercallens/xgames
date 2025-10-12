#!/usr/bin/env python3
"""
CPU-Optimized PPO Training Script
Improvements for faster CPU training:
- Vectorized reward calculation
- Parallel experience collection (optional)
- Better progress tracking
- Automatic checkpointing
- Early stopping based on performance
"""

import sys
import os
import numpy as np
import time
import json
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE, TILE_SIZE
from bomber_game.game_state import GameState
from bomber_game.entities import Player
from bomber_game.agents import SimpleAgent

# Import optimized agent
from bomber_game.agents.ppo_agent_optimized import OptimizedPPOAgent

# Training parameters (optimized for CPU)
EPISODES = 5000
MAX_STEPS = 300  # Reduced for faster episodes
BUFFER_SIZE = 2048  # Collect this many steps before update
SAVE_INTERVAL = 100
EVAL_INTERVAL = 50  # Evaluate performance every N episodes
MODEL_PATH = "bomber_game/models/ppo_agent_optimized.pth"
STATS_PATH = "bomber_game/models/training_stats_optimized.json"

# Early stopping
EARLY_STOP_WIN_RATE = 70.0  # Stop if win rate exceeds this
EARLY_STOP_PATIENCE = 500  # Episodes without improvement


def calculate_reward_vectorized(game_state, agent_player, enemy_player, prev_state, action):
    """
    Optimized reward calculation.
    
    Rewards:
    +200: Win
    -200: Loss
    +20: Destroy soft wall
    +10: Collect power-up
    +5: Move closer to enemy
    -5: Move away from enemy
    +15: Place bomb near enemy
    -20: Place bomb in dangerous position
    +30: Survive dangerous situation
    -0.5: Each step (encourage efficiency)
    """
    reward = 0
    
    # Check win/loss (terminal rewards)
    if not agent_player.alive:
        return -200
    if not enemy_player.alive:
        return +200
    
    # Step penalty
    reward -= 0.5
    
    # Reward for destroying walls
    if prev_state:
        prev_walls = prev_state['walls']
        curr_walls = sum(row.count(2) for row in game_state.grid)
        if curr_walls < prev_walls:
            reward += 20 * (prev_walls - curr_walls)
    
    # Reward for collecting power-ups
    if prev_state and len(game_state.powerups) < prev_state['powerups']:
        reward += 10
    
    # Reward for moving toward enemy
    if prev_state:
        prev_dist = prev_state['enemy_dist']
        curr_dist = abs(agent_player.grid_x - enemy_player.grid_x) + \
                   abs(agent_player.grid_y - enemy_player.grid_y)
        
        if curr_dist < prev_dist:
            reward += 5
        elif curr_dist > prev_dist:
            reward -= 5
    
    # Reward for placing bomb near enemy
    dx, dy, place_bomb = action
    if place_bomb:
        dist_to_enemy = abs(agent_player.grid_x - enemy_player.grid_x) + \
                       abs(agent_player.grid_y - enemy_player.grid_y)
        if dist_to_enemy <= 3:
            reward += 15
        
        # Penalty for dangerous bomb placement
        if _is_dangerous_bomb_placement(game_state, agent_player):
            reward -= 20
    
    # Reward for surviving danger
    if prev_state and prev_state.get('in_danger', False):
        if not _in_danger(game_state, agent_player):
            reward += 30
    
    return reward


def _is_dangerous_bomb_placement(game_state, player):
    """Check if placing bomb here is dangerous."""
    px, py = player.grid_x, player.grid_y
    escape_routes = sum(1 for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                       if game_state.is_walkable(px + dx, py + dy))
    return escape_routes < 2


def _in_danger(game_state, player):
    """Check if player is in danger."""
    px, py = player.grid_x, player.grid_y
    
    for explosion in game_state.explosions:
        if explosion.grid_x == px and explosion.grid_y == py:
            return True
    
    for bomb in game_state.bombs:
        if bomb.timer < 1.5:
            bx, by = bomb.grid_x, bomb.grid_y
            if (px == bx and abs(py - by) <= bomb.bomb_range) or \
               (py == by and abs(px - bx) <= bomb.bomb_range):
                return True
    
    return False


def save_state(game_state, agent_player, enemy_player):
    """Save current state for reward calculation."""
    return {
        'walls': sum(row.count(2) for row in game_state.grid),
        'powerups': len(game_state.powerups),
        'enemy_dist': abs(agent_player.grid_x - enemy_player.grid_x) + \
                     abs(agent_player.grid_y - enemy_player.grid_y),
        'in_danger': _in_danger(game_state, agent_player),
    }


def evaluate_agent(agent, num_episodes=10):
    """
    Evaluate agent performance.
    
    Returns:
        Dictionary with evaluation metrics
    """
    wins = 0
    total_rewards = []
    episode_lengths = []
    
    # Temporarily disable training
    was_training = agent.training
    agent.training = False
    agent.policy.eval()
    
    for _ in range(num_episodes):
        # Initialize game
        game_state = GameState(GRID_SIZE)
        agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
        enemy_player = Player(11, 11, (0, 255, 0), "Enemy")
        game_state.players = [agent_player, enemy_player]
        agent.player = agent_player
        enemy_ai = SimpleAgent(enemy_player)
        
        total_reward = 0
        steps = 0
        prev_state = None
        
        while steps < MAX_STEPS:
            # Agent action
            action = agent.choose_action(game_state)
            dx, dy, place_bomb = action
            
            agent_player.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
            if place_bomb and agent_player.can_place_bomb():
                game_state.place_bomb(agent_player)
            
            # Enemy action
            if enemy_player.alive:
                enemy_action = enemy_ai.choose_action(game_state)
                enemy_dx, enemy_dy, enemy_bomb = enemy_action
                enemy_player.move(enemy_dx, enemy_dy, game_state.grid, TILE_SIZE, game_state)
                if enemy_bomb and enemy_player.can_place_bomb():
                    game_state.place_bomb(enemy_player)
            
            game_state.update(1/30)
            
            reward = calculate_reward_vectorized(game_state, agent_player, enemy_player, prev_state, action)
            total_reward += reward
            prev_state = save_state(game_state, agent_player, enemy_player)
            steps += 1
            
            if not agent_player.alive or not enemy_player.alive:
                break
        
        if agent_player.alive and not enemy_player.alive:
            wins += 1
        
        total_rewards.append(total_reward)
        episode_lengths.append(steps)
    
    # Restore training mode
    agent.training = was_training
    if was_training:
        agent.policy.train()
    
    return {
        'win_rate': wins / num_episodes * 100,
        'avg_reward': np.mean(total_rewards),
        'avg_length': np.mean(episode_lengths),
    }


def save_training_stats(stats, path):
    """Save training statistics to JSON."""
    try:
        with open(path, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(f"⚠️  Could not save stats: {e}")


def load_training_stats(path):
    """Load training statistics from JSON."""
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'total_episodes': 0,
        'total_wins': 0,
        'total_training_time': 0,
        'best_win_rate': 0,
        'episode_rewards': [],
        'episode_lengths': [],
        'eval_win_rates': [],
    }


def train():
    """Train optimized PPO agent."""
    print("=" * 70)
    print("🚀 CPU-OPTIMIZED PPO TRAINING")
    print("=" * 70)
    print()
    
    # Check PyTorch
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"✅ Device: CPU (optimized)")
        print(f"✅ Threads: {torch.get_num_threads()}")
    except ImportError:
        print("❌ PyTorch not installed!")
        print("   Install: pip install torch")
        return
    
    print()
    print(f"📊 Training Configuration:")
    print(f"   Algorithm: PPO (CPU-Optimized)")
    print(f"   Episodes: {EPISODES}")
    print(f"   Max steps per episode: {MAX_STEPS}")
    print(f"   Buffer size: {BUFFER_SIZE}")
    print(f"   Mini-batch size: 64")
    print(f"   Network size: 128 hidden units (optimized)")
    print(f"   Model: {MODEL_PATH}")
    print()
    
    # Create model directory
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Load existing stats
    stats = load_training_stats(STATS_PATH)
    start_episode = stats['total_episodes']
    
    # Statistics
    recent_rewards = deque(maxlen=100)
    recent_lengths = deque(maxlen=100)
    recent_wins = deque(maxlen=100)
    
    wins = 0
    losses = 0
    total_steps = 0
    start_time = time.time()
    best_win_rate = stats.get('best_win_rate', 0)
    episodes_without_improvement = 0
    
    # Create agent
    agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
    agent = OptimizedPPOAgent(
        agent_player, 
        model_path=MODEL_PATH if os.path.exists(MODEL_PATH) else None,
        training=True
    )
    
    print("🎮 Starting training...\n")
    
    try:
        for episode in range(start_episode, start_episode + EPISODES):
            # Initialize game
            game_state = GameState(GRID_SIZE)
            agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
            enemy_player = Player(11, 11, (0, 255, 0), "Enemy")
            game_state.players = [agent_player, enemy_player]
            agent.player = agent_player
            enemy_ai = SimpleAgent(enemy_player)
            
            # Episode variables
            total_reward = 0
            steps = 0
            prev_state = None
            
            while steps < MAX_STEPS:
                # Agent action
                action = agent.choose_action(game_state)
                dx, dy, place_bomb = action
                
                agent_player.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                if place_bomb and agent_player.can_place_bomb():
                    game_state.place_bomb(agent_player)
                
                # Enemy action
                if enemy_player.alive:
                    enemy_action = enemy_ai.choose_action(game_state)
                    enemy_dx, enemy_dy, enemy_bomb = enemy_action
                    enemy_player.move(enemy_dx, enemy_dy, game_state.grid, TILE_SIZE, game_state)
                    if enemy_bomb and enemy_player.can_place_bomb():
                        game_state.place_bomb(enemy_player)
                
                game_state.update(1/30)
                
                # Calculate reward
                reward = calculate_reward_vectorized(game_state, agent_player, enemy_player, prev_state, action)
                total_reward += reward
                
                # Store experience
                done = not agent_player.alive or not enemy_player.alive
                agent.store_reward(reward, done)
                
                prev_state = save_state(game_state, agent_player, enemy_player)
                steps += 1
                total_steps += 1
                
                # Update policy when buffer is full
                if agent.buffer.is_full():
                    agent.update_policy()
                
                if done:
                    break
            
            # Final update for episode
            if agent.buffer.size() > 0:
                agent.update_policy()
            
            # Statistics
            recent_rewards.append(total_reward)
            recent_lengths.append(steps)
            
            won = agent_player.alive and not enemy_player.alive
            recent_wins.append(1 if won else 0)
            
            if won:
                wins += 1
            elif not agent_player.alive:
                losses += 1
            
            # Print progress
            if (episode + 1) % 10 == 0:
                avg_reward = np.mean(recent_rewards)
                avg_length = np.mean(recent_lengths)
                win_rate = np.mean(recent_wins) * 100
                elapsed = time.time() - start_time
                eps_per_sec = (episode - start_episode + 1) / elapsed
                
                print(f"Ep {episode + 1:5d}/{start_episode + EPISODES} | "
                      f"Reward: {avg_reward:7.2f} | "
                      f"Len: {avg_length:5.1f} | "
                      f"Win%: {win_rate:5.1f} | "
                      f"Speed: {eps_per_sec:.2f} ep/s")
            
            # Evaluation
            if (episode + 1) % EVAL_INTERVAL == 0:
                print(f"\n📊 Evaluating at episode {episode + 1}...")
                eval_results = evaluate_agent(agent, num_episodes=20)
                eval_win_rate = eval_results['win_rate']
                
                print(f"   Eval Win Rate: {eval_win_rate:.1f}%")
                print(f"   Eval Avg Reward: {eval_results['avg_reward']:.2f}")
                print(f"   Eval Avg Length: {eval_results['avg_length']:.1f}")
                
                # Track best model
                if eval_win_rate > best_win_rate:
                    best_win_rate = eval_win_rate
                    episodes_without_improvement = 0
                    print(f"   🏆 New best win rate! Saving model...")
                    agent.save_model(MODEL_PATH.replace('.pth', '_best.pth'))
                else:
                    episodes_without_improvement += EVAL_INTERVAL
                
                # Early stopping
                if eval_win_rate >= EARLY_STOP_WIN_RATE:
                    print(f"\n🎉 Target win rate achieved! Stopping early.")
                    break
                
                if episodes_without_improvement >= EARLY_STOP_PATIENCE:
                    print(f"\n⏹️  No improvement for {EARLY_STOP_PATIENCE} episodes. Stopping.")
                    break
                
                print()
            
            # Save model
            if (episode + 1) % SAVE_INTERVAL == 0:
                agent.save_model(MODEL_PATH)
                
                # Update stats
                stats['total_episodes'] = episode + 1
                stats['total_wins'] = wins
                stats['total_training_time'] = time.time() - start_time + stats.get('total_training_time', 0)
                stats['best_win_rate'] = best_win_rate
                save_training_stats(stats, STATS_PATH)
                
                print(f"  💾 Checkpoint saved at episode {episode + 1}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
    
    # Final save
    agent.save_model(MODEL_PATH)
    
    # Final stats
    total_time = time.time() - start_time
    stats['total_episodes'] = episode + 1
    stats['total_wins'] = wins
    stats['total_training_time'] = total_time + stats.get('total_training_time', 0)
    stats['best_win_rate'] = best_win_rate
    save_training_stats(stats, STATS_PATH)
    
    print()
    print("=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"Total episodes: {episode - start_episode + 1}")
    print(f"Total wins: {wins} ({wins/(episode - start_episode + 1)*100:.1f}%)")
    print(f"Total losses: {losses} ({losses/(episode - start_episode + 1)*100:.1f}%)")
    print(f"Best win rate: {best_win_rate:.1f}%")
    print(f"Training time: {total_time/3600:.2f} hours")
    print(f"Speed: {(episode - start_episode + 1)/total_time:.2f} episodes/sec")
    print(f"Model saved: {MODEL_PATH}")
    print()
    print("🎮 Test your agent with: ./launch_bomberman.sh")
    print()


if __name__ == "__main__":
    train()
