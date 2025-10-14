# Reinforcement Learning Improvements Roadmap for Proutman

**Based on**: "Intelligent Bomberman with Reinforcement Learning" (Ngo Hung Minh Triet, 2021)

## Executive Summary

This document outlines a **systematic approach** to enhance Proutman's RL capabilities based on proven research. The paper demonstrates that **SARSA with 5-tiles state representation** achieved 53% win rate in competitive 4-player tests, significantly outperforming other methods.

### Key Research Findings Applied

| Finding | Current Proutman | Proposed Improvement |
|---------|------------------|---------------------|
| SARSA > Q-Learning for Bomberman | Only PPO/Q-Learning | Add SARSA implementation |
| 5-tiles state >> Complete state | Full grid observation | Add limited vision mode |
| Reward engineering critical | Basic rewards | Research-based rewards |
| DQN needs CNN layers | Simple MLP | Add convolutional layers |
| Double Q-Learning reduces bias | Single Q-value | Add Double Q-Learning |

---

## Phase 1: State Representation Improvements
**Priority: HIGH** | **Complexity: MEDIUM** | **Impact: HIGH**

### 1.1 Implement 5-Tiles State Representation

**Research Finding**: 5-tiles representation reduced state space from 10^49 to 10^9 and achieved best results.

**Current State**:
- Proutman uses full grid observation (13x11 = 143 tiles)
- State includes complete game information
- Large state space slows learning

**Proposed Implementation**:

```python
# State components (5 tiles):
state = {
    'current_tile': tile_info(player.x, player.y),     # Player position
    'north_tile': tile_info(player.x, player.y - 1),   # Adjacent tiles
    'east_tile': tile_info(player.x + 1, player.y),
    'south_tile': tile_info(player.x, player.y + 1),
    'west_tile': tile_info(player.x - 1, player.y),
    'nearest_enemy_vector': (dx, dy, manhattan_dist)   # Relative enemy position
}

# Each tile_info includes:
- Tile type: Free(0), Breakable(1), Obstacle(-1)
- Explosion countdown: 0-8 normalized to [0, 1]
- Contains powerup: boolean
```

**Benefits**:
- ✅ Reduces state space by ~1000x
- ✅ Faster learning convergence
- ✅ Better generalization
- ✅ Research-proven effectiveness

**Implementation Steps**:
1. Create `LimitedVisionStateEncoder` class
2. Add Manhattan distance calculation for nearest enemy
3. Normalize tile information to [0, 1] range
4. Add configuration option for state representation type
5. Benchmark against full-grid representation

**Estimated Effort**: 4-6 hours

---

### 1.2 Enhanced State Encoding with Spatial Features

**Research Finding**: DQN suffered from flattening spatial features; CNN layers preserve them.

**Current State**:
- Flattened state vector loses spatial relationships
- No preservation of grid structure

**Proposed Implementation**:

```python
# For CNN-based agents:
state_channels = [
    grid_layer,          # Walls and free spaces
    bomb_layer,          # Bomb positions and countdowns
    explosion_layer,     # Active explosions
    player_layer,        # Player positions
    powerup_layer        # Powerup positions
]
# Shape: (5, 13, 11) - 5 channels, 13x11 grid
```

**Benefits**:
- ✅ Preserves spatial relationships
- ✅ Enables CNN feature extraction
- ✅ Better for DQN/PPO with CNN

**Implementation Steps**:
1. Create `SpatialStateEncoder` class
2. Implement multi-channel grid representation
3. Add data augmentation (rotation/flip for generalization)
4. Integrate with CNN-based agents

**Estimated Effort**: 6-8 hours

---

## Phase 2: RL Algorithm Enhancements
**Priority: HIGH** | **Complexity: HIGH** | **Impact: VERY HIGH**

### 2.1 Implement SARSA Algorithm

**Research Finding**: SARSA with 5-tiles achieved 53% win rate, best overall performance.

**Why SARSA for Bomberman**:
- **On-policy learning**: More conservative, safer strategies
- **Better for safety-critical domains**: Avoids risky exploration
- **Proven results**: 90% win rate vs random, 53% in 4-player competitive

