#!/usr/bin/env python3
"""
Benchmark Enhanced Heuristic Agent

Tests the enhanced heuristic (based on 2021 paper) against:
1. Simple AI (baseline)
2. Improved Heuristic (current 30% win rate)

Target: 40%+ win rate (10% improvement)

Paper's results:
- Beam Search: 96.6% vs MCTS, 99% vs RHEA
- Opponent Prediction: +25.2% win rate
- Survivability Checking: +1.8% win rate
"""

import sys
import os
import time
import json
from collections import defaultdict

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game.game_state import GameState
from bomber_game.heuristics_improved import ImprovedHeuristicAgent
from bomber_game.heuristics_enhanced import EnhancedHeuristicAgent
from bomber_game.agents.simple_agent import SimpleAgent
from bomber_game import TILE_SIZE


class BenchmarkRunner:
    """Run comprehensive benchmarks."""
    
    def __init__(self):
        self.results = {
            'enhanced_vs_simple': {'wins': 0, 'losses': 0, 'draws': 0, 'rewards': []},
            'enhanced_vs_improved': {'wins': 0, 'losses': 0, 'draws': 0, 'rewards': []},
            'improved_vs_simple': {'wins': 0, 'losses': 0, 'draws': 0, 'rewards': []},
        }
    
    def run_game(self, player1_type, player2_type, game_num, total_games, verbose=False):
        """Run a single game."""
        game_state = GameState()
        
        # Add players
        player1 = game_state.add_player(1, 1, (255, 0, 0), f"{player1_type}_1")
        player2 = game_state.add_player(11, 11, (0, 0, 255), f"{player2_type}_2")
        
        # Create agents
        if player1_type == 'enhanced':
            agent1 = EnhancedHeuristicAgent(player1)
        elif player1_type == 'improved':
            agent1 = ImprovedHeuristicAgent(player1)
        else:  # simple
            agent1 = SimpleAgent(player1)
        
        if player2_type == 'enhanced':
            agent2 = EnhancedHeuristicAgent(player2)
        elif player2_type == 'improved':
            agent2 = ImprovedHeuristicAgent(player2)
        else:  # simple
            agent2 = SimpleAgent(player2)
        
        # Run game
        max_steps = 1000
        step = 0
        
        while not game_state.game_over and step < max_steps:
            # Get actions
            action1 = agent1.update(0.1, game_state)
            action2 = agent2.update(0.1, game_state)
            
            # Apply actions
            if action1 and player1.alive:
                dx, dy, place_bomb = action1
                player1.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                if place_bomb:
                    game_state.place_bomb(player1)
            
            if action2 and player2.alive:
                dx, dy, place_bomb = action2
                player2.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                if place_bomb:
                    game_state.place_bomb(player2)
            
            # Update game
            game_state.update(0.1)
            step += 1
        
        # Determine winner
        p1_alive = player1.alive
        p2_alive = player2.alive
        
        if p1_alive and not p2_alive:
            result = 'p1_win'
        elif p2_alive and not p1_alive:
            result = 'p2_win'
        else:
            result = 'draw'
        
        if verbose and game_num % 10 == 0:
            print(f"  Game {game_num}/{total_games}: {result} (steps: {step})")
        
        return result, 0, 0  # Scores not tracked in this version
    
    def run_benchmark(self, matchup, num_games=100, verbose=True):
        """Run benchmark for a specific matchup."""
        player1_type, player2_type = matchup.split('_vs_')
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"🎮 Benchmark: {matchup.upper()}")
            print(f"{'='*70}")
            print(f"Running {num_games} games...")
        
        start_time = time.time()
        
        for game_num in range(1, num_games + 1):
            result, score1, score2 = self.run_game(
                player1_type, player2_type, game_num, num_games,
                verbose=verbose
            )
            
            # Record results
            if result == 'p1_win':
                self.results[matchup]['wins'] += 1
            elif result == 'p2_win':
                self.results[matchup]['losses'] += 1
            else:
                self.results[matchup]['draws'] += 1
            
            self.results[matchup]['rewards'].append(score1)
        
        elapsed = time.time() - start_time
        
        if verbose:
            self._print_results(matchup, elapsed)
    
    def _print_results(self, matchup, elapsed):
        """Print results for a matchup."""
        data = self.results[matchup]
        total = data['wins'] + data['losses'] + data['draws']
        
        win_rate = (data['wins'] / total * 100) if total > 0 else 0
        loss_rate = (data['losses'] / total * 100) if total > 0 else 0
        draw_rate = (data['draws'] / total * 100) if total > 0 else 0
        avg_reward = sum(data['rewards']) / len(data['rewards']) if data['rewards'] else 0
        
        print(f"\n📊 Results:")
        print(f"  Wins:       {data['wins']:3d} ({win_rate:5.1f}%)")
        print(f"  Losses:     {data['losses']:3d} ({loss_rate:5.1f}%)")
        print(f"  Draws:      {data['draws']:3d} ({draw_rate:5.1f}%)")
        print(f"  Avg Reward: {avg_reward:7.1f}")
        print(f"  Time:       {elapsed:.1f}s ({elapsed/total:.2f}s per game)")
    
    def run_all_benchmarks(self, games_per_matchup=100):
        """Run all benchmarks."""
        print("\n" + "="*70)
        print("🚀 ENHANCED HEURISTIC BENCHMARK SUITE")
        print("   Based on 2021 Research Paper")
        print("="*70)
        print(f"\nRunning {games_per_matchup} games per matchup...")
        print("This will take approximately 5-10 minutes.\n")
        
        # Benchmark 1: Enhanced vs Simple (should be high win rate)
        self.run_benchmark('enhanced_vs_simple', games_per_matchup)
        
        # Benchmark 2: Enhanced vs Improved (key test - should win >50%)
        self.run_benchmark('enhanced_vs_improved', games_per_matchup)
        
        # Benchmark 3: Improved vs Simple (baseline - ~30% from previous tests)
        self.run_benchmark('improved_vs_simple', games_per_matchup)
        
        # Print summary
        self._print_summary()
        
        # Save results
        self._save_results()
    
    def _print_summary(self):
        """Print comprehensive summary."""
        print("\n" + "="*70)
        print("📈 BENCHMARK SUMMARY")
        print("="*70)
        
        # Calculate key metrics
        enhanced_vs_simple_wr = self._get_win_rate('enhanced_vs_simple')
        enhanced_vs_improved_wr = self._get_win_rate('enhanced_vs_improved')
        improved_vs_simple_wr = self._get_win_rate('improved_vs_simple')
        
        print(f"\n🎯 Win Rates:")
        print(f"  Enhanced vs Simple AI:    {enhanced_vs_simple_wr:5.1f}%")
        print(f"  Enhanced vs Improved AI:  {enhanced_vs_improved_wr:5.1f}%")
        print(f"  Improved vs Simple AI:    {improved_vs_simple_wr:5.1f}% (baseline)")
        
        # Calculate improvement
        print(f"\n📊 Performance Analysis:")
        
        # Enhanced should beat improved
        if enhanced_vs_improved_wr > 50:
            improvement = enhanced_vs_improved_wr - 50
            print(f"  ✅ Enhanced beats Improved by {improvement:+.1f}%")
        else:
            print(f"  ❌ Enhanced does not beat Improved ({enhanced_vs_improved_wr:.1f}%)")
        
        # Estimate enhanced win rate vs simple
        # If enhanced beats improved X%, and improved beats simple Y%,
        # then enhanced should beat simple roughly X+Y%
        estimated_enhanced_wr = improved_vs_simple_wr + (enhanced_vs_improved_wr - 50)
        print(f"  📈 Estimated Enhanced win rate: {estimated_enhanced_wr:.1f}%")
        
        # Check if we hit target
        target_wr = 40.0
        if estimated_enhanced_wr >= target_wr:
            improvement_pct = estimated_enhanced_wr - improved_vs_simple_wr
            print(f"\n🎉 TARGET ACHIEVED!")
            print(f"  Target:      {target_wr:.1f}%")
            print(f"  Achieved:    {estimated_enhanced_wr:.1f}%")
            print(f"  Improvement: +{improvement_pct:.1f}% (from {improved_vs_simple_wr:.1f}%)")
        else:
            shortfall = target_wr - estimated_enhanced_wr
            print(f"\n⚠️  Target not reached")
            print(f"  Target:    {target_wr:.1f}%")
            print(f"  Achieved:  {estimated_enhanced_wr:.1f}%")
            print(f"  Shortfall: -{shortfall:.1f}%")
        
        # Paper comparison
        print(f"\n📚 Paper Comparison:")
        print(f"  Paper's Beam Search: 96.6% vs MCTS, 99% vs RHEA")
        print(f"  Our Enhanced:        {enhanced_vs_simple_wr:.1f}% vs Simple")
        print(f"  Paper's OP boost:    +25.2% win rate")
        print(f"  Our improvement:     +{enhanced_vs_improved_wr - 50:.1f}% vs baseline")
    
    def _get_win_rate(self, matchup):
        """Get win rate for a matchup."""
        data = self.results[matchup]
        total = data['wins'] + data['losses'] + data['draws']
        return (data['wins'] / total * 100) if total > 0 else 0
    
    def _save_results(self):
        """Save results to JSON."""
        output_file = 'bomber_game/models/enhanced_heuristic_benchmark.json'
        
        # Prepare data
        save_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': {},
        }
        
        for matchup, data in self.results.items():
            total = data['wins'] + data['losses'] + data['draws']
            win_rate = (data['wins'] / total * 100) if total > 0 else 0
            avg_reward = sum(data['rewards']) / len(data['rewards']) if data['rewards'] else 0
            
            save_data['results'][matchup] = {
                'wins': data['wins'],
                'losses': data['losses'],
                'draws': data['draws'],
                'total_games': total,
                'win_rate': win_rate,
                'avg_reward': avg_reward,
            }
        
        # Save
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Benchmark Enhanced Heuristic Agent')
    parser.add_argument('--games', type=int, default=100,
                       help='Number of games per matchup (default: 100)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick test with 20 games per matchup')
    parser.add_argument('--matchup', type=str, choices=['enhanced_vs_simple', 'enhanced_vs_improved', 'improved_vs_simple'],
                       help='Run specific matchup only')
    
    args = parser.parse_args()
    
    # Determine number of games
    if args.quick:
        games = 20
    else:
        games = args.games
    
    # Run benchmarks
    runner = BenchmarkRunner()
    
    if args.matchup:
        runner.run_benchmark(args.matchup, games)
    else:
        runner.run_all_benchmarks(games)
    
    print("\n✅ Benchmark complete!\n")


if __name__ == '__main__':
    main()
