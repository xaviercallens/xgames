"""
Hybrid Agent - Combines Heuristics and Reinforcement Learning
Uses the best of both worlds: strategic heuristics and learned behaviors.
"""

import random
from .agent_base import Agent
from .ppo_agent import PPOAgent
from ..heuristics_improved import ImprovedHeuristicAgent


class HybridAgent(Agent):
    """
    Hybrid agent that combines heuristic and RL strategies.
    
    Modes:
    - 'heuristic_primary': Use heuristics 80%, RL 20%
    - 'balanced': Use heuristics 50%, RL 50%
    - 'rl_primary': Use heuristics 20%, RL 80%
    - 'adaptive': Choose based on confidence/situation
    """
    
    def __init__(self, player, mode='balanced', ppo_model_path=None):
        """
        Initialize hybrid agent.
        
        Args:
            player: Player entity
            mode: Hybrid mode ('heuristic_primary', 'balanced', 'rl_primary', 'adaptive')
            ppo_model_path: Path to trained PPO model (optional)
        """
        super().__init__(player)
        self.mode = mode
        
        # Initialize both agents
        self.heuristic_agent = ImprovedHeuristicAgent(player)
        
        # Try to load PPO agent if model exists
        self.ppo_agent = None
        self.ppo_available = False
        if ppo_model_path:
            try:
                self.ppo_agent = PPOAgent(player, model_path=ppo_model_path, training=False)
                self.ppo_available = True
                print(f"✅ Hybrid Agent: PPO model loaded from {ppo_model_path}")
            except Exception as e:
                print(f"⚠️  Hybrid Agent: Could not load PPO model - using heuristics only")
                print(f"   Error: {e}")
        
        # Set mixing ratios based on mode
        self.mixing_ratios = {
            'heuristic_primary': {'heuristic': 0.8, 'rl': 0.2},
            'balanced': {'heuristic': 0.5, 'rl': 0.5},
            'rl_primary': {'heuristic': 0.2, 'rl': 0.8},
            'adaptive': {'heuristic': 0.5, 'rl': 0.5}  # Will adjust dynamically
        }
        
        # Statistics
        self.decisions = {'heuristic': 0, 'rl': 0, 'combined': 0}
        self.last_decision_type = None
        
    def choose_action(self, game_state):
        """
        Choose action using hybrid strategy.
        
        Args:
            game_state: Current game state
            
        Returns:
            Tuple of (dx, dy, place_bomb)
        """
        if not self.player.alive:
            return (0, 0, False)
        
        # If PPO not available, use heuristics only
        if not self.ppo_available:
            self.decisions['heuristic'] += 1
            self.last_decision_type = 'heuristic'
            return self.heuristic_agent.choose_action(game_state)
        
        # Get actions from both agents
        heuristic_action = self.heuristic_agent.choose_action(game_state)
        rl_action = self.ppo_agent.choose_action(game_state)
        
        # Get confidence from heuristic agent (if available)
        heuristic_confidence = getattr(self.heuristic_agent, 'last_confidence', 0.5)
        
        # Decide which action to use based on mode
        if self.mode == 'adaptive':
            # Use adaptive strategy based on confidence
            action = self._adaptive_decision(heuristic_action, rl_action, heuristic_confidence)
        else:
            # Use probabilistic mixing
            ratio = self.mixing_ratios.get(self.mode, self.mixing_ratios['balanced'])
            action = self._probabilistic_mix(heuristic_action, rl_action, ratio)
        
        return action
    
    def _adaptive_decision(self, heuristic_action, rl_action, heuristic_confidence):
        """
        Adaptively choose between heuristic and RL based on confidence.
        
        Args:
            heuristic_action: Action from heuristic agent
            rl_action: Action from RL agent
            heuristic_confidence: Confidence level of heuristic (0-1)
            
        Returns:
            Chosen action
        """
        # High confidence in heuristic (>0.7) - use it
        if heuristic_confidence > 0.7:
            self.decisions['heuristic'] += 1
            self.last_decision_type = 'heuristic'
            return heuristic_action
        
        # Low confidence in heuristic (<0.3) - use RL
        elif heuristic_confidence < 0.3:
            self.decisions['rl'] += 1
            self.last_decision_type = 'rl'
            return rl_action
        
        # Medium confidence - combine both
        else:
            self.decisions['combined'] += 1
            self.last_decision_type = 'combined'
            return self._combine_actions(heuristic_action, rl_action)
    
    def _probabilistic_mix(self, heuristic_action, rl_action, ratio):
        """
        Probabilistically mix heuristic and RL actions.
        
        Args:
            heuristic_action: Action from heuristic agent
            rl_action: Action from RL agent
            ratio: Dictionary with 'heuristic' and 'rl' probabilities
            
        Returns:
            Chosen action
        """
        if random.random() < ratio['heuristic']:
            self.decisions['heuristic'] += 1
            self.last_decision_type = 'heuristic'
            return heuristic_action
        else:
            self.decisions['rl'] += 1
            self.last_decision_type = 'rl'
            return rl_action
    
    def _combine_actions(self, heuristic_action, rl_action):
        """
        Combine both actions intelligently.
        
        Args:
            heuristic_action: Action from heuristic agent
            rl_action: Action from RL agent
            
        Returns:
            Combined action
        """
        # If both agree on movement, use it
        if heuristic_action[:2] == rl_action[:2]:
            dx, dy = heuristic_action[:2]
        else:
            # Use heuristic for movement (usually safer)
            dx, dy = heuristic_action[:2]
        
        # For bomb placement, use OR logic (place if either suggests)
        place_bomb = heuristic_action[2] or rl_action[2]
        
        return (dx, dy, place_bomb)
    
    def get_statistics(self):
        """
        Get decision statistics.
        
        Returns:
            Dictionary with decision counts and percentages
        """
        total = sum(self.decisions.values())
        if total == 0:
            return self.decisions
        
        stats = {
            'total_decisions': total,
            'heuristic_count': self.decisions['heuristic'],
            'rl_count': self.decisions['rl'],
            'combined_count': self.decisions['combined'],
            'heuristic_percent': (self.decisions['heuristic'] / total) * 100,
            'rl_percent': (self.decisions['rl'] / total) * 100,
            'combined_percent': (self.decisions['combined'] / total) * 100,
            'mode': self.mode,
            'ppo_available': self.ppo_available
        }
        return stats
    
    def reset_statistics(self):
        """Reset decision statistics."""
        self.decisions = {'heuristic': 0, 'rl': 0, 'combined': 0}
        self.last_decision_type = None
    
    def set_mode(self, mode):
        """
        Change hybrid mode.
        
        Args:
            mode: New mode ('heuristic_primary', 'balanced', 'rl_primary', 'adaptive')
        """
        if mode in self.mixing_ratios:
            self.mode = mode
            print(f"🔄 Hybrid mode changed to: {mode}")
        else:
            print(f"⚠️  Invalid mode: {mode}")
    
    def print_statistics(self):
        """Print decision statistics."""
        stats = self.get_statistics()
        print("\n" + "=" * 60)
        print("🎭 HYBRID AGENT STATISTICS")
        print("=" * 60)
        print(f"Mode: {stats['mode']}")
        print(f"PPO Available: {'✅ Yes' if stats['ppo_available'] else '❌ No'}")
        print(f"\nTotal Decisions: {stats['total_decisions']}")
        print(f"  Heuristic: {stats['heuristic_count']} ({stats['heuristic_percent']:.1f}%)")
        print(f"  RL:        {stats['rl_count']} ({stats['rl_percent']:.1f}%)")
        print(f"  Combined:  {stats['combined_count']} ({stats['combined_percent']:.1f}%)")
        print("=" * 60 + "\n")
