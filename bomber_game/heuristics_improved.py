"""
IMPROVED Heuristic strategies with game industry best practices.
Includes A* pathfinding, weighted evaluation functions, and strategic decision-making.

Based on research from:
- A* pathfinding for Bomberman (gocoder.one)
- Game AI evaluation functions
- Reinforcement learning bootstrapping techniques
"""

import random
import heapq
from collections import deque
from . import GRID_SIZE


class PathNode:
    """Node for A* pathfinding."""
    
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Cost from start
        self.h = h  # Heuristic to goal
        self.f = g + h  # Total cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))


class ImprovedHeuristics:
    """
    Improved heuristics using game industry best practices.
    
    Features:
    - A* pathfinding for optimal movement
    - Weighted evaluation function
    - Danger zone prediction
    - Strategic bomb placement
    - Power-up prioritization
    """
    
    # Evaluation weights (tuned for better performance)
    WEIGHTS = {
        'safety': 10.0,          # Highest priority: stay alive
        'powerup': 8.0,          # High priority: collect power-ups
        'wall_destruction': 5.0, # Medium: destroy walls
        'enemy_threat': 7.0,     # High: attack enemies
        'position_control': 3.0, # Low: control center
        'escape_route': 9.0,     # Very high: ensure escape
    }
    
    @staticmethod
    def manhattan_distance(x1, y1, x2, y2):
        """Calculate Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)
    
    @staticmethod
    def get_danger_map(game_state):
        """
        Create a danger map showing explosion risk for each tile.
        
        Returns:
            2D array where higher values = more dangerous
        """
        danger_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Mark current explosions (maximum danger)
        for explosion in game_state.explosions:
            danger_map[explosion.grid_y][explosion.grid_x] = 100
        
        # Mark bomb blast zones (scaled by time remaining)
        for bomb in game_state.bombs:
            bx, by = bomb.grid_x, bomb.grid_y
            bomb_range = bomb.bomb_range
            time_factor = max(10, bomb.timer * 10)  # More danger = less time
            
            # Center of bomb
            danger_map[by][bx] = time_factor
            
            # Blast in 4 directions
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                for dist in range(1, bomb_range + 1):
                    check_x = bx + dx * dist
                    check_y = by + dy * dist
                    
                    if 0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE:
                        if game_state.grid[check_y][check_x] == 1:  # Hard wall
                            break
                        danger_map[check_y][check_x] = max(
                            danger_map[check_y][check_x],
                            time_factor
                        )
                        if game_state.grid[check_y][check_x] == 2:  # Soft wall
                            break
        
        return danger_map
    
    @staticmethod
    def astar_pathfind(start_x, start_y, goal_x, goal_y, game_state, avoid_danger=True):
        """
        A* pathfinding algorithm for optimal path finding.
        
        Args:
            start_x, start_y: Starting position
            goal_x, goal_y: Goal position
            game_state: Current game state
            avoid_danger: Whether to avoid dangerous tiles
            
        Returns:
            List of (x, y) positions forming the path, or None if no path
        """
        if start_x == goal_x and start_y == goal_y:
            return [(start_x, start_y)]
        
        danger_map = ImprovedHeuristics.get_danger_map(game_state) if avoid_danger else None
        
        open_set = []
        closed_set = set()
        
        start_node = PathNode(start_x, start_y, 0, 
                             ImprovedHeuristics.manhattan_distance(start_x, start_y, goal_x, goal_y))
        heapq.heappush(open_set, start_node)
        
        nodes_dict = {(start_x, start_y): start_node}
        max_iterations = 500  # Prevent infinite loops
        iterations = 0
        
        while open_set and iterations < max_iterations:
            iterations += 1
            current = heapq.heappop(open_set)
            
            if current.x == goal_x and current.y == goal_y:
                # Reconstruct path
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return list(reversed(path))
            
            closed_set.add((current.x, current.y))
            
            # Check neighbors
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = current.x + dx, current.y + dy
                
                # Check bounds
                if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
                    continue
                
                # Check if walkable
                if game_state.grid[ny][nx] != 0:
                    continue
                
                # Skip if in closed set
                if (nx, ny) in closed_set:
                    continue
                
                # Calculate cost (add danger penalty)
                move_cost = 1
                if danger_map and danger_map[ny][nx] > 0:
                    move_cost += danger_map[ny][nx] * 0.5  # Penalty for dangerous tiles
                
                g = current.g + move_cost
                h = ImprovedHeuristics.manhattan_distance(nx, ny, goal_x, goal_y)
                
                # Check if we've seen this node before
                if (nx, ny) in nodes_dict:
                    existing = nodes_dict[(nx, ny)]
                    if g < existing.g:
                        # Found better path
                        existing.g = g
                        existing.f = g + h
                        existing.parent = current
                        heapq.heappush(open_set, existing)
                else:
                    # New node
                    neighbor = PathNode(nx, ny, g, h, current)
                    nodes_dict[(nx, ny)] = neighbor
                    heapq.heappush(open_set, neighbor)
        
        return None  # No path found
    
    @staticmethod
    def evaluate_position(x, y, player, game_state):
        """
        Evaluate a position using weighted heuristics.
        
        Returns:
            Score (higher = better position)
        """
        score = 0.0
        danger_map = ImprovedHeuristics.get_danger_map(game_state)
        
        # Safety evaluation (negative for danger)
        if danger_map[y][x] > 0:
            score -= ImprovedHeuristics.WEIGHTS['safety'] * danger_map[y][x]
        else:
            score += ImprovedHeuristics.WEIGHTS['safety']
        
        # Power-up proximity
        for pos, powerup in game_state.powerups.items():
            px, py = pos
            dist = ImprovedHeuristics.manhattan_distance(x, y, px, py)
            if dist > 0:
                # Closer = better, with diminishing returns
                powerup_score = ImprovedHeuristics.WEIGHTS['powerup'] / (dist + 1)
                score += powerup_score
        
        # Wall destruction potential
        walls_nearby = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, player.bomb_range + 1):
                check_x = x + dx * dist
                check_y = y + dy * dist
                
                if 0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE:
                    if game_state.grid[check_y][check_x] == 2:
                        walls_nearby += 1
                    elif game_state.grid[check_y][check_x] == 1:
                        break
        
        score += ImprovedHeuristics.WEIGHTS['wall_destruction'] * walls_nearby
        
        # Enemy threat/opportunity
        for other_player in game_state.players:
            if other_player != player and other_player.alive:
                ex, ey = int(other_player.x), int(other_player.y)
                dist = ImprovedHeuristics.manhattan_distance(x, y, ex, ey)
                
                # Optimal distance: 3-5 tiles (close enough to attack, far enough to escape)
                if 3 <= dist <= 5:
                    score += ImprovedHeuristics.WEIGHTS['enemy_threat']
                elif dist < 3:
                    score -= ImprovedHeuristics.WEIGHTS['enemy_threat'] * 0.5  # Too close
        
        # Position control (center is strategic)
        center_x, center_y = GRID_SIZE // 2, GRID_SIZE // 2
        center_dist = ImprovedHeuristics.manhattan_distance(x, y, center_x, center_y)
        score += ImprovedHeuristics.WEIGHTS['position_control'] * (GRID_SIZE - center_dist) / GRID_SIZE
        
        # Escape route availability
        escape_routes = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0 and danger_map[ny][nx] == 0:
                    escape_routes += 1
        
        score += ImprovedHeuristics.WEIGHTS['escape_route'] * escape_routes
        
        return score
    
    @staticmethod
    def should_place_bomb_improved(player, game_state):
        """
        Improved bomb placement decision using evaluation function.
        
        Returns:
            (should_place, confidence) tuple
        """
        if player.active_bombs >= player.max_bombs:
            return False, 0.0
        
        px, py = int(player.x), int(player.y)
        
        # Check escape routes
        danger_map = ImprovedHeuristics.get_danger_map(game_state)
        escape_routes = 0
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = px + dx, py + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0:
                    # Simulate bomb placement
                    temp_danger = danger_map[ny][nx]
                    if temp_danger == 0:
                        escape_routes += 1
        
        if escape_routes == 0:
            return False, 0.0  # No escape!
        
        # Evaluate bomb placement value
        value = 0.0
        
        # Count destructible walls
        walls_in_range = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, player.bomb_range + 1):
                check_x = px + dx * dist
                check_y = py + dy * dist
                
                if 0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE:
                    if game_state.grid[check_y][check_x] == 2:
                        walls_in_range += 1
                        value += 2.0
                    elif game_state.grid[check_y][check_x] == 1:
                        break
        
        # Check for enemies in range
        for other_player in game_state.players:
            if other_player != player and other_player.alive:
                ex, ey = int(other_player.x), int(other_player.y)
                
                # Check if in blast range
                if ey == py and abs(ex - px) <= player.bomb_range:
                    blocked = False
                    step = 1 if ex > px else -1
                    for check_x in range(px + step, ex, step):
                        if game_state.grid[py][check_x] in [1, 2]:
                            blocked = True
                            break
                    if not blocked:
                        value += 10.0  # High value for enemy hit
                
                if ex == px and abs(ey - py) <= player.bomb_range:
                    blocked = False
                    step = 1 if ey > py else -1
                    for check_y in range(py + step, ey, step):
                        if game_state.grid[check_y][px] in [1, 2]:
                            blocked = True
                            break
                    if not blocked:
                        value += 10.0
        
        # Decision threshold based on value and escape routes
        confidence = min(1.0, value / 15.0)  # Normalize to 0-1
        should_place = value >= 2.0 and escape_routes >= 2
        
        return should_place, confidence
    
    @staticmethod
    def get_best_action(player, game_state):
        """
        Get best action using improved heuristics and A* pathfinding.
        
        Returns:
            (dx, dy, place_bomb, confidence) tuple
        """
        px, py = int(player.x), int(player.y)
        danger_map = ImprovedHeuristics.get_danger_map(game_state)
        
        # Priority 1: Escape from immediate danger
        if danger_map[py][px] > 50:
            # Find safest adjacent tile
            best_dir = None
            min_danger = float('inf')
            
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:
                nx, ny = px + dx, py + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if game_state.grid[ny][nx] == 0:
                        if danger_map[ny][nx] < min_danger:
                            min_danger = danger_map[ny][nx]
                            best_dir = (dx, dy)
            
            if best_dir:
                return (best_dir[0], best_dir[1], False, 1.0)  # High confidence escape
        
        # Priority 2: Strategic bomb placement
        should_bomb, bomb_confidence = ImprovedHeuristics.should_place_bomb_improved(player, game_state)
        
        # Priority 3: Find best position using A* and evaluation
        best_target = None
        best_score = -float('inf')
        
        # Evaluate nearby positions
        search_radius = 5
        for y in range(max(0, py - search_radius), min(GRID_SIZE, py + search_radius + 1)):
            for x in range(max(0, px - search_radius), min(GRID_SIZE, px + search_radius + 1)):
                if game_state.grid[y][x] == 0:
                    score = ImprovedHeuristics.evaluate_position(x, y, player, game_state)
                    if score > best_score:
                        best_score = score
                        best_target = (x, y)
        
        # Use A* to find path to best target
        if best_target:
            path = ImprovedHeuristics.astar_pathfind(px, py, best_target[0], best_target[1], 
                                                     game_state, avoid_danger=True)
            if path and len(path) > 1:
                next_pos = path[1]  # First step in path
                dx = next_pos[0] - px
                dy = next_pos[1] - py
                confidence = min(1.0, best_score / 50.0)
                return (dx, dy, should_bomb, confidence)
        
        # Fallback: safe random move
        safe_moves = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = px + dx, py + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0 and danger_map[ny][nx] < 10:
                    safe_moves.append((dx, dy))
        
        if safe_moves:
            move = random.choice(safe_moves)
            return (move[0], move[1], should_bomb, 0.3)
        
        return (0, 0, False, 0.1)


class ImprovedHeuristicAgent:
    """Agent using improved heuristics with performance tracking."""
    
    def __init__(self, player):
        self.player = player
        self.think_timer = 0
        self.think_delay = 0.15  # Faster thinking
        self.current_action = None
        
        # Performance tracking
        self.total_games = 0
        self.wins = 0
        self.total_reward = 0.0
        self.actions_taken = 0
        self.bombs_placed = 0
        self.walls_destroyed = 0
        self.powerups_collected = 0
    
    def choose_action(self, game_state):
        """Choose action using improved heuristics."""
        dx, dy, place_bomb, confidence = ImprovedHeuristics.get_best_action(self.player, game_state)
        
        # Track statistics
        self.actions_taken += 1
        if place_bomb:
            self.bombs_placed += 1
        
        return (dx, dy, place_bomb)
    
    def update(self, dt, game_state):
        """Update agent with performance tracking."""
        self.think_timer += dt
        
        if self.think_timer >= self.think_delay:
            self.think_timer = 0
            self.current_action = self.choose_action(game_state)
        
        return self.current_action
    
    def record_game_result(self, won, reward):
        """Record game result for statistics."""
        self.total_games += 1
        if won:
            self.wins += 1
        self.total_reward += reward
    
    def get_win_rate(self):
        """Get current win rate."""
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games
    
    def get_average_reward(self):
        """Get average reward per game."""
        if self.total_games == 0:
            return 0.0
        return self.total_reward / self.total_games
    
    def get_stats_string(self):
        """Get formatted statistics string."""
        win_rate = self.get_win_rate() * 100
        avg_reward = self.get_average_reward()
        
        # Determine skill level
        if win_rate >= 70:
            level = "Expert"
        elif win_rate >= 50:
            level = "Advanced"
        elif win_rate >= 30:
            level = "Intermediate"
        elif win_rate >= 10:
            level = "Beginner"
        else:
            level = "Learning"
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║           🤖 IMPROVED HEURISTIC AI - PERFORMANCE             ║
╠══════════════════════════════════════════════════════════════╣
║  Skill Level:      {level:<40} ║
║  Win Rate:         {win_rate:>6.2f}%                                 ║
║  Average Reward:   {avg_reward:>8.2f}                               ║
║  Games Played:     {self.total_games:<40} ║
║  Total Wins:       {self.wins:<40} ║
║  Bombs Placed:     {self.bombs_placed:<40} ║
║  Actions Taken:    {self.actions_taken:<40} ║
╚══════════════════════════════════════════════════════════════╝
"""
