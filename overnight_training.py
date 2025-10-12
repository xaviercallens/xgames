#!/usr/bin/env python3
"""
Overnight PPO Training Script
Optimized for long-duration training with automatic checkpointing,
progress tracking, and adaptive learning rate scheduling.

Features:
- Automatic checkpointing every N episodes
- Progress logging with timestamps
- Adaptive learning rate decay
- Early stopping if performance plateaus
- Resume from checkpoint support
- Performance visualization
- Email/notification support (optional)
"""

import sys
import os
import time
import json
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE
from bomber_game.game_state import GameState
from bomber_game.agents import PPOAgent
from bomber_game.heuristics_improved import ImprovedHeuristicAgent

# ============================================================================
# TRAINING CONFIGURATION
# ============================================================================

# Training duration
TOTAL_EPISODES = 10000
MAX_STEPS_PER_EPISODE = 500
TRAINING_HOURS = 8

# PPO Hyperparameters (optimized for overnight training)
UPDATE_INTERVAL = 4096  # Update every N steps (larger for stability)
BATCH_SIZE = 128
EPOCHS_PER_UPDATE = 10
LEARNING_RATE_START = 3e-4
LEARNING_RATE_END = 1e-5
CLIP_EPSILON = 0.2
GAMMA = 0.99  # Discount factor
GAE_LAMBDA = 0.95  # Generalized Advantage Estimation

# Checkpointing
CHECKPOINT_INTERVAL = 100  # Save every N episodes
AUTOSAVE_INTERVAL = 30 * 60  # Save every 30 minutes (in seconds)
MODELS_DIR = "bomber_game/models"
CHECKPOINT_DIR = os.path.join(MODELS_DIR, "checkpoints")

# Logging
LOG_INTERVAL = 10  # Log every N episodes
STATS_FILE = os.path.join(MODELS_DIR, "training_stats.json")
PROGRESS_FILE = os.path.join(MODELS_DIR, "overnight_progress.json")
LOG_FILE = os.path.join(MODELS_DIR, "training_log.txt")

# Performance tracking
PERFORMANCE_WINDOW = 100  # Episodes to average for performance
PLATEAU_THRESHOLD = 50  # Episodes without improvement before early stop
MIN_WIN_RATE_IMPROVEMENT = 0.01  # Minimum improvement to avoid plateau

# ============================================================================
# GLOBAL STATE
# ============================================================================

training_start_time = None
last_autosave_time = None
best_win_rate = 0.0
episodes_without_improvement = 0
should_stop = False


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global should_stop
    print("\n\n🛑 Training interrupted by user. Saving checkpoint...")
    should_stop = True


signal.signal(signal.SIGINT, signal_handler)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def ensure_directories():
    """Create necessary directories."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)


def log_message(message, to_file=True):
    """Log message to console and file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    if to_file:
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + "\n")


def get_learning_rate(episode, total_episodes):
    """Calculate learning rate with linear decay."""
    progress = episode / total_episodes
    lr = LEARNING_RATE_START + (LEARNING_RATE_END - LEARNING_RATE_START) * progress
    return lr


def load_or_create_stats():
    """Load existing stats or create new ones."""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
                log_message(f"📊 Loaded existing stats: {stats.get('total_episodes', 0)} episodes")
                return stats
        except:
            pass
    
    return {
        'total_episodes': 0,
        'total_wins': 0,
        'total_rewards': 0,
        'episode_rewards': [],
        'win_rates': [],
        'avg_rewards': [],
        'training_start': datetime.now().isoformat(),
        'total_training_time': 0
    }


def save_stats(stats):
    """Save training statistics."""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


