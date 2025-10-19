"""
Network protocol definitions for multiplayer communication.
"""

import json
import time
from enum import Enum
from typing import Dict, Any, Optional


class MessageType(Enum):
    """Message types for network communication."""
    
    # Connection messages
    CONNECT = "CONNECT"
    CONNECT_ACK = "CONNECT_ACK"
    DISCONNECT = "DISCONNECT"
    
    # Game state messages
    GAME_STATE = "GAME_STATE"
    GAME_START = "GAME_START"
    GAME_OVER = "GAME_OVER"
    
    # Player action messages
    PLAYER_ACTION = "PLAYER_ACTION"
    PLAYER_UPDATE = "PLAYER_UPDATE"
    
    # Synchronization messages
    SYNC_REQUEST = "SYNC_REQUEST"
    SYNC_RESPONSE = "SYNC_RESPONSE"
    
    # Heartbeat
    HEARTBEAT = "HEARTBEAT"
    HEARTBEAT_ACK = "HEARTBEAT_ACK"
    
    # Error messages
    ERROR = "ERROR"
    PING = "PING"
    PONG = "PONG"


class GameMessage:
    """Represents a network game message."""
    
    def __init__(self, msg_type: MessageType, data: Optional[Dict[str, Any]] = None):
        """
        Initialize game message.
        
        Args:
            msg_type: Type of message
            data: Message data dictionary
        """
        self.type = msg_type
        self.data = data or {}
        self.timestamp = time.time()
        self.message_id = int(self.timestamp * 1000)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'type': self.type.value,
            'data': self.data,
            'timestamp': self.timestamp,
            'message_id': self.message_id
        }
    
    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps(self.to_dict())
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GameMessage':
        """Create message from dictionary."""
        msg = GameMessage(
            MessageType(data['type']),
            data.get('data', {})
        )
        msg.timestamp = data.get('timestamp', time.time())
        msg.message_id = data.get('message_id', int(msg.timestamp * 1000))
        return msg
    
    @staticmethod
    def from_json(json_str: str) -> 'GameMessage':
        """Create message from JSON string."""
        data = json.loads(json_str)
        return GameMessage.from_dict(data)
    
    def __repr__(self) -> str:
        return f"GameMessage(type={self.type.value}, id={self.message_id})"


class ConnectionMessage(GameMessage):
    """Connection establishment message."""
    
    def __init__(self, player_name: str, player_id: Optional[int] = None):
        """Initialize connection message."""
        data = {
            'player_name': player_name,
            'player_id': player_id,
            'protocol_version': '1.0'
        }
        super().__init__(MessageType.CONNECT, data)


class ConnectionAckMessage(GameMessage):
    """Connection acknowledgment message."""
    
    def __init__(self, player_id: int, game_state: Dict[str, Any]):
        """Initialize connection ack message."""
        data = {
            'player_id': player_id,
            'game_state': game_state,
            'status': 'connected'
        }
        super().__init__(MessageType.CONNECT_ACK, data)


class PlayerActionMessage(GameMessage):
    """Player action message."""
    
    def __init__(self, player_id: int, frame: int, action: Dict[str, Any]):
        """Initialize player action message."""
        data = {
            'player_id': player_id,
            'frame': frame,
            'action': action
        }
        super().__init__(MessageType.PLAYER_ACTION, data)


class GameStateMessage(GameMessage):
    """Game state update message."""
    
    def __init__(self, frame: int, game_state: Dict[str, Any]):
        """Initialize game state message."""
        data = {
            'frame': frame,
            'game_state': game_state
        }
        super().__init__(MessageType.GAME_STATE, data)


class SyncRequestMessage(GameMessage):
    """Synchronization request message."""
    
    def __init__(self, frame: int):
        """Initialize sync request message."""
        data = {'frame': frame}
        super().__init__(MessageType.SYNC_REQUEST, data)


class SyncResponseMessage(GameMessage):
    """Synchronization response message."""
    
    def __init__(self, frame: int, game_state: Dict[str, Any]):
        """Initialize sync response message."""
        data = {
            'frame': frame,
            'game_state': game_state
        }
        super().__init__(MessageType.SYNC_RESPONSE, data)


class HeartbeatMessage(GameMessage):
    """Heartbeat message for connection keep-alive."""
    
    def __init__(self, player_id: int):
        """Initialize heartbeat message."""
        data = {'player_id': player_id}
        super().__init__(MessageType.HEARTBEAT, data)


class ErrorMessage(GameMessage):
    """Error message."""
    
    def __init__(self, error_code: int, error_message: str):
        """Initialize error message."""
        data = {
            'error_code': error_code,
            'error_message': error_message
        }
        super().__init__(MessageType.ERROR, data)


# Message factory
MESSAGE_CLASSES = {
    MessageType.CONNECT: ConnectionMessage,
    MessageType.CONNECT_ACK: ConnectionAckMessage,
    MessageType.PLAYER_ACTION: PlayerActionMessage,
    MessageType.GAME_STATE: GameStateMessage,
    MessageType.SYNC_REQUEST: SyncRequestMessage,
    MessageType.SYNC_RESPONSE: SyncResponseMessage,
    MessageType.HEARTBEAT: HeartbeatMessage,
    MessageType.ERROR: ErrorMessage,
}


def create_message(msg_type: MessageType, **kwargs) -> GameMessage:
    """
    Create a message of the specified type.
    
    Args:
        msg_type: Type of message to create
        **kwargs: Message-specific arguments
        
    Returns:
        GameMessage instance
    """
    msg_class = MESSAGE_CLASSES.get(msg_type, GameMessage)
    return msg_class(**kwargs)
