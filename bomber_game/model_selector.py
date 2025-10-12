"""
Intelligent Model Selector
Automatically chooses the best AI model based on performance statistics.
"""

import os
import json
import shutil
from datetime import datetime


class ModelSelector:
    """Selects the best performing AI model based on win rate statistics."""
    
    def __init__(self, models_dir):
        """
        Initialize model selector.
        
        Args:
            models_dir: Directory containing AI models
        """
        self.models_dir = models_dir
        self.stats_file = os.path.join(models_dir, "training_stats.json")
        self.heuristic_stats_file = os.path.join(models_dir, "heuristic_stats.json")
        self.heuristic_benchmark_file = os.path.join(models_dir, "heuristic_benchmark.json")
        self.best_model_file = os.path.join(models_dir, "best_model.pth")
        self.ppo_model_file = os.path.join(models_dir, "ppo_agent.pth")
        self.pretrained_file = os.path.join(models_dir, "ppo_pretrained.pth")
        
        # Performance thresholds
        self.min_episodes_for_comparison = 50  # Minimum games before comparing
        self.heuristic_baseline_win_rate = 15.0  # Default if not benchmarked
        
    def get_model_stats(self, stats_file):
        """
        Load statistics from file.
        
        Args:
            stats_file: Path to stats JSON file
            
        Returns:
            Dictionary with stats or None
        """
        if not os.path.exists(stats_file):
            return None
            
        try:
            with open(stats_file, 'r') as f:
                stats = json.load(f)
                
            # Calculate win rate if not present
            total_episodes = stats.get('total_episodes', 0)
            total_wins = stats.get('total_wins', 0)
            
            if total_episodes > 0:
                stats['win_rate'] = (total_wins / total_episodes) * 100
            else:
                stats['win_rate'] = 0.0
                
            return stats
        except Exception as e:
            print(f"⚠️  Error loading stats from {stats_file}: {e}")
            return None
    
    def save_model_stats(self, stats, stats_file):
        """
        Save statistics to file.
        
        Args:
            stats: Statistics dictionary
            stats_file: Path to save stats
        """
        try:
            stats['last_updated'] = datetime.now().isoformat()
            with open(stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving stats to {stats_file}: {e}")
    
    def initialize_heuristic_stats(self):
        """Initialize statistics for heuristic baseline."""
        # Check if we have benchmark data
        if os.path.exists(self.heuristic_benchmark_file):
            benchmark_data = self.get_model_stats(self.heuristic_benchmark_file)
            if benchmark_data:
                # Use benchmarked win rate
                stats = {
                    'model_type': 'heuristic',
                    'total_episodes': benchmark_data.get('total_games', 0),
                    'total_wins': benchmark_data.get('heuristic_wins', 0),
                    'win_rate': benchmark_data.get('win_rate', self.heuristic_baseline_win_rate),
                    'description': 'Heuristic agent (benchmarked)',
                    'benchmarked': True,
                    'created': datetime.now().isoformat()
                }
                self.save_model_stats(stats, self.heuristic_stats_file)
                return stats
        
        # No benchmark data, use default or existing
        if not os.path.exists(self.heuristic_stats_file):
            stats = {
                'model_type': 'heuristic',
                'total_episodes': 0,
                'total_wins': 0,
                'win_rate': self.heuristic_baseline_win_rate,
                'description': 'Heuristic agent (estimated)',
                'benchmarked': False,
                'created': datetime.now().isoformat()
            }
            self.save_model_stats(stats, self.heuristic_stats_file)
            return stats
        return self.get_model_stats(self.heuristic_stats_file)
    
    def select_best_model(self):
        """
        Select the best performing model based on statistics.
        
        Returns:
            Dictionary with:
            - 'model_path': Path to best model (or 'heuristic')
            - 'model_type': Type of model
            - 'win_rate': Win rate percentage
            - 'reason': Reason for selection
        """
        print("\n" + "=" * 70)
        print("🎯 INTELLIGENT MODEL SELECTION")
        print("=" * 70)
        
        # Get statistics for all models
        ppo_stats = self.get_model_stats(self.stats_file)
        heuristic_stats = self.initialize_heuristic_stats()
        # Check if PPO model exists
        ppo_exists = os.path.exists(self.ppo_model_file)
        pretrained_exists = os.path.exists(self.pretrained_file)
        
        best_heuristic_wr = self.get_model_stats(self.heuristic_stats_file).get('win_rate', self.heuristic_baseline_win_rate)
        
        print(f"\n📊 Available Models:")
        print(f"   • Enhanced Heuristic: Always available ({best_heuristic_wr:.0f}% baseline)")
        print(f"   • PPO Model: {'✅ Found' if ppo_exists else '❌ Not found'}")
        print(f"   • Pretrained Model: {'✅ Found' if pretrained_exists else '❌ Not found'}")
        bootstrap_stats = self.get_model_stats(self.bootstrap_stats_file)
        if bootstrap_stats:
            bootstrap_wr = bootstrap_stats.get('win_rate', self.bootstrap_win_rate)
            print(f"   • Bootstrap Stats: {bootstrap_wr:.1f}% win rate ({bootstrap_stats.get('total_episodes', 0)} episodes)")
        print(f"   • 🎭 Hybrid Mode: Combines heuristics + RL (available)")
        
        result = {
            'model_path': None,
            'model_type': 'heuristic',
            'win_rate': best_heuristic_wr,
            'reason': 'Default baseline'
        }
        
        # Case 1: No trained model exists - use heuristic
        if not ppo_exists and not pretrained_exists:
            result['reason'] = 'No trained model found - using heuristic baseline'
            print(f"\n🌱 Decision: Use Heuristic Agent")
            print(f"   Reason: {result['reason']}")
            print(f"   💡 Train a model with: ./train.sh")
            return result
        
        # Case 2: Only pretrained exists - use it
        if pretrained_exists and not ppo_exists:
            result['model_path'] = self.pretrained_file
            result['model_type'] = 'ppo_pretrained'
            result['win_rate'] = 20.0  # Estimated
            result['reason'] = 'Using pretrained model (no training yet)'
            print(f"\n🎯 Decision: Use Pretrained Model")
            print(f"   Reason: {result['reason']}")
            print(f"   💡 Train more with: ./train.sh")
            return result
        
        # Case 3: PPO model exists - compare performance
        if ppo_exists and ppo_stats:
            ppo_episodes = ppo_stats.get('total_episodes', 0)
            ppo_win_rate = ppo_stats.get('win_rate', 0.0)
            
            print(f"\n📈 PPO Model Performance:")
            print(f"   Episodes: {ppo_episodes:,}")
            print(f"   Win Rate: {ppo_win_rate:.1f}%")
            
            # Not enough data yet - use pretrained or heuristic
            if ppo_episodes < self.min_episodes_for_comparison:
                if pretrained_exists:
                    result['model_path'] = self.pretrained_file
                    result['model_type'] = 'ppo_pretrained'
                    result['win_rate'] = 20.0
                    result['reason'] = f'PPO model needs more training ({ppo_episodes}/{self.min_episodes_for_comparison} episodes)'
                else:
                    result['model_path'] = 'heuristic'
                    result['reason'] = f'PPO model needs more training ({ppo_episodes}/{self.min_episodes_for_comparison} episodes)'
                
                print(f"\n⏳ Decision: {result['model_type'].upper()}")
                print(f"   Reason: {result['reason']}")
                print(f"   💡 Continue training for better performance")
                return result
            
            # Compare PPO vs Heuristic
            # CRITICAL: Use benchmarked win rate, not default
            heuristic_win_rate = heuristic_stats.get('win_rate', 0)
            if heuristic_win_rate == 0 and heuristic_stats.get('benchmarked', False):
                # Reload from benchmark file if available
                benchmark_file = os.path.join(self.models_dir, "heuristic_benchmark.json")
                if os.path.exists(benchmark_file):
                    benchmark_stats = self.get_model_stats(benchmark_file)
                    if benchmark_stats:
                        heuristic_win_rate = benchmark_stats.get('win_rate', self.heuristic_baseline_win_rate)
            
            # Fallback to baseline if still 0
            if heuristic_win_rate == 0:
                heuristic_win_rate = self.heuristic_baseline_win_rate
            
            print(f"\n⚖️  Performance Comparison:")
            print(f"   PPO Model:     {ppo_win_rate:.1f}%")
            print(f"   Heuristic:     {heuristic_win_rate:.1f}%")
            print(f"   Difference:    {ppo_win_rate - heuristic_win_rate:+.1f}%")
            
            # PPO is better - use it
            if ppo_win_rate >= heuristic_win_rate:
                result['model_path'] = self.ppo_model_file
                result['model_type'] = 'ppo'
                result['win_rate'] = ppo_win_rate
                result['reason'] = f'PPO outperforms heuristic by {ppo_win_rate - heuristic_win_rate:.1f}%'
                
                # Copy to best_model
                self._save_as_best_model(self.ppo_model_file)
                
                print(f"\n🏆 Decision: Use PPO Model")
                print(f"   Reason: {result['reason']}")
                print(f"   ✅ Saved as best model")
            else:
                # Heuristic is better - use it
                result['model_path'] = 'heuristic'
                result['reason'] = f'Heuristic outperforms PPO by {heuristic_win_rate - ppo_win_rate:.1f}%'
                
                print(f"\n🌱 Decision: Use Heuristic Agent")
                print(f"   Reason: {result['reason']}")
                print(f"   💡 PPO needs more training to beat heuristic")
                print(f"   💡 Continue training with: ./train.sh")
        
        # Case 4: PPO exists but no stats - use it cautiously
        elif ppo_exists and not ppo_stats:
            result['model_path'] = self.ppo_model_file
            result['model_type'] = 'ppo'
            result['win_rate'] = 0.0
            result['reason'] = 'PPO model found but no statistics available'
            
            print(f"\n🤖 Decision: Use PPO Model")
            print(f"   Reason: {result['reason']}")
            print(f"   ⚠️  Performance unknown - will track going forward")
        
        print("=" * 70 + "\n")
        return result
    
    def _save_as_best_model(self, model_path):
        """
        Save a model as the best performing model.
        
        Args:
            model_path: Path to model to save as best
        """
        try:
            shutil.copy2(model_path, self.best_model_file)
            print(f"   💾 Copied {os.path.basename(model_path)} → best_model.pth")
        except Exception as e:
            print(f"   ⚠️  Could not save best model: {e}")
    
    def update_heuristic_stats(self, won, game_length):
        """
        Update heuristic statistics after a game.
        
        Args:
            won: Boolean indicating if heuristic won
            game_length: Length of game in seconds
        """
        stats = self.get_model_stats(self.heuristic_stats_file)
        if not stats:
            stats = self.initialize_heuristic_stats()
        
        stats['total_episodes'] = stats.get('total_episodes', 0) + 1
        stats['total_wins'] = stats.get('total_wins', 0) + (1 if won else 0)
        stats['win_rate'] = (stats['total_wins'] / stats['total_episodes']) * 100
        
        self.save_model_stats(stats, self.heuristic_stats_file)
    
    def select_hybrid_mode(self, mode='balanced'):
        """
        Select hybrid mode combining heuristics and RL.
        
        Args:
            mode: 'heuristic_primary', 'balanced', 'rl_primary', or 'adaptive'
            
        Returns:
            Dictionary with hybrid configuration
        """
        result = {
            'model_path': 'hybrid',
            'model_type': 'hybrid',
            'mode': mode,
            'win_rate': 'estimated_high',  # Hybrid typically performs well
            'reason': f'Hybrid mode ({mode}) - combines best of both worlds'
        }
        
        print(f"\n🎭 Hybrid Mode Selected: {mode}")
        print(f"   Combines: Enhanced Heuristics + PPO Model")
        print(f"   Strategy: {mode.replace('_', ' ').title()}")
        print(f"   Benefits: Robust, adaptive, best of both worlds")
        
        return result
    
    def get_performance_report(self):
        """
        Generate a performance report for all models.
        
        Returns:
            String with formatted report
        """
        report = []
        report.append("\n" + "=" * 70)
        report.append("📊 MODEL PERFORMANCE REPORT")
        report.append("=" * 70)
        
        # Heuristic stats
        heuristic_stats = self.get_model_stats(self.heuristic_stats_file)
        if heuristic_stats:
            report.append(f"\n🌱 Heuristic Agent:")
            report.append(f"   Episodes: {heuristic_stats.get('total_episodes', 0):,}")
            report.append(f"   Wins: {heuristic_stats.get('total_wins', 0):,}")
            report.append(f"   Win Rate: {heuristic_stats.get('win_rate', 0):.1f}%")
        
        # PPO stats
        ppo_stats = self.get_model_stats(self.stats_file)
        if ppo_stats:
            report.append(f"\n🤖 PPO Model:")
            report.append(f"   Episodes: {ppo_stats.get('total_episodes', 0):,}")
            report.append(f"   Wins: {ppo_stats.get('total_wins', 0):,}")
            report.append(f"   Win Rate: {ppo_stats.get('win_rate', 0):.1f}%")
            report.append(f"   Training Time: {ppo_stats.get('total_training_time', 0) // 3600}h {(ppo_stats.get('total_training_time', 0) % 3600) // 60}m")
        
        # Hybrid mode info
        report.append(f"\n🎭 Hybrid Mode:")
        report.append(f"   Status: Available")
        report.append(f"   Modes: heuristic_primary, balanced, rl_primary, adaptive")
        report.append(f"   Description: Combines heuristics + RL for best performance")
        
        report.append("=" * 70)
        return "\n".join(report)