**Current State**:
- Only PPO (policy gradient) available
- No SARSA implementation

**Proposed Implementation**:

```python
class SARSAAgent:
    def __init__(self, state_encoder='5-tiles', alpha=0.001, gamma=0.99):
        self.Q = defaultdict(lambda: np.zeros(6))  # 6 actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = 0.1  # Exploration rate
    
    def update(self, s, a, r, s_next, a_next):
        """SARSA update: Q(s,a) ← Q(s,a) + α[r + γQ(s',a') - Q(s,a)]"""
        current_q = self.Q[s][a]
        next_q = self.Q[s_next][a_next]
        td_error = r + self.gamma * next_q - current_q
        self.Q[s][a] += self.alpha * td_error
```

**Implementation Steps**:
1. Create `SARSAAgent` class in `bomber_game/agents/sarsa_agent.py`
2. Implement epsilon-greedy policy
3. Add Q-table serialization (pickle/JSON)
4. Integrate with training pipeline
5. Add to agent selector menu
6. Benchmark against PPO

**Estimated Effort**: 8-12 hours

---

### 2.2 Implement Double Q-Learning

**Research Finding**: Reduces maximization bias, shows competitive performance.

**Current State**:
- Single Q-value estimation in Q-Learning
- Potential overestimation bias

**Proposed Implementation**:

```python
class DoubleQLearningAgent:
    def __init__(self):
        self.Q1 = defaultdict(lambda: np.zeros(6))
        self.Q2 = defaultdict(lambda: np.zeros(6))
    
    def update(self, s, a, r, s_next):
        """Randomly update Q1 or Q2"""
        if random.random() < 0.5:
            # Update Q1 using Q2's value
            a_max = np.argmax(self.Q1[s_next])
            target = r + self.gamma * self.Q2[s_next][a_max]
            self.Q1[s][a] += self.alpha * (target - self.Q1[s][a])
        else:
            # Update Q2 using Q1's value
            a_max = np.argmax(self.Q2[s_next])
            target = r + self.gamma * self.Q1[s_next][a_max]
            self.Q2[s][a] += self.alpha * (target - self.Q2[s][a])
```

**Benefits**:
- ✅ Reduces Q-value overestimation
- ✅ More stable learning
- ✅ Better long-term performance

**Implementation Steps**:
1. Create `DoubleQLearningAgent` class
2. Implement dual Q-table management
3. Add action selection using both Q-tables
4. Integrate with training pipeline

**Estimated Effort**: 6-8 hours

---

### 2.3 Enhanced DQN with Convolutional Layers

**Research Finding**: DQN with MLP suffers from flattened features; CNN layers needed.

**Current State**:
- Simple MLP architecture
- Loses spatial information

**Proposed Implementation**:

