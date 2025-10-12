"""
Model History Tracker - Tracks PPO model performance across different game modes.
Maintains history of all model versions with their performance metrics.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
import torch


class ModelHistory:
    """
    Tracks performance history of PPO models across different game modes.
    Stores multiple versions and selects best per mode.
    """
    
    def __init__(self, models_dir="bomber_game/models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.models_dir / "model_history.json"
        self.history = self._load_history()
        
        # Game modes
        self.game_modes = {
            'vs_simple': 'Against Simple AI',
            'vs_heuristic': 'Against Heuristic AI',
            'vs_human': 'Against Human Player',
            'training': 'Training Mode',
        }
    
    def _load_history(self):
        """Load model history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'versions': [],
            'best_per_mode': {},
            'current_version': 0,
        }
    
    def _save_history(self):
        """Save model history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving model history: {e}")
    
    def record_model_version(self, model_path, mode, performance_metrics):
        """
        Record a new model version with its performance.
        
        Args:
            model_path: Path to the model file
            mode: Game mode (vs_simple, vs_heuristic, vs_human, training)
            performance_metrics: Dict with win_rate, avg_reward, episodes, etc.
        """
        version_id = self.history['current_version'] + 1
        
        # Create version record
        version = {
            'version_id': version_id,
            'timestamp': datetime.now().isoformat(),
            'mode': mode,
            'model_file': f"ppo_agent_v{version_id}.pth",
            'performance': performance_metrics,
        }
        
        # Copy model to versioned file
        versioned_path = self.models_dir / version['model_file']
        try:
            shutil.copy2(model_path, versioned_path)
        except Exception as e:
            print(f"Warning: Could not copy model: {e}")
        
        # Add to history
        self.history['versions'].append(version)
        self.history['current_version'] = version_id
        
        # Update best per mode
        self._update_best_per_mode(version)
        
        self._save_history()
        
        return version_id
    
    def _update_best_per_mode(self, version):
        """Update best model for the given mode."""
        mode = version['mode']
        win_rate = version['performance'].get('win_rate', 0)
        
        if mode not in self.history['best_per_mode']:
            self.history['best_per_mode'][mode] = version['version_id']
        else:
            # Compare with current best
            best_id = self.history['best_per_mode'][mode]
            best_version = self._get_version(best_id)
            
            if best_version:
                best_win_rate = best_version['performance'].get('win_rate', 0)
                if win_rate > best_win_rate:
                    self.history['best_per_mode'][mode] = version['version_id']
    
    def _get_version(self, version_id):
        """Get version by ID."""
        for version in self.history['versions']:
            if version['version_id'] == version_id:
                return version
        return None
    
    def get_best_model_for_mode(self, mode):
        """Get best model for specific game mode."""
        if mode in self.history['best_per_mode']:
            version_id = self.history['best_per_mode'][mode]
            return self._get_version(version_id)
        return None
    
    def get_all_versions(self):
        """Get all model versions."""
        return self.history['versions']
    
    def get_versions_by_mode(self, mode):
        """Get all versions for specific mode."""
        return [v for v in self.history['versions'] if v['mode'] == mode]
    
    def get_performance_trend(self, mode):
        """Get performance trend for a mode."""
        versions = self.get_versions_by_mode(mode)
        
        if not versions:
            return None
        
        trend = {
            'mode': mode,
            'total_versions': len(versions),
            'win_rates': [v['performance'].get('win_rate', 0) for v in versions],
            'avg_rewards': [v['performance'].get('avg_reward', 0) for v in versions],
            'episodes': [v['performance'].get('episodes', 0) for v in versions],
            'timestamps': [v['timestamp'] for v in versions],
        }
        
        # Calculate improvement
        if len(trend['win_rates']) > 1:
            trend['improvement'] = trend['win_rates'][-1] - trend['win_rates'][0]
            trend['improvement_pct'] = (trend['improvement'] / max(trend['win_rates'][0], 0.01)) * 100
        else:
            trend['improvement'] = 0
            trend['improvement_pct'] = 0
        
        return trend
    
    def generate_report(self):
        """Generate comprehensive performance report."""
        report = []
        report.append("=" * 70)
        report.append("📊 MODEL PERFORMANCE HISTORY")
        report.append("=" * 70)
        report.append(f"Total Versions: {len(self.history['versions'])}")
        report.append("")
        
        for mode_key, mode_name in self.game_modes.items():
            report.append(f"\n{'='*70}")
            report.append(f"🎮 {mode_name}")
            report.append(f"{'='*70}")
            
            versions = self.get_versions_by_mode(mode_key)
            
            if not versions:
                report.append("  No versions recorded for this mode")
                continue
            
            report.append(f"  Total Versions: {len(versions)}")
            
            # Best version
            best = self.get_best_model_for_mode(mode_key)
            if best:
                report.append(f"\n  🏆 Best Version: v{best['version_id']}")
                report.append(f"     Win Rate: {best['performance'].get('win_rate', 0):.1f}%")
                report.append(f"     Avg Reward: {best['performance'].get('avg_reward', 0):.2f}")
                report.append(f"     Episodes: {best['performance'].get('episodes', 0):,}")
                report.append(f"     Date: {best['timestamp'][:10]}")
            
            # Latest version
            latest = versions[-1]
            report.append(f"\n  📅 Latest Version: v{latest['version_id']}")
            report.append(f"     Win Rate: {latest['performance'].get('win_rate', 0):.1f}%")
            report.append(f"     Avg Reward: {latest['performance'].get('avg_reward', 0):.2f}")
            report.append(f"     Episodes: {latest['performance'].get('episodes', 0):,}")
            
            # Trend
            trend = self.get_performance_trend(mode_key)
            if trend and trend['improvement'] != 0:
                report.append(f"\n  📈 Trend: {trend['improvement']:+.1f}% ({trend['improvement_pct']:+.1f}% change)")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)
    
    def export_to_csv(self, output_file="model_performance.csv"):
        """Export history to CSV for analysis."""
        import csv
        
        output_path = self.models_dir / output_file
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Version', 'Timestamp', 'Mode', 'Win Rate', 
                'Avg Reward', 'Episodes', 'Model File'
            ])
            
            # Data
            for version in self.history['versions']:
                perf = version['performance']
                writer.writerow([
                    version['version_id'],
                    version['timestamp'],
                    version['mode'],
                    perf.get('win_rate', 0),
                    perf.get('avg_reward', 0),
                    perf.get('episodes', 0),
                    version['model_file'],
                ])
        
        print(f"📊 Exported to {output_path}")


class HeuristicPerformanceTracker:
    """
    Tracks heuristic agent performance over time.
    Detects performance degradation.
    """
    
    def __init__(self, models_dir="bomber_game/models"):
        self.models_dir = Path(models_dir)
        self.history_file = self.models_dir / "heuristic_performance_history.json"
        self.history = self._load_history()
    
    def _load_history(self):
        """Load performance history."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'sessions': [],
            'baseline_win_rate': None,
        }
    
    def _save_history(self):
        """Save performance history."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving heuristic history: {e}")
    
    def record_session(self, opponent_type, games_played, wins, losses, draws):
        """Record a play session."""
        win_rate = (wins / games_played * 100) if games_played > 0 else 0
        
        session = {
            'timestamp': datetime.now().isoformat(),
            'opponent': opponent_type,
            'games': games_played,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': win_rate,
        }
        
        self.history['sessions'].append(session)
        
        # Set baseline if first session
        if self.history['baseline_win_rate'] is None:
            self.history['baseline_win_rate'] = win_rate
        
        self._save_history()
        
        # Check for degradation
        self._check_degradation(win_rate)
    
    def _check_degradation(self, current_win_rate):
        """Check if performance has degraded."""
        if self.history['baseline_win_rate'] is None:
            return
        
        baseline = self.history['baseline_win_rate']
        degradation = baseline - current_win_rate
        
        if degradation > 10:  # More than 10% drop
            print(f"\n⚠️  WARNING: Heuristic Performance Degradation Detected!")
            print(f"   Baseline: {baseline:.1f}%")
            print(f"   Current:  {current_win_rate:.1f}%")
            print(f"   Drop:     {degradation:.1f}%")
            print(f"\n   Possible causes:")
            print(f"   • Opponent AI has improved")
            print(f"   • Game rules changed")
            print(f"   • Random variance (run more games)")
            print(f"   • Heuristic needs tuning\n")
    
    def get_recent_performance(self, num_sessions=10):
        """Get recent performance statistics."""
        recent = self.history['sessions'][-num_sessions:]
        
        if not recent:
            return None
        
        total_games = sum(s['games'] for s in recent)
        total_wins = sum(s['wins'] for s in recent)
        
        return {
            'sessions': len(recent),
            'total_games': total_games,
            'total_wins': total_wins,
            'win_rate': (total_wins / total_games * 100) if total_games > 0 else 0,
            'baseline': self.history['baseline_win_rate'],
        }
    
    def generate_report(self):
        """Generate performance report."""
        report = []
        report.append("=" * 70)
        report.append("🎯 HEURISTIC PERFORMANCE HISTORY")
        report.append("=" * 70)
        
        if not self.history['sessions']:
            report.append("No sessions recorded yet")
            return "\n".join(report)
        
        # Baseline
        if self.history['baseline_win_rate']:
            report.append(f"Baseline Win Rate: {self.history['baseline_win_rate']:.1f}%")
        
        # Recent performance
        recent = self.get_recent_performance(10)
        if recent:
            report.append(f"\nRecent Performance (last {recent['sessions']} sessions):")
            report.append(f"  Games: {recent['total_games']}")
            report.append(f"  Wins: {recent['total_wins']}")
            report.append(f"  Win Rate: {recent['win_rate']:.1f}%")
            
            if recent['baseline']:
                change = recent['win_rate'] - recent['baseline']
                report.append(f"  Change: {change:+.1f}% from baseline")
        
        # By opponent
        report.append("\nPerformance by Opponent:")
        opponents = {}
        for session in self.history['sessions']:
            opp = session['opponent']
            if opp not in opponents:
                opponents[opp] = {'games': 0, 'wins': 0}
            opponents[opp]['games'] += session['games']
            opponents[opp]['wins'] += session['wins']
        
        for opp, stats in opponents.items():
            wr = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
            report.append(f"  {opp}: {wr:.1f}% ({stats['wins']}/{stats['games']})")
        
        report.append("=" * 70)
        return "\n".join(report)


def main():
    """Test the model history system."""
    history = ModelHistory()
    
    print(history.generate_report())
    
    # Heuristic tracker
    heuristic = HeuristicPerformanceTracker()
    print("\n")
    print(heuristic.generate_report())


if __name__ == "__main__":
    main()
