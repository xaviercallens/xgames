"""
Advanced Smart Heuristic AI for PROUTMAN.
Enhanced decision-making with predictive planning, game tree evaluation, and strategic positioning.

Features:
- Multi-step lookahead planning
- Game tree evaluation with minimax
- Predictive bomb placement
- Strategic positioning analysis
- Risk/reward calculation
- Opponent behavior prediction
- Dynamic strategy selection
"""

import random
import math
from collections import deque
from typing import Tuple, List, Dict, Optional
from . import GRID_SIZE


class GameTreeNode:
    """Node in game tree for minimax evaluation."""
    
    def __init__(self, state: Dict, depth: int = 0, is_max: bool = True):
        """Initialize game tree node."""
        self.state = state
        self.depth = depth
        self.is_max = is_max
        self.children = []
        self.value = None
    
    def add_child(self, child: 'GameTreeNode'):
        """Add child node."""
        self.children.append(child)
    
    def is_terminal(self) -> bool:
        """Check if terminal node."""
        return len(self.children) == 0


class PredictiveAnalysis:
    """Predictive analysis for bomb placement and movement."""
    
    @staticmethod
    def predict_bomb_explosion(bomb_x: int, bomb_y: int, bomb_range: int, 
                               grid: List[List[int]], time_remaining: float) -> Dict:
        """
        Predict bomb explosion impact.
        
        Returns:
            Dictionary with explosion predictions
        """
        predictions = {
            'blast_zone': set(),
            'walls_destroyed': 0,
            'safe_zones': [],
            'danger_level': 0.0,
            'time_to_explosion': time_remaining,
        }
        
        # Calculate blast zone
        blast_zone = set()
        blast_zone.add((bomb_x, bomb_y))
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, bomb_range + 1):
                check_x = bomb_x + dx * dist
                check_y = bomb_y + dy * dist
                
                if not (0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE):
                    break
                
                if grid[check_y][check_x] == 1:  # Hard wall
                    break
                
                blast_zone.add((check_x, check_y))
                
                if grid[check_y][check_x] == 2:  # Soft wall
                    predictions['walls_destroyed'] += 1
                    break
        
        predictions['blast_zone'] = blast_zone
        predictions['danger_level'] = 100.0 * (1.0 - time_remaining / 3.0)  # Increases as time runs out
        
        return predictions
    
    @staticmethod
    def find_escape_paths(player_x: int, player_y: int, bomb_x: int, bomb_y: int,
                         bomb_range: int, grid: List[List[int]], 
                         max_depth: int = 5) -> List[List[Tuple[int, int]]]:
        """
        Find multiple escape paths from bomb.
        
        Returns:
            List of escape paths
        """
        paths = []
        visited = set()
        queue = deque([(player_x, player_y, [(player_x, player_y)])])
        
        while queue:
            x, y, path = queue.popleft()
            
            if len(path) > max_depth:
                if path not in paths:
                    paths.append(path)
                continue
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            # Check if safe from bomb
            distance = abs(x - bomb_x) + abs(y - bomb_y)
            if distance > bomb_range + 2:
                if path not in paths:
                    paths.append(path)
                continue
            
            # Explore neighbors
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if grid[ny][nx] == 0 and (nx, ny) not in visited:
                        new_path = path + [(nx, ny)]
                        queue.append((nx, ny, new_path))
        
        return paths


