"""
Base Agent class for AI opponents.
"""

from abc import ABC, abstractmethod


class Agent(ABC):
    """Abstract base class for all AI agents."""
    
    def __init__(self, player):
        """
        Initialize agent.
        
        Args:
            player: Player entity controlled by this agent
        """
        self.player = player
        self.think_timer = 0
        self.think_delay = 0.2  # Think every 0.2 seconds
        self.current_action = None
        
    @abstractmethod
    def choose_action(self, game_state):
        """
        Choose an action based on game state.
        
        Args:
            game_state: Current game state
            
        Returns:
            Action tuple: (dx, dy, place_bomb)
        """
        pass
    
    def update(self, dt, game_state):
        """
        Update agent and execute actions.
        
        Args:
            dt: Delta time
            game_state: Current game state
        """
        self.think_timer += dt
        
        if self.think_timer >= self.think_delay:
            self.think_timer = 0
            self.current_action = self.choose_action(game_state)
        
        return self.current_action
