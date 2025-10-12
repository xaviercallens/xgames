# 🎯 Intelligent Model Selection System

## Overview

Proutman now features an **intelligent model selection system** that automatically chooses the best performing AI opponent based on actual win rate statistics. The game will always use the strongest available AI!

---

## 🧠 **How It Works**

### **Automatic Selection Process:**

1. **Scan Available Models**
   - Heuristic Agent (always available)
   - Pretrained PPO Model
   - Trained PPO Model

2. **Load Performance Statistics**
   - `training_stats.json` - PPO model stats
   - `heuristic_stats.json` - Heuristic baseline stats

3. **Compare Performance**
   - Calculate win rates
   - Minimum 50 episodes required for fair comparison
   - Compare PPO vs Heuristic

4. **Select Best Performer**
   - Choose model with highest win rate
   - Save as `best_model.pth`
   - Load for gameplay

---

## 📊 **Selection Logic**

### **Decision Tree:**

```
Start
  │
  ├─ No trained model exists?
  │   └─ Use Heuristic Agent (baseline)
  │
  ├─ Only pretrained exists?
  │   └─ Use Pretrained PPO Model
  │
  ├─ PPO model exists?
  │   │
  │   ├─ Less than 50 episodes?
  │   │   └─ Use Pretrained or Heuristic (not enough data)
  │   │
  │   └─ 50+ episodes?
  │       │
  │       ├─ PPO Win Rate >= Heuristic Win Rate?
  │       │   └─ Use PPO Model ✅
  │       │
  │       └─ Heuristic Win Rate > PPO Win Rate?
  │           └─ Use Heuristic Agent 🌱
  │
  └─ Fallback: Simple Agent
```

---

## 🎮 **Three AI Types**

### **1. 🌱 Heuristic Agent (Baseline)**

**Description:**
- Pure rule-based AI
- Improved strategic algorithms
- No machine learning

**Capabilities:**
- ✅ Improved bomb placement (2+ walls = place bomb)
- ✅ Smart escape routes (avoids danger)
- ✅ Enemy tracking (80% trap rate in direct line)
- ✅ Efficient wall destruction
- ✅ Power-up prioritization

**Expected Performance:**
- Win Rate: ~15%
- Consistent behavior
- Good baseline opponent

**When Used:**
- No trained model exists
- Trained model underperforms
- Fallback option

---

### **2. 🎯 Pretrained PPO Model**

**Description:**
- Bootstrap trained with heuristics
- Ready for reinforcement learning
- Smart initialization

**Capabilities:**
- ✅ Learned from heuristic demonstrations
- ✅ Neural network decision making
- ✅ Strategic positioning
- ✅ Ready to improve with RL

**Expected Performance:**
- Win Rate: ~20%
- Better than pure heuristics
- Needs more training

**When Used:**
- No fully trained model yet
- Trained model has <50 episodes
- Better than heuristic but not fully trained

---

### **3. 🏆 Trained PPO Model**

**Description:**
- Fully trained with reinforcement learning
- Learned from thousands of games
- Adaptive and strategic

**Capabilities:**
- ✅ Deep reinforcement learning
- ✅ Learns from experience
- ✅ Adapts to player style
- ✅ Strategic decision making
- ✅ Continuously improving

**Performance:**
- Win Rate: Varies (tracked in stats)
- Gets better with more training
- Can exceed 50% with enough training

**When Used:**
- Model has 50+ episodes
- Win rate >= Heuristic baseline
- Best available performer

---

## 📈 **Performance Tracking**

### **Statistics Files:**

#### **training_stats.json** (PPO Model)
```json
{
  "total_episodes": 1234,
  "total_wins": 123,
  "win_rate": 10.0,
  "total_training_time": 13800,
  "current_level": "Beginner",
  "last_updated": "2025-10-12T17:00:00"
}
```

#### **heuristic_stats.json** (Heuristic Baseline)
```json
{
  "model_type": "heuristic",
  "total_episodes": 100,
  "total_wins": 15,
  "win_rate": 15.0,
  "description": "Pure heuristic agent (baseline)",
  "created": "2025-10-12T17:00:00"
}
```

#### **best_model.pth** (Best Performer)
- Automatic copy of best model
- Updated when PPO beats heuristic
- Used for quick loading