```python
class ConvDQN(nn.Module):
    def __init__(self):
        super().__init__()
        # Convolutional layers for spatial features
        self.conv = nn.Sequential(
            nn.Conv2d(5, 32, kernel_size=3, padding=1),  # 5 input channels
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        # Fully connected layers
        self.fc = nn.Sequential(
            nn.Linear(64 * 13 * 11, 512),
            nn.ReLU(),
            nn.Linear(512, 6)  # 6 actions
        )
    
    def forward(self, x):
        # x shape: (batch, 5, 13, 11)
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

**Benefits**:
- ✅ Preserves spatial relationships
- ✅ Better feature extraction
- ✅ Research shows 2.59% win rate vs 0.18% for MLP

**Implementation Steps**:
1. Create `ConvDQN` architecture
2. Modify state encoder to output spatial format
3. Update experience replay for image-like states
4. Add prioritized experience replay
5. Benchmark against current DQN

**Estimated Effort**: 10-14 hours

---

## Phase 3: Reward Function Optimization
**Priority: MEDIUM** | **Complexity: LOW** | **Impact: HIGH**

### 3.1 Research-Based Reward Engineering

**Research Finding**: Reward function critically affects learning; paper provides proven values.

**Current Rewards** (Proutman):
```python
rewards = {
    'win': +200,
    'lose': -200,
    'destroy_wall': +20,
    'collect_powerup': +15,
    'step_penalty': -0.5
}
```

**Research-Proven Rewards**:
```python
rewards = {
    'make_valid_move': -1,      # Encourage movement
    'make_invalid_move': -5,    # Penalize illegal actions
    'kill_player': +500,        # Strong incentive to win
    'die': -300,                # Strong penalty for losing
    'break_wall': +30,          # Moderate reward for progress
    'collect_powerup': +50,     # (Not in paper, but logical)
    'survive_turn': +1,         # (Additional: encourage survival)
    'approach_enemy': +5,       # (Additional: encourage aggression)
}
```

**Key Differences**:
- Higher kill/death rewards (500/-300 vs 200/-200)
- Penalty for all moves (-1) encourages efficiency
- Separate invalid move penalty (-5)
- Wall breaking aligned with research (+30)

**Implementation Steps**:
1. Create `RewardConfigurator` class
2. Implement research-based reward scheme
3. Add A/B testing framework for reward tuning
4. Log reward distributions during training
5. Compare performance with current rewards

**Estimated Effort**: 3-4 hours

---

### 3.2 Adaptive Reward Shaping

**Proposed Enhancement**: Dynamic rewards based on game phase.

```python
class AdaptiveRewardShaper:
    def calculate_reward(self, event, game_state):
        base_reward = BASE_REWARDS[event]
        
        # Early game: Encourage exploration and wall breaking
        if game_state.turn < 50:
            if event == 'break_wall':
                return base_reward * 1.5
        
        # Mid game: Encourage aggression
        elif 50 <= game_state.turn < 150:
            if event == 'approach_enemy':
                return base_reward * 2.0
        
        # Late game: Encourage survival
        else:
            if event == 'survive_turn':
                return base_reward * 3.0
        
        return base_reward
```

**Implementation Steps**:
1. Create reward shaping framework
2. Add game phase detection
3. Implement phase-specific reward multipliers
4. Evaluate impact on learning

**Estimated Effort**: 4-6 hours

---

## Phase 4: Training Enhancements
**Priority: MEDIUM** | **Complexity: MEDIUM** | **Impact: HIGH**

### 4.1 Self-Play Training

**Research Inspiration**: Paper shows competitive multi-agent training improves performance.

**Current State**:
- Training against fixed heuristic opponent
- No agent vs agent training

**Proposed Implementation**:

```python
class SelfPlayTraining:
    def __init__(self, agent_pool_size=5):
        self.agent_pool = []  # Pool of past agents
        self.current_agent = create_agent()
    
    def train_episode(self):
        # Play against random agent from pool
        opponent = random.choice(self.agent_pool) if self.agent_pool else create_heuristic_agent()
        
        # Play game
        result = play_game(self.current_agent, opponent)
        
        # Update agent
        self.current_agent.learn(result)
        
        # Periodically add current agent to pool
        if episode % 100 == 0:
            self.agent_pool.append(copy.deepcopy(self.current_agent))
            if len(self.agent_pool) > self.agent_pool_size:
                self.agent_pool.pop(0)  # Keep pool size limited
