# 🎮 AI Mode Selection Guide

## Overview

The game now features an **interactive AI mode selector** on the splash menu that allows you to choose your opponent difficulty and AI type before each game.

---

## 🎯 Available AI Modes

### 1. **Beginner Bot** 🌱
- **Type**: Simple Heuristic
- **Level**: Beginner
- **Description**: Basic AI - Easy to beat
- **Expected Win Rate**: 10.0%
- **Features**:
  - Simple danger avoidance
  - Random movement patterns
  - Basic bomb placement
- **Best For**: Learning the game, casual play
- **Color**: Green

### 2. **Intermediate Bot** 🎯
- **Type**: Improved Heuristic
- **Level**: Intermediate
- **Description**: Smart heuristic AI
- **Expected Win Rate**: 35.0%
- **Features**:
  - A* pathfinding algorithm
  - Weighted evaluation function
  - Danger zone prediction
  - Strategic bomb placement
  - Performance tracking
- **Best For**: Balanced challenge, learning AI concepts
- **Color**: Orange

### 3. **Advanced Bot (Smart)** 🧠 **[NEW!]**
- **Type**: Advanced Smart Heuristic
- **Level**: Advanced
- **Description**: Advanced Smart Heuristic - Predictive & Strategic
- **Expected Win Rate**: 60.0%
- **Features**:
  - ✅ Predictive bomb placement analysis
  - ✅ Game tree evaluation (minimax algorithm)
  - ✅ Strategic positioning
  - ✅ Opponent behavior prediction
  - ✅ Dynamic strategy selection (4 strategies)
  - ✅ Multi-step lookahead planning
- **Best For**: Competitive play, expert challenge
- **Color**: Blue
- **Status**: Expert-level AI

### 4. **Advanced Bot (PPO)** 🤖
- **Type**: Deep Reinforcement Learning
- **Level**: Advanced
- **Description**: Deep RL - N games (Recent: X% WR)
- **Expected Win Rate**: 25.0% (varies)
- **Features**:
  - Deep Reinforcement Learning (PPO algorithm)
  - Trained on thousands of games
  - Learns from every game
  - Adapts to your strategy
- **Best For**: Adaptive challenge, learning from AI
- **Color**: Red
- **Status**: Available if PPO model exists

### 5. **Hybrid Bot (NEW!)** 🎭
- **Type**: Heuristics + RL Combination
- **Level**: Expert
- **Description**: Heuristics + RL (Adaptive, ~40% WR)
- **Expected Win Rate**: 40.0%
- **Features**:
  - Combines strategic heuristics with learned behaviors
  - Adaptive decision making
  - Best of both worlds approach
  - Robust and reliable performance
- **Best For**: Balanced challenge, hybrid approach
- **Color**: Purple
- **Status**: Available if PPO model exists

### 6. **Expert Bot (Best)** 👑
- **Type**: Best Trained Model
- **Level**: Expert
- **Description**: Best checkpoint (Recent: X% WR)
- **Expected Win Rate**: 25.0% (varies)
- **Features**:
  - Best performing trained model
  - Saved checkpoint from training
  - Highest performance achieved
- **Best For**: Ultimate challenge
- **Color**: Purple
- **Status**: Available if best model exists

---

## 🎮 How to Select AI Mode

### Step 1: Launch Game
```bash
./launch_bomberman.sh
```

### Step 2: Skip Splash Screen
- Press any key to skip the 3-second splash screen
- Or wait for it to auto-skip

### Step 3: Select AI Opponent
The AI selection menu shows all available opponents:

```
🎮 Choose Your Opponent
Select AI difficulty level

[🌱 Beginner Bot]
Basic AI - Easy to beat
Expected Win Rate: 10.0%

[🎯 Intermediate Bot]
Smart heuristic AI
Expected Win Rate: 35.0%

[🧠 Advanced Bot (Smart)]
Advanced Smart Heuristic - Predictive & Strategic
Expected Win Rate: 60.0%

[🤖 Advanced Bot (PPO)]
Deep RL - 4,615 games (Recent: 25% WR)
Expected Win Rate: 25.0%

[🎭 Hybrid Bot (NEW!)]
Heuristics + RL (Adaptive, ~40% WR)
Expected Win Rate: 40.0%

[👑 Expert Bot (Best)]
Best checkpoint (Recent: 25% WR)
Expected Win Rate: 25.0%
```

### Step 4: Navigate and Select
- **↑↓ or W/S**: Move up/down to select
- **ENTER or SPACE**: Confirm selection
- **ESC**: Use default (Beginner Bot)
- **MOUSE**: Click on an option to select

### Step 5: Start Game
Once selected, the game starts with your chosen opponent!

---

## 🧠 Advanced Smart Heuristic Details

### What Makes It Advanced?

**1. Predictive Analysis** 🔮
- Predicts bomb explosions before they happen
- Calculates blast zones accurately
- Finds escape paths automatically
- Multi-step lookahead planning

**2. Game Tree Evaluation** 🌳
- Minimax algorithm for optimal moves
- Alpha-beta pruning for efficiency
- Evaluates multiple move sequences
- 2-3 depth lookahead