class StrategicPositioning:
    """Strategic positioning analysis."""
    
    @staticmethod
    def calculate_position_value(x: int, y: int, player, opponent, 
                                game_state) -> float:
        """
        Calculate strategic value of a position.
        
        Returns:
            Position value score
        """
        value = 0.0
        
        # Control center (strategic advantage)
        center_x, center_y = GRID_SIZE // 2, GRID_SIZE // 2
        center_distance = abs(x - center_x) + abs(y - center_y)
        center_value = (GRID_SIZE - center_distance) / GRID_SIZE
        value += center_value * 5.0
        
        # Distance to opponent (tactical advantage)
        opponent_distance = abs(x - int(opponent.x)) + abs(y - int(opponent.y))
        if 3 <= opponent_distance <= 6:
            value += 10.0  # Optimal attacking distance
        elif opponent_distance < 3:
            value -= 5.0   # Too close
        elif opponent_distance > 8:
            value -= 3.0   # Too far
        
        # Wall proximity (destruction potential)
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
        
        value += walls_nearby * 2.0
        
        # Power-up proximity
        for pos in game_state.powerups:
            px, py = pos
            powerup_distance = abs(x - px) + abs(y - py)
            if powerup_distance < 8:
                value += 5.0 / (powerup_distance + 1)
        
        # Escape route availability
        escape_routes = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0:
                    escape_routes += 1
        
        value += escape_routes * 3.0
        
        return value
    
    @staticmethod
    def find_strategic_positions(player, opponent, game_state, 
                                search_radius: int = 7) -> List[Tuple[int, int, float]]:
        """
        Find all strategic positions with values.
        
        Returns:
            List of (x, y, value) tuples
        """
        positions = []
        player_x, player_y = int(player.x), int(player.y)
        
        for y in range(max(0, player_y - search_radius), 
                      min(GRID_SIZE, player_y + search_radius + 1)):
            for x in range(max(0, player_x - search_radius), 
                          min(GRID_SIZE, player_x + search_radius + 1)):
                
                if game_state.grid[y][x] != 0:
                    continue
                
                value = StrategicPositioning.calculate_position_value(
                    x, y, player, opponent, game_state
                )
                positions.append((x, y, value))
        
        # Sort by value (descending)
        positions.sort(key=lambda p: p[2], reverse=True)
        return positions


