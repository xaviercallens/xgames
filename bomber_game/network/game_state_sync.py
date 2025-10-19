"""
Game state synchronization for multiplayer games.
"""

from typing import Dict, List, Any, Optional
import time


class GameStateSync:
    """Handles synchronization of game state across network."""
    
    def __init__(self, sync_interval: float = 0.016):
        """
        Initialize game state sync.
        
        Args:
            sync_interval: Interval between synchronizations (seconds)
        """
        self.sync_interval = sync_interval
        self.last_sync_time = time.time()
        self.frame = 0
        self.local_state = {}
        self.remote_state = {}
        self.state_history: List[Dict[str, Any]] = []
        self.max_history = 100
    
    def should_sync(self) -> bool:
        """Check if it's time to synchronize."""
        current_time = time.time()
        if current_time - self.last_sync_time >= self.sync_interval:
            self.last_sync_time = current_time
            return True
        return False
    
    def update_local_state(self, state: Dict[str, Any]) -> None:
        """
        Update local game state.
        
        Args:
            state: Local game state
        """
        self.local_state = state.copy()
        self.frame += 1
        self._record_state(state)
    
    def update_remote_state(self, state: Dict[str, Any]) -> None:
        """
        Update remote game state.
        
        Args:
            state: Remote game state from server
        """
        self.remote_state = state.copy()
    
    def get_state_delta(self) -> Dict[str, Any]:
        """
        Get delta (changes) since last sync.
        
        Returns:
            Dictionary containing only changed fields
        """
        delta = {}
        
        # Compare players
        if 'players' in self.local_state and 'players' in self.remote_state:
            local_players = self.local_state['players']
            remote_players = self.remote_state['players']
            
            changed_players = []
            for i, player in enumerate(local_players):
                if i >= len(remote_players) or player != remote_players[i]:
                    changed_players.append(player)
            
            if changed_players:
                delta['players'] = changed_players
        
        # Compare bombs
        if 'bombs' in self.local_state and 'bombs' in self.remote_state:
            if self.local_state['bombs'] != self.remote_state['bombs']:
                delta['bombs'] = self.local_state['bombs']
        
        # Compare explosions
        if 'explosions' in self.local_state and 'explosions' in self.remote_state:
            if self.local_state['explosions'] != self.remote_state['explosions']:
                delta['explosions'] = self.local_state['explosions']
        
        # Compare powerups
        if 'powerups' in self.local_state and 'powerups' in self.remote_state:
            if self.local_state['powerups'] != self.remote_state['powerups']:
                delta['powerups'] = self.local_state['powerups']
        
        return delta
    
    def reconcile_state(self, server_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reconcile local state with server state.
        
        Args:
            server_state: Server's authoritative state
            
        Returns:
            Reconciled state
        """
        # Server state is authoritative
        reconciled = server_state.copy()
        
        # Keep local predictions for smooth gameplay
        if 'players' in self.local_state:
            for i, player in enumerate(self.local_state.get('players', [])):
                if i < len(reconciled.get('players', [])):
                    # Smooth transition between states
                    server_player = reconciled['players'][i]
                    reconciled['players'][i] = self._interpolate_player(
                        server_player, player
                    )
        
        return reconciled
    
    def predict_state(self, frames_ahead: int = 1) -> Dict[str, Any]:
        """
        Predict future state based on current trends.
        
        Args:
            frames_ahead: Number of frames to predict ahead
            
        Returns:
            Predicted state
        """
        predicted = self.local_state.copy()
        
        # Predict player positions based on velocity
        if 'players' in predicted:
            for player in predicted['players']:
                if 'vx' in player and 'vy' in player:
                    player['x'] += player['vx'] * frames_ahead
                    player['y'] += player['vy'] * frames_ahead
        
        return predicted
    
    def get_state_history(self, frame_offset: int = 0) -> Optional[Dict[str, Any]]:
        """
        Get historical state.
        
        Args:
            frame_offset: Frames back to retrieve (0 = current)
            
        Returns:
            Historical state or None
        """
        index = len(self.state_history) - 1 - frame_offset
        if 0 <= index < len(self.state_history):
            return self.state_history[index].copy()
        return None
    
    def _record_state(self, state: Dict[str, Any]) -> None:
        """Record state in history."""
        self.state_history.append(state.copy())
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
    
    def _interpolate_player(self, server_player: Dict, local_player: Dict) -> Dict:
        """
        Interpolate between server and local player state.
        
        Args:
            server_player: Server's player state
            local_player: Local player state
            
        Returns:
            Interpolated player state
        """
        interpolated = server_player.copy()
        
        # Use server position as authoritative
        interpolated['x'] = server_player.get('x', local_player.get('x', 0))
        interpolated['y'] = server_player.get('y', local_player.get('y', 0))
        
        # Keep local velocity for prediction
        if 'vx' in local_player:
            interpolated['vx'] = local_player['vx']
        if 'vy' in local_player:
            interpolated['vy'] = local_player['vy']
        
        return interpolated