**3. Strategic Positioning** 🎯
- Calculates position values
- Controls center of map
- Maintains optimal distance
- Counts escape routes

**4. Opponent Modeling** 👁️
- Tracks opponent movement history
- Predicts next positions
- Estimates bomb placement probability
- Recognizes behavior patterns

**5. Dynamic Strategy Selection** 🎮
- **Aggressive**: When strong and close
- **Defensive**: When balanced
- **Evasive**: When weak and close
- **Balanced**: When far apart

### Performance Comparison

```
Beginner Bot:           ████░░░░░░░░░░░░░░░░  10%
Intermediate Bot:       ███████░░░░░░░░░░░░░░  35%
Advanced Bot (Smart):   ████████████░░░░░░░░░░  60% ⭐
Advanced Bot (PPO):     █████░░░░░░░░░░░░░░░░░  25%
Hybrid Bot:             ████████░░░░░░░░░░░░░░  40%
Expert Bot:             █████░░░░░░░░░░░░░░░░░  25%
```

---

## 🎯 Recommended Choices

### For Beginners
- **Start with**: Beginner Bot
- **Progress to**: Intermediate Bot
- **Challenge**: Advanced Bot (Smart)

### For Intermediate Players
- **Play with**: Intermediate Bot
- **Challenge**: Advanced Bot (Smart)
- **Master**: Hybrid Bot

### For Expert Players
- **Challenge**: Advanced Bot (Smart)
- **Ultimate**: Hybrid Bot + Expert Bot
- **Competitive**: Advanced Bot (PPO)

### For Learning AI
- **Start with**: Intermediate Bot (understand heuristics)
- **Learn from**: Advanced Bot (Smart) (see strategic thinking)
- **Explore**: Hybrid Bot (combine approaches)

---

## 📊 Game Statistics

After each game, you'll see:
- **Win Rate**: Your win percentage vs this opponent
- **Average Reward**: Points earned per game
- **Games Played**: Total games against this opponent
- **Bombs Placed**: Strategic bomb placement count
- **Actions Taken**: Total moves made

---

## 🔄 Switching Opponents

You can change opponents between games:
1. After game ends, press **R** to restart
2. The AI selection menu appears again
3. Choose a different opponent
4. Start new game with new opponent

---

## 💡 Tips for Each Mode

### Beginner Bot
- Easy to predict
- Avoid bombs, you'll win
- Good for learning controls

### Intermediate Bot
- Uses pathfinding
- Avoids danger zones
- Requires strategic thinking

### Advanced Bot (Smart)
- Predicts your moves
- Strategic positioning
- Requires expert play
- Adapts to your tactics

### Advanced Bot (PPO)
- Learns from games
- Improves over time
- Unpredictable
- Adaptive behavior

### Hybrid Bot
- Combines both approaches
- Robust performance
- Balanced challenge
- Reliable opponent

### Expert Bot
- Best trained model
- Highest performance
- Ultimate challenge
- Competitive level

---

## 🎮 Controls During Game

- **WASD or Arrow Keys**: Move
- **Space**: Drop bomb (prout)
- **C**: Drop block (caca)
- **P**: Pause
- **R**: Record gameplay
- **S**: Save recording
- **ESC**: Show stats/menu
- **E**: Show educational stats

---

## 📈 Performance Tracking

The game tracks your performance against each opponent:
- Win rate per opponent
- Average game length
- Bombs placed
- Actions taken
- Rewards earned

View statistics in the educational stats screen (ESC key).

---

## 🚀 Advanced Features

### Predictive Analysis
The Advanced Bot predicts:
- Bomb explosion timing
- Blast zone coverage
- Escape route availability
- Danger levels

### Game Tree Evaluation
The Advanced Bot evaluates:
- Current position strength
- Opponent threat level
- Optimal move sequences
- Multi-step consequences

### Strategic Positioning
The Advanced Bot considers:
- Center control value
- Distance from opponent
- Wall proximity
- Power-up locations
- Escape route count

### Opponent Modeling
The Advanced Bot tracks:
- Movement patterns
- Bomb placement habits
- Velocity and direction
- Behavior predictions

---

## 🏆 Achievements

### Beginner Achievements
- ✅ Beat Beginner Bot
- ✅ Survive 5 minutes
- ✅ Place 10 bombs

### Intermediate Achievements
- ✅ Beat Intermediate Bot
- ✅ Collect 5 power-ups
- ✅ Destroy 20 walls

### Advanced Achievements
- ✅ Beat Advanced Bot (Smart)
- ✅ Win 5 games in a row
- ✅ Achieve 50% win rate

### Expert Achievements
- ✅ Beat Hybrid Bot
- ✅ Beat Expert Bot
- ✅ Master all opponents

---

## 📝 Summary

The AI Mode Selection system provides:
- ✅ 6 different opponent types
- ✅ Varying difficulty levels
- ✅ Clear performance expectations
- ✅ Educational value
- ✅ Competitive challenge
- ✅ Easy selection interface

**Choose your opponent and enjoy the game!** 🎮✨

