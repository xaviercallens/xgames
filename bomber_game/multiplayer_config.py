"""
Game configuration for multiplayer games.
Manages player setup and AI configuration.
"""

from typing import List, Dict, Optional


class PlayerConfig:
    """Configuration for a single player."""
    
    def __init__(self, player_id: int, name: str, player_type: str, 
                 ai_mode: Optional[str] = None, color: tuple = (255, 255, 255)):
        """
        Initialize player configuration.
        
        Args:
            player_id: Player ID (1-4)
            name: Player name
            player_type: 'human' or 'ai'
            ai_mode: AI mode if AI player
            color: Player color (R, G, B)
        """
        self.player_id = player_id
        self.name = name
        self.type = player_type
        self.ai_mode = ai_mode
        self.color = color
    
    def is_human(self) -> bool:
        """Check if human player."""
        return self.type == 'human'
    
    def is_ai(self) -> bool:
        """Check if AI player."""
        return self.type == 'ai'
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'player_id': self.player_id,
            'name': self.name,
            'type': self.type,
            'ai_mode': self.ai_mode,
            'color': self.color
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'PlayerConfig':
        """Create from dictionary."""
        return PlayerConfig(
            data['player_id'],
            data['name'],
            data['type'],
            data.get('ai_mode'),
            tuple(data.get('color', (255, 255, 255)))
        )
    
    def __repr__(self) -> str:
        return f"PlayerConfig(id={self.player_id}, name={self.name}, type={self.type})"


class GameConfig:
    """Configuration for a multiplayer game."""
    
    def __init__(self):
        """Initialize game configuration."""
        self.players: List[PlayerConfig] = []
        self.game_mode = 'local'  # 'local' or 'network'
        self.max_players = 4
        self.grid_size = 13
    
    def add_player(self, player_config: PlayerConfig) -> None:
        """
        Add player to configuration.
        
        Args:
            player_config: Player configuration
        """
        if len(self.players) < self.max_players:
            self.players.append(player_config)
    
    def remove_player(self, player_id: int) -> None:
        """
        Remove player from configuration.
        
        Args:
            player_id: Player ID to remove
        """
        self.players = [p for p in self.players if p.player_id != player_id]
    
    def get_player(self, player_id: int) -> Optional[PlayerConfig]:
        """
        Get player configuration.
        
        Args:
            player_id: Player ID
            
        Returns:
            PlayerConfig or None
        """
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def get_human_players(self) -> List[PlayerConfig]:
        """Get all human players."""
        return [p for p in self.players if p.is_human()]
    
    def get_ai_players(self) -> List[PlayerConfig]:
        """Get all AI players."""
        return [p for p in self.players if p.is_ai()]
    
    def get_player_count(self) -> int:
        """Get total player count."""
        return len(self.players)
    
    def get_human_count(self) -> int:
        """Get human player count."""
        return len(self.get_human_players())
    
    def get_ai_count(self) -> int:
        """Get AI player count."""
        return len(self.get_ai_players())
    
    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return 2 <= len(self.players) <= self.max_players
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'players': [p.to_dict() for p in self.players],
            'game_mode': self.game_mode,
            'max_players': self.max_players,
            'grid_size': self.grid_size
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'GameConfig':
        """Create from dictionary."""
        config = GameConfig()
        config.game_mode = data.get('game_mode', 'local')
        config.max_players = data.get('max_players', 4)
        config.grid_size = data.get('grid_size', 13)
        
        for player_data in data.get('players', []):
            config.add_player(PlayerConfig.from_dict(player_data))
        
        return config
    
    def __repr__(self) -> str:
        return f"GameConfig(players={len(self.players)}, mode={self.game_mode})"


class GameConfigBuilder:
    """Builder for creating game configurations."""
    
    def __init__(self):
        """Initialize builder."""
        self.config = GameConfig()
    
    def set_game_mode(self, mode: str) -> 'GameConfigBuilder':
        """
        Set game mode.
        
        Args:
            mode: 'local' or 'network'
            
        Returns:
            Self for chaining
        """
        self.config.game_mode = mode
        return self
    
    def set_max_players(self, max_players: int) -> 'GameConfigBuilder':
        """
        Set maximum players.
        
        Args:
            max_players: Maximum player count
            
        Returns:
            Self for chaining
        """
        self.config.max_players = max_players
        return self
    
    def add_human_player(self, name: str, color: tuple = (255, 255, 255)) -> 'GameConfigBuilder':
        """
        Add human player.
        
        Args:
            name: Player name
            color: Player color
            
        Returns:
            Self for chaining
        """
        player_id = len(self.config.players) + 1
        player = PlayerConfig(player_id, name, 'human', None, color)
        self.config.add_player(player)
        return self
    
    def add_ai_player(self, name: str, ai_mode: str, color: tuple = (255, 255, 255)) -> 'GameConfigBuilder':
        """
        Add AI player.
        
        Args:
            name: AI name
            ai_mode: AI mode type
            color: Player color
            
        Returns:
            Self for chaining
        """
        player_id = len(self.config.players) + 1
        player = PlayerConfig(player_id, name, 'ai', ai_mode, color)
        self.config.add_player(player)
        return self
    
    def build(self) -> GameConfig:
        """
        Build configuration.
        
        Returns:
            GameConfig instance
        """
        if not self.config.is_valid():
            raise ValueError("Invalid game configuration")
        return self.config


# Preset configurations

def create_1v1_config(human_name: str = 'Player', ai_mode: str = 'intermediate_heuristic') -> GameConfig:
    """Create 1v1 configuration."""
    builder = GameConfigBuilder()
    builder.add_human_player(human_name, (0, 255, 0))
    builder.add_ai_player('AI Opponent', ai_mode, (255, 0, 0))
    return builder.build()


def create_2player_local_config(player1_name: str = 'Player 1', 
                               player2_name: str = 'Player 2') -> GameConfig:
    """Create 2-player local configuration."""
    builder = GameConfigBuilder()
    builder.add_human_player(player1_name, (0, 255, 0))
    builder.add_human_player(player2_name, (255, 0, 0))
    return builder.build()


def create_4player_local_config(names: List[str] = None) -> GameConfig:
    """Create 4-player local configuration."""
    if names is None:
        names = ['Player 1', 'Player 2', 'Player 3', 'Player 4']
    
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    
    builder = GameConfigBuilder()
    for i, name in enumerate(names[:4]):
        builder.add_human_player(name, colors[i])
    return builder.build()


def create_mixed_config(human_names: List[str], ai_modes: List[str]) -> GameConfig:
    """Create mixed human/AI configuration."""
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    
    builder = GameConfigBuilder()
    
    # Add human players
    for i, name in enumerate(human_names):
        builder.add_human_player(name, colors[i])
    
    # Add AI players
    for i, ai_mode in enumerate(ai_modes):
        builder.add_ai_player(f'AI {i + 1}', ai_mode, colors[len(human_names) + i])
    
    return builder.build()
