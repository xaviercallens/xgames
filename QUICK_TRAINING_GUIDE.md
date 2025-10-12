# 🚀 Quick Training Guide - 15 Minute AI Training

## 🎯 **Overview**

Train your AI agent progressively with **automatic checkpointing**, **level progression**, and **in-game display** of training stats!

---

## ✨ **Features**

### **1. Progressive Training**
- **15-minute** focused training sessions
- **Automatic checkpointing** every 60 seconds
- **Cumulative learning** - each session builds on previous
- **Level progression** from Beginner to Master

### **2. Persistent Statistics**
- **Total episodes** trained
- **Total training time** accumulated
- **Win rate** tracking
- **Training sessions** history
- **Current level** based on performance

### **3. In-Game Display**
- **AI Type** (PPO/DQN/Simple)
- **Training Level** with color coding
- **Training Time** accumulated
- **Win Rate** percentage
- **Real-time stats** during gameplay

### **4. Smart Serialization**
- **Auto-save** every 60 seconds
- **Resume training** from last checkpoint
- **Never lose progress**
- **JSON stats** file for tracking

---

## 🎮 **Quick Start**

### **Step 1: Install PyTorch**
```bash
pip install torch torchvision
```

### **Step 2: Run First Training Session**
```bash
./quick_train_agent.py
```

This will:
- ✅ Train for 15 minutes
- ✅ Save checkpoints every 60 seconds
- ✅ Display progress in real-time
- ✅ Create pre-trained model

### **Step 3: Play with Trained AI**
```bash
./launch_bomberman.sh
```

The game will automatically:
- ✅ Load your trained agent
- ✅ Display AI level and stats
- ✅ Show training time
- ✅ Show win rate

### **Step 4: Continue Training**
```bash
# Run another 15-minute session
./quick_train_agent.py
```

Training is **cumulative** - each session improves the AI!

---

## 📊 **AI Level System**

| Level | Win Rate | Color | Description |
|-------|----------|-------|-------------|
| **🔵 Beginner** | 0-19% | Blue | Just starting, learning basics |
| **🟢 Novice** | 20-39% | Green | Understanding game mechanics |
| **🟡 Intermediate** | 40-59% | Yellow | Developing strategies |
| **🟠 Advanced** | 60-74% | Orange | Strong tactical play |
| **🔴 Expert** | 75-84% | Red | Excellent performance |
| **🟣 Master** | 85%+ | Purple | Near-perfect play |

---

## 🔄 **Training Workflow**

### **First Session:**
```bash
./quick_train_agent.py
```

**Output:**
```
🚀 QUICK TRAINING - 15 Minute Progressive Learning Session
================================================================================

✅ PyTorch: 2.1.0
✅ Device: CPU

📊 Current Training Status:
   Total Episodes: 0
   Total Training Time: 0s
   Win Rate: 0.0%
   Current Level: Beginner

🤖 Initializing PPO Agent...

⏱️  Training Duration: 15 minutes
💾 Checkpoint Interval: 60 seconds
🎯 Target: Improve from Beginner

🎮 Starting training...

[████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30.5% | Time: 4m 34s/15m 0s | Episodes: 120 | Win%: 15.2 | Level: Beginner
💾 Checkpoint at 5m 0s...
   ✅ Saved! Level: Beginner, Win Rate: 15.2%

[████████████████████████████████░░░░░░░░░░░░░░] 65.2% | Time: 9m 47s/15m 0s | Episodes: 260 | Win%: 28.5 | Level: Novice
💾 Checkpoint at 10m 0s...
   ✅ Saved! Level: Novice, Win Rate: 28.5%

[██████████████████████████████████████████████] 100.0% | Time: 15m 0s/15m 0s | Episodes: 400 | Win%: 35.8 | Level: Novice

================================================================================
✅ TRAINING SESSION COMPLETE!
================================================================================

📊 Session Statistics:
   Duration: 15m 0s
   Episodes: 400
   Wins: 143 (35.8%)

📈 Overall Statistics:
   Total Episodes: 400
   Total Training Time: 15m 0s
   Overall Win Rate: 35.8%
   Current Level: Novice

🎮 Play with your trained agent: ./launch_bomberman.sh
```

### **Second Session (Cumulative):**
```bash
./quick_train_agent.py
```

**Output:**
```
📊 Current Training Status:
   Total Episodes: 400
   Total Training Time: 15m 0s
   Win Rate: 35.8%
   Current Level: Novice
   Last Updated: 2025-10-12T14:00:00

🎯 Target: Improve from Novice

... training continues ...

📈 Overall Statistics:
   Total Episodes: 800
   Total Training Time: 30m 0s
   Overall Win Rate: 52.3%
   Current Level: Intermediate
```

---

## 🎮 **In-Game Display**

When playing, you'll see:

```
Player: Trumps:2 Cacas:3 Range:2

AI (PPO): Bombs:2 Range:2
Level: Intermediate | Training: 30m | Win Rate: 52%

Controls: WASD=Move, Space=Trump💨, C=Caca💩, P=Pause
```

**Level colors:**
- 🔵 **Blue** = Beginner
- 🟢 **Green** = Novice
- 🟡 **Yellow** = Intermediate
- 🟠 **Orange** = Advanced
- 🔴 **Red** = Expert
- 🟣 **Purple** = Master

---

## 📈 **Training Schedule**

### **Recommended Training Plan:**

#### **Day 1: Foundation** (30 minutes)
```bash
# Session 1: 15 minutes
./quick_train_agent.py
# Expected: Beginner → Novice (20-30% win rate)

# Session 2: 15 minutes
./quick_train_agent.py
# Expected: Novice → Intermediate (40-50% win rate)
```

