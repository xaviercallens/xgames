#!/usr/bin/env python3
"""
Train the RL agent using reinforcement learning.
This script trains a DQN agent to play Bomberman.
"""

import sys
import os
import pygame

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE, TILE_SIZE, FPS
from bomber_game.game_state import GameState
from bomber_game.entities import Player
from bomber_game.agents import RLAgent

# Training parameters
EPISODES = 1000
MAX_STEPS = 500
SAVE_INTERVAL = 100
MODEL_PATH = "bomber_game/models/rl_agent.pth"


def calculate_reward(game_state, agent_player, prev_state):
    """
    Calculate reward for the agent.
    
    Rewards:
    +100: Win (enemy defeated)
    -100: Loss (agent defeated)
    +10: Destroy soft wall
    +5: Collect power-up
    +1: Move closer to enemy
    -1: Move away from enemy
    -5: Get hit by explosion
    -10: Place bomb in dangerous position
    """
    reward = 0
    
    # Check win/loss
    enemy_alive = any(p.alive for p in game_state.players if p != agent_player)
    if not agent_player.alive:
        return -100  # Lost
    if not enemy_alive:
        return +100  # Won
    
    # Small penalty for each step (encourage faster wins)
    reward -= 0.1
    
    # Reward for destroying walls
    if prev_state:
        prev_walls = sum(row.count(2) for row in prev_state['grid'])
        curr_walls = sum(row.count(2) for row in game_state.grid)
        if curr_walls < prev_walls:
            reward += 10 * (prev_walls - curr_walls)
    
    # Reward for collecting power-ups
    if prev_state and len(game_state.powerups) < prev_state['powerups']:
        reward += 5
    
    # Reward for moving toward enemy
    enemy = next((p for p in game_state.players if p != agent_player and p.alive), None)
    if enemy and prev_state:
        prev_dist = abs(prev_state['player_x'] - prev_state['enemy_x']) + \
                   abs(prev_state['player_y'] - prev_state['enemy_y'])
        curr_dist = abs(agent_player.grid_x - enemy.grid_x) + \
                   abs(agent_player.grid_y - enemy.grid_y)
        if curr_dist < prev_dist:
            reward += 1
        elif curr_dist > prev_dist:
            reward -= 1
    
    return reward


def save_state(game_state, agent_player):
    """Save current state for reward calculation."""
    enemy = next((p for p in game_state.players if p != agent_player and p.alive), None)
    return {
        'grid': [row[:] for row in game_state.grid],
        'powerups': len(game_state.powerups),
        'player_x': agent_player.grid_x,
        'player_y': agent_player.grid_y,
        'enemy_x': enemy.grid_x if enemy else 0,
        'enemy_y': enemy.grid_y if enemy else 0,
    }


def train():
    """Train the RL agent."""
    print("=" * 60)
    print("🤖 REINFORCEMENT LEARNING TRAINING")
    print("=" * 60)
    print()
    
    # Check if PyTorch is available
    try:
        import torch
        print(f"✅ PyTorch available: {torch.__version__}")
        print(f"✅ Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    except ImportError:
        print("❌ PyTorch not installed!")
        print("   Install with: pip install torch")
        return
    
    print()
    print(f"📊 Training Parameters:")
    print(f"   Episodes: {EPISODES}")
    print(f"   Max steps per episode: {MAX_STEPS}")
    print(f"   Save interval: {SAVE_INTERVAL}")
    print(f"   Model path: {MODEL_PATH}")
    print()
    
    # Create model directory
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Training statistics
    episode_rewards = []
    episode_lengths = []
    wins = 0
    losses = 0
    
    for episode in range(EPISODES):
        # Initialize game
        game_state = GameState(GRID_SIZE)
        
        # Create players
        agent_player = Player(1, 1, (255, 0, 0), "RL Agent")
        enemy_player = Player(11, 11, (0, 255, 0), "Enemy")
        
        game_state.players = [agent_player, enemy_player]
        
        # Create RL agent
        agent = RLAgent(agent_player, model_path=MODEL_PATH if episode > 0 else None, training=True)
        
        # Episode variables
        total_reward = 0
        steps = 0
        prev_state = None
        done = False
        
        while not done and steps < MAX_STEPS:
            # Get current state
            state = agent._get_state(game_state)
            
            # Choose action
            action = agent.choose_action(game_state)
            dx, dy, place_bomb = action
            
            # Execute action
            agent_player.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
            if place_bomb and agent_player.can_place_bomb():
                game_state.place_bomb(agent_player)
            
            # Simple enemy AI (random moves)
            if enemy_player.alive:
                import random
                enemy_dx = random.choice([-1, 0, 1])
                enemy_dy = random.choice([-1, 0, 1])
                enemy_player.move(enemy_dx, enemy_dy, game_state.grid, TILE_SIZE, game_state)
                if random.random() < 0.1 and enemy_player.can_place_bomb():
                    game_state.place_bomb(enemy_player)
            
            # Update game
            game_state.update(1/30)  # 30 FPS
            
            # Calculate reward
            reward = calculate_reward(game_state, agent_player, prev_state)
            total_reward += reward
            
            # Get next state
            next_state = agent._get_state(game_state)
            
            # Check if done
            done = not agent_player.alive or not enemy_player.alive
            
            # Store experience
            action_idx = agent.actions.index(action)
            agent.remember(state, action_idx, reward, next_state, done)
            
            # Train
            agent.replay()
            
            # Save state for next iteration
            prev_state = save_state(game_state, agent_player)
            steps += 1
        
        # Update target network periodically
        if episode % 10 == 0:
            agent.update_target_model()
        
        # Statistics
        episode_rewards.append(total_reward)
        episode_lengths.append(steps)
        if agent_player.alive and not enemy_player.alive:
            wins += 1
        elif not agent_player.alive:
            losses += 1
        
        # Print progress
        if (episode + 1) % 10 == 0:
            avg_reward = sum(episode_rewards[-10:]) / 10
            avg_length = sum(episode_lengths[-10:]) / 10
            win_rate = wins / (episode + 1) * 100
            print(f"Episode {episode + 1}/{EPISODES} | "
                  f"Avg Reward: {avg_reward:.2f} | "
                  f"Avg Length: {avg_length:.1f} | "
                  f"Win Rate: {win_rate:.1f}% | "
                  f"Epsilon: {agent.epsilon:.3f}")
        
        # Save model periodically
        if (episode + 1) % SAVE_INTERVAL == 0:
            agent.save_model(MODEL_PATH)
            print(f"💾 Model saved at episode {episode + 1}")
    
    # Final save
    agent.save_model(MODEL_PATH)
    
    print()
    print("=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Total episodes: {EPISODES}")
    print(f"Total wins: {wins} ({wins/EPISODES*100:.1f}%)")
    print(f"Total losses: {losses} ({losses/EPISODES*100:.1f}%)")
    print(f"Average reward: {sum(episode_rewards)/len(episode_rewards):.2f}")
    print(f"Model saved to: {MODEL_PATH}")
    print()


if __name__ == "__main__":
    train()
