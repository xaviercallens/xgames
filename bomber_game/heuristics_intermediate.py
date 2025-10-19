"""
Intermediate Smart Heuristic AI for PROUTMAN.
Enhanced decision-making with strategic planning, risk assessment, and adaptive behavior.

Features:
- Multi-level threat assessment
- Strategic bomb placement with lookahead
- Adaptive tactics based on game state
- Opponent modeling
- Resource management
- Tactical positioning
"""

import random
import heapq
import math
from collections import deque
from . import GRID_SIZE


class ThreatAssessment:
    """Advanced threat assessment system."""
    
    def __init__(self):
        """Initialize threat assessment."""
        self.threat_levels = {
            'critical': 100,      # Immediate death
            'high': 75,           # Very dangerous
            'medium': 50,         # Dangerous
            'low': 25,            # Minor threat
            'safe': 0,            # Safe
        }
    
    @staticmethod
    def calculate_blast_zone(bomb_x, bomb_y, bomb_range, grid):
        """Calculate exact blast zone for a bomb."""
        blast_tiles = set()
        blast_tiles.add((bomb_x, bomb_y))
        
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, bomb_range + 1):
                check_x = bomb_x + dx * dist
                check_y = bomb_y + dy * dist
                
                if not (0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE):
                    break
                
                if grid[check_y][check_x] == 1:  # Hard wall
                    break
                
                blast_tiles.add((check_x, check_y))
                
                if grid[check_y][check_x] == 2:  # Soft wall
                    break
        
        return blast_tiles
    
    @staticmethod
    def assess_position_threat(x, y, game_state):
        """
        Assess threat level at a position.
        
        Returns:
            (threat_level, threat_score) tuple
        """
        threat_score = 0.0
        
        # Check all bombs
        for bomb in game_state.bombs:
            blast_zone = ThreatAssessment.calculate_blast_zone(
                bomb.grid_x, bomb.grid_y, bomb.bomb_range, game_state.grid
            )
            
            if (x, y) in blast_zone:
                # In blast zone - calculate danger based on time
                time_factor = bomb.timer / bomb.max_timer
                if time_factor < 0.3:  # Less than 30% time left
                    threat_score += 100  # Critical
                elif time_factor < 0.6:
                    threat_score += 75   # High
                else:
                    threat_score += 50   # Medium
        
        # Check all explosions
        for explosion in game_state.explosions:
            if explosion.grid_x == x and explosion.grid_y == y:
                threat_score += 100  # Critical
        
        # Classify threat level
        if threat_score >= 100:
            return 'critical', threat_score
        elif threat_score >= 75:
            return 'high', threat_score
        elif threat_score >= 50:
            return 'medium', threat_score
        elif threat_score >= 25:
            return 'low', threat_score
        else:
            return 'safe', threat_score
    
    @staticmethod
    def find_safe_zone(player_x, player_y, game_state, search_radius=7):
        """
        Find safest zone within search radius.
        
        Returns:
            (x, y) of safest position or None
        """
        best_pos = None
        best_safety = -float('inf')
        
        for y in range(max(0, player_y - search_radius), 
                      min(GRID_SIZE, player_y + search_radius + 1)):
            for x in range(max(0, player_x - search_radius), 
                          min(GRID_SIZE, player_x + search_radius + 1)):
                
                if game_state.grid[y][x] != 0:
                    continue
                
                threat_level, threat_score = ThreatAssessment.assess_position_threat(
                    x, y, game_state
                )
                
                # Safety score (negative threat)
                safety = -threat_score
                
                if safety > best_safety:
                    best_safety = safety
                    best_pos = (x, y)
        
        return best_pos


