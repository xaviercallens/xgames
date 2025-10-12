#!/usr/bin/env python3
"""
Quick Training Script - 15 Minutes Progressive Training
Trains AI agent with automatic checkpointing and level progression.
"""

import sys
import os
import time
import json
import numpy as np
from datetime import datetime, timedelta
import signal

# Suppress pygame warnings during training
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game import GRID_SIZE, TILE_SIZE
from bomber_game.game_state import GameState
from bomber_game.entities import Player
from bomber_game.agents import PPOAgent, SimpleAgent

# Training configuration
TRAINING_DURATION = 5 * 60  # 5 minutes in seconds
CHECKPOINT_INTERVAL = 30  # Save every 30 seconds
STATS_FILE = "bomber_game/models/training_stats.json"
MODEL_PATH = "bomber_game/models/ppo_agent.pth"

# Level thresholds
LEVELS = [
    {"name": "Beginner", "min_win_rate": 0, "color": "🔵", "emoji": "🐣"},
    {"name": "Novice", "min_win_rate": 20, "color": "🟢", "emoji": "🌱"},
    {"name": "Intermediate", "min_win_rate": 40, "color": "🟡", "emoji": "🎯"},
    {"name": "Advanced", "min_win_rate": 60, "color": "🟠", "emoji": "🔥"},
    {"name": "Expert", "min_win_rate": 75, "color": "🔴", "emoji": "⚡"},
    {"name": "Master", "min_win_rate": 85, "color": "🟣", "emoji": "👑"},
]

# Progress messages
PROGRESS_MESSAGES = {
    "Beginner": [
        "🐣 Learning to walk...",
        "🎮 Understanding the game basics...",
        "🤔 Figuring out how bombs work...",
        "👀 Watching and learning...",
    ],
    "Novice": [
        "🌱 Starting to understand strategy...",
        "💡 Learning to avoid explosions...",
        "🎯 Improving decision making...",
        "📈 Getting smarter...",
    ],
    "Intermediate": [
        "🎯 Developing tactical skills...",
        "🧠 Thinking ahead...",
        "⚔️ Learning combat strategies...",
        "🚀 Making progress...",
    ],
    "Advanced": [
        "🔥 Mastering advanced tactics...",
        "🎓 Becoming a skilled player...",
        "💪 Getting really good...",
        "🌟 Impressive improvement...",
    ],
    "Expert": [
        "⚡ Executing expert strategies...",
        "🏆 Near-perfect gameplay...",
        "🎖️ Dominating the arena...",
        "✨ Exceptional performance...",
    ],
    "Master": [
        "👑 Achieving mastery...",
        "🌌 Playing at peak performance...",
        "🔮 Predicting enemy moves...",
        "🎭 A true Bomberman master...",
    ],
}

# Global flag for graceful shutdown
training_interrupted = False

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global training_interrupted
    training_interrupted = True
    print("\n\n⚠️  Training interruption requested...")
    print("💾 Saving progress before exit...")