#### **Day 2: Improvement** (30 minutes)
```bash
# Session 3: 15 minutes
./quick_train_agent.py
# Expected: Intermediate → Advanced (55-65% win rate)

# Session 4: 15 minutes
./quick_train_agent.py
# Expected: Advanced (65-70% win rate)
```

#### **Day 3: Mastery** (30 minutes)
```bash
# Session 5: 15 minutes
./quick_train_agent.py
# Expected: Advanced → Expert (75-80% win rate)

# Session 6: 15 minutes
./quick_train_agent.py
# Expected: Expert → Master (85%+ win rate)
```

**Total: 90 minutes to Master level!**

---

## 💾 **Files Created**

### **Model File:**
```
bomber_game/models/ppo_agent.pth
```
- Neural network weights
- Optimizer state
- Auto-saved every 60 seconds

### **Statistics File:**
```
bomber_game/models/training_stats.json
```
- Total episodes
- Total training time
- Win/loss records
- Training sessions history
- Current level
- Last updated timestamp

**Example stats.json:**
```json
{
  "total_episodes": 800,
  "total_training_time": 1800,
  "total_wins": 418,
  "total_losses": 382,
  "episode_rewards": [...],
  "win_rates": [...],
  "training_sessions": [
    {
      "date": "2025-10-12T14:00:00",
      "duration": 900,
      "episodes": 400,
      "wins": 143,
      "final_level": "Novice"
    },
    {
      "date": "2025-10-12T14:20:00",
      "duration": 900,
      "episodes": 400,
      "wins": 275,
      "final_level": "Intermediate"
    }
  ],
  "current_level": "Intermediate",
  "last_updated": "2025-10-12T14:20:00"
}
```

---

## 🔧 **Advanced Options**

### **Customize Training Duration:**

Edit `quick_train_agent.py`:
```python
TRAINING_DURATION = 30 * 60  # 30 minutes
CHECKPOINT_INTERVAL = 120    # Save every 2 minutes
```

### **View Training History:**
```bash
cat bomber_game/models/training_stats.json | python -m json.tool
```

### **Reset Training:**
```bash
# Backup first!
cp bomber_game/models/ppo_agent.pth bomber_game/models/ppo_agent_backup.pth
cp bomber_game/models/training_stats.json bomber_game/models/training_stats_backup.json

# Remove to start fresh
rm bomber_game/models/ppo_agent.pth
rm bomber_game/models/training_stats.json
```

---

## 📊 **Progress Tracking**

### **During Training:**
```
[████████████████████████░░░░░░░░░░░░░░░░░░░░░░] 50.2% | Time: 7m 32s/15m 0s | Episodes: 200 | Win%: 42.5 | Level: Intermediate
```

- **Progress bar**: Visual training progress
- **Time**: Current/Total time
- **Episodes**: Games played this session
- **Win%**: Current session win rate
- **Level**: Current AI level

### **Checkpoints:**
```
💾 Checkpoint at 5m 0s...
   ✅ Saved! Level: Intermediate, Win Rate: 42.5%
```

### **Session Complete:**
```
✅ TRAINING SESSION COMPLETE!

📊 Session Statistics:
   Duration: 15m 0s
   Episodes: 400
   Wins: 170 (42.5%)

📈 Overall Statistics:
   Total Episodes: 800
   Total Training Time: 30m 0s
   Overall Win Rate: 52.3%
   Current Level: Intermediate
```

---

## 🎓 **Educational Value**

### **Concepts Demonstrated:**

#### **1. Progressive Learning**
- Start with simple heuristics
- Gradually improve through experience
- Curriculum learning approach

#### **2. Checkpointing**
- Save progress regularly
- Resume from last state
- Never lose training time

#### **3. Transfer Learning**
- Build on previous knowledge
- Cumulative improvement
- Efficient training

#### **4. Performance Metrics**
- Win rate tracking
- Level progression
- Training time monitoring

---

## 💡 **Tips**

### **For Best Results:**

1. **Train Regularly**
   - Multiple short sessions better than one long
   - 15 minutes daily for a week = Master level

2. **Monitor Progress**
   - Watch win rate increase
   - See level progression
   - Track training time

3. **Test Between Sessions**
   - Play against AI after each session
   - Notice improvement
   - Motivating to see progress!

4. **Don't Interrupt**
   - Let full 15 minutes complete
   - Checkpoints save progress
   - Ctrl+C if needed (saves current state)

---

## 🚀 **Quick Commands**

```bash
# Train for 15 minutes
./quick_train_agent.py

# Play with trained AI
./launch_bomberman.sh

# View stats
cat bomber_game/models/training_stats.json

# Check AI level
grep "current_level" bomber_game/models/training_stats.json
```

---

## ✨ **Summary**

### **What You Get:**
- 🤖 **Progressive AI training** (15 min sessions)
- 💾 **Auto-save** every 60 seconds
- 📊 **Level progression** (Beginner → Master)
- 🎮 **In-game stats** display
- 📈 **Cumulative learning**
- 🔄 **Resume training** anytime

### **Training Path:**
```
Session 1 (15m) → Beginner/Novice (20-30%)
Session 2 (15m) → Novice/Intermediate (40-50%)
Session 3 (15m) → Intermediate/Advanced (55-65%)
Session 4 (15m) → Advanced (65-75%)
Session 5 (15m) → Expert (75-85%)
Session 6 (15m) → Master (85%+)
```

### **Result:**
**90 minutes total = Master-level AI!** 🏆

---

## 🎮 **Start Training Now!**

```bash
# Install PyTorch
pip install torch

# Train for 15 minutes
./quick_train_agent.py

# Play and see the results!
./launch_bomberman.sh
```

**Watch your AI evolve from Beginner to Master!** 🚀🤖✨