def save_progress(episode, stats, elapsed_time):
    """Save detailed progress information."""
    progress = {
        'episode': episode,
        'total_episodes': stats['total_episodes'],
        'win_rate': stats['win_rates'][-1] if stats['win_rates'] else 0,
        'avg_reward': stats['avg_rewards'][-1] if stats['avg_rewards'] else 0,
        'elapsed_hours': elapsed_time / 3600,
        'episodes_per_hour': episode / (elapsed_time / 3600) if elapsed_time > 0 else 0,
        'timestamp': datetime.now().isoformat(),
        'best_win_rate': best_win_rate
    }
    
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def save_checkpoint(agent, episode, stats, checkpoint_type="auto"):
    """Save training checkpoint."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_name = f"checkpoint_ep{episode}_{checkpoint_type}_{timestamp}.pth"
    checkpoint_path = os.path.join(CHECKPOINT_DIR, checkpoint_name)
    
    agent.save(checkpoint_path)
    
    # Also save as latest
    latest_path = os.path.join(CHECKPOINT_DIR, "latest_checkpoint.pth")
    agent.save(latest_path)
    
    # Save checkpoint metadata
    metadata = {
        'episode': episode,
        'stats': stats,
        'timestamp': timestamp,
        'checkpoint_type': checkpoint_type
    }
    metadata_path = checkpoint_path.replace('.pth', '_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    log_message(f"💾 Checkpoint saved: {checkpoint_name}")


def find_latest_checkpoint():
    """Find the most recent checkpoint to resume from."""
    latest_path = os.path.join(CHECKPOINT_DIR, "latest_checkpoint.pth")
    if os.path.exists(latest_path):
        return latest_path
    return None


def calculate_reward(game_state, agent_player, enemy_player, prev_state, action):
    """
    Enhanced reward function for overnight training.
    Balanced to encourage both aggressive and defensive play.
    """
    reward = 0
    
    # Terminal rewards
    if not agent_player.alive:
        return -200  # Lost
    if not enemy_player.alive:
        return +200  # Won
    
    # Step penalty (encourage efficiency)
    reward -= 0.5
    
    # Reward for destroying walls
    if prev_state:
        prev_walls = sum(row.count(2) for row in prev_state['grid'])
        curr_walls = sum(row.count(2) for row in game_state.grid)
        if curr_walls < prev_walls:
            reward += 20 * (prev_walls - curr_walls)
    
    # Reward for collecting power-ups
    if prev_state and len(game_state.powerups) < prev_state['powerups']:
        reward += 15
    
    # Strategic positioning reward
    if prev_state:
        prev_dist = abs(prev_state['player_x'] - prev_state['enemy_x']) + \
                   abs(prev_state['player_y'] - prev_state['enemy_y'])
        curr_dist = abs(agent_player.grid_x - enemy_player.grid_x) + \
                   abs(agent_player.grid_y - enemy_player.grid_y)
        
        # Reward for optimal distance (not too close, not too far)
        if 3 <= curr_dist <= 5:
            reward += 3
        elif curr_dist < prev_dist and curr_dist > 2:
            reward += 5
        elif curr_dist > prev_dist and curr_dist > 6:
            reward -= 3
    
    # Bomb placement rewards
    dx, dy, place_bomb = action
    if place_bomb:
        dist_to_enemy = abs(agent_player.grid_x - enemy_player.grid_x) + \
                       abs(agent_player.grid_y - enemy_player.grid_y)
        
        # Reward for strategic bomb placement
        if 2 <= dist_to_enemy <= 4:
            reward += 20
        elif dist_to_enemy <= 1:
            reward -= 15  # Too close, dangerous
        
        # Check if bomb placement is safe
        if has_escape_route(game_state, agent_player):
            reward += 10
        else:
            reward -= 25  # Dangerous placement
    
    # Survival bonus
    if prev_state and prev_state.get('in_danger', False):
        if not is_in_danger(game_state, agent_player):
            reward += 30
    
    return reward


def has_escape_route(game_state, player):
    """Check if player has a safe escape route."""
    px, py = player.grid_x, player.grid_y
    
    # Check adjacent cells
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = px + dx, py + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            if game_state.grid[ny][nx] == 0:  # Empty cell
                return True
    return False


def is_in_danger(game_state, player):
    """Check if player is in danger from explosions."""
    px, py = player.grid_x, player.grid_y
    
    # Check for nearby bombs
    for bomb in game_state.bombs:
        bx, by = bomb.grid_x, bomb.grid_y
        if px == bx and abs(py - by) <= bomb.power:
            return True
        if py == by and abs(px - bx) <= bomb.power:
            return True
    
    return False


def get_state_dict(game_state, player, enemy):
    """Get state dictionary for tracking."""
    return {
        'grid': [row[:] for row in game_state.grid],
        'player_x': player.grid_x,
        'player_y': player.grid_y,
        'enemy_x': enemy.grid_x,
        'enemy_y': enemy.grid_y,
        'powerups': len(game_state.powerups),
        'in_danger': is_in_danger(game_state, player)
    }


def print_training_header():
    """Print training session header."""
    print("\n" + "=" * 80)
    print("🌙 OVERNIGHT PPO TRAINING SESSION")
    print("=" * 80)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target Episodes: {TOTAL_EPISODES:,}")
    print(f"⏰ Max Duration: {TRAINING_HOURS} hours")
    print(f"📊 Update Interval: {UPDATE_INTERVAL:,} steps")
    print(f"💾 Checkpoint Interval: {CHECKPOINT_INTERVAL} episodes")
    print(f"📈 Learning Rate: {LEARNING_RATE_START:.2e} → {LEARNING_RATE_END:.2e}")
    print("=" * 80 + "\n")


def print_progress(episode, stats, elapsed_time, eta):
    """Print training progress."""
    win_rate = stats['win_rates'][-1] if stats['win_rates'] else 0
    avg_reward = stats['avg_rewards'][-1] if stats['avg_rewards'] else 0
    episodes_per_hour = episode / (elapsed_time / 3600) if elapsed_time > 0 else 0
    
    print(f"\n{'=' * 80}")
    print(f"📊 Episode {episode}/{TOTAL_EPISODES} ({episode/TOTAL_EPISODES*100:.1f}%)")
    print(f"{'=' * 80}")
    print(f"🏆 Win Rate (last {PERFORMANCE_WINDOW}): {win_rate:.2f}%")
    print(f"💰 Avg Reward: {avg_reward:.2f}")
    print(f"⏱️  Elapsed: {timedelta(seconds=int(elapsed_time))}")
    print(f"⏳ ETA: {timedelta(seconds=int(eta))}")
    print(f"⚡ Speed: {episodes_per_hour:.1f} episodes/hour")
    print(f"🌟 Best Win Rate: {best_win_rate:.2f}%")
    print(f"{'=' * 80}\n")


# ============================================================================
# MAIN TRAINING LOOP
# ============================================================================

def train_overnight():
    """Main overnight training function."""
    global training_start_time, last_autosave_time, best_win_rate
    global episodes_without_improvement, should_stop
    
    ensure_directories()
    print_training_header()
    
    # Initialize
    training_start_time = time.time()
    last_autosave_time = training_start_time
    
    # Load or create stats
    stats = load_or_create_stats()
    start_episode = stats['total_episodes']
    
    # Create game state
    game_state = GameState(GRID_SIZE)
    agent_player = game_state.add_player(1, 1, (0, 255, 0), "PPO Agent")
    enemy_player = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, (255, 0, 0), "Heuristic")
    
    # Create agents
    checkpoint_path = find_latest_checkpoint()
    if checkpoint_path and start_episode > 0:
        log_message(f"📂 Resuming from checkpoint: {checkpoint_path}")
        agent = PPOAgent(agent_player, model_path=checkpoint_path, training=True)
    else:
        log_message("🆕 Starting fresh training")
        agent = PPOAgent(agent_player, training=True)
    
    enemy_agent = ImprovedHeuristicAgent(enemy_player)
    
    # Training metrics
    recent_wins = deque(maxlen=PERFORMANCE_WINDOW)
    recent_rewards = deque(maxlen=PERFORMANCE_WINDOW)
    
    # Main training loop
    episode = start_episode  # Initialize episode variable
    for episode in range(start_episode + 1, TOTAL_EPISODES + 1):
        # Check time limit
        elapsed_time = time.time() - training_start_time
        if elapsed_time > TRAINING_HOURS * 3600:
            log_message(f"⏰ Time limit reached ({TRAINING_HOURS} hours)")
            break
        
        if should_stop:
            break
        
        # Reset game - recreate game state for fresh episode
        game_state = GameState(GRID_SIZE)
        agent_player = game_state.add_player(1, 1, (0, 255, 0), "PPO Agent")
        enemy_player = game_state.add_player(GRID_SIZE - 2, GRID_SIZE - 2, (255, 0, 0), "Heuristic")
        
        # Reset agent references
        agent.player = agent_player
        enemy_agent.player = enemy_player
        
        episode_reward = 0
        prev_state = None
        
        # Episode loop
        for step in range(MAX_STEPS_PER_EPISODE):
            # Get current state
            curr_state = get_state_dict(game_state, agent_player, enemy_player)
            
            # Agent actions
            agent_action = agent.choose_action(game_state)
            enemy_action = enemy_agent.choose_action(game_state)
            
            # Execute actions
            from bomber_game import TILE_SIZE
            agent_player.move(*agent_action[:2], game_state.grid, TILE_SIZE, game_state)
            if agent_action[2]:
                game_state.place_bomb(agent_player.grid_x, agent_player.grid_y)
            
            enemy_player.move(*enemy_action[:2], game_state.grid, TILE_SIZE, game_state)
            if enemy_action[2]:
                game_state.place_bomb(enemy_player.grid_x, enemy_player.grid_y)
            
            # Update game
            game_state.update(1/FPS)  # dt = 1/FPS for consistent timing
            
            # Calculate reward
            episode_reward += reward
            
            # Store experience (if agent supports it)
            if hasattr(agent, 'store_experience'):
                agent.store_experience(curr_state, agent_action, reward, not agent_player.alive or not enemy_player.alive)
            
            prev_state = curr_state
            
            # Check if episode ended
            if not agent_player.alive or not enemy_player.alive:
                break
        
        # Record results
        won = not enemy_player.alive and agent_player.alive
        recent_wins.append(1 if won else 0)
        recent_rewards.append(episode_reward)
        
        # Update stats
        stats['total_episodes'] = episode
        stats['total_wins'] += 1 if won else 0
        stats['total_rewards'] += episode_reward
        stats['episode_rewards'].append(episode_reward)
        
        # Calculate metrics
        if len(recent_wins) >= PERFORMANCE_WINDOW:
            win_rate = sum(recent_wins) / len(recent_wins) * 100
            avg_reward = sum(recent_rewards) / len(recent_rewards)
            stats['win_rates'].append(win_rate)
            stats['avg_rewards'].append(avg_reward)
            
            # Check for improvement
            if win_rate > best_win_rate + MIN_WIN_RATE_IMPROVEMENT:
                best_win_rate = win_rate
                episodes_without_improvement = 0
                save_checkpoint(agent, episode, stats, "best")
            else:
                episodes_without_improvement += 1
        
        # Update learning rate
        if hasattr(agent, 'set_learning_rate'):
            lr = get_learning_rate(episode, TOTAL_EPISODES)
            agent.set_learning_rate(lr)
        
        # Periodic logging
        if episode % LOG_INTERVAL == 0:
            elapsed = time.time() - training_start_time
            remaining_episodes = TOTAL_EPISODES - episode
            eta = (elapsed / episode) * remaining_episodes if episode > 0 else 0
            print_progress(episode, stats, elapsed, eta)
            save_progress(episode, stats, elapsed)
        
        # Checkpointing
        if episode % CHECKPOINT_INTERVAL == 0:
            save_checkpoint(agent, episode, stats, "periodic")
            save_stats(stats)
        
        # Autosave (time-based)
        current_time = time.time()
        if current_time - last_autosave_time > AUTOSAVE_INTERVAL:
            save_checkpoint(agent, episode, stats, "autosave")
            save_stats(stats)
            last_autosave_time = current_time
        
        # Early stopping check
        if episodes_without_improvement >= PLATEAU_THRESHOLD:
            log_message(f"⚠️  Performance plateau detected ({PLATEAU_THRESHOLD} episodes without improvement)")
            log_message(f"   Best win rate: {best_win_rate:.2f}%")
            break
    
    # Final save
    log_message("\n🏁 Training completed!")
    save_checkpoint(agent, episode, stats, "final")
    save_stats(stats)
    
    # Save final model
    final_model_path = os.path.join(MODELS_DIR, "ppo_agent.pth")
    agent.save(final_model_path)
    log_message(f"💾 Final model saved: {final_model_path}")
    
    # Print summary
    total_time = time.time() - training_start_time
    print("\n" + "=" * 80)
    print("📊 TRAINING SUMMARY")
    print("=" * 80)
    print(f"✅ Episodes Completed: {episode:,}")
    print(f"⏱️  Total Time: {timedelta(seconds=int(total_time))}")
    print(f"🏆 Final Win Rate: {stats['win_rates'][-1] if stats['win_rates'] else 0:.2f}%")
    print(f"🌟 Best Win Rate: {best_win_rate:.2f}%")
    print(f"💰 Avg Reward: {stats['avg_rewards'][-1] if stats['avg_rewards'] else 0:.2f}")
    print(f"📈 Total Wins: {stats['total_wins']:,}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        train_overnight()
    except Exception as e:
        log_message(f"❌ Training error: {e}")
        import traceback
        traceback.print_exc()
        raise
