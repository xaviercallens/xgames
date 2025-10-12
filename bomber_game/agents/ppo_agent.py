"""
Advanced PPO (Proximal Policy Optimization) Agent
Inspired by CoderOne Bomberland competition agents.
More sophisticated than DQN with better sample efficiency.
"""

import numpy as np
import random
from collections import deque
from .agent_base import Agent

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.distributions import Categorical
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available. PPO agent will use fallback heuristics.")


class ActorCritic(nn.Module):
    """Actor-Critic network for PPO."""
    
    def __init__(self, state_size, action_size, hidden_size=256):
        super(ActorCritic, self).__init__()
        
        # Shared feature extraction
        self.shared = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )
        
        # Actor head (policy)
        self.actor = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, action_size),
            nn.Softmax(dim=-1)
        )
        
        # Critic head (value function)
        self.critic = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, 1)
        )
        
    def forward(self, state):
        features = self.shared(state)
        action_probs = self.actor(features)
        state_value = self.critic(features)
        return action_probs, state_value
    
    def act(self, state):
        """Select action using policy."""
        action_probs, _ = self.forward(state)
        dist = Categorical(action_probs)
        action = dist.sample()
        action_log_prob = dist.log_prob(action)
        return action.item(), action_log_prob
    
    def evaluate(self, state, action):
        """Evaluate action for training."""
        action_probs, state_value = self.forward(state)
        dist = Categorical(action_probs)
        action_log_probs = dist.log_prob(action)
        dist_entropy = dist.entropy()
        return action_log_probs, state_value, dist_entropy


