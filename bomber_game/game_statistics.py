"""
Game Statistics Tracker - Comprehensive analytics for Human vs AI gameplay.
Tracks performance, strategy, risk levels, and provides recommendations.
"""

import json
import os
import time
from datetime import datetime
from collections import deque
import math


class GameStatistics:
    """
    Comprehensive game statistics tracker with persistence.
    Tracks human vs AI performance, strategy, risk levels, and history.
    """
    
    def __init__(self, stats_file="bomber_game/models/game_history.json"):
        self.stats_file = stats_file
        
        # Current game stats
        self.game_start_time = time.time()
        self.human_moves = 0
        self.ai_moves = 0
        self.human_bombs_placed = 0
        self.ai_bombs_placed = 0
        self.human_kills = 0
        self.ai_kills = 0
        self.human_near_death = 0
        self.ai_near_death = 0
        self.powerups_collected_human = 0
        self.powerups_collected_ai = 0
        self.walls_destroyed_human = 0
        self.walls_destroyed_ai = 0
        
        # Strategy tracking
        self.human_aggressive_moves = 0
        self.human_defensive_moves = 0
        self.ai_aggressive_moves = 0
        self.ai_defensive_moves = 0
        
        # Risk tracking
        self.human_risk_history = deque(maxlen=100)
        self.ai_risk_history = deque(maxlen=100)
        
        # Performance history (last 10 games)
        self.recent_games = deque(maxlen=10)
        
        # Load historical data
        self.history = self._load_history()
        
        # AI info
        self.ai_type = "Unknown"
        self.ai_model_path = None
        
    def _load_history(self):
        """Load game history from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'total_games': 0,
            'human_wins': 0,
            'ai_wins': 0,
            'draws': 0,
            'games': [],
            'human_stats': {
                'total_moves': 0,
                'total_bombs': 0,
                'total_kills': 0,
                'avg_game_time': 0,
                'best_win_streak': 0,
                'current_win_streak': 0,
            },
            'ai_stats': {
                'total_moves': 0,
                'total_bombs': 0,
                'total_kills': 0,
                'avg_game_time': 0,
                'best_win_streak': 0,
                'current_win_streak': 0,
            }
        }
    
    def _save_history(self):
        """Save game history to file."""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Could not save game history: {e}")
    
    def set_ai_info(self, ai_type, model_path=None):
        """Set AI information."""
        self.ai_type = ai_type
        self.ai_model_path = model_path
    
    def reset(self):
        """Reset current game statistics for a new game."""
        self.game_start_time = time.time()
        self.human_moves = 0
        self.ai_moves = 0
        self.human_bombs_placed = 0
        self.ai_bombs_placed = 0
        self.human_kills = 0
        self.ai_kills = 0
        self.human_near_death = 0
        self.ai_near_death = 0
        self.powerups_collected_human = 0
        self.powerups_collected_ai = 0
        self.walls_destroyed_human = 0
        self.walls_destroyed_ai = 0
        
        # Strategy tracking
        self.human_aggressive_moves = 0
        self.human_defensive_moves = 0
        self.ai_aggressive_moves = 0
        self.ai_defensive_moves = 0
        
        # Risk tracking
        self.human_risk_history.clear()
        self.ai_risk_history.clear()
    
    def record_move(self, is_human, position, game_state):
        """Record a player move and analyze strategy."""
        if is_human:
            self.human_moves += 1
            # Analyze strategy
            risk = self._calculate_risk(position, game_state)
            self.human_risk_history.append(risk)
            
            # Check if aggressive (moving toward enemy)
            enemy_pos = self._get_enemy_position(game_state, is_human)
            if enemy_pos:
                dist = self._manhattan_distance(position, enemy_pos)
                if dist < 5:
                    self.human_aggressive_moves += 1
                else:
                    self.human_defensive_moves += 1
        else:
            self.ai_moves += 1
            risk = self._calculate_risk(position, game_state)
            self.ai_risk_history.append(risk)
            
            enemy_pos = self._get_enemy_position(game_state, is_human)
            if enemy_pos:
                dist = self._manhattan_distance(position, enemy_pos)
                if dist < 5:
                    self.ai_aggressive_moves += 1
                else:
                    self.ai_defensive_moves += 1
    
    def record_bomb(self, is_human):
        """Record bomb placement."""
        if is_human:
            self.human_bombs_placed += 1
        else:
            self.ai_bombs_placed += 1
    
    def record_near_death(self, is_human):
        """Record near-death experience."""
        if is_human:
            self.human_near_death += 1
        else:
            self.ai_near_death += 1
    
    def record_powerup(self, is_human):
        """Record powerup collection."""
        if is_human:
            self.powerups_collected_human += 1
        else:
            self.powerups_collected_ai += 1
    
    def record_wall_destroyed(self, is_human):
        """Record wall destruction."""
        if is_human:
            self.walls_destroyed_human += 1
        else:
            self.walls_destroyed_ai += 1
    
    def _calculate_risk(self, position, game_state):
        """Calculate risk level at position (0-100)."""
        risk = 0
        px, py = position
        
        # Check bombs
        for bomb in game_state.bombs:
            bx, by = bomb.grid_x, bomb.grid_y
            dist = abs(px - bx) + abs(py - by)
            
            if dist <= bomb.bomb_range:
                # Higher risk for closer bombs and shorter timers
                time_factor = max(0, (3.0 - bomb.timer) / 3.0)
                dist_factor = max(0, (bomb.bomb_range - dist) / bomb.bomb_range)
                risk += 50 * time_factor * dist_factor
        
        # Check explosions
        for explosion in game_state.explosions:
            if explosion.grid_x == px and explosion.grid_y == py:
                risk += 100
        
        return min(100, risk)
    
    def _get_enemy_position(self, game_state, is_human):
        """Get enemy position."""
        for player in game_state.players:
            if (is_human and player.name == "AI") or (not is_human and player.name == "Player"):
                if player.alive:
                    return (player.grid_x, player.grid_y)
        return None
    
    def _manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_current_risk(self, is_human):
        """Get current risk level."""
        history = self.human_risk_history if is_human else self.ai_risk_history
        if len(history) > 0:
            return sum(history) / len(history)
        return 0
    
    def get_strategy(self, is_human):
        """Get current strategy (aggressive/defensive/balanced)."""
        if is_human:
            aggressive = self.human_aggressive_moves
            defensive = self.human_defensive_moves
        else:
            aggressive = self.ai_aggressive_moves
            defensive = self.ai_defensive_moves
        
        total = aggressive + defensive
        if total == 0:
            return "Balanced"
        
        ratio = aggressive / total
        if ratio > 0.6:
            return "Aggressive"
        elif ratio < 0.4:
            return "Defensive"
        else:
            return "Balanced"
    
    def get_performance_score(self, is_human):
        """Calculate performance score (0-100)."""
        if is_human:
            moves = self.human_moves
            bombs = self.human_bombs_placed
            near_death = self.human_near_death
            powerups = self.powerups_collected_human
            walls = self.walls_destroyed_human
        else:
            moves = self.ai_moves
            bombs = self.ai_bombs_placed
            near_death = self.ai_near_death
            powerups = self.powerups_collected_ai
            walls = self.walls_destroyed_ai
        
        if moves == 0:
            return 50
        
        # Calculate score
        score = 50  # Base score
        
        # Efficiency: bombs per move
        if moves > 0:
            bomb_efficiency = min(30, (bombs / moves) * 100)
            score += bomb_efficiency
        
        # Survival: penalty for near-death
        survival_penalty = min(20, near_death * 5)
        score -= survival_penalty
        
        # Powerups bonus
        powerup_bonus = min(10, powerups * 2)
        score += powerup_bonus
        
        # Walls destroyed bonus
        walls_bonus = min(10, walls)
        score += walls_bonus
        
        return max(0, min(100, score))
    
    def finish_game(self, winner_name):
        """Finish game and save statistics."""
        game_time = time.time() - self.game_start_time
        
        # Determine winner
        human_won = (winner_name == "Player")
        ai_won = (winner_name == "AI")
        draw = (winner_name is None or winner_name == "Draw")
        
        # Update history
        self.history['total_games'] += 1
        
        if human_won:
            self.history['human_wins'] += 1
            self.history['human_stats']['current_win_streak'] += 1
            self.history['ai_stats']['current_win_streak'] = 0
            
            if self.history['human_stats']['current_win_streak'] > self.history['human_stats']['best_win_streak']:
                self.history['human_stats']['best_win_streak'] = self.history['human_stats']['current_win_streak']
        elif ai_won:
            self.history['ai_wins'] += 1
            self.history['ai_stats']['current_win_streak'] += 1
            self.history['human_stats']['current_win_streak'] = 0
            
            if self.history['ai_stats']['current_win_streak'] > self.history['ai_stats']['best_win_streak']:
                self.history['ai_stats']['best_win_streak'] = self.history['ai_stats']['current_win_streak']
        else:
            self.history['draws'] += 1
            self.history['human_stats']['current_win_streak'] = 0
            self.history['ai_stats']['current_win_streak'] = 0
        
        # Update cumulative stats
        self.history['human_stats']['total_moves'] += self.human_moves
        self.history['human_stats']['total_bombs'] += self.human_bombs_placed
        self.history['ai_stats']['total_moves'] += self.ai_moves
        self.history['ai_stats']['total_bombs'] += self.ai_bombs_placed
        
        # Save game record
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'duration': game_time,
            'winner': winner_name,
            'ai_type': self.ai_type,
            'human': {
                'moves': self.human_moves,
                'bombs': self.human_bombs_placed,
                'near_death': self.human_near_death,
                'powerups': self.powerups_collected_human,
                'walls': self.walls_destroyed_human,
                'strategy': self.get_strategy(True),
                'avg_risk': self.get_current_risk(True),
                'performance': self.get_performance_score(True),
            },
            'ai': {
                'moves': self.ai_moves,
                'bombs': self.ai_bombs_placed,
                'near_death': self.ai_near_death,
                'powerups': self.powerups_collected_ai,
                'walls': self.walls_destroyed_ai,
                'strategy': self.get_strategy(False),
                'avg_risk': self.get_current_risk(False),
                'performance': self.get_performance_score(False),
            }
        }
        
        self.history['games'].append(game_record)
        self.recent_games.append(game_record)
        
        # Keep only last 50 games in history
        if len(self.history['games']) > 50:
            self.history['games'] = self.history['games'][-50:]
        
        # Save to file
        self._save_history()
    
    def get_recommendations(self):
        """Get gameplay recommendations based on statistics."""
        recommendations = []
        
        # Analyze human performance
        human_strategy = self.get_strategy(True)
        human_risk = self.get_current_risk(True)
        human_perf = self.get_performance_score(True)
        
        # Risk recommendations
        if human_risk > 60:
            recommendations.append("⚠️ HIGH RISK: Play more defensively, avoid bomb zones")
        elif human_risk < 20:
            recommendations.append("💡 LOW RISK: You can be more aggressive")
        
        # Strategy recommendations
        if human_strategy == "Aggressive" and human_perf < 50:
            recommendations.append("🎯 Try a more balanced approach - aggression isn't working")
        elif human_strategy == "Defensive" and human_perf < 50:
            recommendations.append("⚔️ Be more aggressive - take more risks")
        
        # Bomb efficiency
        if self.human_moves > 20:
            bomb_ratio = self.human_bombs_placed / self.human_moves
            if bomb_ratio < 0.1:
                recommendations.append("💣 Place more bombs - you're too conservative")
            elif bomb_ratio > 0.3:
                recommendations.append("🎯 Focus on strategic bomb placement, not quantity")
        
        # Powerup collection
        if self.powerups_collected_human < 2 and self.human_moves > 30:
            recommendations.append("⭐ Collect more power-ups for advantage")
        
        # Near-death situations
        if self.human_near_death > 3:
            recommendations.append("🛡️ Improve escape routes - plan ahead")
        
        # Win streak
        if self.history['human_stats']['current_win_streak'] >= 3:
            recommendations.append("🔥 ON FIRE! Keep up the great play!")
        elif self.history['ai_stats']['current_win_streak'] >= 3:
            recommendations.append("💪 AI is dominating - change your strategy")
        
        if not recommendations:
            recommendations.append("✅ Good gameplay! Keep it up!")
        
        return recommendations
    
    def get_win_rate(self, is_human):
        """Get win rate percentage."""
        total = self.history['total_games']
        if total == 0:
            return 0
        
        if is_human:
            wins = self.history['human_wins']
        else:
            wins = self.history['ai_wins']
        
        return (wins / total) * 100
    
    def get_recent_trend(self, is_human):
        """Get recent performance trend (last 5 games)."""
        if len(self.recent_games) < 2:
            return "Insufficient data"
        
        recent = list(self.recent_games)[-5:]
        wins = sum(1 for g in recent if g['winner'] == ("Player" if is_human else "AI"))
        
        win_rate = (wins / len(recent)) * 100
        
        if win_rate >= 60:
            return "📈 Improving"
        elif win_rate <= 40:
            return "📉 Declining"
        else:
            return "➡️ Stable"
