#!/usr/bin/env python3
"""
Analyze Model Performance - Review PPO and Heuristic performance.
Tests models across different game modes and identifies issues.
"""

import sys
import time
from pathlib import Path
from bomber_game.game_state import GameState
from bomber_game.heuristics_improved import ImprovedHeuristicAgent
from bomber_game.agents import SimpleAgent, PPOAgent
from bomber_game import GRID_SIZE, GREEN, RED, TILE_SIZE
from bomber_game.model_history import ModelHistory, HeuristicPerformanceTracker
import json


def test_agent_vs_opponent(agent, opponent, agent_name, opponent_name, num_games=50, verbose=False):
    """
    Test an agent against an opponent.
    Returns: (wins, losses, draws, avg_reward, game_durations)
    """
    wins = 0
    losses = 0
    draws = 0
    total_reward = 0
    durations = []
    
    print(f"\nTesting {agent_name} vs {opponent_name} ({num_games} games)...")
    
    for game_num in range(num_games):
        # Create game
        game_state = GameState(GRID_SIZE)
        player1 = game_state.add_player(1, 1, GREEN, agent_name)
        player2 = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, RED, opponent_name)
        
        # Assign agents
        if agent_name == "Heuristic":
            agent_obj = ImprovedHeuristicAgent(player1)
        elif agent_name == "PPO":
            agent_obj = agent
        else:
            agent_obj = SimpleAgent(player1)
        
        if opponent_name == "Simple":
            opponent_obj = SimpleAgent(player2)
        elif opponent_name == "Heuristic":
            opponent_obj = ImprovedHeuristicAgent(player2)
        else:
            opponent_obj = opponent
        
        # Run game
        start_time = time.time()
        steps = 0
        max_steps = 3000
        dt = 0.016
        game_reward = 0
        
        while not game_state.game_over and steps < max_steps:
            # Agent action
            if player1.alive:
                action = agent_obj.update(dt, game_state)
                if action:
                    dx, dy, place_bomb = action
                    player1.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                    if place_bomb:
                        game_state.place_bomb(player1)
                    # Simple reward tracking
                    if not player1.alive:
                        game_reward -= 300  # Death penalty
                    elif not player2.alive:
                        game_reward += 500  # Kill reward
            
            # Opponent action
            if player2.alive:
                action = opponent_obj.update(dt, game_state)
                if action:
                    dx, dy, place_bomb = action
                    player2.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                    if place_bomb:
                        game_state.place_bomb(player2)
            
            game_state.update(dt)
            steps += 1
        
        duration = time.time() - start_time
        durations.append(duration)
        
        # Determine outcome
        if game_state.winner == player1:
            wins += 1
        elif game_state.winner == player2:
            losses += 1
        else:
            draws += 1
        
        total_reward += game_reward
        
        if verbose and (game_num + 1) % 10 == 0:
            current_wr = (wins / (game_num + 1)) * 100
            print(f"  Progress: {game_num + 1}/{num_games} - WR: {current_wr:.1f}%")
    
    avg_reward = total_reward / num_games
    avg_duration = sum(durations) / len(durations)
    
    return wins, losses, draws, avg_reward, avg_duration


