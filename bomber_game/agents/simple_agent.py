"""
Simple AI agent with basic heuristics.
"""

import random
from .agent_base import Agent


class SimpleAgent(Agent):
    """
    Simple AI that:
    1. Avoids explosions
    2. Moves toward the player
    3. Places bombs when close to player
    """
    
    def __init__(self, player):
        super().__init__(player)
        self.target_player = None
        self.think_delay = 0.15  # Smarter, faster thinking
        
    def choose_action(self, game_state):
        """Choose action using simple heuristics."""
        if not self.player.alive:
            return (0, 0, False)
        
        # Find target player (first alive player that's not us)
        self.target_player = None
        for player in game_state.players:
            if player != self.player and player.alive:
                self.target_player = player
                break
        
        # Priority 1: Avoid danger
        if self._in_danger(game_state):
            return self._find_safe_move(game_state)
        
        # Priority 2: Place bomb if near enemy (more aggressive)
        if self.target_player and self._near_enemy(game_state):
            if self.player.can_place_bomb() and random.random() < 0.7:  # 70% chance
                return (0, 0, True)
        
        # Priority 3: Move toward enemy
        if self.target_player:
            return self._move_toward_enemy(game_state)
        
        # Default: Random move
        return self._random_move(game_state)
    
    def _in_danger(self, game_state):
        """Check if AI is in danger from explosions."""
        px, py = self.player.grid_x, self.player.grid_y
        
        # Check if standing on explosion
        for explosion in game_state.explosions:
            if explosion.grid_x == px and explosion.grid_y == py:
                return True
        
        # Check if bomb nearby will explode soon
        for bomb in game_state.bombs:
            if bomb.timer < 1.5:  # Less than 1.5 seconds
                # Check if in blast range
                bx, by = bomb.grid_x, bomb.grid_y
                if px == bx and abs(py - by) <= bomb.bomb_range:
                    return True
                if py == by and abs(px - bx) <= bomb.bomb_range:
                    return True
        
        return False
    
    def _find_safe_move(self, game_state):
        """Find a safe direction to move."""
        px, py = self.player.grid_x, self.player.grid_y
        
        # Try all directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = px + dx, py + dy
            
            if game_state.is_walkable(nx, ny):
                # Check if this position is safe
                safe = True
                for bomb in game_state.bombs:
                    bx, by = bomb.grid_x, bomb.grid_y
                    if nx == bx and abs(ny - by) <= bomb.bomb_range:
                        safe = False
                        break
                    if ny == by and abs(nx - bx) <= bomb.bomb_range:
                        safe = False
                        break
                
                if safe:
                    return (dx, dy, False)
        
        # No safe move, try any walkable
        for dx, dy in directions:
            nx, ny = px + dx, py + dy
            if game_state.is_walkable(nx, ny):
                return (dx, dy, False)
        
        return (0, 0, False)
    
    def _near_enemy(self, game_state):
        """Check if near enemy player."""
        if not self.target_player:
            return False
        
        px, py = self.player.grid_x, self.player.grid_y
        tx, ty = self.target_player.grid_x, self.target_player.grid_y
        
        distance = abs(px - tx) + abs(py - ty)  # Manhattan distance
        return distance <= 4  # Increased range for more aggressive AI
    
    def _move_toward_enemy(self, game_state):
        """Move toward enemy player."""
        if not self.target_player:
            return (0, 0, False)
        
        px, py = self.player.grid_x, self.player.grid_y
        tx, ty = self.target_player.grid_x, self.target_player.grid_y
        
        # Calculate direction
        dx = 0 if px == tx else (1 if tx > px else -1)
        dy = 0 if py == ty else (1 if ty > py else -1)
        
        # Try horizontal first
        if dx != 0 and game_state.is_walkable(px + dx, py):
            return (dx, 0, False)
        
        # Try vertical
        if dy != 0 and game_state.is_walkable(px, py + dy):
            return (0, dy, False)
        
        # Can't move toward enemy, try random
        return self._random_move(game_state)
    
    def _random_move(self, game_state):
        """Make a random valid move."""
        px, py = self.player.grid_x, self.player.grid_y
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = px + dx, py + dy
            if game_state.is_walkable(nx, ny):
                return (dx, dy, False)
        
        return (0, 0, False)