class StrategicPlanning:
    """Strategic planning and decision-making."""
    
    @staticmethod
    def evaluate_bomb_placement(player_x, player_y, player, game_state):
        """
        Evaluate bomb placement with lookahead.
        
        Returns:
            (should_place, value, escape_routes) tuple
        """
        if player.active_bombs >= player.max_bombs:
            return False, 0.0, 0
        
        # Check escape routes
        escape_routes = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = player_x + dx, player_y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0:
                    threat_level, _ = ThreatAssessment.assess_position_threat(
                        nx, ny, game_state
                    )
                    if threat_level == 'safe':
                        escape_routes += 1
        
        if escape_routes == 0:
            return False, 0.0, 0
        
        # Calculate bomb value
        value = 0.0
        
        # Count walls that would be destroyed
        walls_destroyed = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, player.bomb_range + 1):
                check_x = player_x + dx * dist
                check_y = player_y + dy * dist
                
                if not (0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE):
                    break
                
                if game_state.grid[check_y][check_x] == 2:
                    walls_destroyed += 1
                    value += 3.0
                elif game_state.grid[check_y][check_x] == 1:
                    break
        
        # Check for power-ups that would be revealed
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            for dist in range(1, player.bomb_range + 1):
                check_x = player_x + dx * dist
                check_y = player_y + dy * dist
                
                if not (0 <= check_x < GRID_SIZE and 0 <= check_y < GRID_SIZE):
                    break
                
                if (check_x, check_y) in game_state.powerups:
                    value += 5.0
                
                if game_state.grid[check_y][check_x] != 0:
                    break
        
        # Check for enemy threat
        for other_player in game_state.players:
            if other_player != player and other_player.alive:
                ex, ey = int(other_player.x), int(other_player.y)
                
                # Check if enemy is in blast range
                blast_zone = ThreatAssessment.calculate_blast_zone(
                    player_x, player_y, player.bomb_range, game_state.grid
                )
                
                if (ex, ey) in blast_zone:
                    value += 15.0  # High value for enemy hit
        
        # Bonus for strategic positioning
        if escape_routes >= 2:
            value *= 1.2  # 20% bonus for multiple escape routes
        
        should_place = value >= 3.0 and escape_routes >= 1
        
        return should_place, value, escape_routes
    
    @staticmethod
    def find_power_up_target(player_x, player_y, game_state):
        """Find nearest valuable power-up."""
        best_powerup = None
        best_distance = float('inf')
        
        for pos, powerup in game_state.powerups.items():
            px, py = pos
            distance = abs(px - player_x) + abs(py - player_y)
            
            if distance < best_distance:
                best_distance = distance
                best_powerup = pos
        
        return best_powerup
    
    @staticmethod
    def find_wall_target(player_x, player_y, player, game_state):
        """Find best wall to destroy."""
        best_wall = None
        best_score = -float('inf')
        
        search_radius = 6
        for y in range(max(0, player_y - search_radius), 
                      min(GRID_SIZE, player_y + search_radius + 1)):
            for x in range(max(0, player_x - search_radius), 
                          min(GRID_SIZE, player_x + search_radius + 1)):
                
                if game_state.grid[y][x] != 2:  # Not a soft wall
                    continue
                
                # Check if reachable
                distance = abs(x - player_x) + abs(y - player_y)
                if distance > 8:
                    continue
                
                # Score based on proximity and wall value
                score = 10.0 / (distance + 1)
                
                # Bonus if power-up might be behind
                if (x, y) in game_state.powerups:
                    score += 20.0
                
                if score > best_score:
                    best_score = score
                    best_wall = (x, y)
        
        return best_wall


class AdaptiveBehavior:
    """Adaptive behavior based on game state."""
    
    def __init__(self):
        """Initialize adaptive behavior."""
        self.aggression_level = 0.5  # 0.0 = defensive, 1.0 = aggressive
        self.last_action = None
        self.stuck_counter = 0
        self.max_stuck_frames = 10
    
    def update_aggression(self, player, opponent, game_state):
        """Update aggression level based on game state."""
        if not opponent.alive:
            self.aggression_level = 0.1  # Very defensive if winning
        elif player.bomb_range > opponent.bomb_range:
            self.aggression_level = 0.8  # Aggressive if stronger
        elif player.max_bombs > opponent.max_bombs:
            self.aggression_level = 0.7  # Fairly aggressive
        else:
            self.aggression_level = 0.4  # Defensive if weaker
    
    def should_pursue_opponent(self, player_x, player_y, opponent, aggression):
        """Determine if should pursue opponent."""
        if not opponent.alive:
            return False
        
        ox, oy = int(opponent.x), int(opponent.y)
        distance = abs(ox - player_x) + abs(oy - player_y)
        
        # Pursue if close and aggressive
        if distance < 5 and aggression > 0.6:
            return True
        
        # Pursue if very close regardless
        if distance < 3:
            return True
        
        return False


