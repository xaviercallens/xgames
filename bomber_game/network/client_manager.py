"""
Client manager for connecting to multiplayer games.
"""

import time
from typing import Dict, Optional
from .network_manager import NetworkManager
from .protocol import GameMessage, MessageType, PlayerActionMessage


class ClientManager(NetworkManager):
    """
    Client manager for connecting to multiplayer games.
    Handles player actions and state synchronization.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 8888, player_name: str = 'Player'):
        """
        Initialize client manager.
        
        Args:
            host: Server host address
            port: Server port
            player_name: Name of this player
        """
        super().__init__(is_server=False, host=host, port=port)
        self.player_name = player_name
        self.player_id = None
        self.game_state = {}
        self.frame = 0
        self.game_running = False
        self.last_heartbeat = time.time()
        self.heartbeat_interval = 5.0  # Send heartbeat every 5 seconds
    
    def connect(self) -> bool:
        """
        Connect to server.
        
        Returns:
            True if successful
        """
        if not self.connect_to_server(self.host, self.port):
            return False
        
        # Send connection message
        message = GameMessage(
            MessageType.CONNECT,
            {
                'player_name': self.player_name,
                'protocol_version': '1.0'
            }
        )
        self.send_message(message)
        
        print(f"📡 Connecting to server at {self.host}:{self.port}")
        return True
    
    def send_player_action(self, action: Dict) -> None:
        """
        Send player action to server.
        
        Args:
            action: Action dictionary with 'dx', 'dy', 'place_bomb'
        """
        if not self.connected or self.player_id is None:
            return
        
        message = PlayerActionMessage(
            self.player_id,
            self.frame,
            action
        )
        self.send_message(message)
    
    def update(self, delta_time: float) -> None:
        """
        Update client state.
        
        Args:
            delta_time: Time since last update
        """
        self.frame += 1
        
        # Process incoming messages
        self.process_messages()
        
        # Send heartbeat periodically
        current_time = time.time()
        if current_time - self.last_heartbeat >= self.heartbeat_interval:
            self._send_heartbeat()
            self.last_heartbeat = current_time
    
    def get_game_state(self) -> Dict:
        """Get current game state."""
        return self.game_state.copy()
    
    def is_game_running(self) -> bool:
        """Check if game is running."""
        return self.game_running
    
    def get_player_info(self) -> Dict:
        """Get player information."""
        return {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'connected': self.connected,
            'frame': self.frame,
            'game_running': self.game_running
        }
    
    def _send_heartbeat(self) -> None:
        """Send heartbeat to server."""
        if self.player_id is None:
            return
        
        message = GameMessage(
            MessageType.HEARTBEAT,
            {'player_id': self.player_id}
        )
        self.send_message(message)
