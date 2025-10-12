"""
Game Recorder - Records gameplay actions for replay and analysis.
"""

import json
import time
from datetime import datetime
from pathlib import Path
import gzip


class GameRecorder:
    """
    Records all game actions and state for replay and analysis.
    Exports data at end of game for review and training.
    """
    
    def __init__(self, game_id=None):
        self.game_id = game_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.recording = {
            'game_id': self.game_id,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'duration': 0,
            'winner': None,
            'players': {},
            'initial_state': {},
            'actions': [],
            'events': [],
            'frames': [],
            'statistics': {},
        }
        
        self.start_time = time.time()
        self.frame_count = 0
        self.recording_enabled = True
        
    def set_initial_state(self, game_state):
        """Record initial game state."""
        self.recording['initial_state'] = {
            'grid_size': len(game_state.grid),
            'wall_layout': self._serialize_grid(game_state.grid),
            'players': [
                {
                    'name': p.name,
                    'position': (p.grid_x, p.grid_y),
                    'color': p.color,
                    'stats': {
                        'max_bombs': p.max_bombs,
                        'bomb_range': p.bomb_range,
                        'speed': p.speed,
                    }
                }
                for p in game_state.players
            ],
            'powerups': [
                {
                    'type': p.powerup_type,
                    'position': (p.grid_x, p.grid_y)
                }
                for p in game_state.powerups.values()
            ]
        }
    
    def record_action(self, player_name, action_type, details=None):
        """Record a player action."""
        if not self.recording_enabled:
            return
        
        action = {
            'frame': self.frame_count,
            'timestamp': time.time() - self.start_time,
            'player': player_name,
            'action': action_type,
            'details': details or {}
        }
        
        self.recording['actions'].append(action)
    
    def record_event(self, event_type, details=None):
        """Record a game event."""
        if not self.recording_enabled:
            return
        
        event = {
            'frame': self.frame_count,
            'timestamp': time.time() - self.start_time,
            'type': event_type,
            'details': details or {}
        }
        
        self.recording['events'].append(event)
    
    def record_frame(self, game_state, sample_rate=10):
        """Record game state at current frame (sampled)."""
        if not self.recording_enabled:
            return
        
        self.frame_count += 1
        
        # Sample frames to reduce file size
        if self.frame_count % sample_rate != 0:
            return
        
        frame = {
            'frame': self.frame_count,
            'timestamp': time.time() - self.start_time,
            'players': [
                {
                    'name': p.name,
                    'position': (p.grid_x, p.grid_y),
                    'alive': p.alive,
                    'stats': {
                        'max_bombs': p.max_bombs,
                        'bomb_range': p.bomb_range,
                        'speed': p.speed,
                    }
                }
                for p in game_state.players
            ],
            'bombs': [
                {
                    'position': (b.grid_x, b.grid_y),
                    'timer': b.timer,
                    'range': b.bomb_range,
                    'owner': b.owner.name if b.owner else None
                }
                for b in game_state.bombs
            ],
            'explosions': len(game_state.explosions),
            'powerups': len(game_state.powerups),
        }
        
        self.recording['frames'].append(frame)
    
    def record_move(self, player_name, from_pos, to_pos):
        """Record player movement."""
        self.record_action(player_name, 'move', {
            'from': from_pos,
            'to': to_pos
        })
    
    def record_bomb_placed(self, player_name, position):
        """Record bomb placement."""
        self.record_action(player_name, 'place_bomb', {
            'position': position
        })
    
    def record_bomb_exploded(self, position, range_val):
        """Record bomb explosion."""
        self.record_event('bomb_exploded', {
            'position': position,
            'range': range_val
        })
    
    def record_player_death(self, player_name, cause):
        """Record player death."""
        self.record_event('player_death', {
            'player': player_name,
            'cause': cause
        })
    
    def record_powerup_collected(self, player_name, powerup_type, position):
        """Record powerup collection."""
        self.record_action(player_name, 'collect_powerup', {
            'type': powerup_type,
            'position': position
        })
    
    def record_wall_destroyed(self, position):
        """Record wall destruction."""
        self.record_event('wall_destroyed', {
            'position': position
        })
    
    def finish_recording(self, winner_name, statistics=None):
        """Finish recording and prepare for export."""
        self.recording['end_time'] = datetime.now().isoformat()
        self.recording['duration'] = time.time() - self.start_time
        self.recording['winner'] = winner_name
        self.recording['total_frames'] = self.frame_count
        self.recording['statistics'] = statistics or {}
        
        self.recording_enabled = False
    
    def export_json(self, directory="bomber_game/replays"):
        """Export recording as JSON file."""
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        filename = f"{directory}/game_{self.game_id}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.recording, f, indent=2)
        
        return filename
    
    def export_compressed(self, directory="bomber_game/replays"):
        """Export recording as compressed JSON file."""
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        filename = f"{directory}/game_{self.game_id}.json.gz"
        
        json_data = json.dumps(self.recording, indent=2)
        
        with gzip.open(filename, 'wt', encoding='utf-8') as f:
            f.write(json_data)
        
        return filename
    
    def export_summary(self, directory="bomber_game/replays"):
        """Export game summary (lightweight)."""
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        summary = {
            'game_id': self.game_id,
            'start_time': self.recording['start_time'],
            'end_time': self.recording['end_time'],
            'duration': self.recording['duration'],
            'winner': self.recording['winner'],
            'total_frames': self.frame_count,
            'total_actions': len(self.recording['actions']),
            'total_events': len(self.recording['events']),
            'statistics': self.recording['statistics'],
        }
        
        filename = f"{directory}/summary_{self.game_id}.json"
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return filename
    
    def _serialize_grid(self, grid):
        """Serialize grid to list format."""
        return [[cell for cell in row] for row in grid]
    
    def get_statistics(self):
        """Get recording statistics."""
        return {
            'total_actions': len(self.recording['actions']),
            'total_events': len(self.recording['events']),
            'total_frames': self.frame_count,
            'duration': time.time() - self.start_time,
            'actions_by_player': self._count_actions_by_player(),
            'events_by_type': self._count_events_by_type(),
        }
    
    def _count_actions_by_player(self):
        """Count actions by each player."""
        counts = {}
        for action in self.recording['actions']:
            player = action['player']
            counts[player] = counts.get(player, 0) + 1
        return counts
    
    def _count_events_by_type(self):
        """Count events by type."""
        counts = {}
        for event in self.recording['events']:
            event_type = event['type']
            counts[event_type] = counts.get(event_type, 0) + 1
        return counts


