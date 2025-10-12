"""
Teleport Door Entity
Allows players to teleport between door pairs on the map borders.
"""

import pygame
from .entity import Entity


class TeleportDoor(Entity):
    """
    Teleport door that allows players to enter and exit at different locations.
    Doors are placed on map borders and linked in pairs.
    """
    
    def __init__(self, x, y, door_id, color=(255, 0, 255)):
        """
        Initialize teleport door.
        
        Args:
            x, y: Grid position
            door_id: Unique identifier for this door
            color: Door color (RGB tuple)
        """
        super().__init__(x, y, 32, 32)  # Full tile size
        self.grid_x = x
        self.grid_y = y
        self.door_id = door_id
        self.color = color
        self.linked_door = None  # Will be set to paired door
        self.animation_frame = 0
        self.animation_speed = 0.1
        
    def link_to(self, other_door):
        """
        Link this door to another door for teleportation.
        
        Args:
            other_door: TeleportDoor to link to
        """
        self.linked_door = other_door
        other_door.linked_door = self
        
    def can_teleport(self, player):
        """
        Check if player can use this door.
        
        Args:
            player: Player entity
            
        Returns:
            True if player is on door and linked door exists
        """
        if not self.linked_door:
            return False
            
        # Check if player is on this door
        player_x, player_y = int(player.x), int(player.y)
        return player_x == self.grid_x and player_y == self.grid_y
        
    def teleport_player(self, player):
        """
        Teleport player to linked door.
        
        Args:
            player: Player entity to teleport
        """
        if self.linked_door:
            player.x = self.linked_door.grid_x
            player.y = self.linked_door.grid_y
            return True
        return False
        
    def update(self, dt):
        """Update door animation."""
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 1.0:
            self.animation_frame = 0.0
            
    def draw(self, screen, tile_size):
        """
        Draw teleport door with animation.
        
        Args:
            screen: Pygame surface
            tile_size: Size of each tile in pixels
        """
        x = self.grid_x * tile_size
        y = self.grid_y * tile_size
        
        # Draw pulsing door
        pulse = int(50 * abs(self.animation_frame - 0.5) * 2)
        color = tuple(min(255, c + pulse) for c in self.color)
        
        # Draw door background
        pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))
        
        # Draw door symbol (portal effect)
        center_x = x + tile_size // 2
        center_y = y + tile_size // 2
        radius = int(tile_size * 0.3)
        
        # Outer ring
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 2)
        
        # Inner ring (animated)
        inner_radius = int(radius * (0.5 + 0.3 * self.animation_frame))
        pygame.draw.circle(screen, (200, 200, 255), (center_x, center_y), inner_radius, 1)
        
        # Draw door ID
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.door_id), True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)


class TeleportDoorManager:
    """Manages all teleport doors on the map."""
    
    def __init__(self, grid_size):
        """
        Initialize door manager.
        
        Args:
            grid_size: Size of the game grid
        """
        self.grid_size = grid_size
        self.doors = []
        self.door_pairs = []
        
    def create_door_pairs(self, num_pairs):
        """
        Create pairs of linked teleport doors on map borders.
        
        Args:
            num_pairs: Number of door pairs to create
        """
        import random
        
        # Define border positions (excluding corners)
        border_positions = []
        
        # Top and bottom borders
        for x in range(2, self.grid_size - 2):
            border_positions.append((x, 0))  # Top
            border_positions.append((x, self.grid_size - 1))  # Bottom
            
        # Left and right borders
        for y in range(2, self.grid_size - 2):
            border_positions.append((0, y))  # Left
            border_positions.append((self.grid_size - 1, y))  # Right
            
        # Shuffle and select positions
        random.shuffle(border_positions)
        
        # Create door pairs
        colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow
            (255, 128, 0),    # Orange
            (128, 0, 255),    # Purple
            (0, 255, 128),    # Green-cyan
        ]
        
        for i in range(min(num_pairs, len(border_positions) // 2)):
            # Get two positions for this pair
            pos1 = border_positions[i * 2]
            pos2 = border_positions[i * 2 + 1]
            
            # Create doors
            color = colors[i % len(colors)]
            door1 = TeleportDoor(pos1[0], pos1[1], i + 1, color)
            door2 = TeleportDoor(pos2[0], pos2[1], i + 1, color)
            
            # Link doors
            door1.link_to(door2)
            
            # Add to lists
            self.doors.extend([door1, door2])
            self.door_pairs.append((door1, door2))
            
    def get_door_at(self, x, y):
        """
        Get door at specific position.
        
        Args:
            x, y: Grid position
            
        Returns:
            TeleportDoor or None
        """
        for door in self.doors:
            if door.grid_x == x and door.grid_y == y:
                return door
        return None
        
    def update(self, dt):
        """Update all doors."""
        for door in self.doors:
            door.update(dt)
            
    def draw(self, screen, tile_size):
        """Draw all doors."""
        for door in self.doors:
            door.draw(screen, tile_size)
