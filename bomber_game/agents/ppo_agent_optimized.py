"""
CPU-Optimized PPO Agent for Bomberman
Improvements:
- Vectorized operations for faster CPU computation
- Mini-batch training with shuffling
- Optimized network architecture
- Better memory management
- Adaptive learning rate
- Early stopping for efficiency
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
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available. Optimized PPO agent will use fallback heuristics.")


class OptimizedActorCritic(nn.Module):
    """
    Optimized Actor-Critic network for CPU training.
    
    Improvements:
    - Smaller network (faster forward pass)
    - Batch normalization for faster convergence
    - Shared backbone with separate heads
    - Efficient activation functions
    """
    
    def __init__(self, state_size, action_size, hidden_size=128):
        super(OptimizedActorCritic, self).__init__()
        
        # Shared feature extraction (smaller for CPU efficiency)
        self.shared = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.LayerNorm(hidden_size),  # Faster than BatchNorm for small batches
            nn.Tanh(),  # Faster than ReLU on some CPUs
            nn.Linear(hidden_size, hidden_size // 2),
            nn.LayerNorm(hidden_size // 2),
            nn.Tanh(),
        )
        
        # Actor head (policy) - simplified
        self.actor = nn.Linear(hidden_size // 2, action_size)
        
        # Critic head (value function) - simplified
        self.critic = nn.Linear(hidden_size // 2, 1)
        
        # Initialize weights for faster convergence
        self._initialize_weights()
        
    def _initialize_weights(self):
        """Initialize weights with orthogonal initialization."""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.orthogonal_(m.weight, gain=np.sqrt(2))
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0.0)
    
    def forward(self, state):
        """Forward pass through network."""
        features = self.shared(state)
        action_logits = self.actor(features)
        action_probs = F.softmax(action_logits, dim=-1)
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


class RolloutBuffer:
    """
    Efficient rollout buffer for PPO.
    Stores experiences and provides mini-batches for training.
    """
    
    def __init__(self, buffer_size=2048):
        self.buffer_size = buffer_size
        self.clear()
    
    def clear(self):
        """Clear all stored experiences."""
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.values = []
        self.is_terminals = []
        self.ptr = 0
    
    def store(self, state, action, log_prob, reward, value, done):
        """Store a single experience."""
        self.states.append(state)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.values.append(value)
        self.is_terminals.append(done)
        self.ptr += 1
    
    def get(self):
        """Get all experiences as numpy arrays."""
        return {
            'states': np.array(self.states, dtype=np.float32),
            'actions': np.array(self.actions, dtype=np.int64),
            'log_probs': np.array(self.log_probs, dtype=np.float32),
            'rewards': np.array(self.rewards, dtype=np.float32),
            'values': np.array(self.values, dtype=np.float32),
            'is_terminals': np.array(self.is_terminals, dtype=np.float32)
        }
    
    def size(self):
        """Get current buffer size."""
        return len(self.states)
    
    def is_full(self):
        """Check if buffer is full."""
        return self.size() >= self.buffer_size


class OptimizedPPOAgent(Agent):
    """
    CPU-Optimized PPO Agent with advanced features:
    - Vectorized operations
    - Mini-batch training
    - Adaptive learning rate
    - Early stopping
    - Better sample efficiency
    """
    
    def __init__(self, player, model_path=None, training=False):
        super().__init__(player)
        self.training = training
        self.think_delay = 0.05
        
        # Action space
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
        
        # State representation
        self.state_size = 13 * 13 + 20
        self.action_size = len(self.actions)
        
        # Optimized PPO hyperparameters for CPU
        self.gamma = 0.99
        self.gae_lambda = 0.95
        self.clip_epsilon = 0.2
        self.c1 = 0.5  # Value loss coefficient
        self.c2 = 0.01  # Entropy coefficient
        self.initial_lr = 3e-4
        self.min_lr = 1e-5
        self.lr_decay = 0.995  # Decay learning rate over time
        
        # Training parameters optimized for CPU
        self.epochs = 4  # Reduced from 10 for faster training
        self.mini_batch_size = 64  # Process in smaller chunks
        self.buffer_size = 2048  # Collect experiences before update
        self.max_grad_norm = 0.5
        
        # Early stopping
        self.target_kl = 0.02  # Stop if KL divergence too high
        
        # Rollout buffer
        self.buffer = RolloutBuffer(self.buffer_size)
        
        # Statistics
        self.update_count = 0
        
        # Initialize model
        if TORCH_AVAILABLE:
            # Force CPU for consistency
            self.device = torch.device("cpu")
            
            # Smaller network for faster CPU computation
            self.policy = OptimizedActorCritic(
                self.state_size, 
                self.action_size,
                hidden_size=128  # Reduced from 256
            ).to(self.device)
            
            # Optimizer with adaptive learning rate
            self.optimizer = optim.Adam(
                self.policy.parameters(), 
                lr=self.initial_lr,
                eps=1e-5
            )
            
            # Learning rate scheduler
            self.scheduler = optim.lr_scheduler.ExponentialLR(
                self.optimizer,
                gamma=self.lr_decay
            )
            
            # Load pre-trained weights if available
            if model_path:
                try:
                    checkpoint = torch.load(model_path, map_location=self.device)
                    self.policy.load_state_dict(checkpoint['model_state_dict'])
                    if training and 'optimizer_state_dict' in checkpoint:
                        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                    if 'update_count' in checkpoint:
                        self.update_count = checkpoint['update_count']
                    print(f"✅ Loaded optimized PPO model from {model_path}")
                except Exception as e:
                    print(f"⚠️  Could not load model: {e}")
            
            # Set to training/eval mode
            if training:
                self.policy.train()
            else:
                self.policy.eval()
        else:
            self.policy = None
    
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
                with torch.no_grad():
                    action_idx, action_log_prob = self.policy.act(state_tensor)
                    _, value = self.policy(state_tensor)
                
                # Store for training (will add reward later)
                self.current_state = state
                self.current_action = action_idx
                self.current_log_prob = action_log_prob.item()
                self.current_value = value.item()
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
        """Enhanced state representation."""
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
        
        # 4. Player direction
        direction_map = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
        dir_idx = direction_map.get(self.player.direction, 0)
        state.append(dir_idx / 3.0)
        state.append(self.player.speed / 10.0)
        
        # 5. Bomb availability
        state.append(self.player.active_bombs / max(self.player.max_bombs, 1))
        state.append(1.0 if self.player.can_place_bomb() else 0.0)
        
        # 6. Nearest bomb information
        nearest_bomb = self._get_nearest_bomb_info(game_state)
        state.extend(nearest_bomb)
        
        # 7. Danger zones
        danger_dirs = self._get_danger_directions(game_state)
        state.extend(danger_dirs)
        
        # 8. Power-up information
        powerup_info = self._get_powerup_info(game_state)
        state.extend(powerup_info)
        
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
        dangers = [0, 0, 0, 0]
        
        for bomb in game_state.bombs:
            if bomb.timer < 1.5:
                bx, by = bomb.grid_x, bomb.grid_y
                if px == bx:
                    if py > by and py - by <= bomb.bomb_range:
                        dangers[0] = 1
                    elif py < by and by - py <= bomb.bomb_range:
                        dangers[1] = 1
                if py == by:
                    if px > bx and px - bx <= bomb.bomb_range:
                        dangers[2] = 1
                    elif px < bx and bx - px <= bomb.bomb_range:
                        dangers[3] = 1
        
        return dangers
    
    def _get_powerup_info(self, game_state):
        """Get power-up information."""
        px, py = self.player.grid_x, self.player.grid_y
        count = len(game_state.powerups)
        
        if count > 0:
            nearest_pos = min(game_state.powerups.keys(), 
                             key=lambda pos: abs(px - pos[0]) + abs(py - pos[1]))
            nearest_powerup = game_state.powerups[nearest_pos]
            dist = abs(px - nearest_pos[0]) + abs(py - nearest_pos[1])
            powerup_type = nearest_powerup.powerup_type if hasattr(nearest_powerup, 'powerup_type') else 0
            return [count / 10.0, min(dist / 13.0, 1.0), powerup_type / 2.0]
        
        return [0, 1.0, 0]
    
    def update(self, dt, game_state):
        """Update agent and execute actions."""
        self.think_timer += dt
        
        if self.think_timer >= self.think_delay:
            self.think_timer = 0
            self.current_action = self.choose_action(game_state)
        
        return self.current_action
    
    def store_reward(self, reward, done):
        """Store reward for PPO training."""
        if self.training and TORCH_AVAILABLE and hasattr(self, 'current_state'):
            self.buffer.store(
                self.current_state,
                self.current_action,
                self.current_log_prob,
                reward,
                self.current_value,
                done
            )
    
    def update_policy(self):
        """
        Update policy using PPO with CPU optimizations.
        
        Improvements:
        - Mini-batch training
        - Early stopping based on KL divergence
        - Vectorized advantage calculation
        - Gradient clipping
        """
        if not self.training or not TORCH_AVAILABLE or self.buffer.size() < self.mini_batch_size:
            return
        
        # Get all experiences
        data = self.buffer.get()
        
        # Convert to tensors (vectorized)
        states = torch.FloatTensor(data['states']).to(self.device)
        actions = torch.LongTensor(data['actions']).to(self.device)
        old_log_probs = torch.FloatTensor(data['log_probs']).to(self.device)
        rewards = data['rewards']
        values = data['values']
        dones = data['is_terminals']
        
        # Calculate returns and advantages using GAE (vectorized)
        returns, advantages = self._calculate_gae_vectorized(rewards, values, dones)
        returns = torch.FloatTensor(returns).to(self.device)
        advantages = torch.FloatTensor(advantages).to(self.device)
        
        # Normalize advantages for stability
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # Mini-batch training
        batch_size = self.buffer.size()
        indices = np.arange(batch_size)
        
        for epoch in range(self.epochs):
            # Shuffle indices for mini-batches
            np.random.shuffle(indices)
            
            epoch_kl = 0
            epoch_batches = 0
            
            # Process mini-batches
            for start_idx in range(0, batch_size, self.mini_batch_size):
                end_idx = min(start_idx + self.mini_batch_size, batch_size)
                batch_indices = indices[start_idx:end_idx]
                
                # Get mini-batch
                batch_states = states[batch_indices]
                batch_actions = actions[batch_indices]
                batch_old_log_probs = old_log_probs[batch_indices]
                batch_returns = returns[batch_indices]
                batch_advantages = advantages[batch_indices]
                
                # Evaluate actions
                log_probs, state_values, dist_entropy = self.policy.evaluate(
                    batch_states, batch_actions
                )
                
                # Calculate ratios
                ratios = torch.exp(log_probs - batch_old_log_probs)
                
                # Calculate KL divergence for early stopping
                with torch.no_grad():
                    kl = (batch_old_log_probs - log_probs).mean()
                    epoch_kl += kl.item()
                    epoch_batches += 1
                
                # Calculate surrogate losses
                surr1 = ratios * batch_advantages
                surr2 = torch.clamp(ratios, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * batch_advantages
                
                # Calculate losses
                actor_loss = -torch.min(surr1, surr2).mean()
                critic_loss = F.mse_loss(state_values.squeeze(), batch_returns)
                entropy_loss = -dist_entropy.mean()
                
                # Total loss
                loss = actor_loss + self.c1 * critic_loss + self.c2 * entropy_loss
                
                # Update
                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
                self.optimizer.step()
            
            # Early stopping if KL divergence too high
            avg_kl = epoch_kl / epoch_batches if epoch_batches > 0 else 0
            if avg_kl > self.target_kl:
                print(f"  ⚠️  Early stopping at epoch {epoch + 1}/{self.epochs} (KL={avg_kl:.4f})")
                break
        
        # Update learning rate
        self.scheduler.step()
        self.update_count += 1
        
        # Clear buffer
        self.buffer.clear()
    
    def _calculate_gae_vectorized(self, rewards, values, dones):
        """
        Calculate Generalized Advantage Estimation (vectorized for speed).
        
        Args:
            rewards: Array of rewards
            values: Array of value estimates
            dones: Array of done flags
            
        Returns:
            returns: Array of returns
            advantages: Array of advantages
        """
        advantages = np.zeros_like(rewards, dtype=np.float32)
        returns = np.zeros_like(rewards, dtype=np.float32)
        
        gae = 0
        next_value = 0
        
        # Calculate GAE backwards
        for t in reversed(range(len(rewards))):
            if dones[t]:
                next_value = 0
                gae = 0
            
            delta = rewards[t] + self.gamma * next_value - values[t]
            gae = delta + self.gamma * self.gae_lambda * gae
            
            advantages[t] = gae
            returns[t] = gae + values[t]
            next_value = values[t]
        
        return returns, advantages
    
    def save_model(self, path):
        """Save model with optimizer state and training progress."""
        if TORCH_AVAILABLE:
            torch.save({
                'model_state_dict': self.policy.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'update_count': self.update_count,
                'scheduler_state_dict': self.scheduler.state_dict(),
            }, path)
            print(f"✅ Optimized PPO model saved to {path}")
    
    def load_model(self, path):
        """Load model with optimizer state."""
        if TORCH_AVAILABLE:
            try:
                checkpoint = torch.load(path, map_location=self.device)
                self.policy.load_state_dict(checkpoint['model_state_dict'])
                if self.training:
                    if 'optimizer_state_dict' in checkpoint:
                        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                    if 'scheduler_state_dict' in checkpoint:
                        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
                    if 'update_count' in checkpoint:
                        self.update_count = checkpoint['update_count']
                print(f"✅ Optimized PPO model loaded from {path}")
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