---

## 🎯 **Example Selection Scenarios**

### **Scenario 1: Fresh Start**

**Situation:**
- No trained model exists
- Only heuristic available

**Selection:**
```
🌱 Using Improved Heuristic Agent
   Reason: No trained model found - using heuristic baseline
   Expected Win Rate: ~15.0%
   
💡 Train AI to beat heuristic: ./train.sh
```

---

### **Scenario 2: Early Training**

**Situation:**
- PPO model exists
- Only 30 episodes trained
- Not enough data

**Selection:**
```
🎯 Using Pretrained PPO Model
   Reason: PPO model needs more training (30/50 episodes)
   Expected Win Rate: ~20.0%
   
💡 Continue training for better performance
```

---

### **Scenario 3: PPO Underperforming**

**Situation:**
- PPO: 100 episodes, 8% win rate
- Heuristic: 15% win rate
- Heuristic is better

**Selection:**
```
======================================================================
🎯 INTELLIGENT MODEL SELECTION
======================================================================

📈 PPO Model Performance:
   Episodes: 100
   Win Rate: 8.0%

⚖️  Performance Comparison:
   PPO Model:     8.0%
   Heuristic:     15.0%
   Difference:    -7.0%

🌱 Decision: Use Heuristic Agent
   Reason: Heuristic outperforms PPO by 7.0%
   💡 PPO needs more training to beat heuristic
   💡 Continue training with: ./train.sh
======================================================================
```

---

### **Scenario 4: PPO Winning**

**Situation:**
- PPO: 500 episodes, 25% win rate
- Heuristic: 15% win rate
- PPO is better!

**Selection:**
```
======================================================================
🎯 INTELLIGENT MODEL SELECTION
======================================================================

📈 PPO Model Performance:
   Episodes: 500
   Win Rate: 25.0%

⚖️  Performance Comparison:
   PPO Model:     25.0%
   Heuristic:     15.0%
   Difference:    +10.0%

🏆 Decision: Use PPO Model
   Reason: PPO outperforms heuristic by 10.0%
   ✅ Saved as best model
======================================================================

🏆 Using Trained PPO Model
   Reason: PPO outperforms heuristic by 10.0%
   Win Rate: 25.0%

📊 Detailed Statistics:
   🎯 Skill Level: Intermediate
   🎮 Games Played: 500
   🏆 Games Won: 125
   ⏱️  Training Time: 2h 30m
   
   💪 This AI is quite skilled - prepare for a challenge!
```

---

## 🔧 **Configuration**

### **Thresholds (in model_selector.py):**

```python
# Minimum episodes before comparing models
min_episodes_for_comparison = 50

# Expected heuristic baseline win rate
heuristic_baseline_win_rate = 15.0
```

**Adjust these to:**
- Require more/less training before comparison
- Set different baseline expectations

---

## 💡 **Improved Heuristics**

### **Key Improvements:**

#### **1. Better Bomb Placement**

**Old Logic:**
- Place if any wall nearby
- Random 30% chance for enemies

**New Logic:**
```python
# Place if 2+ walls in range (efficient)
if walls_in_range >= 2:
    return True

# Place if 1 wall (70% chance)
if walls_in_range == 1:
    return random.random() < 0.7

# Place if enemy in direct line (80% chance)
if enemy_in_line_of_sight:
    return random.random() < 0.8

# Place if enemy nearby (40% chance)
if enemy_distance <= 3:
    return random.random() < 0.4
```

**Benefits:**
- More efficient wall destruction
- Higher enemy trap rate
- Better strategic positioning

---

#### **2. Enemy Tracking**

**New Features:**
- Detects direct line of sight
- Checks for blocking walls
- Calculates optimal trapping positions
- Higher probability for direct hits (80% vs 30%)

**Code:**
```python
# Check if enemy is in direct line
if enemy_y == py and abs(enemy_x - px) <= player.bomb_range:
    # Check no walls blocking
    if not blocked:
        return random.random() < 0.8  # 80% chance!
```

---

#### **3. Escape Routes**

**Improvements:**
- Must have escape route before placing bomb
- Calculates safe directions
- Moves away from nearest bomb
- Prioritizes survival

---

