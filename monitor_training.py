#!/usr/bin/env python3
"""
Training Monitor - Real-time monitoring of overnight training
Displays live progress, generates plots, and sends notifications
"""

import os
import json
import time
import sys
from datetime import datetime, timedelta

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib not available. Install with: pip install matplotlib")

MODELS_DIR = "bomber_game/models"
STATS_FILE = os.path.join(MODELS_DIR, "training_stats.json")
PROGRESS_FILE = os.path.join(MODELS_DIR, "overnight_progress.json")
PLOTS_DIR = os.path.join(MODELS_DIR, "plots")


def ensure_directories():
    """Create necessary directories."""
    os.makedirs(PLOTS_DIR, exist_ok=True)


def load_stats():
    """Load training statistics."""
    if not os.path.exists(STATS_FILE):
        return None
    
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


def load_progress():
    """Load current progress."""
    if not os.path.exists(PROGRESS_FILE):
        return None
    
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


def generate_plots(stats):
    """Generate training progress plots."""
    if not MATPLOTLIB_AVAILABLE:
        return
    
    ensure_directories()
    
    # Plot 1: Win Rate over time
    if stats.get('win_rates'):
        plt.figure(figsize=(12, 6))
        plt.plot(stats['win_rates'], linewidth=2, color='#2ecc71')
        plt.title('Win Rate Over Training', fontsize=16, fontweight='bold')
        plt.xlabel('Episode (x100)', fontsize=12)
        plt.ylabel('Win Rate (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'win_rate.png'), dpi=150)
        plt.close()
    
    # Plot 2: Average Reward over time
    if stats.get('avg_rewards'):
        plt.figure(figsize=(12, 6))
        plt.plot(stats['avg_rewards'], linewidth=2, color='#3498db')
        plt.title('Average Reward Over Training', fontsize=16, fontweight='bold')
        plt.xlabel('Episode (x100)', fontsize=12)
        plt.ylabel('Average Reward', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'avg_reward.png'), dpi=150)
        plt.close()
    
    # Plot 3: Episode Rewards (last 1000)
    if stats.get('episode_rewards'):
        recent_rewards = stats['episode_rewards'][-1000:]
        plt.figure(figsize=(12, 6))
        plt.plot(recent_rewards, linewidth=1, alpha=0.6, color='#e74c3c')
        plt.title('Recent Episode Rewards (Last 1000)', fontsize=16, fontweight='bold')
        plt.xlabel('Episode', fontsize=12)
        plt.ylabel('Reward', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'episode_rewards.png'), dpi=150)
        plt.close()
    
    # Plot 4: Combined view
    if stats.get('win_rates') and stats.get('avg_rewards'):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        ax1.plot(stats['win_rates'], linewidth=2, color='#2ecc71')
        ax1.set_title('Win Rate Progress', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Episode (x100)', fontsize=11)
        ax1.set_ylabel('Win Rate (%)', fontsize=11)
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(stats['avg_rewards'], linewidth=2, color='#3498db')
        ax2.set_title('Average Reward Progress', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Episode (x100)', fontsize=11)
        ax2.set_ylabel('Average Reward', fontsize=11)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'combined_progress.png'), dpi=150)
        plt.close()
    
    print(f"📊 Plots saved to: {PLOTS_DIR}/")


