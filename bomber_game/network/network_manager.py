"""
Network manager for handling multiplayer connections.
"""

import socket
import threading
import json
from typing import Dict, List, Optional, Callable
from .protocol import GameMessage, MessageType


class NetworkManager:
    """
    Manages network connections for multiplayer games.
    Handles both server and client operations.
    """
    
    def __init__(self, is_server: bool = False, host: str = 'localhost', port: int = 8888):
        """
        Initialize network manager.
        
        Args:
            is_server: Whether this is a server instance
            host: Host address
            port: Port number
        """
        self.is_server = is_server
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.running = False
        
        # Connection management
        self.connections: Dict[int, socket.socket] = {}
        self.player_ids: Dict[socket.socket, int] = {}
        self.player_names: Dict[int, str] = {}
        
        # Message handling
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        self.message_queue: List[GameMessage] = []
        
        # Threading
        self.receive_thread = None
        self.send_thread = None
        self.lock = threading.Lock()
    
    def start_server(self, max_players: int = 4) -> bool:
        """
        Start server.
        
        Args:
            max_players: Maximum number of players
            
        Returns:
            True if successful
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(max_players)
            
            self.running = True
            self.connected = True
            
            # Start accept thread
            self.receive_thread = threading.Thread(target=self._accept_connections, daemon=True)
            self.receive_thread.start()
            
            print(f"✅ Server started on {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def connect_to_server(self, host: str, port: int) -> bool:
        """
        Connect to server as client.
        
        Args:
            host: Server host
            port: Server port
            
        Returns:
            True if successful
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            self.running = True
            self.connected = True
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            self.receive_thread.start()
            
            print(f"✅ Connected to server at {host}:{port}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to server: {e}")
            return False
    
    def send_message(self, message: GameMessage, player_id: Optional[int] = None) -> bool:
        """
        Send message to player or broadcast.
        
        Args:
            message: Message to send
            player_id: Target player ID (None for broadcast)
            
        Returns:
            True if successful
        """
        try:
            with self.lock:
                if player_id is not None:
                    # Send to specific player
                    if player_id in self.connections:
                        sock = self.connections[player_id]
                        self._send_to_socket(sock, message)
                        return True
                else:
                    # Broadcast to all
                    for sock in self.connections.values():
                        self._send_to_socket(sock, message)
                    return True
            return False
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def broadcast_message(self, message: GameMessage) -> bool:
        """
        Broadcast message to all connected players.
        
        Args:
            message: Message to broadcast
            
        Returns:
            True if successful
        """
        return self.send_message(message, player_id=None)
    
    def register_handler(self, msg_type: MessageType, handler: Callable) -> None:
        """
        Register message handler.
        
        Args:
            msg_type: Message type to handle
            handler: Handler function
        """
        if msg_type not in self.message_handlers:
            self.message_handlers[msg_type] = []
        self.message_handlers[msg_type].append(handler)
    
    def process_messages(self) -> List[GameMessage]:
        """
        Process queued messages.
        
        Returns:
            List of processed messages
        """
        processed = []
        with self.lock:
            for message in self.message_queue:
                # Call registered handlers
                if message.type in self.message_handlers:
                    for handler in self.message_handlers[message.type]:
                        try:
                            handler(message)
                        except Exception as e:
                            print(f"❌ Error in message handler: {e}")
                processed.append(message)
            self.message_queue.clear()
        return processed
    
    def disconnect(self) -> None:
        """Disconnect from network."""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
        print("✅ Disconnected from network")
    
    def get_connected_players(self) -> int:
        """Get number of connected players."""
        return len(self.connections)
    
    def get_player_name(self, player_id: int) -> Optional[str]:
        """Get player name by ID."""
        return self.player_names.get(player_id)
    
    # Private methods
    
    def _accept_connections(self) -> None:
        """Accept incoming connections (server only)."""
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                print(f"📡 New connection from {address}")
                
                # Assign player ID
                player_id = len(self.connections) + 1
                
                with self.lock:
                    self.connections[player_id] = client_socket
                    self.player_ids[client_socket] = player_id
                
                # Start receive thread for this client
                thread = threading.Thread(
                    target=self._receive_from_client,
                    args=(client_socket, player_id),
                    daemon=True
                )
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"❌ Error accepting connection: {e}")
    
    def _receive_from_client(self, client_socket: socket.socket, player_id: int) -> None:
        """Receive messages from client."""
        while self.running:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Parse message
                message = GameMessage.from_json(data.decode('utf-8'))
                
                with self.lock:
                    self.message_queue.append(message)
            except Exception as e:
                print(f"❌ Error receiving from client {player_id}: {e}")
                break
        
        # Clean up
        with self.lock:
            if player_id in self.connections:
                del self.connections[player_id]
            if client_socket in self.player_ids:
                del self.player_ids[client_socket]
        
        try:
            client_socket.close()
        except:
            pass
        
        print(f"📡 Client {player_id} disconnected")
    
    def _receive_messages(self) -> None:
        """Receive messages (client only)."""
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                # Parse message
                message = GameMessage.from_json(data.decode('utf-8'))
                
                with self.lock:
                    self.message_queue.append(message)
            except Exception as e:
                if self.running:
                    print(f"❌ Error receiving message: {e}")
    
    def _send_to_socket(self, sock: socket.socket, message: GameMessage) -> None:
        """Send message to socket."""
        try:
            data = message.to_json().encode('utf-8')
            sock.sendall(data)
        except Exception as e:
            print(f"❌ Error sending to socket: {e}")
