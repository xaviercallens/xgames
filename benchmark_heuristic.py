#!/usr/bin/env python3
"""
Benchmark Heuristic Agent Performance.
Runs actual test games to measure real win rate.
"""

import sys
import time
from bomber_game.game_state import GameState
from bomber_game.heuristics_improved import ImprovedHeuristicAgent
from bomber_game.agents import SimpleAgent
from bomber_game import GRID_SIZE, GREEN, RED, TILE_SIZE
import json
from pathlib import Path


def run_test_game(game_id, verbose=False):
    """
    Run a single test game between heuristic AI and simple AI.
    Returns: (winner, duration, stats)
    """
    # Create game state
    game_state = GameState(GRID_SIZE)
    player1 = game_state.add_player(1, 1, GREEN, "Heuristic")
    player2 = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, RED, "Simple")
    
    # Create agents
    heuristic_agent = ImprovedHeuristicAgent(player1)
    simple_agent = SimpleAgent(player2)
    
    # Run game
    start_time = time.time()
    steps = 0
    max_steps = 3000  # ~50 seconds at 60 FPS
    dt = 0.016  # 60 FPS
    
    while not game_state.game_over and steps < max_steps:
        # Update heuristic agent
        if player1.alive:
            action = heuristic_agent.update(dt, game_state)
            if action:
                dx, dy, place_bomb = action
                player1.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                if place_bomb:
                    game_state.place_bomb(player1)
        
        # Update simple agent
        if player2.alive:
            action = simple_agent.update(dt, game_state)
            if action:
                dx, dy, place_bomb = action
                player2.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                if place_bomb:
                    game_state.place_bomb(player2)
        
        # Update game state
        game_state.update(dt)
        steps += 1
    
    duration = time.time() - start_time
    
    # Determine winner
    if game_state.winner:
        winner = game_state.winner.name
    else:
        winner = "Draw"
    
    stats = {
        'game_id': game_id,
        'winner': winner,
        'duration': duration,
        'steps': steps,
        'heuristic_alive': player1.alive,
        'simple_alive': player2.alive,
    }
    
    if verbose:
        print(f"  Game {game_id}: {winner} wins in {duration:.1f}s ({steps} steps)")
    
    return winner, duration, stats