def print_status(stats, progress):
    """Print current training status."""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("\n" + "=" * 80)
    print("🔍 OVERNIGHT TRAINING MONITOR")
    print("=" * 80)
    print(f"🕐 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")
    
    if not stats or not progress:
        print("⚠️  No training data found. Training may not have started yet.")
        print(f"   Looking for: {STATS_FILE}")
        return
    
    # Current progress
    print("📊 CURRENT PROGRESS")
    print("-" * 80)
    print(f"Episode: {progress.get('episode', 0):,} / {progress.get('total_episodes', 0):,}")
    print(f"Win Rate: {progress.get('win_rate', 0):.2f}%")
    print(f"Avg Reward: {progress.get('avg_reward', 0):.2f}")
    print(f"Best Win Rate: {progress.get('best_win_rate', 0):.2f}%")
    print()
    
    # Time information
    print("⏱️  TIME INFORMATION")
    print("-" * 80)
    elapsed_hours = progress.get('elapsed_hours', 0)
    print(f"Elapsed: {timedelta(hours=elapsed_hours)}")
    print(f"Speed: {progress.get('episodes_per_hour', 0):.1f} episodes/hour")
    
    if progress.get('episodes_per_hour', 0) > 0:
        remaining_episodes = progress.get('total_episodes', 0) - progress.get('episode', 0)
        eta_hours = remaining_episodes / progress['episodes_per_hour']
        print(f"ETA: {timedelta(hours=eta_hours)}")
    print()
    
    # Overall statistics
    print("📈 OVERALL STATISTICS")
    print("-" * 80)
    print(f"Total Episodes: {stats.get('total_episodes', 0):,}")
    print(f"Total Wins: {stats.get('total_wins', 0):,}")
    print(f"Total Rewards: {stats.get('total_rewards', 0):.2f}")
    
    if stats.get('total_episodes', 0) > 0:
        overall_win_rate = (stats['total_wins'] / stats['total_episodes']) * 100
        print(f"Overall Win Rate: {overall_win_rate:.2f}%")
    print()
    
    # Recent performance
    if stats.get('win_rates') and len(stats['win_rates']) > 0:
        print("🎯 RECENT PERFORMANCE (Last 100 Episodes)")
        print("-" * 80)
        recent_win_rate = stats['win_rates'][-1]
        recent_reward = stats['avg_rewards'][-1] if stats.get('avg_rewards') else 0
        
        print(f"Win Rate: {recent_win_rate:.2f}%")
        print(f"Avg Reward: {recent_reward:.2f}")
        
        # Trend
        if len(stats['win_rates']) > 1:
            prev_win_rate = stats['win_rates'][-2]
            trend = recent_win_rate - prev_win_rate
            trend_symbol = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
            print(f"Trend: {trend_symbol} {trend:+.2f}%")
    
    print("\n" + "=" * 80)
    print("💡 Press Ctrl+C to exit monitor")
    print("=" * 80 + "\n")


def monitor_continuous(refresh_interval=30):
    """Continuously monitor training progress."""
    print("🔍 Starting training monitor...")
    print(f"📊 Refresh interval: {refresh_interval} seconds")
    print("💡 Press Ctrl+C to exit\n")
    
    try:
        while True:
            stats = load_stats()
            progress = load_progress()
            print_status(stats, progress)
            
            # Generate plots periodically
            if stats and MATPLOTLIB_AVAILABLE:
                generate_plots(stats)
            
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print("\n\n👋 Monitor stopped by user")


def print_summary():
    """Print final training summary."""
    stats = load_stats()
    
    if not stats:
        print("⚠️  No training data found")
        return
    
    print("\n" + "=" * 80)
    print("📊 TRAINING SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ Total Episodes: {stats.get('total_episodes', 0):,}")
    print(f"🏆 Total Wins: {stats.get('total_wins', 0):,}")
    print(f"💰 Total Rewards: {stats.get('total_rewards', 0):.2f}")
    
    if stats.get('total_episodes', 0) > 0:
        overall_win_rate = (stats['total_wins'] / stats['total_episodes']) * 100
        print(f"📈 Overall Win Rate: {overall_win_rate:.2f}%")
    
    if stats.get('win_rates'):
        print(f"🌟 Final Win Rate: {stats['win_rates'][-1]:.2f}%")
        print(f"🎯 Best Win Rate: {max(stats['win_rates']):.2f}%")
    
    if stats.get('avg_rewards'):
        print(f"💎 Final Avg Reward: {stats['avg_rewards'][-1]:.2f}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Generate final plots
    if MATPLOTLIB_AVAILABLE:
        print("📊 Generating final plots...")
        generate_plots(stats)
        print(f"✅ Plots saved to: {PLOTS_DIR}/\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor overnight training progress")
    parser.add_argument("--interval", type=int, default=30,
                       help="Refresh interval in seconds (default: 30)")
    parser.add_argument("--summary", action="store_true",
                       help="Print summary and exit (no continuous monitoring)")
    parser.add_argument("--plots", action="store_true",
                       help="Generate plots and exit")
    
    args = parser.parse_args()
    
    if args.summary:
        print_summary()
    elif args.plots:
        stats = load_stats()
        if stats and MATPLOTLIB_AVAILABLE:
            generate_plots(stats)
            print("✅ Plots generated")
        else:
            print("⚠️  No data or matplotlib not available")
    else:
        monitor_continuous(args.interval)
