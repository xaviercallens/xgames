"""
Hybrid AI Agent - Combines Heuristics with Reinforcement Learning

This agent uses the best of both worlds:
- Heuristic reasoning for strategic decisions
- RL model for tactical execution
- Ensemble voting for final actions
"""

import random
import numpy as np
from .heuristics_enhanced import EnhancedHeuristics, EnhancedHeuristicAgent
from .agents.ppo_agent import PPOAgent


class HybridAgent:
    """
    Hybrid agent combining heuristics and reinforcement learning.
    
    Strategy:
    1. Heuristic provides strategic guidance (where to go, when to bomb)
    2. RL model provides tactical execution (how to move, timing)
    3. Ensemble voting combines both for final decision
    
    Modes:
    - 'heuristic_primary': Heuristic leads, RL assists (70/30)
    - 'balanced': Equal weight (50/50)
    - 'rl_primary': RL leads, heuristic assists (30/70)
    - 'adaptive': Dynamically adjusts based on performance
    """
    
    def __init__(self, player, mode='balanced', ppo_model_path=None):
        """
        Initialize hybrid agent.
        
        Args:
            player: Player entity
            mode: Hybrid mode ('heuristic_primary', 'balanced', 'rl_primary', 'adaptive')
            ppo_model_path: Path to PPO model (optional)
        """
        self.player = player
        self.mode = mode
        
        # Initialize sub-agents
        self.heuristic_agent = EnhancedHeuristicAgent(player)
        self.rl_agent = None
        
        # Try to load RL agent
        if ppo_model_path:
            try:
                self.rl_agent = PPOAgent(player)
                self.rl_agent.load(ppo_model_path)
                self.has_rl = True
            except Exception as e:
                print(f"⚠️  Could not load RL agent: {e}")
                self.has_rl = False
        else:
            self.has_rl = False
        
        # Weights for ensemble voting
        self.weights = self._get_weights(mode)
        
        # Performance tracking
        self.total_games = 0
        self.wins = 0
        self.heuristic_decisions = 0
        self.rl_decisions = 0
        self.ensemble_decisions = 0
        
        # Adaptive mode parameters
        self.heuristic_success_rate = 0.5
        self.rl_success_rate = 0.5
        self.recent_outcomes = []  # Track last N outcomes
        self.adaptive_window = 20  # Window for adaptive learning
        
        # Think timer
        self.think_timer = 0
        self.think_delay = 0.1
        self.current_action = None
    
    def _get_weights(self, mode):
        """Get voting weights for specified mode."""
        weights = {
            'heuristic_primary': {'heuristic': 0.7, 'rl': 0.3},
            'balanced': {'heuristic': 0.5, 'rl': 0.5},
            'rl_primary': {'heuristic': 0.3, 'rl': 0.7},
            'adaptive': {'heuristic': 0.5, 'rl': 0.5},  # Will adjust dynamically
        }
        return weights.get(mode, weights['balanced'])
    
    def _update_adaptive_weights(self):
        """Update weights based on recent performance (adaptive mode only)."""
        if self.mode != 'adaptive' or len(self.recent_outcomes) < 5:
            return
        
        # Calculate success rates from recent outcomes
        recent_window = self.recent_outcomes[-self.adaptive_window:]
        
        heuristic_successes = sum(1 for outcome in recent_window if outcome['decision'] == 'heuristic' and outcome['success'])
        rl_successes = sum(1 for outcome in recent_window if outcome['decision'] == 'rl' and outcome['success'])
        
        heuristic_total = sum(1 for outcome in recent_window if outcome['decision'] == 'heuristic')
        rl_total = sum(1 for outcome in recent_window if outcome['decision'] == 'rl')
        
        # Update success rates
        if heuristic_total > 0:
            self.heuristic_success_rate = heuristic_successes / heuristic_total
        if rl_total > 0:
            self.rl_success_rate = rl_successes / rl_total
        
        # Adjust weights based on success rates
        total_success = self.heuristic_success_rate + self.rl_success_rate
        if total_success > 0:
            self.weights['heuristic'] = self.heuristic_success_rate / total_success
            self.weights['rl'] = self.rl_success_rate / total_success
    
    def choose_action(self, game_state):
        """
        Choose action using hybrid approach.
        
        Args:
            game_state: Current game state
            
        Returns:
            (dx, dy, place_bomb) tuple
        """
        # Get heuristic recommendation
        heuristic_action = self.heuristic_agent.choose_action(game_state)
        heuristic_dx, heuristic_dy, heuristic_bomb = heuristic_action
        
        # Get RL recommendation if available
        if self.has_rl and self.rl_agent:
            try:
                rl_action = self.rl_agent.choose_action(game_state)
                rl_dx, rl_dy, rl_bomb = rl_action
            except Exception as e:
                # Fallback to heuristic if RL fails
                rl_dx, rl_dy, rl_bomb = heuristic_dx, heuristic_dy, heuristic_bomb
        else:
            # No RL available - use heuristic
            rl_dx, rl_dy, rl_bomb = heuristic_dx, heuristic_dy, heuristic_bomb
        
        # Ensemble voting
        final_action = self._ensemble_vote(
            (heuristic_dx, heuristic_dy, heuristic_bomb),
            (rl_dx, rl_dy, rl_bomb),
            game_state
        )
        
        return final_action
    
    def _ensemble_vote(self, heuristic_action, rl_action, game_state):
        """
        Combine heuristic and RL actions using weighted voting.
        
        Args:
            heuristic_action: (dx, dy, bomb) from heuristic
            rl_action: (dx, dy, bomb) from RL
            game_state: Current game state
            
        Returns:
            Final (dx, dy, bomb) action
        """
        h_dx, h_dy, h_bomb = heuristic_action
        r_dx, r_dy, r_bomb = rl_action
        
        # Update adaptive weights if in adaptive mode
        if self.mode == 'adaptive':
            self._update_adaptive_weights()
        
        # Get weights
        h_weight = self.weights['heuristic']
        r_weight = self.weights['rl']
        
        # Vote on movement direction
        if (h_dx, h_dy) == (r_dx, r_dy):
            # Both agree - use it
            final_dx, final_dy = h_dx, h_dy
            decision_type = 'agreement'
        else:
            # Disagree - use weighted random selection
            if random.random() < h_weight:
                final_dx, final_dy = h_dx, h_dy
                decision_type = 'heuristic'
                self.heuristic_decisions += 1
            else:
                final_dx, final_dy = r_dx, r_dy
                decision_type = 'rl'
                self.rl_decisions += 1
        
        # Vote on bomb placement
        if h_bomb == r_bomb:
            # Both agree
            final_bomb = h_bomb
        else:
            # Disagree - use weighted random selection
            # But be conservative - only bomb if high confidence
            if h_bomb and h_weight > 0.6:
                final_bomb = True
            elif r_bomb and r_weight > 0.6:
                final_bomb = True
            else:
                # Not confident enough - don't bomb
                final_bomb = False
        
        self.ensemble_decisions += 1
        
        # Validate action is safe (use heuristic's safety check)
        px, py = int(self.player.x), int(self.player.y)
        danger_map = EnhancedHeuristics.get_danger_map(game_state)
        
        # Check if proposed move is safe
        new_x, new_y = px + final_dx, py + final_dy
        if (0 <= new_x < len(game_state.grid[0]) and 
            0 <= new_y < len(game_state.grid) and
            game_state.grid[new_y][new_x] == 0):
            # Move is valid
            if danger_map[new_y][new_x] > 50:
                # Too dangerous - find safer alternative
                safe_actions = EnhancedHeuristics.prune_unsafe_actions(
                    self.player, game_state, danger_map
                )
                if safe_actions:
                    final_dx, final_dy = random.choice(safe_actions)
                    final_bomb = False  # Don't bomb if in danger
        
        return (final_dx, final_dy, final_bomb)
    
    def update(self, dt, game_state):
        """Update agent with think timer."""
        self.think_timer += dt
        
        if self.think_timer >= self.think_delay:
            self.think_timer = 0
            self.current_action = self.choose_action(game_state)
        
        return self.current_action
    
    def record_outcome(self, decision_type, success):
        """
        Record outcome for adaptive learning.
        
        Args:
            decision_type: 'heuristic', 'rl', or 'agreement'
            success: Boolean indicating if action was successful
        """
        self.recent_outcomes.append({
            'decision': decision_type,
            'success': success,
        })
        
        # Keep only recent window
        if len(self.recent_outcomes) > self.adaptive_window * 2:
            self.recent_outcomes = self.recent_outcomes[-self.adaptive_window:]
    
    def record_game_result(self, won, reward):
        """Record game result."""
        self.total_games += 1
        if won:
            self.wins += 1
        
        # Update sub-agents
        self.heuristic_agent.record_game_result(won, reward)
        if self.has_rl and self.rl_agent:
            self.rl_agent.record_game_result(won, reward)
    
    def get_win_rate(self):
        """Get win rate."""
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games
    
    def get_stats_string(self):
        """Get formatted statistics."""
        win_rate = self.get_win_rate() * 100
        
        # Determine skill level
        if win_rate >= 70:
            level = "Expert"
        elif win_rate >= 50:
            level = "Advanced"
        elif win_rate >= 40:
            level = "Intermediate+"
        elif win_rate >= 30:
            level = "Intermediate"
        else:
            level = "Learning"
        
        # Calculate decision distribution
        total_decisions = self.heuristic_decisions + self.rl_decisions + self.ensemble_decisions
        if total_decisions > 0:
            h_pct = (self.heuristic_decisions / total_decisions) * 100
            r_pct = (self.rl_decisions / total_decisions) * 100
        else:
            h_pct = r_pct = 0
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║           🎭 HYBRID AI AGENT - PERFORMANCE                   ║
║        (Heuristics + Reinforcement Learning)                 ║
╠══════════════════════════════════════════════════════════════╣
║  Mode:             {self.mode:<40} ║
║  Skill Level:      {level:<40} ║
║  Win Rate:         {win_rate:>6.2f}%                                 ║
║  Games Played:     {self.total_games:<40} ║
║  Total Wins:       {self.wins:<40} ║
╠══════════════════════════════════════════════════════════════╣
║  Decision Distribution:                                      ║
║    Heuristic:      {h_pct:>5.1f}% ({self.heuristic_decisions} decisions)                    ║
║    RL Model:       {r_pct:>5.1f}% ({self.rl_decisions} decisions)                    ║
║    Ensemble:       {self.ensemble_decisions:<40} ║
╠══════════════════════════════════════════════════════════════╣
║  Weights (Current):                                          ║
║    Heuristic:      {self.weights['heuristic']:.1%}                                       ║
║    RL Model:       {self.weights['rl']:.1%}                                       ║
╠══════════════════════════════════════════════════════════════╣
║  Components:                                                 ║
║    ✓ Enhanced Heuristic (Beam Search + Opponent Prediction) ║
║    {'✓' if self.has_rl else '✗'} PPO Reinforcement Learning Model                      ║
╚══════════════════════════════════════════════════════════════╝
"""


def create_hybrid_agent(player, mode='balanced', models_dir='bomber_game/models'):
    """
    Factory function to create hybrid agent.
    
    Args:
        player: Player entity
        mode: Hybrid mode
        models_dir: Directory containing models
        
    Returns:
        HybridAgent instance
    """
    import os
    
    # Try to find best PPO model
    ppo_model_path = None
    best_model = os.path.join(models_dir, 'best_model.pth')
    ppo_model = os.path.join(models_dir, 'ppo_agent.pth')
    
    if os.path.exists(best_model):
        ppo_model_path = best_model
    elif os.path.exists(ppo_model):
        ppo_model_path = ppo_model
    
    return HybridAgent(player, mode=mode, ppo_model_path=ppo_model_path)


if __name__ == '__main__':
    print("🎭 Hybrid Agent - Combines Heuristics with Reinforcement Learning")
    print("\nModes:")
    print("  • heuristic_primary: Heuristic leads (70/30)")
    print("  • balanced: Equal weight (50/50)")
    print("  • rl_primary: RL leads (30/70)")
    print("  • adaptive: Dynamically adjusts based on performance")
    print("\nBenefits:")
    print("  ✓ Best of both worlds")
    print("  ✓ Strategic + Tactical intelligence")
    print("  ✓ Robust fallback (heuristic)")
    print("  ✓ Adaptive learning")
