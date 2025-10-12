#!/usr/bin/env python3
"""
Complete Training Pipeline with Heuristic Bootstrap
1. Bootstrap with heuristics (if needed)
2. Continue with reinforcement learning
3. Save and persist progress
"""

import sys
import os
import subprocess

# Suppress warnings
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

MODEL_PATH = "bomber_game/models/ppo_agent.pth"
BOOTSTRAP_STATS = "bomber_game/models/bootstrap_stats.json"


def print_header():
    """Print training header."""
    print("\n" + "=" * 80)
    print("🚀 COMPLETE AI TRAINING PIPELINE")
    print("=" * 80)
    print()
    print("📋 Training Steps:")
    print("   1️⃣  Bootstrap with heuristics (teach basic strategies)")
    print("   2️⃣  Reinforcement learning (5-minute sessions)")
    print("   3️⃣  Persistent model storage")
    print()
    print("=" * 80)
    print()


def check_bootstrap_needed():
    """Check if bootstrap training is needed."""
    if not os.path.exists(MODEL_PATH):
        return True
    
    if not os.path.exists(BOOTSTRAP_STATS):
        return True
    
    # Check model size (empty models are small)
    if os.path.getsize(MODEL_PATH) < 1000:
        return True
    
    return False


def run_bootstrap():
    """Run bootstrap training."""
    print("🎓 Step 1: Bootstrap Training with Heuristics")
    print("=" * 80)
    print()
    print("📚 Teaching the AI basic game strategies...")
    print("   This will take a few minutes...")
    print()
    
    # Run bootstrap script
    result = subprocess.run(
        [sys.executable, "bootstrap_agent.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    if result.returncode != 0:
        print("\n❌ Bootstrap training failed!")
        return False
    
    print("\n✅ Bootstrap training complete!")
    return True


def run_training():
    """Run main training."""
    print("\n🎮 Step 2: Reinforcement Learning Training")
    print("=" * 80)
    print()
    print("🧠 Continuing training with reinforcement learning...")
    print("   Duration: 5 minutes")
    print("   Auto-save: Every 30 seconds")
    print()
    
    # Run training script
    result = subprocess.run(
        [sys.executable, "quick_train_agent.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    if result.returncode != 0:
        print("\n❌ Training failed!")
        return False
    
    print("\n✅ Training complete!")
    return True


def main():
    """Main training pipeline."""
    print_header()
    
    # Check if bootstrap is needed
    needs_bootstrap = check_bootstrap_needed()
    
    if needs_bootstrap:
        print("🔍 No trained model found or bootstrap needed")
        print("   Starting from scratch with heuristic bootstrap...")
        print()
        
        if not run_bootstrap():
            print("\n❌ Training pipeline failed at bootstrap stage")
            return 1
    else:
        print("✅ Found existing trained model")
        print("   Skipping bootstrap, continuing with reinforcement learning...")
        print()
    
    # Run main training
    if not run_training():
        print("\n❌ Training pipeline failed at training stage")
        return 1
    
    # Success summary
    print("\n" + "=" * 80)
    print("🎉 TRAINING PIPELINE COMPLETE!")
    print("=" * 80)
    print()
    print("✅ Your AI agent is now trained and ready!")
    print()
    print("📊 Model Information:")
    print(f"   Location: {MODEL_PATH}")
    print(f"   Size: {os.path.getsize(MODEL_PATH) / 1024:.1f} KB")
    print()
    print("🎮 Next Steps:")
    print("   • Test your AI: ./launch_bomberman.sh")
    print("   • Continue training: ./train_with_heuristics.py")
    print("   • Quick session: ./quick_train_agent.py")
    print()
    print("=" * 80)
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
