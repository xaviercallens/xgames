"""
Message handler for processing network messages.
"""

from typing import Callable, Dict, List
from .protocol import GameMessage, MessageType


class MessageHandler:
    """Handles routing and processing of network messages."""
    
    def __init__(self):
        """Initialize message handler."""
        self.handlers: Dict[MessageType, List[Callable]] = {}
    
    def register(self, msg_type: MessageType, handler: Callable) -> None:
        """
        Register message handler.
        
        Args:
            msg_type: Message type to handle
            handler: Handler function
        """
        if msg_type not in self.handlers:
            self.handlers[msg_type] = []
        self.handlers[msg_type].append(handler)
    
    def unregister(self, msg_type: MessageType, handler: Callable) -> None:
        """
        Unregister message handler.
        
        Args:
            msg_type: Message type
            handler: Handler function to remove
        """
        if msg_type in self.handlers:
            try:
                self.handlers[msg_type].remove(handler)
            except ValueError:
                pass
    
    def handle(self, message: GameMessage) -> None:
        """
        Handle message by calling registered handlers.
        
        Args:
            message: Message to handle
        """
        if message.type in self.handlers:
            for handler in self.handlers[message.type]:
                try:
                    handler(message)
                except Exception as e:
                    print(f"❌ Error in message handler: {e}")
    
    def clear(self) -> None:
        """Clear all handlers."""
        self.handlers.clear()
