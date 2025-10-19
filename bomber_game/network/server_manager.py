"""
Server manager for hosting multiplayer games.
"""

import time
from typing import Dict, Optional, List
from .network_manager import NetworkManager
from .protocol import GameMessage, MessageType, GameStateMessage


class ServerManager(NetworkManager):
    """
    Server manager for hosting multiplayer games.
    Handles game state synchronization and player management.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 8888, max_players: int = 4):
        """
        Initialize server manager.
        
        Args:
            host: Server host address
            port: Server port
            max_players: Maximum number of players
        """
        super().__init__(is_server=True, host=host, port=port)
        self.max_players = max_players
        self.game_state = {}
        self.frame = 0
        self.game_running = False
        self.last_sync_time = time.time()
        self.sync_interval = 0.016  # ~60 FPS
    
    def start(self) -> bool:
        """Start server."""
        return self.start_server(self.max_players)
    
    def set_game_state(self, game_state: Dict) -> None:
        """
        Set current game state.
        
        Args:
            game_state: Game state dictionary
        """
        self.game_state = game_state
    
    def update_game_state(self, delta_time: float) -> None:
        """
        Update game state and synchronize with clients.
        
        Args:
            delta_time: Time since last update
        """
        self.frame += 1
        
        # Process incoming messages
        self.process_messages()
        
        # Synchronize game state periodically
        current_time = time.time()
        if current_time - self.last_sync_time >= self.sync_interval:
            self._broadcast_game_state()
            self.last_sync_time = current_time
    
    def broadcast_game_start(self) -> None:
        """Broadcast game start message."""
        message = GameMessage(
            MessageType.GAME_START,
            {
                'frame': self.frame,
                'game_state': self.game_state,
                'max_players': self.max_players
            }
        )
        self.broadcast_message(message)
        self.game_running = True
        print("🎮 Game started on server")
    
    def broadcast_game_over(self, winner_id: Optional[int] = None) -> None:
        """
        Broadcast game over message.
        
        Args:
            winner_id: ID of winning player
        """
        message = GameMessage(
            MessageType.GAME_OVER,
            {
                'frame': self.frame,
                'winner_id': winner_id,
                'game_state': self.game_state
            }
        )
        self.broadcast_message(message)
        self.game_running = False
        print("🏁 Game over on server")
    
    def get_server_info(self) -> Dict:
        """Get server information."""
        return {
            'host': self.host,
            'port': self.port,
            'max_players': self.max_players,
            'connected_players': self.get_connected_players(),
            'game_running': self.game_running,
            'frame': self.frame,
            'player_names': self.player_names.copy()
        }
    
    def _broadcast_game_state(self) -> None:
        """Broadcast current game state to all clients."""
        message = GameStateMessage(self.frame, self.game_state)
        self.broadcast_message(message)
