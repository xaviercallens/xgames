#!/usr/bin/env python3
"""
Create a pre-trained PPO model with smart initialization.
This gives the agent a head start with good initial weights.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = "bomber_game/models/ppo_pretrained.pth"


def create_pretrained_model():
    """Create pre-trained model with smart initialization."""
    print("=" * 70)
    print("🎯 CREATING PRE-TRAINED PPO MODEL")
    print("=" * 70)
    print()
    
    try:
        import torch
        import torch.nn as nn
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch not installed!")
        print("   Install: pip install torch")
        return
    
    # Import after checking torch
    from bomber_game.agents.ppo_agent import ActorCritic
    
    # Model parameters
    state_size = 13 * 13 + 20  # 189 features
    action_size = 10
    
    print(f"📊 Model Configuration:")
    print(f"   State size: {state_size}")
    print(f"   Action size: {action_size}")
    print(f"   Architecture: Actor-Critic")
    print()
    
    # Create model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ActorCritic(state_size, action_size).to(device)
    
    # Smart initialization
    print("🧠 Applying smart initialization...")
    
    # 1. Orthogonal initialization for better gradient flow
    for m in model.modules():
        if isinstance(m, nn.Linear):
            nn.init.orthogonal_(m.weight, gain=np.sqrt(2))
            nn.init.constant_(m.bias, 0.0)
    
    # 2. Adjust actor output layer for exploration
    # Initialize last layer of actor with smaller weights
    with torch.no_grad():
        for param in model.actor[-2].parameters():  # Last linear layer before softmax
            param.data *= 0.01  # Small weights = more uniform initial policy
    
    # 3. Initialize critic to predict reasonable values
    with torch.no_grad():
        model.critic[-1].bias.data.fill_(0.0)  # Start with zero value estimates
    
    print("✅ Smart initialization complete!")
    print()
    
    # Create optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
    
    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, MODEL_PATH)
    
    print(f"💾 Pre-trained model saved to: {MODEL_PATH}")
    print()
    
    # Model summary
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print("📈 Model Summary:")
    print(f"   Total parameters: {total_params:,}")
    print(f"   Trainable parameters: {trainable_params:,}")
    print()
    
    # Test forward pass
    print("🧪 Testing model...")
    test_state = torch.randn(1, state_size).to(device)
    with torch.no_grad():
        action_probs, value = model(test_state)
        print(f"   Action probs shape: {action_probs.shape}")
        print(f"   Value shape: {value.shape}")
        print(f"   Action probs sum: {action_probs.sum().item():.4f} (should be ~1.0)")
    
    print()
    print("=" * 70)
    print("✅ PRE-TRAINED MODEL CREATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("📚 Next Steps:")
    print("   1. Train: ./train_ppo_agent.py")
    print("   2. Or copy to: bomber_game/models/ppo_agent.pth")
    print("   3. Play: ./launch_bomberman.sh")
    print()


if __name__ == "__main__":
    create_pretrained_model()