class PPOAgent(Agent):
    """
    PPO Agent with advanced features:
    - Actor-Critic architecture
    - Clipped surrogate objective
    - Generalized Advantage Estimation (GAE)
    - Better sample efficiency than DQN
    - Inspired by Bomberland competition agents
    """
    
    def __init__(self, player, model_path=None, training=False):
        super().__init__(player)
        self.training = training
        self.think_delay = 0.05  # Very fast decision making
        
        # Action space (enhanced from DQN)
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
        
        # Enhanced state representation (Bomberland-inspired)
        self.state_size = 13 * 13 + 20  # Grid + enhanced features
        self.action_size = len(self.actions)
        
        # PPO hyperparameters
        self.gamma = 0.99  # Discount factor
        self.gae_lambda = 0.95  # GAE parameter
        self.clip_epsilon = 0.2  # PPO clip parameter
        self.c1 = 0.5  # Value loss coefficient
        self.c2 = 0.01  # Entropy coefficient
        self.learning_rate = 3e-4
        self.epochs = 10  # PPO epochs per update
        self.batch_size = 64
        
        # Memory for PPO
        self.memory = PPOMemory()
        
        # Initialize model
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.policy = ActorCritic(self.state_size, self.action_size).to(self.device)
            self.optimizer = optim.Adam(self.policy.parameters(), lr=self.learning_rate)
            
            # Load pre-trained weights if available
            if model_path:
                try:
                    checkpoint = torch.load(model_path, map_location=self.device)
                    self.policy.load_state_dict(checkpoint['model_state_dict'])
                    if training and 'optimizer_state_dict' in checkpoint:
                        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                    print(f"✅ Loaded PPO model from {model_path}")
                except Exception as e:
                    print(f"⚠️  Could not load model: {e}")
                    self._initialize_pretrained_weights()
            else:
                self._initialize_pretrained_weights()
        else:
            self.policy = None
    
    def _initialize_pretrained_weights(self):
        """Initialize with smart pre-trained weights for faster learning."""
        if not TORCH_AVAILABLE:
            return
        
        # Initialize with Xavier/He initialization
        for m in self.policy.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight, gain=np.sqrt(2))
                nn.init.constant_(m.bias, 0.0)
        
        print("✅ Initialized PPO model with smart weights")
    
    def choose_action(self, game_state):
        """Choose action using PPO policy."""
        if not self.player.alive:
            return (0, 0, False)
        
        # Get state representation
        state = self._get_state(game_state)
        
        if TORCH_AVAILABLE and self.policy is not None:
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            
            if self.training:
                # Sample from policy
                action_idx, action_log_prob = self.policy.act(state_tensor)
                # Store for training
                self.memory.states.append(state)
                self.memory.actions.append(action_idx)
                self.memory.log_probs.append(action_log_prob.item())
            else:
                # Greedy action selection
                with torch.no_grad():
                    action_probs, _ = self.policy(state_tensor)
                    action_idx = action_probs.argmax().item()
            
            return self.actions[action_idx]
        else:
            # Fallback to heuristic
            return self._heuristic_action(game_state, state)
    
    def _get_state(self, game_state):
        """
        Enhanced state representation inspired by Bomberland.
        
        Features:
        - Grid (169 values)
        - Player position (2)
        - Enemy position (2)
        - Player velocity/direction (2)
        - Bomb availability (2)
        - Nearest bomb info (3)
        - Danger zones (4)
        - Power-up locations (3)
        - Game progress (2)
        """
        state = []
        
        # 1. Grid representation (169 values)
        for row in game_state.grid:
            state.extend(row)
        
        # 2. Player position (normalized)
        state.append(self.player.grid_x / 13.0)
        state.append(self.player.grid_y / 13.0)
        
        # 3. Enemy position
        enemy = self._find_enemy(game_state)
        if enemy:
            state.append(enemy.grid_x / 13.0)
            state.append(enemy.grid_y / 13.0)
        else:
            state.extend([0.5, 0.5])
        
        # 4. Player direction (one-hot-ish)
        direction_map = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
        dir_idx = direction_map.get(self.player.direction, 0)
        state.append(dir_idx / 3.0)
        state.append(self.player.speed / 10.0)
        
        # 5. Bomb availability
        state.append(self.player.active_bombs / max(self.player.max_bombs, 1))
        state.append(1.0 if self.player.can_place_bomb() else 0.0)
        
        # 6. Nearest bomb information
        nearest_bomb = self._get_nearest_bomb_info(game_state)
        state.extend(nearest_bomb)  # [distance, timer, in_range]
        
        # 7. Danger zones (4 directions)
        danger_dirs = self._get_danger_directions(game_state)
        state.extend(danger_dirs)
        
        # 8. Power-up information
        powerup_info = self._get_powerup_info(game_state)
        state.extend(powerup_info)  # [count, nearest_dist, type]
        
        # 9. Game progress
        state.append(len(game_state.bombs) / 10.0)
        walls_destroyed = 1.0 - (sum(row.count(2) for row in game_state.grid) / 50.0)
        state.append(walls_destroyed)
        
        return np.array(state, dtype=np.float32)
    
    def _get_nearest_bomb_info(self, game_state):
        """Get information about nearest bomb."""
        px, py = self.player.grid_x, self.player.grid_y
        min_dist = 999
        bomb_timer = 0
        in_range = 0
        
        for bomb in game_state.bombs:
            dist = abs(px - bomb.grid_x) + abs(py - bomb.grid_y)
            if dist < min_dist:
                min_dist = dist
                bomb_timer = bomb.timer
                # Check if player is in blast range
                bx, by = bomb.grid_x, bomb.grid_y
                if (px == bx and abs(py - by) <= bomb.bomb_range) or \
                   (py == by and abs(px - bx) <= bomb.bomb_range):
                    in_range = 1
        
        return [
            min(min_dist / 13.0, 1.0),
            bomb_timer / 3.0 if bomb_timer > 0 else 0,
            float(in_range)
        ]
    
    def _get_danger_directions(self, game_state):
        """Check danger in 4 directions."""
        px, py = self.player.grid_x, self.player.grid_y
        dangers = [0, 0, 0, 0]  # up, down, left, right
        
        for bomb in game_state.bombs:
            if bomb.timer < 1.5:
                bx, by = bomb.grid_x, bomb.grid_y
                # Check each direction
                if px == bx:
                    if py > by and py - by <= bomb.bomb_range:
                        dangers[0] = 1  # up
                    elif py < by and by - py <= bomb.bomb_range:
                        dangers[1] = 1  # down
                if py == by:
                    if px > bx and px - bx <= bomb.bomb_range:
                        dangers[2] = 1  # left
                    elif px < bx and bx - px <= bomb.bomb_range:
                        dangers[3] = 1  # right
        
        return dangers
    
    def _get_powerup_info(self, game_state):
        """Get power-up information."""
        px, py = self.player.grid_x, self.player.grid_y
        count = len(game_state.powerups)
        
        if count > 0:
            nearest = min(game_state.powerups, 
                         key=lambda p: abs(px - p.grid_x) + abs(py - p.grid_y))
            dist = abs(px - nearest.grid_x) + abs(py - nearest.grid_y)
            return [count / 10.0, min(dist / 13.0, 1.0), nearest.powerup_type / 2.0]
        
        return [0, 1.0, 0]
    
    def store_reward(self, reward, done):
        """Store reward for PPO training."""
        if self.training and TORCH_AVAILABLE:
            self.memory.rewards.append(reward)
            self.memory.is_terminals.append(done)
    
    def update(self):
        """Update policy using PPO."""
        if not self.training or not TORCH_AVAILABLE or len(self.memory.states) < self.batch_size:
            return
        
        # Convert to tensors
        old_states = torch.FloatTensor(np.array(self.memory.states)).to(self.device)
        old_actions = torch.LongTensor(self.memory.actions).to(self.device)
        old_log_probs = torch.FloatTensor(self.memory.log_probs).to(self.device)
        
        # Calculate returns and advantages using GAE
        returns, advantages = self._calculate_gae(self.memory.rewards, 
                                                   self.memory.is_terminals,
                                                   old_states)
        
        # PPO update for multiple epochs
        for _ in range(self.epochs):
            # Evaluate old actions
            log_probs, state_values, dist_entropy = self.policy.evaluate(old_states, old_actions)
            
            # Calculate ratios
            ratios = torch.exp(log_probs - old_log_probs.detach())
            
            # Calculate surrogate losses
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
            
            # Calculate losses
            actor_loss = -torch.min(surr1, surr2).mean()
            critic_loss = 0.5 * (returns - state_values).pow(2).mean()
            entropy_loss = -dist_entropy.mean()
            
            # Total loss
            loss = actor_loss + self.c1 * critic_loss + self.c2 * entropy_loss
            
            # Update
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
            self.optimizer.step()
        
        # Clear memory
        self.memory.clear()
    
    def _calculate_gae(self, rewards, is_terminals, states):
        """Calculate Generalized Advantage Estimation."""
        returns = []
        advantages = []
        gae = 0
        
        # Get values
        with torch.no_grad():
            _, values = self.policy(states)
            values = values.squeeze().cpu().numpy()
        
        # Calculate GAE
        next_value = 0
        for t in reversed(range(len(rewards))):
            if is_terminals[t]:
                next_value = 0
                gae = 0
            
            delta = rewards[t] + self.gamma * next_value - values[t]
            gae = delta + self.gamma * self.gae_lambda * gae
            
            returns.insert(0, gae + values[t])
            advantages.insert(0, gae)
            next_value = values[t]
        
        # Normalize advantages
        advantages = torch.FloatTensor(advantages).to(self.device)
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        returns = torch.FloatTensor(returns).to(self.device)
        
        return returns, advantages
    
    def save_model(self, path):
        """Save model with optimizer state."""
        if TORCH_AVAILABLE:
            torch.save({
                'model_state_dict': self.policy.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
            }, path)
            print(f"✅ PPO model saved to {path}")
    
    def load_model(self, path):
        """Load model with optimizer state."""
        if TORCH_AVAILABLE:
            try:
                checkpoint = torch.load(path, map_location=self.device)
                self.policy.load_state_dict(checkpoint['model_state_dict'])
                if self.training and 'optimizer_state_dict' in checkpoint:
                    self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                print(f"✅ PPO model loaded from {path}")
            except Exception as e:
                print(f"⚠️  Could not load model: {e}")
    
    # Heuristic fallback methods
    def _heuristic_action(self, game_state, state):
        """Fallback heuristic."""
        if self._in_danger(game_state):
            return self._find_safe_move(game_state)
        
        enemy = self._find_enemy(game_state)
        if enemy and self._near_enemy(game_state, enemy):
            if self.player.can_place_bomb() and random.random() < 0.8:
                return (0, 0, True)
        
        if enemy:
            return self._move_toward_enemy(game_state, enemy)
        
        return self._random_move(game_state)
    
    def _find_enemy(self, game_state):
        for player in game_state.players:
            if player != self.player and player.alive:
                return player
        return None
    
    def _in_danger(self, game_state):
        px, py = self.player.grid_x, self.player.grid_y
        for explosion in game_state.explosions:
            if explosion.grid_x == px and explosion.grid_y == py:
                return True
        for bomb in game_state.bombs:
            if bomb.timer < 1.5:
                bx, by = bomb.grid_x, bomb.grid_y
                if (px == bx and abs(py - by) <= bomb.bomb_range) or \
                   (py == by and abs(px - bx) <= bomb.bomb_range):
                    return True
        return False
    
    def _find_safe_move(self, game_state):
        px, py = self.player.grid_x, self.player.grid_y
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = px + dx, py + dy
            if game_state.is_walkable(nx, ny):
                safe = True
                for bomb in game_state.bombs:
                    bx, by = bomb.grid_x, bomb.grid_y
                    if (nx == bx and abs(ny - by) <= bomb.bomb_range) or \
                       (ny == by and abs(nx - bx) <= bomb.bomb_range):
                        safe = False
                        break
                if safe:
                    return (dx, dy, False)
        return (0, 0, False)
    
    def _near_enemy(self, game_state, enemy):
        px, py = self.player.grid_x, self.player.grid_y
        tx, ty = enemy.grid_x, enemy.grid_y
        return abs(px - tx) + abs(py - ty) <= 3
    
    def _move_toward_enemy(self, game_state, enemy):
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
        px, py = self.player.grid_x, self.player.grid_y
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            if game_state.is_walkable(px + dx, py + dy):
                return (dx, dy, False)
        return (0, 0, False)


class PPOMemory:
    """Memory buffer for PPO."""
    
    def __init__(self):
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.is_terminals = []
    
    def clear(self):
        self.states.clear()
        self.actions.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.is_terminals.clear()
