#!/usr/bin/env python3
"""
Benchmark script to compare original PPO vs optimized PPO performance.
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import torch
    from bomber_game.entities import Player
    from bomber_game.agents.ppo_agent import PPOAgent
    from bomber_game.agents.ppo_agent_optimized import OptimizedPPOAgent
    from bomber_game.game_state import GameState
    from bomber_game import GRID_SIZE
except ImportError as e:
    print(f"Error importing: {e}")
    print("Make sure PyTorch is installed: pip install torch")
    sys.exit(1)


def benchmark_forward_pass(agent_class, num_iterations=1000):
    """Benchmark forward pass speed."""
    player = Player(1, 1, (255, 0, 0), "Test")
    agent = agent_class(player, training=False)
    
    if agent.policy is None:
        return None
    
    # Create dummy state
    game_state = GameState(GRID_SIZE)
    game_state.players = [player]
    
    # Warmup
    for _ in range(10):
        agent.choose_action(game_state)
    
    # Benchmark
    start_time = time.time()
    for _ in range(num_iterations):
        agent.choose_action(game_state)
    elapsed = time.time() - start_time
    
    return elapsed / num_iterations * 1000  # ms per forward pass


def benchmark_training_update(agent_class, buffer_size=2048):
    """Benchmark training update speed."""
    player = Player(1, 1, (255, 0, 0), "Test")
    agent = agent_class(player, training=True)
    
    if agent.policy is None:
        return None
    
    # Create dummy experiences
    game_state = GameState(GRID_SIZE)
    game_state.players = [player]
    
    # Fill buffer
    for _ in range(buffer_size):
        action = agent.choose_action(game_state)
        agent.store_reward(np.random.randn(), False)
    
    # Benchmark update
    start_time = time.time()
    agent.update_policy()
    elapsed = time.time() - start_time
    
    return elapsed * 1000  # ms


def count_parameters(agent_class):
    """Count number of parameters in model."""
    player = Player(1, 1, (255, 0, 0), "Test")
    agent = agent_class(player, training=False)
    
    if agent.policy is None:
        return None
    
    return sum(p.numel() for p in agent.policy.parameters())


def measure_memory_usage(agent_class):
    """Measure approximate memory usage."""
    player = Player(1, 1, (255, 0, 0), "Test")
    agent = agent_class(player, training=True)
    
    if agent.policy is None:
        return None
    
    # Estimate memory
    param_memory = sum(p.numel() * p.element_size() for p in agent.policy.parameters())
    buffer_memory = 0
    
    if hasattr(agent, 'buffer'):
        # Optimized agent
        buffer_memory = agent.buffer.buffer_size * (189 * 4 + 4 * 5)  # state + metadata
    elif hasattr(agent, 'memory'):
        # Original agent
        buffer_memory = 2048 * (189 * 4 + 4 * 5)  # estimate
    
    total_mb = (param_memory + buffer_memory) / (1024 * 1024)
    return total_mb


def main():
    """Run benchmarks."""
    print("=" * 70)
    print("🔬 PPO PERFORMANCE BENCHMARK")
    print("=" * 70)
    print()
    
    print(f"PyTorch version: {torch.__version__}")
    print(f"Device: CPU")
    print(f"Threads: {torch.get_num_threads()}")
    print()
    
    print("=" * 70)
    print("📊 BENCHMARK RESULTS")
    print("=" * 70)
    print()
    
    # Forward pass benchmark
    print("1️⃣  Forward Pass Speed (1000 iterations)")
    print("-" * 70)
    
    original_forward = benchmark_forward_pass(PPOAgent)
    optimized_forward = benchmark_forward_pass(OptimizedPPOAgent)
    
    if original_forward and optimized_forward:
        improvement = (original_forward - optimized_forward) / original_forward * 100
        print(f"   Original PPO:    {original_forward:.2f} ms/forward")
        print(f"   Optimized PPO:   {optimized_forward:.2f} ms/forward")
        print(f"   Improvement:     {improvement:+.1f}% faster")
    else:
        print("   ⚠️  Could not benchmark (PyTorch not available)")
    print()
    
    # Training update benchmark
    print("2️⃣  Training Update Speed (2048 experiences)")
    print("-" * 70)
    
    original_update = benchmark_training_update(PPOAgent)
    optimized_update = benchmark_training_update(OptimizedPPOAgent)
    
    if original_update and optimized_update:
        improvement = (original_update - optimized_update) / original_update * 100
        print(f"   Original PPO:    {original_update:.0f} ms/update")
        print(f"   Optimized PPO:   {optimized_update:.0f} ms/update")
        print(f"   Improvement:     {improvement:+.1f}% faster")
    else:
        print("   ⚠️  Could not benchmark (PyTorch not available)")
    print()
    
    # Parameter count
    print("3️⃣  Model Size")
    print("-" * 70)
    
    original_params = count_parameters(PPOAgent)
    optimized_params = count_parameters(OptimizedPPOAgent)
    
    if original_params and optimized_params:
        reduction = (original_params - optimized_params) / original_params * 100
        print(f"   Original PPO:    {original_params:,} parameters")
        print(f"   Optimized PPO:   {optimized_params:,} parameters")
        print(f"   Reduction:       {reduction:.1f}% smaller")
    else:
        print("   ⚠️  Could not count parameters")
    print()
    
    # Memory usage
    print("4️⃣  Memory Usage (estimated)")
    print("-" * 70)
    
    original_memory = measure_memory_usage(PPOAgent)
    optimized_memory = measure_memory_usage(OptimizedPPOAgent)
    
    if original_memory and optimized_memory:
        reduction = (original_memory - optimized_memory) / original_memory * 100
        print(f"   Original PPO:    {original_memory:.1f} MB")
        print(f"   Optimized PPO:   {optimized_memory:.1f} MB")
        print(f"   Reduction:       {reduction:.1f}% less memory")
    else:
        print("   ⚠️  Could not measure memory")
    print()
    
    # Summary
    print("=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)
    print()
    
    if all([original_forward, optimized_forward, original_update, optimized_update]):
        forward_speedup = original_forward / optimized_forward
        update_speedup = original_update / optimized_update
        overall_speedup = (forward_speedup + update_speedup) / 2
        
        print(f"   Forward Pass:    {forward_speedup:.2f}x faster")
        print(f"   Training Update: {update_speedup:.2f}x faster")
        print(f"   Overall:         {overall_speedup:.2f}x speedup")
        print()
        print(f"   🚀 Expected training time reduction: ~{(1 - 1/overall_speedup)*100:.0f}%")
    else:
        print("   ⚠️  Incomplete benchmark results")
    
    print()
    print("=" * 70)
    print()
    print("💡 Tips:")
    print("   • Use optimized PPO for faster CPU training")
    print("   • Original PPO may be better for GPU training")
    print("   • Adjust hyperparameters based on your hardware")
    print()
    print("📚 See RL_OPTIMIZATION_GUIDE.md for more details")
    print()


if __name__ == "__main__":
    main()
