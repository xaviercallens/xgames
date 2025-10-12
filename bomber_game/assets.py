"""
Asset manager for Trump Man game.
Loads and caches images and sounds.
"""

import pygame
import os

class AssetManager:
    """Manages game assets (images, sounds, etc.)"""
    
    def __init__(self):
        """Initialize asset manager."""
        self.images = {}
        self.base_path = os.path.join(os.path.dirname(__file__), 'assets')
        self.images_path = os.path.join(self.base_path, 'images')
        
    def load_image(self, filename, scale=None):
        """
        Load an image file.
        
        Args:
            filename: Name of the image file
            scale: Optional tuple (width, height) to scale image
            
        Returns:
            pygame.Surface with the image
        """
        # Check cache
        cache_key = f"{filename}_{scale}" if scale else filename
        if cache_key in self.images:
            return self.images[cache_key]
        
        # Load image
        filepath = os.path.join(self.images_path, filename)
        try:
            image = pygame.image.load(filepath)
            
            # Scale if requested
            if scale:
                image = pygame.transform.scale(image, scale)
            
            # Convert for better performance
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
            
            # Cache it
            self.images[cache_key] = image
            return image
            
        except pygame.error as e:
            print(f"Warning: Could not load image {filename}: {e}")
            # Return a colored surface as fallback
            surf = pygame.Surface(scale if scale else (64, 64))
            surf.fill((255, 0, 255))  # Magenta for missing textures
            return surf
    
    def get_player_sprite(self, player_num, size=(60, 60)):
        """Get player sprite."""
        filename = f"player{player_num}_60_60.png"
        return self.load_image(filename, size)
    
    def get_bomb_sprite(self, size=(60, 60)):
        """Get bomb sprite."""
        return self.load_image("bomb.png", size)
    
    def get_wall_sprite(self, size=(64, 64)):
        """Get wall sprite."""
        return self.load_image("wallhard.png", size)
    
    def get_tiles_spritesheet(self):
        """Get the tiles spritesheet."""
        return self.load_image("tiles_bomberman.png")
    
    def extract_tile(self, spritesheet, x, y, width, height, scale=None):
        """
        Extract a tile from a spritesheet.
        
        Args:
            spritesheet: The spritesheet surface
            x, y: Position in the spritesheet
            width, height: Size of the tile
            scale: Optional tuple to scale the extracted tile
            
        Returns:
            pygame.Surface with the tile
        """
        tile = pygame.Surface((width, height), pygame.SRCALPHA)
        tile.blit(spritesheet, (0, 0), (x, y, width, height))
        
        if scale:
            tile = pygame.transform.scale(tile, scale)
        
        return tile


# Global asset manager instance
_asset_manager = None

def get_asset_manager():
    """Get the global asset manager instance."""
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager
