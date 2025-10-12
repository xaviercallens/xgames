#!/usr/bin/env python3
"""
Bootstrap PPO Training with Heuristic Agent.
Pre-trains PPO agent by imitating the improved heuristic agent.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from pathlib import Path
import json
from datetime import datetime

from bomber_game.game_state import GameState
from bomber_game.heuristics_improved import ImprovedHeuristicAgent
from bomber_game.agents.ppo_agent_optimized import OptimizedPPOAgent, OptimizedActorCritic
from bomber_game import GRID_SIZE, GREEN, RED


def collect_heuristic_demonstrations(num_episodes=100):
    """
    Collect demonstration data from heuristic agent.
    Returns: list of (state, action) pairs
    """
    print(f"🎓 Collecting {num_episodes} demonstrations from heuristic agent...")
    
    demonstrations = []
    
    for episode in range(num_episodes):
        # Create game state
        game_state = GameState(GRID_SIZE)
        player1 = game_state.add_player(1, 1, GREEN, "Player")
        player2 = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, RED, "AI")
        
        # Create heuristic agent
        heuristic_agent = ImprovedHeuristicAgent(player2)
        
        # Run episode
        steps = 0
        max_steps = 500
        
        while not game_state.game_over and steps < max_steps:
            # Get heuristic action
            action = heuristic_agent.update(0.016, game_state)  # 60 FPS
            
            if action and player2.alive:
                dx, dy, place_bomb = action
                
                # Get state before action
                state = heuristic_agent._get_state_representation(game_state)
                
                # Convert action to discrete action index
                # 0-3: move directions, 4: place bomb
                if place_bomb:
                    action_idx = 4
                elif dx == -1:
                    action_idx = 0  # Left
                elif dx == 1:
                    action_idx = 1  # Right
                elif dy == -1:
                    action_idx = 2  # Up
                elif dy == 1:
                    action_idx = 3  # Down
                else:
                    action_idx = 5  # No action
                
                demonstrations.append((state, action_idx))
                
                # Execute action
                player2.move(dx, dy, game_state.grid, 32, game_state)
                if place_bomb:
                    game_state.place_bomb(player2)
            
            # Update game state
            game_state.update(0.016)
            steps += 1
        
        if (episode + 1) % 10 == 0:
            print(f"  Collected {episode + 1}/{num_episodes} episodes ({len(demonstrations)} samples)")
    
    print(f"✅ Collected {len(demonstrations)} demonstration samples")
    return demonstrations


def train_with_behavioral_cloning(demonstrations, epochs=50, batch_size=64):
    """
    Train PPO agent using behavioral cloning on heuristic demonstrations.
    """
    print(f"\n🎯 Training PPO agent with behavioral cloning...")
    print(f"  Epochs: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Samples: {len(demonstrations)}")
    
    # Create PPO agent
    state_size = len(demonstrations[0][0])
    action_size = 6  # 4 directions + bomb + no action
    
    model = OptimizedActorCritic(state_size, action_size)
    optimizer = optim.Adam(model.parameters(), lr=3e-4)
    criterion = nn.CrossEntropyLoss()
    
    # Convert demonstrations to tensors
    states = torch.FloatTensor([d[0] for d in demonstrations])
    actions = torch.LongTensor([d[1] for d in demonstrations])
    
    # Training loop
    best_loss = float('inf')
    
    for epoch in range(epochs):
        total_loss = 0
        num_batches = 0
        
        # Shuffle data
        indices = torch.randperm(len(demonstrations))
        
        for i in range(0, len(demonstrations), batch_size):
            batch_indices = indices[i:i+batch_size]
            batch_states = states[batch_indices]
            batch_actions = actions[batch_indices]
            
            # Forward pass
            action_probs, _ = model(batch_states)
            
            # Compute loss
            loss = criterion(action_probs, batch_actions)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        avg_loss = total_loss / num_batches
        
        if avg_loss < best_loss:
            best_loss = avg_loss
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch + 1}/{epochs} - Loss: {avg_loss:.4f} (Best: {best_loss:.4f})")
    
    print(f"✅ Training complete! Best loss: {best_loss:.4f}")
    
    return model


def save_bootstrapped_model(model, output_path="bomber_game/models/ppo_agent_pretrained.pth"):
    """Save the bootstrapped model."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    torch.save({
        'model_state_dict': model.state_dict(),
        'bootstrap_method': 'behavioral_cloning',
        'source': 'improved_heuristic',
        'timestamp': datetime.now().isoformat(),
    }, output_path)
    
    print(f"💾 Saved bootstrapped model to {output_path}")


def create_bootstrap_metadata(output_path="bomber_game/models/bootstrap_metadata.json"):
    """Create metadata file for bootstrapped model."""
    metadata = {
        'method': 'behavioral_cloning',
        'source_agent': 'ImprovedHeuristicAgent',
        'timestamp': datetime.now().isoformat(),
        'description': 'PPO agent bootstrapped with heuristic demonstrations',
        'expected_performance': {
            'win_rate': 25.0,
            'level': 'Intermediate',
            'notes': 'Should perform better than random, ready for RL fine-tuning'
        }
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"📝 Saved bootstrap metadata to {output_path}")


def main():
    """Main bootstrap training pipeline."""
    print("=" * 70)
    print("🚀 PPO BOOTSTRAP TRAINING WITH HEURISTIC AGENT")
    print("=" * 70)
    print()
    
    # Step 1: Collect demonstrations
    demonstrations = collect_heuristic_demonstrations(num_episodes=100)
    
    if len(demonstrations) == 0:
        print("❌ No demonstrations collected. Exiting.")
        return
    
    # Step 2: Train with behavioral cloning
    model = train_with_behavioral_cloning(demonstrations, epochs=50, batch_size=64)
    
    # Step 3: Save model
    save_bootstrapped_model(model)
    
    # Step 4: Create metadata
    create_bootstrap_metadata()
    
    print()
    print("=" * 70)
    print("✅ BOOTSTRAP TRAINING COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Test the bootstrapped model: ./launch_bomberman.sh")
    print("  2. Fine-tune with RL: python train_ppo_optimized.py")
    print("  3. The model will continue learning from gameplay")
    print()


if __name__ == "__main__":
    main()