class TrainingStats:
    """Track and persist training statistics."""
    
    def __init__(self):
        self.total_episodes = 0
        self.total_training_time = 0
        self.total_wins = 0
        self.total_losses = 0
        self.episode_rewards = []
        self.win_rates = []
        self.training_sessions = []
        self.current_level = "Beginner"
        self.last_updated = None
        
        self.load()
    
    def load(self):
        """Load existing stats."""
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    data = json.load(f)
                    self.total_episodes = data.get('total_episodes', 0)
                    self.total_training_time = data.get('total_training_time', 0)
                    self.total_wins = data.get('total_wins', 0)
                    self.total_losses = data.get('total_losses', 0)
                    self.episode_rewards = data.get('episode_rewards', [])
                    self.win_rates = data.get('win_rates', [])
                    self.training_sessions = data.get('training_sessions', [])
                    self.current_level = data.get('current_level', 'Beginner')
                    self.last_updated = data.get('last_updated')
                    print(f"✅ Loaded existing training stats: {self.total_episodes} episodes")
            except Exception as e:
                print(f"⚠️  Could not load stats: {e}")
    
    def save(self):
        """Save current stats."""
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        data = {
            'total_episodes': self.total_episodes,
            'total_training_time': self.total_training_time,
            'total_wins': self.total_wins,
            'total_losses': self.total_losses,
            'episode_rewards': self.episode_rewards[-1000:],  # Keep last 1000
            'win_rates': self.win_rates[-100:],  # Keep last 100
            'training_sessions': self.training_sessions,
            'current_level': self.current_level,
            'last_updated': datetime.now().isoformat(),
        }
        with open(STATS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def update_level(self):
        """Update AI level based on win rate."""
        if not self.win_rates:
            return
        
        recent_win_rate = np.mean(self.win_rates[-20:]) * 100
        
        for level in reversed(LEVELS):
            if recent_win_rate >= level['min_win_rate']:
                self.current_level = level['name']
                break
    
    def get_win_rate(self):
        """Get current win rate."""
        if self.total_episodes == 0:
            return 0
        return (self.total_wins / self.total_episodes) * 100
    
    def add_episode(self, reward, won):
        """Add episode result."""
        self.total_episodes += 1
        self.episode_rewards.append(reward)
        if won:
            self.total_wins += 1
        else:
            self.total_losses += 1
        
        # Calculate win rate for last 20 episodes
        recent_episodes = min(20, self.total_episodes)
        recent_wins = sum(1 for i in range(-recent_episodes, 0) 
                         if i < 0 and self.episode_rewards[i] > 100)
        win_rate = recent_wins / recent_episodes
        self.win_rates.append(win_rate)
        
        self.update_level()


def calculate_reward(game_state, agent_player, enemy_player, prev_state, action):
    """Calculate reward with curriculum learning."""
    reward = 0
    
    # Win/Loss
    if not agent_player.alive:
        return -200
    if not enemy_player.alive:
        return +200
    
    # Step penalty
    reward -= 0.5
    
    # Destroy walls
    if prev_state:
        prev_walls = sum(row.count(2) for row in prev_state['grid'])
        curr_walls = sum(row.count(2) for row in game_state.grid)
        if curr_walls < prev_walls:
            reward += 20 * (prev_walls - curr_walls)
    
    # Power-ups
    if prev_state and len(game_state.powerups) < prev_state['powerups']:
        reward += 10
    
    # Distance to enemy
    if prev_state:
        prev_dist = abs(prev_state['player_x'] - prev_state['enemy_x']) + \
                   abs(prev_state['player_y'] - prev_state['enemy_y'])
        curr_dist = abs(agent_player.grid_x - enemy_player.grid_x) + \
                   abs(agent_player.grid_y - enemy_player.grid_y)
        
        if curr_dist < prev_dist:
            reward += 5
        elif curr_dist > prev_dist:
            reward -= 5
    
    # Strategic bomb placement
    dx, dy, place_bomb = action
    if place_bomb:
        dist_to_enemy = abs(agent_player.grid_x - enemy_player.grid_x) + \
                       abs(agent_player.grid_y - enemy_player.grid_y)
        if dist_to_enemy <= 3:
            reward += 15
    
    # Survival bonus
    if prev_state and prev_state.get('in_danger', False):
        if not _in_danger(game_state, agent_player):
            reward += 30
    
    return reward


def _in_danger(game_state, player):
    """Check if player is in danger."""
    px, py = player.grid_x, player.grid_y
    
    for explosion in game_state.explosions:
        if explosion.grid_x == px and explosion.grid_y == py:
            return True
    
    for bomb in game_state.bombs:
        if bomb.timer < 1.5:
            bx, by = bomb.grid_x, bomb.grid_y
            if (px == bx and abs(py - by) <= bomb.bomb_range) or \
               (py == by and abs(px - bx) <= bomb.bomb_range):
                return True
    
    return False


def save_state(game_state, agent_player, enemy_player):
    """Save game state."""
    return {
        'grid': [row[:] for row in game_state.grid],
        'powerups': len(game_state.powerups),
        'player_x': agent_player.grid_x,
        'player_y': agent_player.grid_y,
        'enemy_x': enemy_player.grid_x,
        'enemy_y': enemy_player.grid_y,
        'in_danger': _in_danger(game_state, agent_player),
    }


def format_time(seconds):
    """Format seconds to readable time."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def print_progress_bar(current, total, width=50):
    """Print a progress bar."""
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percent = progress * 100
    return f"[{bar}] {percent:.1f}%"


def get_progress_message(level, episode_count):
    """Get a contextual progress message."""
    messages = PROGRESS_MESSAGES.get(level, ["Training..."])
    idx = (episode_count // 50) % len(messages)
    return messages[idx]


def print_banner():
    """Print training banner."""
    print("\n" + "=" * 80)
    print("🤖 BOMBERMAN AI TRAINING - Progressive Learning System")
    print("=" * 80)
    print()
    print("🎯 Mission: Train an intelligent AI agent to master Bomberman")
    print("⏱️  Duration: 5 minutes of focused learning")
    print("💾 Auto-save: Every 30 seconds")
    print("🎮 Result: Smarter AI with each session!")
    print()
    print("=" * 80)
    print()


def quick_train():
    """Quick 5-minute training session."""
    global training_interrupted
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print_banner()
    
    # Check PyTorch
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"✅ Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    except ImportError:
        print("❌ PyTorch not installed!")
        print("   Install: pip install torch")
        return
    
    print()
    
    # Load or create stats
    stats = TrainingStats()
    
    print(f"📊 Current Training Status:")
    print(f"   Total Episodes: {stats.total_episodes}")
    print(f"   Total Training Time: {format_time(stats.total_training_time)}")
    print(f"   Win Rate: {stats.get_win_rate():.1f}%")
    print(f"   Current Level: {stats.current_level}")
    if stats.last_updated:
        print(f"   Last Updated: {stats.last_updated}")
    print()
    
    # Create model directory
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    # Initialize agent
    print("🤖 Initializing PPO Agent...")
    agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
    agent = PPOAgent(agent_player, model_path=MODEL_PATH if os.path.exists(MODEL_PATH) else None, training=True)
    print()
    
    # Training session info
    session_start = time.time()
    session_episodes = 0
    session_wins = 0
    last_checkpoint = time.time()
    
    print(f"⏱️  Training Duration: {TRAINING_DURATION // 60} minutes")
    print(f"💾 Checkpoint Interval: {CHECKPOINT_INTERVAL} seconds")
    
    # Get level emoji
    level_emoji = next((l["emoji"] for l in LEVELS if l["name"] == stats.current_level), "🤖")
    print(f"{level_emoji} Starting Level: {stats.current_level}")
    print()
    print("🎮 Training in progress... (Press Ctrl+C to stop gracefully)")
    print()
    
    last_message_time = time.time()
    message_interval = 30  # Show message every 30 seconds
    
    try:
        while True:
            elapsed = time.time() - session_start
            
            # Check if training interrupted
            if training_interrupted:
                print("\n⚠️  Training interrupted by user!")
                break
            
            # Check if training time is up
            if elapsed >= TRAINING_DURATION:
                break
            
            # Initialize game
            game_state = GameState(GRID_SIZE)
            agent_player = Player(1, 1, (255, 0, 0), "PPO Agent")
            enemy_player = Player(11, 11, (0, 255, 0), "Enemy")
            game_state.players = [agent_player, enemy_player]
            agent.player = agent_player
            
            # Enemy AI
            enemy_ai = SimpleAgent(enemy_player)
            
            # Episode variables
            total_reward = 0
            steps = 0
            max_steps = 500
            prev_state = None
            done = False
            
            # Run episode
            while not done and steps < max_steps:
                # Agent action
                action = agent.choose_action(game_state)
                dx, dy, place_bomb = action
                
                agent_player.move(dx, dy, game_state.grid, TILE_SIZE, game_state)
                if place_bomb and agent_player.can_place_bomb():
                    game_state.place_bomb(agent_player)
                
                # Enemy action
                if enemy_player.alive:
                    enemy_action = enemy_ai.choose_action(game_state)
                    enemy_dx, enemy_dy, enemy_bomb = enemy_action
                    enemy_player.move(enemy_dx, enemy_dy, game_state.grid, TILE_SIZE, game_state)
                    if enemy_bomb and enemy_player.can_place_bomb():
                        game_state.place_bomb(enemy_player)
                
                # Update game
                game_state.update(1/30)
                
                # Calculate reward
                reward = calculate_reward(game_state, agent_player, enemy_player, prev_state, action)
                total_reward += reward
                
                # Store experience
                done = not agent_player.alive or not enemy_player.alive
                agent.store_reward(reward, done)
                
                prev_state = save_state(game_state, agent_player, enemy_player)
                steps += 1
            
            # Update policy
            agent.update_policy()
            
            # Update stats
            won = agent_player.alive and not enemy_player.alive
            stats.add_episode(total_reward, won)
            session_episodes += 1
            if won:
                session_wins += 1
            
            # Print progress every 10 episodes
            if session_episodes % 10 == 0:
                elapsed = time.time() - session_start
                remaining = TRAINING_DURATION - elapsed
                progress = print_progress_bar(elapsed, TRAINING_DURATION)
                session_win_rate = (session_wins / session_episodes) * 100
                
                # Get level emoji
                level_emoji = next((l["emoji"] for l in LEVELS if l["name"] == stats.current_level), "🤖")
                
                print(f"\r{progress} | "
                      f"⏱️  {format_time(elapsed)}/{format_time(TRAINING_DURATION)} | "
                      f"🎮 {session_episodes} games | "
                      f"🏆 {session_win_rate:.1f}% | "
                      f"{level_emoji} {stats.current_level}", end="", flush=True)
            
            # Show progress message periodically
            current_time = time.time()
            if current_time - last_message_time >= message_interval:
                message = get_progress_message(stats.current_level, session_episodes)
                print(f"\n   {message}")
                last_message_time = current_time
            
            # Checkpoint
            current_time = time.time()
            if current_time - last_checkpoint >= CHECKPOINT_INTERVAL:
                print()  # New line after progress
                level_emoji = next((l["emoji"] for l in LEVELS if l["name"] == stats.current_level), "🤖")
                print(f"💾 Checkpoint at {format_time(elapsed)}...")
                agent.save_model(MODEL_PATH)
                stats.total_training_time += elapsed
                stats.save()
                last_checkpoint = current_time
                print(f"   ✅ Progress saved! {level_emoji} {stats.current_level} | 🏆 {stats.get_win_rate():.1f}% win rate")
                
                # Show improvement message
                if stats.total_episodes > 100:
                    improvement = stats.get_win_rate() - (stats.total_wins - session_wins) / (stats.total_episodes - session_episodes) * 100 if stats.total_episodes > session_episodes else 0
                    if improvement > 0:
                        print(f"   📈 Improved by {improvement:.1f}% this session!")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
    
    # Final save
    print("\n")
    print("=" * 80)
    print("💾 Saving final checkpoint...")
    agent.save_model(MODEL_PATH)
    
    session_duration = time.time() - session_start
    stats.total_training_time += session_duration
    stats.training_sessions.append({
        'date': datetime.now().isoformat(),
        'duration': session_duration,
        'episodes': session_episodes,
        'wins': session_wins,
        'final_level': stats.current_level,
    })
    stats.save()
    
    # Get level info
    level_emoji = next((l["emoji"] for l in LEVELS if l["name"] == stats.current_level), "🤖")
    level_color = next((l["color"] for l in LEVELS if l["name"] == stats.current_level), "🤖")
    
    print("=" * 80)
    print("✅ TRAINING SESSION COMPLETE!")
    print("=" * 80)
    print()
    print(f"📊 Session Summary:")
    print(f"   ⏱️  Duration: {format_time(session_duration)}")
    print(f"   🎮 Episodes: {session_episodes}")
    print(f"   🏆 Wins: {session_wins} ({(session_wins/session_episodes*100):.1f}%)")
    print()
    print(f"📈 AI Intelligence Report:")
    print(f"   🧠 Total Training: {format_time(stats.total_training_time)}")
    print(f"   🎯 Total Episodes: {stats.total_episodes}")
    print(f"   🏆 Overall Win Rate: {stats.get_win_rate():.1f}%")
    print(f"   {level_emoji} Current Level: {level_color} {stats.current_level}")
    print()
    
    # Show level progression message
    if stats.get_win_rate() < 20:
        print("💡 Keep training! Your AI is learning the basics.")
    elif stats.get_win_rate() < 40:
        print("🌱 Good progress! Your AI is developing strategies.")
    elif stats.get_win_rate() < 60:
        print("🎯 Impressive! Your AI is becoming tactical.")
    elif stats.get_win_rate() < 75:
        print("🔥 Excellent! Your AI is mastering advanced techniques.")
    elif stats.get_win_rate() < 85:
        print("⚡ Outstanding! Your AI is playing at expert level.")
    else:
        print("👑 Incredible! Your AI has achieved mastery!")
    
    print()
    print("=" * 80)
    print(f"🎮 Test your AI: ./launch_bomberman.sh")
    print(f"🔄 Continue training: ./quick_train_agent.py")
    print("=" * 80)
    print()


if __name__ == "__main__":
    quick_train()
