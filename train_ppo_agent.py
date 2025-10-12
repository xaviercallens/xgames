#!/usr/bin/env python3
"""
Train PPO agent - Advanced RL training inspired by Bomberland competition.
Uses Proximal Policy Optimization for better sample efficiency.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE, TILE_SIZE
from bomber_game.game_state import GameState
from bomber_game.entities import Player
from bomber_game.agents import PPOAgent, SimpleAgent

# Training parameters
EPISODES = 2000
MAX_STEPS = 500
UPDATE_INTERVAL = 2048  # Update every N steps
SAVE_INTERVAL = 100
MODEL_PATH = "bomber_game/models/ppo_agent.pth"


def calculate_reward(game_state, agent_player, enemy_player, prev_state, action):
    """
    Advanced reward function inspired by Bomberland.
    
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
    
    # Check win/loss
    if not agent_player.alive:
        return -200  # Lost
    if not enemy_player.alive:
        return +200  # Won
    
    # Small penalty for each step
    reward -= 0.5
    
    # Reward for destroying walls
    if prev_state:
        prev_walls = sum(row.count(2) for row in prev_state['grid'])
        curr_walls = sum(row.count(2) for row in game_state.grid)
        if curr_walls < prev_walls:
            reward += 20 * (prev_walls - curr_walls)
    
    # Reward for collecting power-ups
    if prev_state and len(game_state.powerups) < prev_state['powerups']:
        reward += 10
    
    # Reward for moving toward enemy
    if prev_state:
        prev_dist = abs(prev_state['player_x'] - prev_state['enemy_x']) + \
                   abs(prev_state['player_y'] - prev_state['enemy_y'])
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
        
        # Penalty for placing bomb in dangerous position
        if _is_dangerous_bomb_placement(game_state, agent_player):
            reward -= 20
    
    # Reward for surviving dangerous situations
    if prev_state and prev_state.get('in_danger', False):
        if not _in_danger(game_state, agent_player):
            reward += 30
    
    return reward


def _is_dangerous_bomb_placement(game_state, player):
    """Check if placing bomb here is dangerous."""
    px, py = player.grid_x, player.grid_y
    
    # Check if player can escape
    escape_routes = 0
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = px + dx, py + dy
        if game_state.is_walkable(nx, ny):
            escape_routes += 1
    
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
    """Save current state."""
    return {
        'grid': [row[:] for row in game_state.grid],
        'powerups': len(game_state.powerups),
        'player_x': agent_player.grid_x,
        'player_y': agent_player.grid_y,
        'enemy_x': enemy_player.grid_x,
        'enemy_y': enemy_player.grid_y,
        'in_danger': _in_danger(game_state, agent_player),
    }


def train():
    """Train PPO agent."""
    print("=" * 70)
    print("🤖 PPO AGENT TRAINING - Bomberland-Inspired")
    print("=" * 70)
    print()
    
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
    print(f"📊 Training Configuration:")
    print(f"   Algorithm: PPO (Proximal Policy Optimization)")
    print(f"   Episodes: {EPISODES}")
    print(f"   Max steps: {MAX_STEPS}")
    print(f"   Update interval: {UPDATE_INTERVAL}")
    print(f"   Model: {MODEL_PATH}")
    print()
    
    # Create model directory
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Statistics
    episode_rewards = []
    episode_lengths = []
    wins = 0
    losses = 0
    total_steps = 0
    
    # Create agent (load existing if available)
    agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
    agent = PPOAgent(agent_player, model_path=MODEL_PATH if os.path.exists(MODEL_PATH) else None, training=True)
    
    print("🎮 Starting training...\n")
    
    for episode in range(EPISODES):
        # Initialize game
        game_state = GameState(GRID_SIZE)
        
        # Create players
        agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
        enemy_player = Player(11, 11, (0, 255, 0), "Enemy")
        
        game_state.players = [agent_player, enemy_player]
        
        # Update agent's player reference
        agent.player = agent_player
        
        # Create enemy AI
        enemy_ai = SimpleAgent(enemy_player)
        
        # Episode variables
        total_reward = 0
        steps = 0
        prev_state = None
        done = False
        
        while not done and steps < MAX_STEPS:
            # Agent action
            action = agent.choose_action(game_state)
            dx, dy, place_bomb = action
            
            # Execute agent action
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
            
            # Update game
            game_state.update(1/30)
            
            # Calculate reward
            reward = calculate_reward(game_state, agent_player, enemy_player, prev_state, action)
            total_reward += reward
            
            # Store experience
            done = not agent_player.alive or not enemy_player.alive
            agent.store_reward(reward, done)
            
            # Save state
            prev_state = save_state(game_state, agent_player, enemy_player)
            steps += 1
            total_steps += 1
            
            # Update policy
            if total_steps % UPDATE_INTERVAL == 0:
                agent.update()
                print(f"  📈 Policy updated at step {total_steps}")
        
        # Final update for episode
        agent.update()
        
        # Statistics
        episode_rewards.append(total_reward)
        episode_lengths.append(steps)
        if agent_player.alive and not enemy_player.alive:
            wins += 1
        elif not agent_player.alive:
            losses += 1
        
        # Print progress
        if (episode + 1) % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            avg_length = np.mean(episode_lengths[-10:])
            win_rate = wins / (episode + 1) * 100
            print(f"Episode {episode + 1:4d}/{EPISODES} | "
                  f"Reward: {avg_reward:7.2f} | "
                  f"Length: {avg_length:5.1f} | "
                  f"Win%: {win_rate:5.1f} | "
                  f"Steps: {total_steps}")
        
        # Save model
        if (episode + 1) % SAVE_INTERVAL == 0:
            agent.save_model(MODEL_PATH)
            print(f"  💾 Model saved at episode {episode + 1}")
    
    # Final save
    agent.save_model(MODEL_PATH)
    
    print()
    print("=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"Total episodes: {EPISODES}")
    print(f"Total wins: {wins} ({wins/EPISODES*100:.1f}%)")
    print(f"Total losses: {losses} ({losses/EPISODES*100:.1f}%)")
    print(f"Average reward: {np.mean(episode_rewards):.2f}")
    print(f"Best reward: {max(episode_rewards):.2f}")
    print(f"Model saved: {MODEL_PATH}")
    print()
    print("🎮 Test your agent with: ./launch_bomberman.sh")
    print()


if __name__ == "__main__":
    train()