def analyze_ppo_performance():
    """Analyze PPO model performance across different modes."""
    print("=" * 70)
    print("🤖 PPO MODEL PERFORMANCE ANALYSIS")
    print("=" * 70)
    
    models_dir = Path("bomber_game/models")
    ppo_model = models_dir / "ppo_agent.pth"
    
    if not ppo_model.exists():
        print("❌ PPO model not found!")
        return
    
    # Load PPO agent
    from bomber_game.game_state import GameState
    game_state = GameState(GRID_SIZE)
    dummy_player = game_state.add_player(1, 1, GREEN, "PPO")
    
    try:
        ppo_agent = PPOAgent(dummy_player, model_path=str(ppo_model), training=False)
    except Exception as e:
        print(f"❌ Error loading PPO model: {e}")
        return
    
    # Test against different opponents
    results = {}
    
    # 1. vs Simple AI
    print("\n📊 Mode 1: vs Simple AI")
    wins, losses, draws, avg_reward, avg_duration = test_agent_vs_opponent(
        ppo_agent, None, "PPO", "Simple", num_games=50, verbose=True
    )
    
    win_rate = (wins / 50) * 100
    results['vs_simple'] = {
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'win_rate': win_rate,
        'avg_reward': avg_reward,
        'avg_duration': avg_duration,
    }
    
    print(f"\n  Results:")
    print(f"    Wins: {wins}/50 ({win_rate:.1f}%)")
    print(f"    Losses: {losses}")
    print(f"    Draws: {draws}")
    print(f"    Avg Reward: {avg_reward:.2f}")
    print(f"    Avg Duration: {avg_duration:.2f}s")
    
    # 2. vs Heuristic AI
    print("\n📊 Mode 2: vs Heuristic AI")
    wins, losses, draws, avg_reward, avg_duration = test_agent_vs_opponent(
        ppo_agent, None, "PPO", "Heuristic", num_games=50, verbose=True
    )
    
    win_rate = (wins / 50) * 100
    results['vs_heuristic'] = {
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'win_rate': win_rate,
        'avg_reward': avg_reward,
        'avg_duration': avg_duration,
    }
    
    print(f"\n  Results:")
    print(f"    Wins: {wins}/50 ({win_rate:.1f}%)")
    print(f"    Losses: {losses}")
    print(f"    Draws: {draws}")
    print(f"    Avg Reward: {avg_reward:.2f}")
    print(f"    Avg Duration: {avg_duration:.2f}s")
    
    # Summary
    print("\n" + "=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)
    
    for mode, data in results.items():
        print(f"\n{mode}:")
        print(f"  Win Rate: {data['win_rate']:.1f}%")
        print(f"  Avg Reward: {data['avg_reward']:.2f}")
        
        # Performance assessment
        if data['win_rate'] < 10:
            print(f"  Assessment: ⚠️ Needs significant training")
        elif data['win_rate'] < 30:
            print(f"  Assessment: 📚 Learning, needs more training")
        elif data['win_rate'] < 50:
            print(f"  Assessment: 🎯 Good progress, approaching competitive")
        else:
            print(f"  Assessment: 🏆 Strong performance!")
    
    # Save results
    results_file = models_dir / "ppo_performance_analysis.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to {results_file}")
    
    return results


def analyze_heuristic_performance():
    """Analyze heuristic performance and check for degradation."""
    print("\n" + "=" * 70)
    print("🎯 HEURISTIC PERFORMANCE ANALYSIS")
    print("=" * 70)
    
    # Test heuristic vs simple
    print("\n📊 Testing Heuristic vs Simple AI (100 games)...")
    
    wins, losses, draws, avg_reward, avg_duration = test_agent_vs_opponent(
        None, None, "Heuristic", "Simple", num_games=100, verbose=True
    )
    
    win_rate = (wins / 100) * 100
    
    print(f"\n  Results:")
    print(f"    Wins: {wins}/100 ({win_rate:.1f}%)")
    print(f"    Losses: {losses}")
    print(f"    Draws: {draws}")
    print(f"    Avg Duration: {avg_duration:.2f}s")
    
    # Compare with benchmark
    benchmark_file = Path("bomber_game/models/heuristic_benchmark.json")
    if benchmark_file.exists():
        with open(benchmark_file, 'r') as f:
            benchmark = json.load(f)
        
        benchmark_wr = benchmark.get('win_rate', 0)
        difference = win_rate - benchmark_wr
        
        print(f"\n  Comparison with Benchmark:")
        print(f"    Benchmark WR: {benchmark_wr:.1f}%")
        print(f"    Current WR:   {win_rate:.1f}%")
        print(f"    Difference:   {difference:+.1f}%")
        
        if abs(difference) < 5:
            print(f"    Status: ✅ Performance is stable")
        elif difference > 0:
            print(f"    Status: 📈 Performance improved!")
        else:
            print(f"    Status: ⚠️ Performance degraded - investigating...")
            
            # Investigate causes
            print(f"\n  Possible causes of degradation:")
            print(f"    • Random variance (run more games)")
            print(f"    • Opponent AI improved")
            print(f"    • Game mechanics changed")
            print(f"    • Heuristic weights need tuning")
    
    # Record in tracker
    tracker = HeuristicPerformanceTracker()
    tracker.record_session("Simple AI", 100, wins, losses, draws)
    
    print("\n" + tracker.generate_report())
    
    return win_rate


def main():
    """Main analysis script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze model performance')
    parser.add_argument('--ppo', action='store_true', help='Analyze PPO model')
    parser.add_argument('--heuristic', action='store_true', help='Analyze heuristic')
    parser.add_argument('--all', action='store_true', help='Analyze all models')
    parser.add_argument('--quick', action='store_true', help='Quick test (20 games)')
    
    args = parser.parse_args()
    
    if not (args.ppo or args.heuristic or args.all):
        args.all = True
    
    if args.all or args.ppo:
        analyze_ppo_performance()
    
    if args.all or args.heuristic:
        analyze_heuristic_performance()
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