## 📊 **Performance Comparison**

### **Expected Win Rates:**

| AI Type | Win Rate | Training Time | Description |
|---------|----------|---------------|-------------|
| **Heuristic** | ~15% | None | Baseline, consistent |
| **Pretrained** | ~20% | 1-2 hours | Bootstrap trained |
| **PPO (Early)** | 5-15% | 2-4 hours | Learning phase |
| **PPO (Mid)** | 15-30% | 4-8 hours | Improving |
| **PPO (Advanced)** | 30-50% | 8-12 hours | Strong opponent |
| **PPO (Expert)** | 50%+ | 12+ hours | Very challenging |

---

## 🚀 **Usage**

### **Automatic (Default):**

Just launch the game:
```bash
./launch_bomberman.sh
```

The system automatically:
1. Scans for models
2. Loads statistics
3. Compares performance
4. Selects best model
5. Shows decision reasoning

---

### **Manual Model Check:**

View performance report:
```python
from bomber_game.model_selector import ModelSelector

selector = ModelSelector("bomber_game/models")
print(selector.get_performance_report())
```

**Output:**
```
======================================================================
📊 MODEL PERFORMANCE REPORT
======================================================================

🌱 Heuristic Agent:
   Episodes: 100
   Wins: 15
   Win Rate: 15.0%

🤖 PPO Model:
   Episodes: 500
   Wins: 125
   Win Rate: 25.0%
   Training Time: 2h 30m
======================================================================
```

---

## 🎓 **Educational Value**

### **What Kids Learn:**

1. **Performance Metrics**
   - Win rates
   - Statistical comparison
   - Data-driven decisions

2. **Model Selection**
   - Baseline comparison
   - A/B testing concepts
   - Best practices

3. **Continuous Improvement**
   - Iterative training
   - Performance tracking
   - Optimization

4. **Decision Making**
   - Logic trees
   - Threshold-based decisions
   - Fallback strategies

---

## 🔍 **Troubleshooting**

### **Issue: Always uses heuristic**

**Cause:** PPO model hasn't beaten heuristic yet

**Solution:**
```bash
# Train more
./train.sh

# Select long training (2000+ episodes)
# Wait for win rate to exceed 15%
```

---

### **Issue: No statistics shown**

**Cause:** Stats files missing

**Solution:**
```bash
# Initialize heuristic stats
python3 -c "from bomber_game.model_selector import ModelSelector; ModelSelector('bomber_game/models').initialize_heuristic_stats()"

# Train PPO to generate stats
./train.sh
```

---

### **Issue: Want to force specific model**

**Solution:**
Temporarily modify `game_engine.py`:
```python
# Force heuristic
self.ai_agent = HeuristicAgent(self.ai_player)

# Force PPO
self.ai_agent = PPOAgent(self.ai_player, model_path="path/to/model.pth", training=False)
```

---

## 📚 **API Reference**

### **ModelSelector Class**

```python
class ModelSelector:
    def __init__(self, models_dir):
        """Initialize with models directory."""
        
    def select_best_model(self):
        """
        Select best model based on performance.
        
        Returns:
            dict: {
                'model_path': str or 'heuristic',
                'model_type': str,
                'win_rate': float,
                'reason': str
            }
        """
        
    def get_model_stats(self, stats_file):
        """Load statistics from file."""
        
    def initialize_heuristic_stats(self):
        """Initialize heuristic baseline stats."""
        
    def get_performance_report(self):
        """Generate performance report."""
```

---

## ✨ **Summary**

### **Key Benefits:**

✅ **Always Best Opponent** - Automatically uses strongest AI  
✅ **Performance-Based** - Data-driven selection  
✅ **Improved Baseline** - Better heuristics (15% win rate)  
✅ **Transparent** - Shows decision reasoning  
✅ **Educational** - Teaches model selection  
✅ **Automatic** - No manual configuration  
✅ **Adaptive** - Switches as models improve  

### **Result:**

**Players always face the best available AI opponent!**

The system ensures:
- Fair challenges
- Continuous improvement
- Transparent decisions
- Educational value

**Train your AI and watch it beat the heuristic baseline!** 🚀🎯✨

---

**Made with ❤️ for intelligent gameplay!** 🤖📊