```

**Benefits**:
- ✅ Agent learns from diverse opponents
- ✅ Prevents overfitting to one strategy
- ✅ Emergent complex strategies

**Implementation Steps**:
1. Create `SelfPlayTraining` class
2. Implement agent pool management
3. Add opponent sampling strategies
4. Integrate with overnight training
5. Track Elo ratings for agent pool

**Estimated Effort**: 8-10 hours

---

### 4.2 Curriculum Learning

**Research Inspiration**: Paper starts with stationary opponent, then random, then competitive.

**Proposed Curriculum**:

```python
curriculum = [
    # Stage 1: Learn basics (100 episodes)
    {
        'opponent': 'stationary',
        'spawning_bombs': False,
        'grid_size': (7, 7),
        'goal': 'Learn movement and bomb placement'
    },
    # Stage 2: Learn dodging (200 episodes)
    {
        'opponent': 'random_mover',
        'spawning_bombs': False,
        'grid_size': (9, 9),
        'goal': 'Learn to dodge and chase'
    },
    # Stage 3: Learn competition (300 episodes)
    {
        'opponent': 'heuristic',
        'spawning_bombs': True,
        'grid_size': (11, 11),
        'goal': 'Learn full game strategy'
    },
    # Stage 4: Master level (ongoing)
    {
        'opponent': 'self_play',
        'spawning_bombs': True,
        'grid_size': (13, 11),
        'goal': 'Achieve expert performance'
    }
]
```

**Implementation Steps**:
1. Create `CurriculumTrainer` class
2. Define curriculum stages
3. Implement automatic progression criteria
4. Add curriculum visualization
5. Integrate with training pipeline

**Estimated Effort**: 6-8 hours

---

### 4.3 Experience Replay Improvements

**Research Finding**: DQN uses experience replay with batch size 16, buffer size 100K.

**Current State**:
- Basic experience replay (if any)
- No prioritization

**Proposed Enhancement**:

```python
class PrioritizedExperienceReplay:
    def __init__(self, capacity=100000, alpha=0.6, beta=0.4):
        self.capacity = capacity
        self.buffer = []
        self.priorities = np.zeros(capacity)
        self.alpha = alpha  # Priority exponent
        self.beta = beta    # Importance sampling
    
    def add(self, experience, td_error):
        priority = (abs(td_error) + 1e-5) ** self.alpha
        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
        else:
            idx = len(self.buffer) % self.capacity
            self.buffer[idx] = experience
        self.priorities[len(self.buffer) - 1] = priority
    
    def sample(self, batch_size=64):
        # Sample based on priorities
        probs = self.priorities[:len(self.buffer)]
        probs = probs / probs.sum()
        
        indices = np.random.choice(len(self.buffer), batch_size, p=probs)
        samples = [self.buffer[i] for i in indices]
        
        # Importance sampling weights
        weights = (len(self.buffer) * probs[indices]) ** (-self.beta)
        weights = weights / weights.max()
        
        return samples, weights, indices
```

**Benefits**:
- ✅ Learn from important experiences more frequently
- ✅ Faster convergence
- ✅ Better sample efficiency

**Implementation Steps**:
1. Implement `PrioritizedExperienceReplay`
2. Modify DQN agent to use prioritized replay
3. Add importance sampling weight correction
4. Tune alpha and beta parameters
5. Benchmark against uniform sampling

**Estimated Effort**: 8-10 hours

---

## Phase 5: Exploration Strategies
**Priority: LOW** | **Complexity: MEDIUM** | **Impact: MEDIUM**

### 5.1 Epsilon-Greedy Schedule

**Research Setting**: Paper uses different epsilon schedules for different algorithms.

**Current State**:
- Simple epsilon-greedy
- No scheduling

**Proposed Implementation**:

```python
class ExplorationScheduler:
    def __init__(self, initial_eps=1.0, final_eps=0.01, decay_episodes=1000):
        self.initial_eps = initial_eps
        self.final_eps = final_eps
        self.decay_episodes = decay_episodes
    
    def get_epsilon(self, episode):
        # Linear decay
        if episode < self.decay_episodes:
            return self.initial_eps - (self.initial_eps - self.final_eps) * (episode / self.decay_episodes)
        return self.final_eps
    
    def get_epsilon_exponential(self, episode, decay_rate=0.995):
        # Exponential decay
        return max(self.final_eps, self.initial_eps * (decay_rate ** episode))
```

**Research Parameters**:
- Tabular methods (SARSA, Q-Learning): ε = 0.1 (constant)
- DQN: ε = 0.5 → 0.01 (linear decay)

**Implementation Steps**:
1. Create `ExplorationScheduler` class
2. Add multiple decay strategies (linear, exponential, step)
3. Integrate with all RL agents
4. Log exploration rate during training
5. Tune decay parameters per algorithm

**Estimated Effort**: 3-4 hours

---

### 5.2 Entropy Regularization (for Policy Gradient)

**Enhancement for PPO**:

```python
class PPOWithEntropy:
    def calculate_loss(self, policy_loss, value_loss, entropy):
        total_loss = policy_loss + 0.5 * value_loss - 0.01 * entropy
        # Entropy bonus encourages exploration
        return total_loss
