"""
Heuristic strategies for bootstrapping AI agent training.
These represent common video game strategies that help the agent learn faster.
"""

import random
from . import GRID_SIZE


class GameHeuristics:
    """Collection of heuristic strategies for Bomberman gameplay."""
    
    @staticmethod
    def is_safe_position(x, y, game_state):
        """
        Check if a position is safe (no bombs/explosions nearby).
        
        Args:
            x, y: Grid position to check
            game_state: Current game state
            
        Returns:
            True if position is safe, False otherwise
        """
        # Check for explosions
        for explosion in game_state.explosions:
            if explosion.grid_x == x and explosion.grid_y == y:
                return False
        
        # Check for bombs and their blast radius
        for bomb in game_state.bombs:
            bomb_x, bomb_y = bomb.grid_x, bomb.grid_y
            bomb_range = bomb.bomb_range
            
            # Check if in horizontal blast line
            if bomb_y == y and abs(bomb_x - x) <= bomb_range:
                # Check if there's a wall blocking
                blocked = False
                step = 1 if x > bomb_x else -1
                for check_x in range(bomb_x + step, x, step):
                    if game_state.grid[check_y][check_x] in [1, 2]:  # Wall or destructible
                        blocked = True
                        break
                if not blocked:
                    return False
            
            # Check if in vertical blast line
            if bomb_x == x and abs(bomb_y - y) <= bomb_range:
                # Check if there's a wall blocking
                blocked = False
                step = 1 if y > bomb_y else -1
                for check_y in range(bomb_y + step, y, step):
                    if game_state.grid[check_y][x] in [1, 2]:  # Wall or destructible
                        blocked = True
                        break
                if not blocked:
                    return False
        
        return True
    
    @staticmethod
    def get_unblocked_directions(player, game_state):
        """
        Get all unblocked movement directions.
        
        Args:
            player: Player entity
            game_state: Current game state
            
        Returns:
            List of (dx, dy) tuples for valid moves
        """
        px, py = int(player.x), int(player.y)
        directions = []
        
        # Check all 4 directions
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = px + dx, py + dy
            
            # Check bounds
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                # Check if walkable
                if game_state.grid[new_y][new_x] == 0:
                    directions.append((dx, dy))
        
        return directions
    
    @staticmethod
    def get_safe_directions(player, game_state):
        """
        Get safe movement directions (unblocked and away from danger).
        
        Args:
            player: Player entity
            game_state: Current game state
            
        Returns:
            List of (dx, dy) tuples for safe moves
        """
        px, py = int(player.x), int(player.y)
        safe_dirs = []
        
        unblocked = GameHeuristics.get_unblocked_directions(player, game_state)
        
        for dx, dy in unblocked:
            new_x, new_y = px + dx, py + dy
            if GameHeuristics.is_safe_position(new_x, new_y, game_state):
                safe_dirs.append((dx, dy))
        
        return safe_dirs
    
    @staticmethod
    def should_place_bomb(player, game_state):
        """
        IMPROVED Heuristic: Should the player place a bomb?
        
        Args:
            player: Player entity
            game_state: Current game state
            
        Returns:
            True if bomb should be placed, False otherwise
        """
        if player.active_bombs >= player.max_bombs:
            return False
        
        px, py = int(player.x), int(player.y)
        
        # Must have escape route
        safe_dirs = GameHeuristics.get_safe_directions(player, game_state)
        if len(safe_dirs) == 0:
            return False
        
        # Count destructible walls in range
        walls_in_range = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, player.bomb_range + 1):
                check_x = px + dx * dist
                check_y = py + dy * dist
                
                if 0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE:
                    if game_state.grid[check_y][check_x] == 2:  # Destructible wall
                        walls_in_range += 1
                    elif game_state.grid[check_y][check_x] == 1:  # Hard wall
                        break  # Can't see past walls
        
        # Place bomb if 2+ walls in range (efficient)
        if walls_in_range >= 2:
            return True
        
        # Place bomb if 1 wall and no better position nearby
        if walls_in_range == 1:
            return random.random() < 0.7  # 70% chance
        
        # Check if enemy is in bomb range
        for other_player in game_state.players:
            if other_player != player and other_player.alive:
                enemy_x, enemy_y = int(other_player.x), int(other_player.y)
                
                # Check if enemy is in direct line
                if enemy_y == py and abs(enemy_x - px) <= player.bomb_range:
                    # Check no walls blocking
                    blocked = False
                    step = 1 if enemy_x > px else -1
                    for check_x in range(px + step, enemy_x, step):
                        if game_state.grid[py][check_x] in [1, 2]:
                            blocked = True
                            break
                    if not blocked:
                        return random.random() < 0.8  # 80% chance to trap enemy
                
                if enemy_x == px and abs(enemy_y - py) <= player.bomb_range:
                    # Check no walls blocking
                    blocked = False
                    step = 1 if enemy_y > py else -1
                    for check_y in range(py + step, enemy_y, step):
                        if game_state.grid[check_y][px] in [1, 2]:
                            blocked = True
                            break
                    if not blocked:
                        return random.random() < 0.8  # 80% chance to trap enemy
                
                # Enemy nearby but not in direct line
                dist = abs(px - enemy_x) + abs(py - enemy_y)
                if dist <= 3:
                    return random.random() < 0.4  # 40% chance
        
        return False
    
    @staticmethod
    def get_escape_direction(player, game_state):
        """
        Get direction to escape from danger.
        
        Args:
            player: Player entity
            game_state: Current game state
            
        Returns:
            (dx, dy) tuple for escape direction, or (0, 0) if safe
        """
        px, py = int(player.x), int(player.y)
        
        # If current position is safe, no need to escape
        if GameHeuristics.is_safe_position(px, py, game_state):
            return (0, 0)
        
        # Get safe directions
        safe_dirs = GameHeuristics.get_safe_directions(player, game_state)
        
        if safe_dirs:
            # Find direction that moves away from nearest bomb
            nearest_bomb = None
            min_dist = float('inf')
            
            for bomb in game_state.bombs:
                dist = abs(px - bomb.grid_x) + abs(py - bomb.grid_y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_bomb = bomb
            
            if nearest_bomb:
                # Move away from bomb
                best_dir = None
                max_dist = -1
                
                for dx, dy in safe_dirs:
                    new_x, new_y = px + dx, py + dy
                    dist = abs(new_x - nearest_bomb.grid_x) + abs(new_y - nearest_bomb.grid_y)
                    if dist > max_dist:
                        max_dist = dist
                        best_dir = (dx, dy)
                
                return best_dir if best_dir else safe_dirs[0]
            
            return safe_dirs[0]
        
        # No safe direction, try any unblocked direction
        unblocked = GameHeuristics.get_unblocked_directions(player, game_state)
        return unblocked[0] if unblocked else (0, 0)
    
    @staticmethod
    def get_heuristic_action(player, game_state):
        """
        Get a complete heuristic action based on game state.
        
        This combines multiple heuristics:
        1. Escape from danger if in danger
        2. Place bomb if strategic
        3. Move towards objectives (walls, enemies, powerups)
        
        Args:
            player: Player entity
            game_state: Current game state
            
        Returns:
            (dx, dy, place_bomb) action tuple
        """
        px, py = int(player.x), int(player.y)
        
        # Priority 1: Escape from danger
        if not GameHeuristics.is_safe_position(px, py, game_state):
            escape_dir = GameHeuristics.get_escape_direction(player, game_state)
            return (escape_dir[0], escape_dir[1], False)
        
        # Priority 2: Place bomb if strategic
        place_bomb = GameHeuristics.should_place_bomb(player, game_state)
        
        # Priority 3: Movement strategy
        safe_dirs = GameHeuristics.get_safe_directions(player, game_state)
        
        if not safe_dirs:
            # No safe moves, stay put or try unblocked
            unblocked = GameHeuristics.get_unblocked_directions(player, game_state)
            if unblocked:
                move = random.choice(unblocked)
                return (move[0], move[1], place_bomb)
            return (0, 0, place_bomb)
        
        # Find nearest objective
        best_dir = None
        min_dist = float('inf')
        
        # Check for destructible walls
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if game_state.grid[y][x] == 2:  # Destructible wall
                    dist = abs(px - x) + abs(py - y)
                    if dist < min_dist:
                        min_dist = dist
                        # Move towards it
                        for dx, dy in safe_dirs:
                            new_dist = abs((px + dx) - x) + abs((py + dy) - y)
                            if new_dist < dist:
                                best_dir = (dx, dy)
                                break
        
        # Check for powerups
        for pos, powerup in game_state.powerups.items():
            x, y = pos
            dist = abs(px - x) + abs(py - y)
            if dist < min_dist:
                min_dist = dist
                # Move towards it
                for dx, dy in safe_dirs:
                    new_dist = abs((px + dx) - x) + abs((py + dy) - y)
                    if new_dist < dist:
                        best_dir = (dx, dy)
                        break
        
        # Check for enemies
        for other_player in game_state.players:
            if other_player != player and other_player.alive:
                enemy_x, enemy_y = int(other_player.x), int(other_player.y)
                dist = abs(px - enemy_x) + abs(py - enemy_y)
                
                # Don't get too close without a bomb
                if dist > 3 and dist < min_dist:
                    min_dist = dist
                    # Move towards enemy
                    for dx, dy in safe_dirs:
                        new_dist = abs((px + dx) - enemy_x) + abs((py + dy) - enemy_y)
                        if new_dist < dist:
                            best_dir = (dx, dy)
                            break
        
        # If no objective found, explore randomly
        if best_dir is None:
            best_dir = random.choice(safe_dirs)
        
        return (best_dir[0], best_dir[1], place_bomb)


class HeuristicAgent:
    """Agent that uses pure heuristics (for bootstrapping)."""
    
    def __init__(self, player):
        """Initialize heuristic agent."""
        self.player = player
        self.think_timer = 0
        self.think_delay = 0.2
        self.current_action = None
    
    def choose_action(self, game_state):
        """Choose action using heuristics."""
        return GameHeuristics.get_heuristic_action(self.player, game_state)
    
    def update(self, dt, game_state):
        """Update agent."""
        self.think_timer += dt
        
        if self.think_timer >= self.think_delay:
            self.think_timer = 0
            self.current_action = self.choose_action(game_state)
        
        return self.current_action
