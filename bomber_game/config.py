"""
Configuration file for Bomberman game.
Contains all game settings and parameters.
"""

# Game settings
GAME_CONFIG = {
    'grid_size': 13,
    'tile_size': 32,
    'fps': 30,
    'bomb_timer': 3.0,  # seconds
    'explosion_duration': 0.5,  # seconds
}

# Player settings
PLAYER_CONFIG = {
    'speed': 7,  # tiles per second (increased for easier gameplay)
    'initial_bombs': 2,  # Start with 2 bombs
    'initial_range': 2,  # explosion range in tiles
    'max_bombs': 8,
    'max_range': 10,
    'max_speed': 10,
    'max_cacas': 3,  # Maximum caca blocks
    'caca_duration': 5.0,  # How long caca lasts
}

# AI settings
AI_CONFIG = {
    'difficulty': 'hard',  # easy, medium, hard
    'reaction_time': 0.3,  # seconds (faster reaction)
    'think_time': 0.15,  # seconds between decisions (smarter)
}

# Map generation
MAP_CONFIG = {
    'soft_wall_density': 0.25,  # Percentage of empty spaces with soft walls (reduced for easier gameplay)
    'powerup_chance': 0.5,  # Chance of powerup under soft wall (increased for more rewards)
}

# Reinforcement Learning settings
RL_CONFIG = {
    'learning_rate': 0.001,
    'discount_factor': 0.99,
    'epsilon_start': 1.0,
    'epsilon_end': 0.01,
    'epsilon_decay': 0.995,
    'batch_size': 32,
    'memory_size': 10000,
    'target_update_frequency': 1000,  # steps
}

# Reward function parameters
REWARD_CONFIG = {
    'survival': 1,
    'wall_destroyed': 10,
    'enemy_hit': 100,
    'powerup_collected': 50,
    'death': -100,
    'danger_penalty': -5,
    'move_toward_enemy': 2,
}

# Training settings
TRAINING_CONFIG = {
    'num_episodes': 1000,
    'max_steps_per_episode': 1000,
    'save_frequency': 100,  # episodes
    'eval_frequency': 50,  # episodes
    'eval_episodes': 10,
}

# Visualization settings
VIZ_CONFIG = {
    'show_grid': True,
    'show_danger_zones': False,
    'show_pathfinding': False,
    'show_q_values': False,
}

# Educational mode settings
EDU_CONFIG = {
    'tutorial_mode': False,
    'show_hints': True,
    'explain_decisions': False,
    'slow_motion': False,
}
