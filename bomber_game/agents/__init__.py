"""
AI agents for Bomberman game.
"""

from .agent_base import Agent
from .ppo_agent import PPOAgent
from .hybrid_agent import HybridAgent

try:
    from .dqn_agent import DQNAgent
    from .random_agent import RandomAgent
    __all__ = ['Agent', 'PPOAgent', 'DQNAgent', 'RandomAgent', 'HybridAgent']
except ImportError:
    __all__ = ['Agent', 'PPOAgent', 'HybridAgent']