def benchmark_heuristic(num_games=100, save_results=True):
    """
    Benchmark heuristic agent over multiple games.
    """
    print("=" * 70)
    print("🧪 HEURISTIC AGENT BENCHMARK")
    print("=" * 70)
    print(f"Running {num_games} test games...")
    print(f"Heuristic AI vs Simple AI")
    print()
    
    results = {
        'total_games': num_games,
        'heuristic_wins': 0,
        'simple_wins': 0,
        'draws': 0,
        'total_duration': 0,
        'games': [],
    }
    
    start_time = time.time()
    
    for i in range(num_games):
        winner, duration, stats = run_test_game(i + 1, verbose=(i % 10 == 0))
        
        if winner == "Heuristic":
            results['heuristic_wins'] += 1
        elif winner == "Simple":
            results['simple_wins'] += 1
        else:
            results['draws'] += 1
        
        results['total_duration'] += duration
        results['games'].append(stats)
        
        # Progress update
        if (i + 1) % 10 == 0:
            current_wr = (results['heuristic_wins'] / (i + 1)) * 100
            print(f"  Progress: {i + 1}/{num_games} - Current WR: {current_wr:.1f}%")
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    results['win_rate'] = (results['heuristic_wins'] / num_games) * 100
    results['avg_game_duration'] = results['total_duration'] / num_games
    results['total_benchmark_time'] = total_time
    
    # Print results
    print()
    print("=" * 70)
    print("📊 BENCHMARK RESULTS")
    print("=" * 70)
    print(f"Total Games:        {num_games}")
    print(f"Heuristic Wins:     {results['heuristic_wins']} ({results['win_rate']:.1f}%)")
    print(f"Simple Wins:        {results['simple_wins']} ({(results['simple_wins']/num_games)*100:.1f}%)")
    print(f"Draws:              {results['draws']} ({(results['draws']/num_games)*100:.1f}%)")
    print()
    print(f"Avg Game Duration:  {results['avg_game_duration']:.2f}s")
    print(f"Total Time:         {total_time:.1f}s")
    print(f"Games/Second:       {num_games/total_time:.2f}")
    print("=" * 70)
    
    # Save results
    if save_results:
        output_file = Path("bomber_game/models/heuristic_benchmark.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Update model selector data
        update_model_selector_data(results['win_rate'])
    
    return results


def update_model_selector_data(heuristic_win_rate):
    """Update model selector with heuristic benchmark data."""
    from datetime import datetime
    
    selector_file = Path("bomber_game/models/heuristic_stats.json")
    
    # Load benchmark data for complete stats
    benchmark_file = Path("bomber_game/models/heuristic_benchmark.json")
    total_games = 0
    total_wins = 0
    
    if benchmark_file.exists():
        with open(benchmark_file, 'r') as f:
            benchmark_data = json.load(f)
            total_games = benchmark_data.get('total_games', 0)
            total_wins = benchmark_data.get('heuristic_wins', 0)
    
    data = {
        'model_type': 'heuristic',
        'total_episodes': total_games,
        'total_wins': total_wins,
        'win_rate': heuristic_win_rate,
        'agent_type': 'improved_heuristic',
        'benchmarked': True,
        'description': 'Heuristic agent (benchmarked)',
        'last_updated': datetime.now().isoformat()
    }
    
    with open(selector_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Updated heuristic stats: {heuristic_win_rate:.1f}% win rate")


def compare_with_ppo():
    """Compare heuristic performance with PPO model."""
    print("\n" + "=" * 70)
    print("⚖️  PERFORMANCE COMPARISON")
    print("=" * 70)
    
    # Load heuristic results
    heuristic_file = Path("bomber_game/models/heuristic_benchmark.json")
    if not heuristic_file.exists():
        print("❌ Heuristic benchmark not found. Run benchmark first.")
        return
    
    with open(heuristic_file, 'r') as f:
        heuristic_data = json.load(f)
    
    # Load PPO results
    ppo_file = Path("bomber_game/models/training_stats.json")
    ppo_win_rate = 0.0
    if ppo_file.exists():
        with open(ppo_file, 'r') as f:
            ppo_data = json.load(f)
            total_episodes = ppo_data.get('total_episodes', 0)
            total_wins = ppo_data.get('total_wins', 0)
            ppo_win_rate = (total_wins / total_episodes * 100) if total_episodes > 0 else 0
    
    heuristic_wr = heuristic_data['win_rate']
    
    print(f"Heuristic Agent:    {heuristic_wr:.1f}%")
    print(f"PPO Model:          {ppo_win_rate:.1f}%")
    print()
    
    if ppo_win_rate > heuristic_wr:
        diff = ppo_win_rate - heuristic_wr
        print(f"✅ PPO outperforms heuristic by {diff:.1f}%")
        print(f"   PPO is {(ppo_win_rate/heuristic_wr):.2f}x better")
    elif heuristic_wr > ppo_win_rate:
        diff = heuristic_wr - ppo_win_rate
        print(f"⚠️  Heuristic outperforms PPO by {diff:.1f}%")
        print(f"   Heuristic is {(heuristic_wr/ppo_win_rate):.2f}x better")
        print(f"   💡 PPO needs more training!")
    else:
        print(f"🤝 Both agents perform equally")
    
    print("=" * 70)


def main():
    """Main benchmark script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Benchmark heuristic agent')
    parser.add_argument('--games', type=int, default=100,
                       help='Number of games to run (default: 100)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick test with 20 games')
    parser.add_argument('--compare', action='store_true',
                       help='Compare with PPO after benchmark')
    
    args = parser.parse_args()
    
    num_games = 20 if args.quick else args.games
    
    # Run benchmark
    results = benchmark_heuristic(num_games=num_games)
    
    # Compare with PPO
    if args.compare:
        compare_with_ppo()
    
    print("\n✅ Benchmark complete!")
    print(f"   Heuristic Win Rate: {results['win_rate']:.1f}%")
    print(f"   Use this for accurate model comparison")


if __name__ == "__main__":
    main()