class ReplayManager:
    """Manages game replays and provides analysis."""
    
    def __init__(self, replay_dir="bomber_game/replays"):
        self.replay_dir = Path(replay_dir)
        self.replay_dir.mkdir(parents=True, exist_ok=True)
    
    def list_replays(self):
        """List all available replays."""
        replays = []
        
        for file in self.replay_dir.glob("summary_*.json"):
            try:
                with open(file, 'r') as f:
                    summary = json.load(f)
                    replays.append(summary)
            except:
                continue
        
        return sorted(replays, key=lambda x: x['start_time'], reverse=True)
    
    def load_replay(self, game_id):
        """Load a full replay."""
        # Try compressed first
        compressed_file = self.replay_dir / f"game_{game_id}.json.gz"
        if compressed_file.exists():
            with gzip.open(compressed_file, 'rt', encoding='utf-8') as f:
                return json.load(f)
        
        # Try uncompressed
        json_file = self.replay_dir / f"game_{game_id}.json"
        if json_file.exists():
            with open(json_file, 'r') as f:
                return json.load(f)
        
        return None
    
    def get_player_statistics(self, player_name, num_games=10):
        """Get statistics for a player across multiple games."""
        replays = self.list_replays()[:num_games]
        
        stats = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'total_actions': 0,
            'avg_game_duration': 0,
            'win_rate': 0,
        }
        
        total_duration = 0
        
        for replay in replays:
            stats['total_games'] += 1
            
            if replay['winner'] == player_name:
                stats['wins'] += 1
            else:
                stats['losses'] += 1
            
            total_duration += replay.get('duration', 0)
            
            # Load full replay for detailed stats
            full_replay = self.load_replay(replay['game_id'])
            if full_replay:
                player_actions = [a for a in full_replay['actions'] if a['player'] == player_name]
                stats['total_actions'] += len(player_actions)
        
        if stats['total_games'] > 0:
            stats['win_rate'] = (stats['wins'] / stats['total_games']) * 100
            stats['avg_game_duration'] = total_duration / stats['total_games']
        
        return stats
