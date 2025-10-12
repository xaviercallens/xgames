"""
Game state management for Bomberman.
"""

import random
from .entities import Player, Bomb, Explosion, PowerUp, Caca
from .entities.teleport_door import TeleportDoorManager
from .entities.bomb_machine import BombMachine
from .config import MAP_CONFIG


class GameState:
    """Manages the game state including grid, entities, and game logic."""
    
    def __init__(self, grid_size=13):
        """
        Initialize game state.
        
        Args:
            grid_size: Size of the grid (grid_size x grid_size)
        """
        self.grid_size = grid_size
        self.powerups = {}  # {(x, y): PowerUp} - Initialize before _generate_grid
        self.grid = self._generate_grid()
        
        # Entities
        self.players = []
        self.bombs = []
        self.explosions = []
        self.cacas = []  # Caca blocks!
        
        # New features
        self.teleport_doors = TeleportDoorManager(grid_size)
        self.teleport_doors.create_door_pairs(MAP_CONFIG.get('num_teleport_doors', 4))
        
        # Clear grid tiles where doors are placed so players can walk on them
        for door in self.teleport_doors.doors:
            self.grid[door.grid_y][door.grid_x] = 0  # Make walkable
        
        self.bomb_machine = None
        if MAP_CONFIG.get('bomb_machine_enabled', True):
            self.bomb_machine = BombMachine(grid_size, self)
            # Clear grid tile where bomb machine is placed
            self.grid[self.bomb_machine.grid_y][self.bomb_machine.grid_x] = 0
        
        # Game state
        self.game_over = False
        self.winner = None
        self.game_time = 0.0  # Track total game time for cooldowns
        
    def _generate_grid(self):
        """Generate game grid with walls and soft walls."""
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Place indestructible walls (border and pattern)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Border walls
                if x == 0 or x == self.grid_size - 1 or y == 0 or y == self.grid_size - 1:
                    grid[y][x] = 1
                # Interior wall pattern (every other tile)
                elif x % 2 == 0 and y % 2 == 0:
                    grid[y][x] = 1
        
        # Place soft walls randomly (but not in starting positions)
        safe_zones = [
            (1, 1), (2, 1), (1, 2),  # Top-left (player 1)
            (self.grid_size - 2, self.grid_size - 2),  # Bottom-right (player 2)
            (self.grid_size - 3, self.grid_size - 2),
            (self.grid_size - 2, self.grid_size - 3),
        ]
        
        # Get wall density from config
        wall_density = MAP_CONFIG.get('soft_wall_density', 0.05)
        powerup_chance = MAP_CONFIG.get('powerup_chance', 0.6)
        
        for y in range(1, self.grid_size - 1):
            for x in range(1, self.grid_size - 1):
                if grid[y][x] == 0 and (x, y) not in safe_zones:
                    if random.random() < wall_density:  # Use config density
                        grid[y][x] = 2
                        # Chance of power-up under soft wall
                        if random.random() < powerup_chance:
                            powerup_type = random.randint(0, 5)  # 0-5 for 6 types
                            self.powerups[(x, y)] = PowerUp(x, y, powerup_type)
        
        return grid
    
    def add_player(self, x, y, color, name="Player"):
        """Add a player to the game."""
        player = Player(x, y, color, name)
        self.players.append(player)
        return player
    
    def place_bomb(self, player):
        """Place a bomb for the player."""
        if not player.can_place_bomb():
            return None
        
        # Place bomb at player's grid position
        x, y = player.grid_x, player.grid_y
        
        # Check if there's already a bomb here
        for bomb in self.bombs:
            if bomb.grid_x == x and bomb.grid_y == y:
                return None
        
        bomb = Bomb(x, y, player.bomb_range, player)
        player.active_bombs += 1
        self.bombs.append(bomb)
        return bomb
    
    def place_caca(self, player):
        """Place a caca block for the player."""
        if not player.can_place_caca():
            return None
        
        # Place caca at player's grid position
        x, y = player.grid_x, player.grid_y
        
        # Check if there's already something here
        for caca in self.cacas:
            if caca.grid_x == x and caca.grid_y == y:
                return None
        for bomb in self.bombs:
            if bomb.grid_x == x and bomb.grid_y == y:
                return None
        
        caca = Caca(x, y, player)
        player.active_cacas += 1
        self.cacas.append(caca)
        return caca
    
    def update(self, dt):
        """Update all game entities."""
        # Update game time
        self.game_time += dt
        
        # Update bombs
        for bomb in self.bombs[:]:
            bomb.update(dt)
            if bomb.exploded:
                self._create_explosion(bomb)
                self.bombs.remove(bomb)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update(dt)
            if not explosion.alive:
                self.explosions.remove(explosion)
        
        # Update cacas
        for caca in self.cacas[:]:
            caca.update(dt)
            if not caca.alive:
                self.cacas.remove(caca)
                # Owner can place another caca
                if caca.owner:
                    caca.owner.active_cacas -= 1
        
        # Update power-ups
        for powerup in list(self.powerups.values()):
            powerup.update(dt)
        
        # Update teleport doors
        if self.teleport_doors:
            self.teleport_doors.update(dt)
            # Check if players are on doors
            for player in self.players:
                if player.alive:
                    door = self.teleport_doors.get_door_at(int(player.x), int(player.y))
                    if door and door.can_teleport(player, self.game_time):
                        door.teleport_player(player, self.game_time)
        
        # Update bomb machine
        if self.bomb_machine:
            dropped_bomb = self.bomb_machine.update(dt, self)
            if dropped_bomb:
                self.bombs.append(dropped_bomb)
        
        # Check collisions
        self._check_collisions()
        
        # Check win condition
        self._check_win_condition()
    
    def _create_explosion(self, bomb):
        """Create explosion from bomb."""
        x, y = bomb.grid_x, bomb.grid_y
        bomb_range = bomb.bomb_range
        
        # Center explosion
        self.explosions.append(Explosion(x, y))
        
        # Spread in 4 directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        
        for dx, dy in directions:
            for i in range(1, bomb_range + 1):
                ex, ey = x + dx * i, y + dy * i
                
                # Check bounds
                if ex < 0 or ex >= self.grid_size or ey < 0 or ey >= self.grid_size:
                    break
                
                # Check for walls
                if self.grid[ey][ex] == 1:  # Indestructible wall
                    break
                
                # Add explosion
                self.explosions.append(Explosion(ex, ey))
                
                # Destroy soft wall
                if self.grid[ey][ex] == 2:
                    self.grid[ey][ex] = 0
                    break
    
    def _check_collisions(self):
        """Check for collisions between entities."""
        # Check player-explosion collisions
        for player in self.players:
            if not player.alive:
                continue
                
            px, py = player.grid_x, player.grid_y
            for explosion in self.explosions:
                if explosion.grid_x == px and explosion.grid_y == py:
                    player.alive = False
        
        # Check player-powerup collisions
        for player in self.players:
            if not player.alive:
                continue
                
            px, py = player.grid_x, player.grid_y
            if (px, py) in self.powerups:
                powerup = self.powerups[(px, py)]
                player.add_powerup(powerup.powerup_type)
                del self.powerups[(px, py)]
    
    def _check_win_condition(self):
        """Check if game is over."""
        alive_players = [p for p in self.players if p.alive]
        
        if len(alive_players) == 0:
            self.game_over = True
            self.winner = None  # Draw
        elif len(alive_players) == 1 and len(self.players) > 1:
            self.game_over = True
            self.winner = alive_players[0]
    
    def get_tile(self, x, y):
        """Get tile type at position."""
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return 1  # Treat out of bounds as wall
        return self.grid[y][x]
    
    def is_walkable(self, x, y):
        """Check if position is walkable."""
        tile = self.get_tile(x, y)
        if tile in [1, 2]:  # Wall or soft wall
            return False
        
        # Check for bombs
        for bomb in self.bombs:
            if bomb.grid_x == x and bomb.grid_y == y:
                return False
        
        # Check for cacas (poop blocks!)
        for caca in self.cacas:
            if caca.grid_x == x and caca.grid_y == y:
                return False
        
        return True