class GameTreeEvaluation:
    """Game tree evaluation with minimax algorithm."""
    
    @staticmethod
    def evaluate_state(player, opponent, game_state, depth: int = 0) -> float:
        """
        Evaluate game state using heuristic evaluation function.
        
        Returns:
            State evaluation score
        """
        if depth > 3:  # Limit depth
            return GameTreeEvaluation._heuristic_eval(player, opponent, game_state)
        
        # Terminal states
        if not opponent.alive:
            return 1000.0  # Winning state
        if not player.alive:
            return -1000.0  # Losing state
        
        return GameTreeEvaluation._heuristic_eval(player, opponent, game_state)
    
    @staticmethod
    def _heuristic_eval(player, opponent, game_state) -> float:
        """Heuristic evaluation function."""
        score = 0.0
        
        # Player advantage
        if player.bomb_range > opponent.bomb_range:
            score += 50.0
        if player.max_bombs > opponent.max_bombs:
            score += 30.0
        
        # Position advantage
        player_pos_value = StrategicPositioning.calculate_position_value(
            int(player.x), int(player.y), player, opponent, game_state
        )
        opponent_pos_value = StrategicPositioning.calculate_position_value(
            int(opponent.x), int(opponent.y), opponent, player, game_state
        )
        
        score += (player_pos_value - opponent_pos_value) * 2.0
        
        # Resource advantage
        score += (player.active_bombs - opponent.active_bombs) * 10.0
        
        return score
    
    @staticmethod
    def minimax(player, opponent, game_state, depth: int = 0, 
                is_maximizing: bool = True, alpha: float = -float('inf'),
                beta: float = float('inf')) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Returns:
            Best evaluation score
        """
        if depth >= 2:  # Limit search depth
            return GameTreeEvaluation.evaluate_state(player, opponent, game_state, depth)
        
        if is_maximizing:
            max_eval = -float('inf')
            
            # Try different moves
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:
                # Simulate move
                new_x = int(player.x) + dx
                new_y = int(player.y) + dy
                
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    if game_state.grid[new_y][new_x] == 0:
                        # Evaluate this move
                        eval_score = GameTreeEvaluation.minimax(
                            player, opponent, game_state, depth + 1, False, alpha, beta
                        )
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        
                        if beta <= alpha:
                            break  # Beta cutoff
            
            return max_eval if max_eval != -float('inf') else 0.0
        else:
            min_eval = float('inf')
            
            # Opponent tries to minimize
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:
                new_x = int(opponent.x) + dx
                new_y = int(opponent.y) + dy
                
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    if game_state.grid[new_y][new_x] == 0:
                        eval_score = GameTreeEvaluation.minimax(
                            player, opponent, game_state, depth + 1, True, alpha, beta
                        )
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        
                        if beta <= alpha:
                            break  # Alpha cutoff
            
            return min_eval if min_eval != float('inf') else 0.0


class OpponentModeling:
    """Model and predict opponent behavior."""
    
    def __init__(self):
        """Initialize opponent modeling."""
        self.move_history = deque(maxlen=20)
        self.bomb_history = deque(maxlen=10)
        self.predicted_moves = []
    
    def record_move(self, x: int, y: int, placed_bomb: bool):
        """Record opponent move."""
        self.move_history.append((x, y))
        if placed_bomb:
            self.bomb_history.append((x, y))
    
    def predict_next_position(self, opponent_x: int, opponent_y: int) -> Tuple[int, int]:
        """
        Predict opponent's next position.
        
        Returns:
            Predicted (x, y) position
        """
        if len(self.move_history) < 2:
            return int(opponent_x), int(opponent_y)
        
        # Calculate velocity from recent moves
        recent_x = [m[0] for m in list(self.move_history)[-5:]]
        recent_y = [m[1] for m in list(self.move_history)[-5:]]
        
        if len(recent_x) > 1:
            vx = recent_x[-1] - recent_x[-2]
            vy = recent_y[-1] - recent_y[-2]
        else:
            vx, vy = 0, 0
        
        predicted_x = int(opponent_x) + vx
        predicted_y = int(opponent_y) + vy
        
        # Clamp to grid
        predicted_x = max(0, min(GRID_SIZE - 1, predicted_x))
        predicted_y = max(0, min(GRID_SIZE - 1, predicted_y))
        
        return predicted_x, predicted_y
    
    def predict_bomb_placement_probability(self, opponent_x: int, opponent_y: int) -> float:
        """
        Predict probability opponent will place bomb.
        
        Returns:
            Probability (0.0-1.0)
        """
        if len(self.bomb_history) == 0:
            return 0.3  # Default probability
        
        # Calculate bomb placement frequency
        bomb_frequency = len(self.bomb_history) / max(1, len(self.move_history))
        
        # Adjust based on proximity to walls
        walls_nearby = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, 4):
                check_x = int(opponent_x) + dx * dist
                check_y = int(opponent_y) + dy * dist
                
                if 0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE:
                    if check_x == int(opponent_x) and check_y == int(opponent_y):
                        continue
        
        return min(1.0, bomb_frequency + 0.2)


class DynamicStrategySelection:
    """Dynamically select strategy based on game state."""
    
    @staticmethod
    def select_strategy(player, opponent, game_state) -> str:
        """
        Select best strategy for current game state.
        
        Returns:
            Strategy name: 'aggressive', 'defensive', 'balanced', 'evasive'
        """
        player_x, player_y = int(player.x), int(player.y)
        opponent_x, opponent_y = int(opponent.x), int(opponent.y)
        
        distance = abs(player_x - opponent_x) + abs(player_y - opponent_y)
        
        # Evaluate player strength
        player_strength = (player.bomb_range + player.max_bombs) / 4.0
        opponent_strength = (opponent.bomb_range + opponent.max_bombs) / 4.0
        strength_ratio = player_strength / max(1.0, opponent_strength)
        
        # Select strategy
        if strength_ratio > 1.3 and distance < 8:
            return 'aggressive'  # Strong and close: attack
        elif strength_ratio < 0.7 and distance < 6:
            return 'evasive'  # Weak and close: escape
        elif distance > 10:
            return 'balanced'  # Far apart: balanced approach
        else:
            return 'defensive'  # Default: defensive


class AdvancedSmartHeuristic:
    """Advanced smart heuristic AI with predictive planning."""
    
    def __init__(self, player):
        """Initialize advanced smart heuristic."""
        self.player = player
        self.predictive_analysis = PredictiveAnalysis()
        self.strategic_positioning = StrategicPositioning()
        self.game_tree = GameTreeEvaluation()
        self.opponent_model = OpponentModeling()
        self.strategy_selector = DynamicStrategySelection()
        
        # Performance tracking
        self.total_games = 0
        self.wins = 0
        self.total_reward = 0.0
        self.actions_taken = 0
        self.bombs_placed = 0
        self.strategy_history = []
        
        # Timing
        self.think_timer = 0
        self.think_delay = 0.15  # Thinking delay in seconds
        self.current_action = None
    
    def choose_action(self, player, opponent, game_state) -> Tuple[int, int, bool]:
        """
        Choose action using advanced smart heuristics.
        
        Returns:
            (dx, dy, place_bomb) tuple
        """
        px, py = int(player.x), int(player.y)
        
        # Select strategy
        strategy = self.strategy_selector.select_strategy(player, opponent, game_state)
        self.strategy_history.append(strategy)
        
        # Execute strategy
        if strategy == 'aggressive':
            return self._aggressive_strategy(player, opponent, game_state)
        elif strategy == 'defensive':
            return self._defensive_strategy(player, opponent, game_state)
        elif strategy == 'evasive':
            return self._evasive_strategy(player, opponent, game_state)
        else:
            return self._balanced_strategy(player, opponent, game_state)
    
    def update(self, dt, game_state):
        """
        Update agent with timing control.
        
        Args:
            dt: Delta time in seconds
            game_state: Current game state
            
        Returns:
            Current action tuple (dx, dy, place_bomb)
        """
        self.think_timer += dt
        
        if self.think_timer >= self.think_delay:
            self.think_timer = 0
            # Get opponent from game state
            opponent = None
            for player in game_state.players:
                if player != self.player:
                    opponent = player
                    break
            
            if opponent:
                self.current_action = self.choose_action(self.player, opponent, game_state)
            else:
                self.current_action = (0, 0, False)
        
        return self.current_action if self.current_action else (0, 0, False)
    
    def _aggressive_strategy(self, player, opponent, game_state) -> Tuple[int, int, bool]:
        """Aggressive strategy: pursue and attack opponent."""
        px, py = int(player.x), int(player.y)
        ox, oy = int(opponent.x), int(opponent.y)
        
        # Move towards opponent
        dx = 1 if ox > px else (-1 if ox < px else 0)
        dy = 1 if oy > py else (-1 if oy < py else 0)
        
        # Verify move is safe
        if 0 <= px + dx < GRID_SIZE and 0 <= py + dy < GRID_SIZE:
            if game_state.grid[py + dy][px + dx] == 0:
                # Place bomb if close and safe
                should_bomb = abs(ox - px) <= 4 and player.active_bombs < player.max_bombs
                self.actions_taken += 1
                if should_bomb:
                    self.bombs_placed += 1
                return (dx, dy, should_bomb)
        
        # Fallback
        self.actions_taken += 1
        return (0, 0, False)
    
    def _defensive_strategy(self, player, opponent, game_state) -> Tuple[int, int, bool]:
        """Defensive strategy: maintain distance and control."""
        px, py = int(player.x), int(player.y)
        
        # Find best strategic position
        positions = self.strategic_positioning.find_strategic_positions(
            player, opponent, game_state, search_radius=5
        )
        
        if positions:
            target_x, target_y, _ = positions[0]
            dx = 1 if target_x > px else (-1 if target_x < px else 0)
            dy = 1 if target_y > py else (-1 if target_y < py else 0)
            
            # Place bomb if strategic
            should_bomb = player.active_bombs < player.max_bombs and random.random() < 0.3
            self.actions_taken += 1
            if should_bomb:
                self.bombs_placed += 1
            return (dx, dy, should_bomb)
        
        self.actions_taken += 1
        return (0, 0, False)
    
    def _evasive_strategy(self, player, opponent, game_state) -> Tuple[int, int, bool]:
        """Evasive strategy: escape from opponent."""
        px, py = int(player.x), int(player.y)
        ox, oy = int(opponent.x), int(opponent.y)
        
        # Move away from opponent
        dx = -1 if ox > px else (1 if ox < px else 0)
        dy = -1 if oy > py else (1 if oy < py else 0)
        
        # Verify move is safe
        if 0 <= px + dx < GRID_SIZE and 0 <= py + dy < GRID_SIZE:
            if game_state.grid[py + dy][px + dx] == 0:
                self.actions_taken += 1
                return (dx, dy, False)
        
        # Try alternative escape
        for alt_dx, alt_dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            if 0 <= px + alt_dx < GRID_SIZE and 0 <= py + alt_dy < GRID_SIZE:
                if game_state.grid[py + alt_dy][px + alt_dx] == 0:
                    self.actions_taken += 1
                    return (alt_dx, alt_dy, False)
        
        self.actions_taken += 1
        return (0, 0, False)
    
    def _balanced_strategy(self, player, opponent, game_state) -> Tuple[int, int, bool]:
        """Balanced strategy: opportunistic approach."""
        px, py = int(player.x), int(player.y)
        
        # Use game tree evaluation
        best_move = (0, 0, False)
        best_score = -float('inf')
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:
            nx, ny = px + dx, py + dy
            
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0:
                    # Evaluate this move
                    score = self.game_tree.minimax(player, opponent, game_state)
                    
                    if score > best_score:
                        best_score = score
                        should_bomb = player.active_bombs < player.max_bombs and random.random() < 0.4
                        best_move = (dx, dy, should_bomb)
        
        self.actions_taken += 1
        if best_move[2]:
            self.bombs_placed += 1
        return best_move
    
    def record_game_result(self, won, reward):
        """Record game result."""
        self.total_games += 1
        if won:
            self.wins += 1
        self.total_reward += reward
    
    def get_win_rate(self):
        """Get win rate."""
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games
    
    def get_average_reward(self):
        """Get average reward."""
        if self.total_games == 0:
            return 0.0
        return self.total_reward / self.total_games
    
    def get_stats_string(self):
        """Get formatted statistics."""
        win_rate = self.get_win_rate() * 100
        avg_reward = self.get_average_reward()
        
        # Determine skill level
        if win_rate >= 75:
            level = "Expert"
        elif win_rate >= 60:
            level = "Advanced"
        elif win_rate >= 45:
            level = "Intermediate"
        elif win_rate >= 25:
            level = "Beginner"
        else:
            level = "Learning"
        
        # Most used strategy
        if self.strategy_history:
            most_used = max(set(self.strategy_history), 
                          key=self.strategy_history.count)
        else:
            most_used = "N/A"
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║         🧠 ADVANCED SMART HEURISTIC - PERFORMANCE            ║
╠══════════════════════════════════════════════════════════════╣
║  Skill Level:      {level:<40} ║
║  Win Rate:         {win_rate:>6.2f}%                                 ║
║  Average Reward:   {avg_reward:>8.2f}                               ║
║  Games Played:     {self.total_games:<40} ║
║  Total Wins:       {self.wins:<40} ║
║  Bombs Placed:     {self.bombs_placed:<40} ║
║  Actions Taken:    {self.actions_taken:<40} ║
║  Primary Strategy: {most_used:<40} ║
╚══════════════════════════════════════════════════════════════╝
"""
