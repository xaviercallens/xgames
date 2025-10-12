# 📊 Model Performance Tracking Guide

## Overview

Comprehensive system for tracking PPO model performance across different game modes and monitoring heuristic agent stability.

---

## 🎯 Features

### **1. Model History Tracking**
- Tracks all PPO model versions
- Records performance per game mode
- Automatically selects best model per mode
- Maintains complete version history
- Exports data for analysis

### **2. Heuristic Performance Monitoring**
- Tracks heuristic performance over time
- Detects performance degradation (>10% drop)
- Compares with baseline
- Records all play sessions
- Alerts on issues

### **3. Performance Analysis**
- Tests models across different opponents
- Generates comprehensive reports
- Identifies performance issues
- Provides recommendations
- Exports results to JSON/CSV

---

## 📈 Current Performance Status

### **Heuristic Agent:**
```
Benchmark Win Rate: 29.0% (100 games)
Current Win Rate:   27.0% (100 games)
Difference:         -2.0%
Status:             ✅ STABLE (within 5%)

Assessment: Performance is consistent and stable.
No degradation detected.
```

### **PPO Agent:**
```
Training Episodes: 2,475
Win Rate:         0.3%
Status:           🌱 Early Learning

Assessment: Agent is in early learning phase.
Needs 5,000-10,000 episodes to become competitive.
Expected to reach 30%+ after sufficient training.
```

---

## 🚀 Usage

### **Analyze All Models:**
```bash
python analyze_model_performance.py --all
```

### **Analyze PPO Only:**
```bash
python analyze_model_performance.py --ppo
```

### **Analyze Heuristic Only:**
```bash
python analyze_model_performance.py --heuristic
```

### **Quick Test (20 games):**
```bash
python analyze_model_performance.py --quick
```

---

## 📊 Game Modes

### **1. vs_simple**
- **Opponent:** Simple/Random AI
- **Purpose:** Baseline testing
- **Expected WR:** 30-50% (trained agent)

### **2. vs_heuristic**
- **Opponent:** Improved Heuristic AI
- **Purpose:** Competitive testing
- **Expected WR:** 20-40% (well-trained agent)

### **3. vs_human**
- **Opponent:** Human player
- **Purpose:** Real-world performance
- **Expected WR:** Varies by human skill

### **4. training**
- **Opponent:** Various (self-play, mixed)
- **Purpose:** Learning and improvement
- **Expected WR:** Increases over time

---

## 📁 Output Files

### **Model History:**
```
bomber_game/models/model_history.json
```
Contains:
- All model versions
- Performance per mode
- Best model per mode
- Timestamps and metadata

### **Heuristic History:**
```
bomber_game/models/heuristic_performance_history.json
```
Contains:
- All play sessions
- Win rates over time
- Baseline performance
- Degradation alerts

### **Performance Analysis:**
```
bomber_game/models/ppo_performance_analysis.json
```
Contains:
- Latest test results
- Win rates per mode
- Average rewards
- Performance assessment

### **CSV Export:**
```
bomber_game/models/model_performance.csv
```
Contains:
- Version, Timestamp, Mode
- Win Rate, Avg Reward, Episodes
- Ready for Excel/analysis tools

---

## 🔍 Performance Metrics

### **Win Rate:**
- Percentage of games won
- Primary performance indicator
- Tracked per game mode

### **Average Reward:**
- Mean reward per game
- Indicates learning quality
- Based on reward function:
  - Valid move: -1
  - Kill player: +500
  - Die: -300
  - Break wall: +30

### **Episodes:**
- Total games played
- Training progress indicator
- More episodes = better learning

### **Game Duration:**
- Average game length
- Indicates strategy efficiency
- Shorter = more decisive play

---

## 📈 Performance Trends

### **Expected Learning Curve:**

```
Episodes    Win Rate    Stage
0-500       0-5%        🌱 Initial Learning
500-1000    5-15%       📚 Basic Understanding
1000-2500   15-25%      🎯 Developing Strategy
2500-5000   25-35%      💪 Competitive
5000+       35-50%+     🏆 Expert Level
```

### **Heuristic Baseline:**
```
vs Simple AI:    27-29%
vs Random:       40-50%
vs Self:         ~50%
```

---

## ⚠️ Performance Issues

### **Degradation Detection:**

The system automatically detects:
- **>10% drop** from baseline
- Consistent poor performance
- Unusual patterns

### **Possible Causes:**

1. **Random Variance:**
   - Solution: Run more games (100+)
   - Normal fluctuation: ±5%

2. **Opponent Improved:**
   - Solution: Retrain against new opponent
   - Update training strategy

3. **Game Rules Changed:**
   - Solution: Review recent changes
   - Retrain if necessary

4. **Model Degradation:**
   - Solution: Revert to previous version
   - Check training parameters

---

## 🎓 Best Practices

### **Regular Testing:**
```bash
# Weekly performance check
python analyze_model_performance.py --all

# After training session
python analyze_model_performance.py --ppo

# Heuristic stability check
python analyze_model_performance.py --heuristic
```

