"""
Reinforcement Learning AI agent using Deep Q-Network (DQN).
Inspired by modern RL approaches for Bomberman.
"""

import numpy as np
import random
from collections import deque
from .agent_base import Agent

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available. RL agent will use fallback heuristics.")


class DQN(nn.Module):
    """Deep Q-Network for Bomberman."""
    
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, action_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)


class RLAgent(Agent):
    """
    Reinforcement Learning agent using DQN.
    
    Features:
    - Deep Q-Network for action selection
    - State representation from game grid
    - Pre-trained weights support
    - Experience replay for training
    - Epsilon-greedy exploration
    """
    
    def __init__(self, player, model_path=None, training=False):
        super().__init__(player)
        self.training = training
        self.think_delay = 0.1  # Fast decision making
        
        # Action space: [stay, up, down, left, right, bomb, bomb+up, bomb+down, bomb+left, bomb+right]
        self.actions = [
            (0, 0, False),   # 0: Stay
            (0, -1, False),  # 1: Up
            (0, 1, False),   # 2: Down
            (-1, 0, False),  # 3: Left
            (1, 0, False),   # 4: Right
            (0, 0, True),    # 5: Bomb
            (0, -1, True),   # 6: Bomb + Up
            (0, 1, True),    # 7: Bomb + Down
            (-1, 0, True),   # 8: Bomb + Left
            (1, 0, True),    # 9: Bomb + Right
        ]
        
        # RL parameters
        self.state_size = 13 * 13 + 10  # Grid + extra features
        self.action_size = len(self.actions)
        self.epsilon = 0.0 if not training else 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.95  # Discount factor
        self.learning_rate = 0.001
        
        # Experience replay
        self.memory = deque(maxlen=2000)
        self.batch_size = 32
        
        # Initialize model
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = DQN(self.state_size, self.action_size).to(self.device)
            self.target_model = DQN(self.state_size, self.action_size).to(self.device)
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
            self.criterion = nn.MSELoss()
            
            # Load pre-trained weights if available
            if model_path:
                try:
                    self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                    self.target_model.load_state_dict(self.model.state_dict())
                    print(f"✅ Loaded pre-trained model from {model_path}")
                except Exception as e:
                    print(f"⚠️  Could not load model: {e}")
            else:
                self.target_model.load_state_dict(self.model.state_dict())
        else:
            self.model = None
            
        self.last_state = None
        self.last_action = None
        self.last_reward = 0
        
    def choose_action(self, game_state):
        """Choose action using DQN or fallback heuristics."""
        if not self.player.alive:
            return (0, 0, False)
        
        # Get state representation
        state = self._get_state(game_state)
        
        if TORCH_AVAILABLE and self.model is not None:
            # Epsilon-greedy action selection
            if self.training and random.random() < self.epsilon:
                action_idx = random.randint(0, self.action_size - 1)
            else:
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                    q_values = self.model(state_tensor)
                    action_idx = q_values.argmax().item()
            
            # Store for training
            if self.training:
                self.last_state = state
                self.last_action = action_idx
            
            return self.actions[action_idx]
        else:
            # Fallback to heuristic-based decision
            return self._heuristic_action(game_state, state)
    
    def _get_state(self, game_state):
        """
        Extract state representation from game.
        
        State includes:
        - Grid representation (13x13 = 169 values)
        - Player position (2 values)
        - Enemy position (2 values)
        - Bomb count (1 value)
        - Nearest bomb distance (1 value)
        - Danger level (1 value)
        - Power-up count (1 value)
        - Health/alive status (1 value)
        - Can place bomb (1 value)
        """
        state = []
        
        # Flatten grid (13x13)
        for row in game_state.grid:
            state.extend(row)
        
        # Player position (normalized)
        state.append(self.player.grid_x / 13.0)
        state.append(self.player.grid_y / 13.0)
        
        # Enemy position (normalized)
        enemy = self._find_enemy(game_state)
        if enemy:
            state.append(enemy.grid_x / 13.0)
            state.append(enemy.grid_y / 13.0)
        else:
            state.extend([0.5, 0.5])
        
        # Bomb count
        state.append(self.player.active_bombs / max(self.player.max_bombs, 1))
        
        # Nearest bomb distance (normalized)
        nearest_bomb_dist = self._nearest_bomb_distance(game_state)
        state.append(min(nearest_bomb_dist / 13.0, 1.0))
        
        # Danger level (0-1)
        state.append(1.0 if self._in_danger(game_state) else 0.0)
        
        # Power-up count
        state.append(len(game_state.powerups) / 10.0)
        
        # Alive status
        state.append(1.0 if self.player.alive else 0.0)
        
        # Can place bomb
        state.append(1.0 if self.player.can_place_bomb() else 0.0)
        
        return np.array(state, dtype=np.float32)
    
    def _heuristic_action(self, game_state, state):
        """Fallback heuristic when PyTorch not available."""
        # Priority 1: Avoid danger
        if self._in_danger(game_state):
            return self._find_safe_move(game_state)
        
        # Priority 2: Place bomb near enemy
        enemy = self._find_enemy(game_state)
        if enemy and self._near_enemy(game_state, enemy):
            if self.player.can_place_bomb() and random.random() < 0.8:
                return (0, 0, True)
        
        # Priority 3: Move toward enemy
        if enemy:
            return self._move_toward_enemy(game_state, enemy)
        
        # Default: Random move
        return self._random_move(game_state)
    
    def _find_enemy(self, game_state):
        """Find enemy player."""
        for player in game_state.players:
            if player != self.player and player.alive:
                return player
        return None
    
    def _in_danger(self, game_state):
        """Check if in danger from explosions or bombs."""
        px, py = self.player.grid_x, self.player.grid_y
        
        # Check explosions
        for explosion in game_state.explosions:
            if explosion.grid_x == px and explosion.grid_y == py:
                return True
        
        # Check bombs
        for bomb in game_state.bombs:
            if bomb.timer < 1.5:
                bx, by = bomb.grid_x, bomb.grid_y
                if px == bx and abs(py - by) <= bomb.bomb_range:
                    return True
                if py == by and abs(px - bx) <= bomb.bomb_range:
                    return True
        
        return False
    
    def _nearest_bomb_distance(self, game_state):
        """Calculate distance to nearest bomb."""
        px, py = self.player.grid_x, self.player.grid_y
        min_dist = 999
        
        for bomb in game_state.bombs:
            dist = abs(px - bomb.grid_x) + abs(py - bomb.grid_y)
            min_dist = min(min_dist, dist)
        
        return min_dist
    
    def _find_safe_move(self, game_state):
        """Find safe direction."""
        px, py = self.player.grid_x, self.player.grid_y
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = px + dx, py + dy
            if game_state.is_walkable(nx, ny):
                safe = True
                for bomb in game_state.bombs:
                    bx, by = bomb.grid_x, bomb.grid_y
                    if nx == bx and abs(ny - by) <= bomb.bomb_range:
                        safe = False
                        break
                    if ny == by and abs(nx - bx) <= bomb.bomb_range:
                        safe = False
                        break
                if safe:
                    return (dx, dy, False)
        
        return (0, 0, False)
    
    def _near_enemy(self, game_state, enemy):
        """Check if near enemy."""
        px, py = self.player.grid_x, self.player.grid_y
        tx, ty = enemy.grid_x, enemy.grid_y
        distance = abs(px - tx) + abs(py - ty)
        return distance <= 3
    
    def _move_toward_enemy(self, game_state, enemy):
        """Move toward enemy."""
        px, py = self.player.grid_x, self.player.grid_y
        tx, ty = enemy.grid_x, enemy.grid_y
        
        dx = 0 if px == tx else (1 if tx > px else -1)
        dy = 0 if py == ty else (1 if ty > py else -1)
        
        if dx != 0 and game_state.is_walkable(px + dx, py):
            return (dx, 0, False)
        if dy != 0 and game_state.is_walkable(px, py + dy):
            return (0, dy, False)
        
        return self._random_move(game_state)
    
    def _random_move(self, game_state):
        """Random valid move."""
        px, py = self.player.grid_x, self.player.grid_y
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = px + dx, py + dy
            if game_state.is_walkable(nx, ny):
                return (dx, dy, False)
        
        return (0, 0, False)
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay memory."""
        if self.training:
            self.memory.append((state, action, reward, next_state, done))
    
    def replay(self):
        """Train on batch of experiences."""
        if not TORCH_AVAILABLE or not self.training or len(self.memory) < self.batch_size:
            return
        
        batch = random.sample(self.memory, self.batch_size)
        
        for state, action, reward, next_state, done in batch:
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)
            
            target = reward
            if not done:
                target = reward + self.gamma * self.target_model(next_state_tensor).max().item()
            
            target_f = self.model(state_tensor)
            target_f[0][action] = target
            
            self.optimizer.zero_grad()
            loss = self.criterion(self.model(state_tensor), target_f)
            loss.backward()
            self.optimizer.step()
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def update_target_model(self):
        """Update target network."""
        if TORCH_AVAILABLE:
            self.target_model.load_state_dict(self.model.state_dict())
    
    def save_model(self, path):
        """Save model weights."""
        if TORCH_AVAILABLE:
            torch.save(self.model.state_dict(), path)
            print(f"✅ Model saved to {path}")
    
    def load_model(self, path):
        """Load model weights."""
        if TORCH_AVAILABLE:
            try:
                self.model.load_state_dict(torch.load(path, map_location=self.device))
                self.target_model.load_state_dict(self.model.state_dict())
                print(f"✅ Model loaded from {path}")
            except Exception as e:
                print(f"⚠️  Could not load model: {e}")