```

**Implementation Steps**:
1. Add entropy calculation to PPO agent
2. Add entropy coefficient to hyperparameters
3. Monitor entropy during training
4. Tune coefficient for balance

**Estimated Effort**: 2-3 hours

---

## Phase 6: Evaluation and Analysis
**Priority: MEDIUM** | **Complexity: LOW** | **Impact: MEDIUM**

### 6.1 Comprehensive Benchmark Suite

**Research Approach**: Paper uses three test types.

**Proposed Test Suite**:

```python
benchmark_tests = [
    # 1. Learnability Test (like paper)
    {
        'name': 'Basic Skills',
        'opponent': 'stationary',
        'metrics': ['avg_reward', 'walls_broken', 'survival_time'],
        'goal': 'Verify basic learning capability'
    },
    # 2. Advance Test
    {
        'name': 'Dynamic Opponent',
        'opponent': 'random',
        'metrics': ['win_rate', 'avg_reward', 'kills'],
        'goal': 'Test adaptation to moving opponent'
    },
    # 3. Competitive Test
    {
        'name': '4-Player Battle',
        'opponents': ['agent1', 'agent2', 'agent3'],
        'metrics': ['win_rate', 'ranking', 'survival_time'],
        'goal': 'Multi-agent competitive performance'
    },
    # 4. Heuristic Benchmark
    {
        'name': 'vs Improved Heuristic',
        'opponent': 'improved_heuristic',
        'metrics': ['win_rate', 'avg_reward'],
        'goal': 'Compare to hand-crafted strategy'
    }
]
```

**Implementation Steps**:
1. Create `BenchmarkSuite` class
2. Implement all test scenarios
3. Add automated reporting
4. Create visualization dashboard
5. Run weekly benchmarks

**Estimated Effort**: 6-8 hours

---

### 6.2 Performance Metrics Dashboard

**Proposed Metrics**:

```python
metrics = {
    'learning': ['win_rate_over_time', 'avg_reward_over_time', 'loss_curve'],
    'gameplay': ['walls_broken', 'powerups_collected', 'kills', 'deaths'],
    'strategy': ['bomb_placement_accuracy', 'escape_success_rate', 'aggression_score'],
    'efficiency': ['episodes_per_hour', 'convergence_speed', 'sample_efficiency']
}
```

**Implementation Steps**:
1. Create metrics collection system
2. Build interactive dashboard (Plotly/Dash)
3. Add real-time monitoring
4. Generate PDF reports

**Estimated Effort**: 8-10 hours

---

## Implementation Roadmap

### Sprint 1: Foundation (2-3 weeks)
- [ ] **Week 1**: Implement 5-tiles state representation (Phase 1.1)
- [ ] **Week 2**: Implement SARSA algorithm (Phase 2.1)
- [ ] **Week 3**: Research-based reward function (Phase 3.1)

**Deliverable**: Working SARSA agent with 5-tiles representation

---

### Sprint 2: Algorithm Diversity (2-3 weeks)
- [ ] **Week 4**: Implement Double Q-Learning (Phase 2.2)
- [ ] **Week 5**: Enhanced DQN with CNN (Phase 2.3)
- [ ] **Week 6**: Benchmark all algorithms

**Deliverable**: Three RL algorithms ready for comparison

---

### Sprint 3: Training Pipeline (2-3 weeks)
- [ ] **Week 7**: Self-play training (Phase 4.1)
- [ ] **Week 8**: Curriculum learning (Phase 4.2)
- [ ] **Week 9**: Experience replay improvements (Phase 4.3)

**Deliverable**: Advanced training pipeline

---

### Sprint 4: Refinement (1-2 weeks)
- [ ] **Week 10**: Exploration strategies (Phase 5)
- [ ] **Week 11**: Evaluation suite (Phase 6)

**Deliverable**: Complete RL system with evaluation

---

## Success Metrics

### Quantitative Goals (Based on Research)

| Metric | Current | Target (Research-Based) | Status |
|--------|---------|------------------------|--------|
| Win rate vs Random | ~30% | 90% (SARSA 5-tiles) | 🎯 Target |
| Win rate in 4-player | ~10% | 53% (SARSA 5-tiles) | 🎯 Target |
| Training time to 50% WR | 8h | 4h (with improvements) | 🎯 Target |
| State space size | Large | 10^9 (5-tiles) | 🎯 Target |

### Qualitative Goals

- ✅ Agent learns safe bomb placement
- ✅ Agent learns to dodge explosions
- ✅ Agent learns to break walls efficiently
- ✅ Agent learns to hunt opponents
- ✅ Agent balances aggression and safety

---

## File Structure for Implementation

```
bomber_game/
├── agents/
│   ├── sarsa_agent.py              # NEW: SARSA implementation
│   ├── double_q_agent.py           # NEW: Double Q-Learning
│   ├── conv_dqn_agent.py           # NEW: CNN-based DQN
│   └── ppo_agent.py                # EXISTING: Update with improvements
├── state_encoders/
│   ├── five_tiles_encoder.py       # NEW: 5-tiles representation
│   ├── spatial_encoder.py          # NEW: CNN-compatible encoding
│   └── full_grid_encoder.py        # EXISTING: Refactored
├── training/
│   ├── self_play.py                # NEW: Self-play training
│   ├── curriculum.py               # NEW: Curriculum learning
│   ├── experience_replay.py        # NEW: Prioritized replay
│   └── reward_shaper.py            # NEW: Adaptive rewards
├── evaluation/
│   ├── benchmark_suite.py          # NEW: Comprehensive benchmarks
│   ├── metrics_collector.py        # NEW: Performance tracking
│   └── dashboard.py                # NEW: Visualization
└── utils/
    ├── exploration.py              # NEW: Epsilon scheduling
    └── hyperparameter_tuner.py     # NEW: Auto-tuning
