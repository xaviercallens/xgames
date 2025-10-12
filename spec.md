# Bomberman Educational Game Specification
## Teaching Python, Machine Learning & Reinforcement Learning

---

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Educational Objectives](#educational-objectives)
3. [Game Features & Mechanics](#game-features--mechanics)
4. [Architecture Design](#architecture-design)
5. [Learning Path & Progression](#learning-path--progression)
6. [Technical Specifications](#technical-specifications)
7. [Implementation Plan](#implementation-plan)
8. [AI/ML Integration](#aiml-integration)
9. [Success Metrics](#success-metrics)

---

## 🎯 Project Overview

### Purpose
Create an educational Bomberman-inspired game that teaches:
- **Python programming fundamentals**
- **Object-oriented programming (OOP)**
- **Game development concepts**
- **Machine Learning basics**
- **Reinforcement Learning principles**
- **Multi-agent systems**

### Target Audience
- **Primary**: Students learning Python and AI (beginner to intermediate)
- **Age Range**: 12+ years old
- **Prerequisites**: Basic Python syntax knowledge

### Key Features
- Human vs AI gameplay
- Progressive difficulty levels
- Visual learning aids
- Code examples and explanations
- Step-by-step AI training process

---

## 📖 Educational Objectives

### Phase 1: Python Fundamentals (Weeks 1-2)
**Learning Goals:**
- Variables, data types, and control flow
- Functions and classes
- Lists, dictionaries, and data structures
- File I/O and modules
- Pygame basics

**Project Activities:**
- Build basic game window
- Create player movement
- Implement collision detection
- Design simple game loop

### Phase 2: Game Development (Weeks 3-4)
**Learning Goals:**
- Object-oriented design patterns
- Game state management
- Event handling
- Sprite animation
- Sound and graphics

**Project Activities:**
- Implement Bomberman character
- Create destructible walls
- Add bomb mechanics
- Power-ups system
- Scoring and lives

### Phase 3: AI Basics (Weeks 5-6)
**Learning Goals:**
- What is AI?
- Decision trees
- Pathfinding algorithms (A*)
- State machines
- Heuristics

**Project Activities:**
- Simple rule-based AI
- AI movement patterns
- Basic enemy behavior
- Difficulty scaling

### Phase 4: Machine Learning Introduction (Weeks 7-8)
**Learning Goals:**
- ML concepts and terminology
- Supervised vs unsupervised learning
- Neural networks basics
- Training and testing
- Overfitting and underfitting

**Project Activities:**
- Data collection from gameplay
- Feature engineering
- Simple ML model for move prediction
- Visualizing learning curves

### Phase 5: Reinforcement Learning (Weeks 9-12)
**Learning Goals:**
- RL framework (Agent, Environment, Reward)
- Q-Learning algorithm
- Exploration vs Exploitation
- Deep Q-Networks (DQN)
- Policy gradients

**Project Activities:**
- Implement Q-Learning agent
- Design reward function
- Train agent to play Bomberman
- Compare different RL algorithms
- Visualize agent learning process

---

## 🎮 Game Features & Mechanics

### Core Gameplay
1. **Grid-based World** (13x13 or 15x15)
2. **Player Character** - Bomberman with 4-directional movement
3. **Bombs** - Placeable explosives with timed detonation
4. **Destructible Walls** - Soft blocks that can be destroyed
5. **Indestructible Walls** - Hard blocks that cannot be destroyed
6. **Power-ups** - Hidden under soft blocks

### Power-ups
- **Bomb Up** - Increase max bombs
- **Fire Up** - Increase explosion range
- **Speed Up** - Increase movement speed
- **Invincibility** - Temporary invulnerability (advanced)
- **Remote Detonator** - Manually trigger bombs (advanced)

### Game Modes

#### 1. Tutorial Mode
- Step-by-step instructions
- Guided gameplay
- Explains each mechanic
- No AI opponent

#### 2. Practice Mode
- Player vs Simple AI
- Adjustable difficulty
- No time limit
- Focus on learning

#### 3. Challenge Mode
- Player vs Advanced AI
- Multiple difficulty levels
- Leaderboard
- Achievements

#### 4. Training Mode
- Watch AI train in real-time
- Visualize learning process
- Adjust hyperparameters
- Export trained models

#### 5. Custom Mode
- Load custom AI agents
- Adjust game rules
- Create custom maps
- Experiment freely

### Win Conditions
- **Elimination**: Defeat all enemies
- **Time-based**: Highest score when time runs out
- **Survival**: Last player standing

---

## 🏗️ Architecture Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Game Application                   │
├─────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────────────────┐  │
│  │  Game Engine  │  │     AI Framework          │  │
│  │  (Pygame)     │  │  (RL/ML Components)       │  │
│  └───────────────┘  └───────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────────────────┐  │
│  │  Game Logic   │  │    Agent System           │  │
│  │  - Physics    │  │  - Rule-based AI          │  │
│  │  - Collision  │  │  - ML Agent               │  │
│  │  - Rules      │  │  - RL Agent (Q-Learning)  │  │
│  └───────────────┘  └───────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────────────────┐  │
│  │  Rendering    │  │    Data/Analytics         │  │
│  │  - Graphics   │  │  - Logging                │  │
│  │  - UI         │  │  - Metrics                │  │
│  │  - Animation  │  │  - Visualization          │  │
│  └───────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Game Engine Layer
```python
class GameEngine:
    - pygame initialization
    - main game loop
    - FPS control
    - event handling
    - state management
```

#### 2. Game State
```python
class GameState:
    - grid/map representation
    - player positions
    - bomb locations
    - wall states
    - power-up locations
    - scores and lives
```

#### 3. Entity System
```python
class Entity (Base Class):
    - position
    - sprite
    - collision box
    
class Player(Entity):
    - movement
    - bomb placement
    - power-ups inventory
    
class Bomb(Entity):
    - timer
    - explosion range
    - detonation logic
    
class PowerUp(Entity):
    - type
    - effect
```

#### 4. AI Agent Interface
```python
class Agent (Abstract Base Class):
    - observe(game_state) -> observation
    - act(observation) -> action
    - learn(experience) -> None
    
class RuleBasedAgent(Agent):
    - simple heuristics
    - predefined strategies
    
class MLAgent(Agent):
    - neural network
    - decision making
    
class RLAgent(Agent):
    - Q-table or Q-network
    - exploration strategy
    - reward function
    - learning algorithm
```

#### 5. Reinforcement Learning Framework
```python
class RLEnvironment:
    - reset() -> initial_state
    - step(action) -> (next_state, reward, done, info)
    - render() -> None
    
class ReplayBuffer:
    - store experiences
    - sample batches
    
class RewardFunction:
    - calculate_reward(state, action, next_state)
    - reward shaping
```

---

## 📈 Learning Path & Progression

### Week-by-Week Breakdown

#### **Week 1-2: Python Basics & Game Setup**
**Objectives:**
- Set up development environment
- Learn Pygame basics
- Create game window and basic rendering

**Deliverables:**
- Working game window
- Player sprite on screen
- Basic keyboard input

**Teaching Materials:**
- Python syntax guide
- Pygame tutorial
- Code comments explaining every line

---

#### **Week 3-4: Game Mechanics**
**Objectives:**
- Implement core Bomberman gameplay
- Learn collision detection
- Understand game loops

**Deliverables:**
- Player movement (4 directions)
- Bomb placement and explosion
- Wall destruction
- Basic map layout

**Code Example:**
```python
class Player:
    def move(self, direction):
        # Move player if valid
        new_x, new_y = self.get_new_position(direction)
        if self.is_valid_move(new_x, new_y):
            self.x, self.y = new_x, new_y
```

---

#### **Week 5-6: Rule-Based AI**
**Objectives:**
- Understand AI decision-making
- Implement simple AI opponent
- Learn pathfinding basics

**Deliverables:**
- AI that moves randomly
- AI that avoids bombs
- AI that seeks player
- A* pathfinding algorithm

**Teaching Concepts:**
- State representation
- Action selection
- Heuristics and scoring

---

#### **Week 7-8: Introduction to ML**
**Objectives:**
- Understand ML concepts
- Collect training data
- Build simple neural network

**Deliverables:**
- Data collection system
- Feature extraction
- Simple supervised learning model
- Prediction visualization

**Libraries Introduced:**
- NumPy
- Pandas
- scikit-learn (optional)
- Matplotlib

---

#### **Week 9-10: Q-Learning Basics**
**Objectives:**
- Understand RL framework
- Implement tabular Q-Learning
- Understand rewards and penalties

**Deliverables:**
- Q-table implementation
- Simple Q-Learning agent
- Reward function design
- Training visualization

**Key Concepts:**
```python
# Q-Learning Update Rule
Q(s, a) = Q(s, a) + α * [r + γ * max(Q(s', a')) - Q(s, a)]

Where:
- s = current state
- a = action taken
- r = reward received
- s' = next state
- α = learning rate
- γ = discount factor
```

---

#### **Week 11-12: Deep Q-Learning (DQN)**
**Objectives:**
- Understand deep learning basics
- Implement DQN
- Compare with Q-Learning

**Deliverables:**
- Neural network Q-function
- Experience replay buffer
- Target network
- Trained DQN agent

**Libraries Introduced:**
- TensorFlow or PyTorch
- OpenAI Gym wrapper

---

## 🔧 Technical Specifications

### System Requirements
- **Python**: 3.8+
- **OS**: Windows, macOS, Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB

### Dependencies
```python
# Core Game
pygame >= 2.5.0
numpy >= 1.24.0
pillow >= 10.0.0

# Machine Learning
tensorflow >= 2.15.0  # or pytorch >= 2.0.0
scikit-learn >= 1.3.0
pandas >= 2.0.0

# Visualization
matplotlib >= 3.7.0
seaborn >= 0.12.0

# Utilities
tqdm >= 4.65.0  # Progress bars
tensorboard >= 2.15.0  # Training visualization
```

### Game Configuration
```yaml
# config.yaml
game:
  grid_size: 13
  tile_size: 32
  fps: 30
  bomb_timer: 3.0  # seconds
  explosion_duration: 0.5  # seconds

player:
  speed: 4  # tiles per second
  initial_bombs: 1
  initial_range: 1

ai:
  difficulty: "medium"  # easy, medium, hard
  reaction_time: 0.5  # seconds

reinforcement_learning:
  learning_rate: 0.001
  discount_factor: 0.99
  epsilon_start: 1.0
  epsilon_end: 0.01
  epsilon_decay: 0.995
  batch_size: 32
  memory_size: 10000
```

### State Representation

#### For Simple AI (Grid-based)
```python
state = {
    'grid': 13x13 array,  # Wall types
    'player_pos': (x, y),
    'ai_pos': (x, y),
    'bombs': [(x, y, timer), ...],
    'power_ups': [(x, y, type), ...],
}
```

#### For ML/RL (Feature Vector)
```python
features = [
    # Position features (2)
    player_x, player_y,
    
    # Danger features (4)
    danger_up, danger_down, danger_left, danger_right,
    
    # Enemy features (2)
    enemy_distance, enemy_angle,
    
    # Power-up features (2)
    nearest_powerup_distance, nearest_powerup_angle,
    
    # Bomb features (3)
    bombs_available, bomb_range, bombs_nearby,
    
    # Grid features (variable)
    # One-hot encoded nearby tiles
]
```

### Action Space
```python
actions = {
    0: "NO_OP",       # Do nothing
    1: "UP",          # Move up
    2: "DOWN",        # Move down
    3: "LEFT",        # Move left
    4: "RIGHT",       # Move right
    5: "PLACE_BOMB",  # Place bomb
}
```

### Reward Function Design
```python
def calculate_reward(state, action, next_state):
    reward = 0
    
    # Survival bonus
    reward += 1
    
    # Wall destruction
    if walls_destroyed > 0:
        reward += walls_destroyed * 10
    
    # Enemy hit
    if enemy_hit:
        reward += 100
    
    # Power-up collection
    if power_up_collected:
        reward += 50
    
    # Death penalty
    if player_died:
        reward -= 100
    
    # Danger penalty (near explosion)
    if in_danger:
        reward -= 5
    
    # Movement toward enemy
    if distance_to_enemy < previous_distance:
        reward += 2
    
    return reward
```

---

## 📋 Implementation Plan

### Phase 1: Core Game (2 weeks)
**Priority: CRITICAL**

#### Tasks:
1. ✅ Set up project structure
2. ✅ Create game window with Pygame
3. ✅ Implement grid system
4. ✅ Add player character and controls
5. ✅ Implement bomb mechanics
6. ✅ Add wall destruction
7. ✅ Create power-up system
8. ✅ Add scoring and game over

**Files to Create:**
```
bomber_game/
├── __init__.py
├── main.py                    # Entry point
├── config.py                  # Configuration
├── game_engine.py             # Main game loop
├── entities/
│   ├── __init__.py
│   ├── entity.py              # Base class
│   ├── player.py              # Player class
│   ├── bomb.py                # Bomb class
│   └── powerup.py             # PowerUp class
├── game_state.py              # State management
├── rendering.py               # Graphics
└── utils.py                   # Helper functions
```

---

### Phase 2: Rule-Based AI (1 week)
**Priority: HIGH**

#### Tasks:
1. ✅ Create Agent base class
2. ✅ Implement RandomAgent
3. ✅ Implement SimpleAgent (avoid bombs)
4. ✅ Implement PathfindingAgent (A*)
5. ✅ Add difficulty levels

**Files to Create:**
```
bomber_game/
├── agents/
│   ├── __init__.py
│   ├── agent_base.py          # Abstract base
│   ├── random_agent.py        # Random movements
│   ├── simple_agent.py        # Basic heuristics
│   └── pathfinding_agent.py   # A* pathfinding
└── pathfinding.py             # A* algorithm
```

---

### Phase 3: Data Collection & ML (1 week)
**Priority: MEDIUM**

#### Tasks:
1. ✅ Add data logging system
2. ✅ Collect gameplay data
3. ✅ Feature engineering
4. ✅ Train supervised learning model
5. ✅ Evaluate model performance

**Files to Create:**
```
bomber_game/
├── ml/
│   ├── __init__.py
│   ├── data_collector.py      # Log game data
│   ├── feature_extractor.py   # Extract features
│   ├── ml_model.py            # Neural network
│   └── ml_agent.py            # ML-based agent
└── visualization/
    ├── __init__.py
    └── training_plots.py      # Visualize learning
```

---

### Phase 4: Reinforcement Learning (2 weeks)
**Priority: HIGH**

#### Tasks:
1. ✅ Create RL environment wrapper
2. ✅ Implement Q-Learning
3. ✅ Add experience replay
4. ✅ Implement DQN
5. ✅ Training loop with checkpoints
6. ✅ Hyperparameter tuning

**Files to Create:**
```
bomber_game/
├── rl/
│   ├── __init__.py
│   ├── environment.py         # Gym-like interface
│   ├── q_learning.py          # Q-Learning
│   ├── dqn.py                 # Deep Q-Network
│   ├── replay_buffer.py       # Experience replay
│   ├── rewards.py             # Reward functions
│   └── rl_agent.py            # RL agent
└── training/
    ├── __init__.py
    ├── train_q_learning.py    # Training script
    ├── train_dqn.py           # DQN training
    └── evaluate.py            # Evaluation
```

---

### Phase 5: Educational Features (1 week)
**Priority: MEDIUM**

#### Tasks:
1. ✅ Tutorial mode
2. ✅ Visualization dashboard
3. ✅ Step-by-step mode
4. ✅ Documentation
5. ✅ Example notebooks

**Files to Create:**
```
bomber_game/
├── tutorial/
│   ├── __init__.py
│   ├── tutorial_mode.py       # Guided gameplay
│   └── explanations.py        # Text explanations
├── visualization/
│   ├── dashboard.py           # Real-time viz
│   ├── q_table_viz.py         # Q-table heatmap
│   └── network_viz.py         # Neural net viz
└── notebooks/
    ├── 01_introduction.ipynb
    ├── 02_game_mechanics.ipynb
    ├── 03_rule_based_ai.ipynb
    ├── 04_ml_basics.ipynb
    └── 05_reinforcement_learning.ipynb
```

---

## 🤖 AI/ML Integration

### 1. Rule-Based AI

#### Random Agent (Easiest)
```python
class RandomAgent(Agent):
    def act(self, observation):
        return random.choice(ACTIONS)
```

#### Simple Heuristic Agent
```python
class SimpleAgent(Agent):
    def act(self, observation):
        # Priority 1: Avoid explosions
        if self.in_danger(observation):
            return self.find_safe_move(observation)
        
        # Priority 2: Place bomb near enemy
        if self.enemy_nearby(observation):
            return ACTION_PLACE_BOMB
        
        # Priority 3: Move toward enemy
        return self.move_toward_enemy(observation)
```

#### A* Pathfinding Agent
```python
class PathfindingAgent(Agent):
    def act(self, observation):
        path = self.a_star(
            start=self.position,
            goal=self.target_position,
            grid=observation['grid']
        )
        return self.path_to_action(path)
```

---

### 2. Machine Learning Agent

#### Supervised Learning
```python
class MLAgent(Agent):
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        model = tf.keras.Sequential([
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(len(ACTIONS), activation='softmax')
        ])
        return model
    
    def act(self, observation):
        features = self.extract_features(observation)
        action_probs = self.model.predict(features)
        return np.argmax(action_probs)
```

---

### 3. Reinforcement Learning Agent

#### Q-Learning (Tabular)
```python
class QLearningAgent(Agent):
    def __init__(self, learning_rate=0.1, discount=0.99):
        self.q_table = defaultdict(lambda: np.zeros(len(ACTIONS)))
        self.lr = learning_rate
        self.gamma = discount
        self.epsilon = 1.0
    
    def act(self, state):
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)  # Explore
        return np.argmax(self.q_table[state])  # Exploit
    
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q
        
        # Decay epsilon
        self.epsilon = max(0.01, self.epsilon * 0.995)
```

#### Deep Q-Network (DQN)
```python
class DQNAgent(Agent):
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = ReplayBuffer(capacity=10000)
        
        self.q_network = self.build_network()
        self.target_network = self.build_network()
        self.update_target_network()
        
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
    
    def build_network(self):
        model = tf.keras.Sequential([
            Dense(256, activation='relu', input_shape=(self.state_size,)),
            Dense(256, activation='relu'),
            Dense(128, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        q_values = self.q_network.predict(state, verbose=0)
        return np.argmax(q_values[0])
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.add(state, action, reward, next_state, done)
    
    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        
        batch = self.memory.sample(batch_size)
        states, actions, rewards, next_states, dones = batch
        
        # Calculate target Q-values
        target_q = rewards + self.gamma * \
                   np.max(self.target_network.predict(next_states, verbose=0), axis=1) * \
                   (1 - dones)
        
        # Get current Q-values
        current_q = self.q_network.predict(states, verbose=0)
        current_q[range(batch_size), actions] = target_q
        
        # Train network
        self.q_network.fit(states, current_q, epochs=1, verbose=0)
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def update_target_network(self):
        self.target_network.set_weights(self.q_network.get_weights())
```

---

## 📊 Success Metrics

### Educational Success
- Student can explain RL concepts
- Student can modify reward function
- Student can train new agents
- Student understands trade-offs

### Technical Success
- Game runs at 30+ FPS
- AI agents are competitive
- Training converges within 1000 episodes
- DQN agent beats rule-based AI

### Code Quality
- Well-documented code
- Modular architecture
- Unit tests for core functions
- Clear examples and tutorials

---

## 🎓 Teaching Resources

### Jupyter Notebooks
1. **Introduction to Python & Pygame**
2. **Building the Game**
3. **Rule-Based AI**
4. **Introduction to Machine Learning**
5. **Reinforcement Learning Basics**
6. **Deep Q-Networks**
7. **Advanced Topics**

### Video Tutorials (Optional)
- Setting up the environment
- Understanding the game code
- Training your first AI
- Visualizing learning

### Exercises
1. Modify player speed
2. Add new power-ups
3. Create custom maps
4. Design new reward function
5. Implement Double DQN
6. Add more agents (multiplayer)

---

## 🔮 Future Extensions

### Gameplay
- Multiple AI opponents
- Team-based gameplay
- Online multiplayer
- Custom map editor

### AI/ML
- PPO (Proximal Policy Optimization)
- A3C (Asynchronous Actor-Critic)
- Self-play training
- Transfer learning
- Multi-agent RL

### Educational
- Web-based version
- Interactive visualization
- Leaderboard system
- Certification program

---

## 📝 Development Timeline

### Sprint 1 (Week 1-2): Foundation
- Set up project structure
- Implement core game mechanics
- Create basic graphics
- Test gameplay

### Sprint 2 (Week 3): Rule-Based AI
- Implement agent system
- Create 3 difficulty levels
- Add AI vs AI mode

### Sprint 3 (Week 4): Data & ML
- Data collection
- Feature engineering
- Train supervised model
- Compare with rule-based

### Sprint 4 (Week 5-6): Reinforcement Learning
- Q-Learning implementation
- DQN implementation
- Training pipeline
- Model evaluation

### Sprint 5 (Week 7): Polish & Documentation
- Tutorial mode
- Visualization dashboard
- Documentation
- Jupyter notebooks
- Final testing

---

## 🎯 Next Steps

1. **Review this specification** with your son
2. **Set up development environment** (already done!)
3. **Start with Phase 1**: Core game implementation
4. **Create first notebook**: Introduction to the project
5. **Build incrementally**: One feature at a time

---

## 📚 Recommended Reading

### For Students
- "Python Crash Course" by Eric Matthes
- "Make Your Own Python Text Adventure" by Phillip Johnson
- "Hands-On Reinforcement Learning with Python" by Sudharsan Ravichandiran

### For Parents/Mentors
- "Deep Reinforcement Learning Hands-On" by Maxim Lapan
- "Reinforcement Learning: An Introduction" by Sutton & Barto
- OpenAI Spinning Up in Deep RL

---

## 🤝 Contributing

This is an educational project! Encourage your son to:
- Experiment with code
- Break things and fix them
- Ask "what if?" questions
- Share learnings with others

---

**Let's build an amazing learning experience! 🚀**