### **Version Management:**
```python
from bomber_game.model_history import ModelHistory

history = ModelHistory()

# Record new version
history.record_model_version(
    model_path="bomber_game/models/ppo_agent.pth",
    mode="vs_heuristic",
    performance_metrics={
        'win_rate': 35.5,
        'avg_reward': 125.3,
        'episodes': 5000,
    }
)

# Get best model for mode
best = history.get_best_model_for_mode('vs_heuristic')
print(f"Best model: v{best['version_id']} - {best['performance']['win_rate']:.1f}%")
```

### **Monitoring:**
```python
from bomber_game.model_history import HeuristicPerformanceTracker

tracker = HeuristicPerformanceTracker()

# Record session
tracker.record_session(
    opponent_type="Simple AI",
    games_played=100,
    wins=27,
    losses=55,
    draws=18
)

# Check recent performance
recent = tracker.get_recent_performance(10)
print(f"Recent WR: {recent['win_rate']:.1f}%")
```

---

## 📊 Analysis Reports

### **Model History Report:**
```bash
python -c "from bomber_game.model_history import ModelHistory; print(ModelHistory().generate_report())"
```

Output:
```
======================================================================
📊 MODEL PERFORMANCE HISTORY
======================================================================
Total Versions: 5

======================================================================
🎮 Against Simple AI
======================================================================
  Total Versions: 2
  
  🏆 Best Version: v3
     Win Rate: 45.2%
     Avg Reward: 234.5
     Episodes: 5,000
     Date: 2025-10-12
  
  📅 Latest Version: v5
     Win Rate: 43.8%
     Avg Reward: 221.3
     Episodes: 7,500
  
  📈 Trend: +15.3% (+51.2% change)
======================================================================
```

### **Heuristic Report:**
```bash
python -c "from bomber_game.model_history import HeuristicPerformanceTracker; print(HeuristicPerformanceTracker().generate_report())"
```

Output:
```
======================================================================
🎯 HEURISTIC PERFORMANCE HISTORY
======================================================================
Baseline Win Rate: 29.0%

Recent Performance (last 10 sessions):
  Games: 1,000
  Wins: 275
  Win Rate: 27.5%
  Change: -1.5% from baseline

Performance by Opponent:
  Simple AI: 27.5% (275/1000)
  Random AI: 45.2% (90/199)
======================================================================
```

---

## 🔧 Troubleshooting

### **Issue: Low Win Rate**
```
Problem: PPO win rate < 5% after 1000+ episodes
Solution:
  1. Check reward function
  2. Verify state representation
  3. Adjust learning rate
  4. Increase training episodes
  5. Review exploration strategy
```

### **Issue: Heuristic Degradation**
```
Problem: Heuristic drops >10% from baseline
Solution:
  1. Run more games (variance check)
  2. Compare with benchmark
  3. Review recent code changes
  4. Check opponent changes
  5. Retune heuristic weights
```

### **Issue: Inconsistent Performance**
```
Problem: Win rate varies wildly (±20%)
Solution:
  1. Increase test games (50 → 100+)
  2. Check for randomness issues
  3. Verify opponent consistency
  4. Review game mechanics
```

---

## 📚 Integration with Training

### **During Training:**
```python
# After each training session
history = ModelHistory()
history.record_model_version(
    model_path="bomber_game/models/ppo_agent.pth",
    mode="training",
    performance_metrics={
        'win_rate': current_win_rate,
        'avg_reward': avg_reward,
        'episodes': total_episodes,
    }
)

# Check if best model
best = history.get_best_model_for_mode('training')
if best['version_id'] == history.history['current_version']:
    print("🏆 New best model!")
```

### **Model Selection:**
```python
# Select best model for specific opponent
history = ModelHistory()

# Playing against human
best_vs_human = history.get_best_model_for_mode('vs_human')
if best_vs_human:
    model_path = best_vs_human['model_file']
    # Load this model
```

---

## 🎯 Performance Goals

### **Short-term (1-2 weeks):**
- ✅ Heuristic stable at 27-29%
- 🎯 PPO reaches 10% vs Simple
- 🎯 PPO reaches 5% vs Heuristic

### **Medium-term (1 month):**
- 🎯 PPO reaches 30% vs Simple
- 🎯 PPO reaches 20% vs Heuristic
- 🎯 Consistent performance across modes

### **Long-term (3 months):**
- 🎯 PPO reaches 50% vs Simple
- 🎯 PPO reaches 35% vs Heuristic
- 🎯 Competitive against human players

---

## 📞 Support

### **Questions:**
- Check this guide
- Review code comments
- Run analysis scripts
- Check output files

### **Issues:**
- Run diagnostics: `python analyze_model_performance.py --all`
- Check history: `cat bomber_game/models/model_history.json`
- Review logs: Check console output
- Test manually: `./launch_bomberman.sh`

---

**Performance tracking system ready for production use!** 📊🚀

*Last Updated: 2025-10-12*  
*Version: 1.0*  
*Status: Production Ready*