```

---

## Risk Mitigation

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SARSA doesn't converge | Medium | High | Start with research hyperparameters |
| 5-tiles loses too much info | Low | High | A/B test vs full grid |
| CNN training too slow | Medium | Medium | Use smaller networks initially |
| Self-play unstable | Medium | Medium | Keep opponent pool diverse |

### Resource Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Training time too long | Medium | High | Use GPU, optimize code |
| Memory overflow | Low | High | Limit replay buffer size |
| Implementation time exceeds estimate | High | Medium | Prioritize phases by impact |

---

## Next Steps for Windsurf

### Immediate Actions (This Session)

1. **Review this roadmap** with user
2. **Prioritize phases** based on user goals
3. **Start with Phase 1.1** (5-tiles state representation) if approved
4. **Set up development branch** for RL improvements

### Implementation Strategy

For each phase, follow this pattern:

1. **Create isolated module** (don't break existing code)
2. **Write unit tests** for new components
3. **Benchmark against baseline** (current PPO)
4. **Document results** in progress file
5. **Integrate if successful** or iterate

---

## References

- **Primary Research**: "Intelligent Bomberman with Reinforcement Learning" (Ngo Hung Minh Triet, 2021)
- **Additional**: "Developing a Successful Bomberman Agent" (Kowalczyk et al., 2021)
- **Current Proutman**: See `bomber_game/agents/` for existing implementations

---

## Appendix: Research Comparison

### Original Research Setup vs Proutman

| Aspect | Research (2021) | Proutman (Current) |
|--------|-----------------|-------------------|
| Grid Size | 7x7 | 13x11 |
| Players | 2-4 | 2 |
| Bomb Timer | 3 turns | 8 turns |
| Bomb Range | 1 tile | 3 tiles (upgradeable) |
| State Space | 10^49 (complete) | Similar |
| Best Algorithm | SARSA + 5-tiles | PPO + full grid |
| Training Episodes | 10K per generation | 1K-10K |
| Evaluation Episodes | 100 per generation | Variable |

### Why SARSA is Promising for Proutman

1. **On-policy safety**: Bomberman rewards cautious play
2. **Proven track record**: 53% win rate in competitive tests
3. **Simpler than PPO**: Easier to debug and tune
4. **Research-validated**: Multiple papers confirm effectiveness

---

**Created**: 2025-10-14  
**Status**: 📋 Proposed  
**Next Action**: Review with team and select Sprint 1 tasks