class IntermediateSmartHeuristic:
    """Intermediate smart heuristic AI."""
    
    def __init__(self, player):
        """Initialize intermediate smart heuristic."""
        self.player = player
        self.threat_assessment = ThreatAssessment()
        self.strategic_planning = StrategicPlanning()
        self.adaptive_behavior = AdaptiveBehavior()
        
        # Performance tracking
        self.total_games = 0
        self.wins = 0
        self.total_reward = 0.0
        self.actions_taken = 0
        self.bombs_placed = 0
        self.powerups_collected = 0
    
    def choose_action(self, player, opponent, game_state):
        """
        Choose action using intermediate smart heuristics.
        
        Returns:
            (dx, dy, place_bomb) tuple
        """
        px, py = int(player.x), int(player.y)
        
        # Update adaptive behavior
        self.adaptive_behavior.update_aggression(player, opponent, game_state)
        
        # Priority 1: Escape critical danger
        threat_level, threat_score = ThreatAssessment.assess_position_threat(
            px, py, game_state
        )
        
        if threat_level == 'critical':
            # Find safe zone immediately
            safe_pos = ThreatAssessment.find_safe_zone(px, py, game_state, search_radius=5)
            if safe_pos:
                dx = 1 if safe_pos[0] > px else (-1 if safe_pos[0] < px else 0)
                dy = 1 if safe_pos[1] > py else (-1 if safe_pos[1] < py else 0)
                return (dx, dy, False)
        
        # Priority 2: Strategic bomb placement
        should_bomb, bomb_value, escape_routes = StrategicPlanning.evaluate_bomb_placement(
            px, py, player, game_state
        )
        
        # Priority 3: Decide target based on game state
        target = None
        
        # If aggressive and opponent close, pursue
        if self.adaptive_behavior.should_pursue_opponent(
            px, py, opponent, self.adaptive_behavior.aggression_level
        ):
            target = (int(opponent.x), int(opponent.y))
        
        # Otherwise, prioritize power-ups
        if target is None:
            powerup_target = StrategicPlanning.find_power_up_target(px, py, game_state)
            if powerup_target and powerup_target in game_state.powerups:
                target = powerup_target
        
        # Otherwise, target walls
        if target is None:
            wall_target = StrategicPlanning.find_wall_target(px, py, player, game_state)
            if wall_target:
                target = wall_target
        
        # Move towards target
        if target:
            dx = 1 if target[0] > px else (-1 if target[0] < px else 0)
            dy = 1 if target[1] > py else (-1 if target[1] < py else 0)
            
            # Verify move is safe
            threat_level, _ = ThreatAssessment.assess_position_threat(
                px + dx, py + dy, game_state
            )
            
            if threat_level != 'critical':
                self.actions_taken += 1
                if should_bomb:
                    self.bombs_placed += 1
                return (dx, dy, should_bomb)
        
        # Fallback: safe random move
        safe_moves = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = px + dx, py + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if game_state.grid[ny][nx] == 0:
                    threat_level, _ = ThreatAssessment.assess_position_threat(
                        nx, ny, game_state
                    )
                    if threat_level in ['safe', 'low']:
                        safe_moves.append((dx, dy))
        
        if safe_moves:
            move = random.choice(safe_moves)
            self.actions_taken += 1
            if should_bomb:
                self.bombs_placed += 1
            return (move[0], move[1], should_bomb)
        
        self.actions_taken += 1
        return (0, 0, False)
    
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
        if win_rate >= 70:
            level = "Expert"
        elif win_rate >= 50:
            level = "Advanced"
        elif win_rate >= 35:
            level = "Intermediate"
        elif win_rate >= 15:
            level = "Beginner"
        else:
            level = "Learning"
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║        🧠 INTERMEDIATE SMART HEURISTIC - PERFORMANCE         ║
╠══════════════════════════════════════════════════════════════╣
║  Skill Level:      {level:<40} ║
║  Win Rate:         {win_rate:>6.2f}%                                 ║
║  Average Reward:   {avg_reward:>8.2f}                               ║
║  Games Played:     {self.total_games:<40} ║
║  Total Wins:       {self.wins:<40} ║
║  Bombs Placed:     {self.bombs_placed:<40} ║
║  Actions Taken:    {self.actions_taken:<40} ║
║  Aggression:       {self.adaptive_behavior.aggression_level:>6.2f}                                  ║
╚══════════════════════════════════════════════════════════════╝
"""
