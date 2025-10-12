# 📊 Statistics Panel Guide

## Overview

The **Statistics Panel** provides comprehensive real-time analytics for Human vs AI gameplay, featuring performance tracking, strategy analysis, risk assessment, and intelligent recommendations.

---

## 🎯 Features

### 1. **AI Opponent Information**
- **AI Type**: Shows current AI (PPO, Heuristic, etc.)
- **Description**: Brief AI capability description
- **Win Rate**: Historical AI performance
- **Real-time Updates**: Always current

### 2. **Current Game Statistics**
- **Game Duration**: Real-time timer
- **Human Stats**:
  - Moves made
  - Bombs placed
  - Power-ups collected
  - Walls destroyed
- **AI Stats**: Same metrics for AI opponent
- **Live Tracking**: Updates every action

### 3. **Risk Levels** ⚠️
- **Real-time Risk Assessment** (0-100%)
- **Color-Coded Bars**:
  - 🟢 Green (0-40%): Safe
  - 🟠 Orange (40-70%): Moderate risk
  - 🔴 Red (70-100%): High danger
- **Separate Tracking**: Human and AI risk levels
- **Algorithm**: Considers bomb proximity, timers, explosions

### 4. **Strategy Analysis** 🎯
- **Strategy Types**:
  - ⚔️ **Aggressive**: Close-range combat (60%+ aggressive moves)
  - 🛡️ **Defensive**: Safe play (40%- aggressive moves)
  - ⚖️ **Balanced**: Mixed approach (40-60%)
- **Real-time Classification**: Updates as you play
- **Both Players**: Human and AI strategies shown

### 5. **Performance Scores** ⭐
- **Score Range**: 0-100
- **Factors**:
  - Bomb efficiency (bombs per move)
  - Survival (penalty for near-death)
  - Power-up collection bonus
  - Wall destruction bonus
- **Color-Coded**:
  - 🟢 Green (75-100): Excellent
  - 🟠 Orange (50-74): Good
  - 🔴 Red (0-49): Needs improvement
- **Live Updates**: Continuous calculation

### 6. **Historical Statistics** 📜
- **Total Games**: All-time game count
- **Win Rates**: Human vs AI percentages
- **Win Streaks**: Current streak display
- **Performance Trend**: Last 5 games analysis
  - 📈 Improving (60%+ wins)
  - ➡️ Stable (40-60% wins)
  - 📉 Declining (40%- wins)

### 7. **Performance Graph** 📊
- **Real-time Line Graph**: Last 20 data points
- **Dual Lines**: Human (green) vs AI (red)
- **Visual Comparison**: Easy performance tracking
- **Grid Background**: Clear reading
- **Auto-scaling**: Adapts to data

### 8. **Recommendations & Tips** 💡
- **Smart Suggestions**: Based on your gameplay
- **Risk-Based Advice**:
  - High risk → Play defensively
  - Low risk → Be more aggressive
- **Strategy Tips**:
  - Aggressive not working → Try balanced
  - Too defensive → Take more risks
- **Performance Guidance**:
  - Bomb efficiency tips
  - Power-up collection reminders
  - Escape route planning
- **Motivational Messages**:
  - Win streak encouragement
  - Comeback suggestions

---

## 📐 Panel Layout

```
┌─────────────────────────────────────┐
│      📊 GAME ANALYTICS              │
├─────────────────────────────────────┤
│ 🤖 AI OPPONENT                      │
│   Type: PPO                         │
│   Deep RL (Trained)                 │
│   Win Rate: 45.2%                   │
├─────────────────────────────────────┤
│ 📈 CURRENT GAME                     │
│   Time: 45s                         │
│   👤 Human:                         │
│     Moves: 23                       │
│     Bombs: 5                        │
│     Power-ups: 2                    │
│     Walls: 8                        │
│   🤖 AI:                            │
│     Moves: 25                       │
│     Bombs: 6                        │
│     Power-ups: 1                    │
│     Walls: 7                        │
├─────────────────────────────────────┤
│ ⚠️ RISK LEVELS                      │
│   Human: ████████░░░░ 65%          │
│   AI:    ███░░░░░░░░░ 25%          │
├─────────────────────────────────────┤
│ 🎯 STRATEGY                         │
│   Human: ⚔️ Aggressive              │
│   AI: 🛡️ Defensive                  │
├─────────────────────────────────────┤
│ ⭐ PERFORMANCE                      │
│   Human: ████████░░░░ 72           │
│   AI:    ██████░░░░░░ 58           │
├─────────────────────────────────────┤
│ 📜 HISTORY                          │
│   Total Games: 15                   │
│   Human: 60.0% | AI: 40.0%         │
│   🔥 Human Streak: 3                │
│   Trend: 📈 Improving               │
├─────────────────────────────────────┤
│ 📊 PERFORMANCE                      │
│   ┌───────────────────────────┐    │
│   │    /\  Human               │    │
│   │   /  \/\                   │    │
│   │  /      \  AI              │    │
│   │ /        \/                │    │
│   └───────────────────────────┘    │
├─────────────────────────────────────┤
│ 💡 TIPS                             │
│   ✅ Good gameplay! Keep it up!    │
│   💣 Place more strategic bombs    │
│   ⭐ Collect more power-ups        │
└─────────────────────────────────────┘
```

---

## 🔢 Metrics Explained

### Risk Calculation
```python
Risk = Σ(bomb_danger) + explosion_danger

bomb_danger = 50 * time_factor * distance_factor
  where:
    time_factor = (3.0 - bomb.timer) / 3.0
    distance_factor = (bomb_range - distance) / bomb_range

explosion_danger = 100 (if in explosion)
```

### Strategy Classification
```python
aggressive_ratio = aggressive_moves / total_moves

if ratio > 0.6:  → Aggressive
elif ratio < 0.4: → Defensive
else:             → Balanced
```

### Performance Score
```python
base_score = 50

+ bomb_efficiency (0-30): (bombs/moves) * 100
- survival_penalty (0-20): near_death * 5
+ powerup_bonus (0-10): powerups * 2
+ walls_bonus (0-10): walls_destroyed

Final: max(0, min(100, total))
```

---

## 💾 Data Persistence

### Storage Location
```
bomber_game/models/game_history.json
```

### Data Structure
```json
{
  "total_games": 15,
  "human_wins": 9,
  "ai_wins": 6,
  "draws": 0,
  "human_stats": {
    "total_moves": 450,
    "total_bombs": 120,
    "total_kills": 9,
    "best_win_streak": 5,
    "current_win_streak": 3
  },
  "ai_stats": {
    "total_moves": 480,
    "total_bombs": 135,
    "total_kills": 6,
    "best_win_streak": 3,
    "current_win_streak": 0
  },
  "games": [
    {
      "timestamp": "2025-10-12T19:54:07",
      "duration": 45.2,
      "winner": "Player",
      "ai_type": "PPO",
      "human": {
        "moves": 30,
        "bombs": 8,
        "strategy": "Aggressive",
        "avg_risk": 55.2,
        "performance": 72
      },
      "ai": {
        "moves": 32,
        "bombs": 9,
        "strategy": "Defensive",
        "avg_risk": 35.8,
        "performance": 58
      }
    }
  ]
}
```

### Retention Policy
- **Last 50 games** stored in file
- **Last 10 games** in memory for quick access
- **Cumulative stats** never deleted

---

## 🎮 Usage

### Automatic Tracking
Everything is tracked automatically:
- ✅ No manual input required
- ✅ Real-time updates
- ✅ Persistent across games
- ✅ Automatic saving

### Viewing Statistics
1. **During Game**: Right panel shows live stats
2. **After Game**: Stats saved automatically
3. **Next Game**: History loaded and displayed
4. **Restart**: Stats persist, new game begins

### Understanding Recommendations
```
⚠️ HIGH RISK → Avoid bomb zones
💡 LOW RISK → Be more aggressive
🎯 Strategy not working → Change approach
💣 Low bomb efficiency → Place more bombs
⭐ Few power-ups → Collect more
🛡️ Many near-deaths → Plan escape routes
🔥 Win streak → Keep it up!
💪 AI dominating → Change strategy
```

---

## 🔧 Technical Details

### Files
- **`bomber_game/game_statistics.py`**: Core statistics engine
- **`bomber_game/stats_panel.py`**: UI rendering
- **`bomber_game/game_engine.py`**: Integration

### Key Classes

#### `GameStatistics`
```python
# Initialize
stats = GameStatistics()

# Track events
stats.record_move(is_human, position, game_state)
stats.record_bomb(is_human)
stats.record_powerup(is_human)
stats.record_near_death(is_human)

# Get metrics
risk = stats.get_current_risk(is_human)
strategy = stats.get_strategy(is_human)
performance = stats.get_performance_score(is_human)
recommendations = stats.get_recommendations()

# Finish game
stats.finish_game(winner_name)
```

#### `StatsPanel`
```python
# Initialize
panel = StatsPanel(x, y, width, height)

# Render
panel.draw(screen, stats, game_state)
```

---

## 📊 Example Scenarios

### Scenario 1: Aggressive Player
```
Strategy: ⚔️ Aggressive
Risk: 75% (High)
Performance: 45 (Low)

Recommendations:
- ⚠️ HIGH RISK: Play more defensively
- 🎯 Try balanced approach - aggression isn't working
- 🛡️ Improve escape routes - plan ahead
```

### Scenario 2: Defensive Player
```
Strategy: 🛡️ Defensive
Risk: 15% (Low)
Performance: 55 (Medium)

Recommendations:
- 💡 LOW RISK: You can be more aggressive
- ⚔️ Be more aggressive - take more risks
- 💣 Place more bombs - you're too conservative
```

### Scenario 3: Balanced Player
```
Strategy: ⚖️ Balanced
Risk: 45% (Moderate)
Performance: 78 (High)

Recommendations:
- ✅ Good gameplay! Keep it up!
- ⭐ Collect more power-ups for advantage
```

### Scenario 4: Win Streak
```
Strategy: ⚖️ Balanced
Risk: 35% (Low)
Performance: 85 (Excellent)
Win Streak: 5

Recommendations:
- 🔥 ON FIRE! Keep up the great play!
- ✅ Good gameplay! Keep it up!
```

---

## 🎯 Tips for Best Results

### Improve Your Score
1. **Bomb Efficiency**: Place bombs strategically, not randomly
2. **Survival**: Avoid near-death situations
3. **Power-ups**: Collect them for bonuses
4. **Walls**: Destroy walls for points

### Lower Your Risk
1. **Watch Timers**: Monitor bomb countdowns
2. **Escape Routes**: Always have an exit
3. **Safe Zones**: Move to low-risk areas
4. **Prediction**: Anticipate explosions

### Optimize Strategy
1. **Aggressive**: When ahead, pressure opponent
2. **Defensive**: When behind, play safe
3. **Balanced**: Most versatile approach
4. **Adapt**: Change based on recommendations

---

## 🐛 Troubleshooting

### Stats Not Updating
- **Check**: Game is running (not paused)
- **Verify**: Actions are being performed
- **Restart**: Press R to restart game

### History Not Saving
- **Check**: `bomber_game/models/` directory exists
- **Permissions**: Write access to directory
- **Disk Space**: Sufficient space available

### Panel Not Visible
- **Resolution**: Ensure screen width > 1100px
- **Window**: Not minimized or hidden
- **Restart**: Restart game application

---

## 📈 Future Enhancements

### Planned Features
- [ ] Export statistics to CSV
- [ ] Detailed game replay
- [ ] Heatmap visualization
- [ ] Advanced analytics dashboard
- [ ] Multiplayer statistics
- [ ] Achievement system
- [ ] Leaderboards

---

## 🎓 Educational Value

### Learning Opportunities
- **Data Analysis**: Understanding metrics
- **Strategy**: Tactical decision-making
- **Risk Management**: Assessing danger
- **Performance Optimization**: Improving gameplay
- **Pattern Recognition**: Identifying trends

### STEM Skills
- **Mathematics**: Calculations and percentages
- **Statistics**: Data interpretation
- **Computer Science**: Algorithm understanding
- **Game Theory**: Strategic thinking

---

## 📞 Support

### Questions?
- Check this guide
- Review code comments
- Test different scenarios
- Experiment with strategies

### Feedback
- Report bugs via GitHub Issues
- Suggest features
- Share strategies
- Contribute improvements

---

**Enjoy the enhanced analytics and improve your gameplay! 📊🎮**

*Last Updated: 2025-10-12*  
*Version: 1.0*  
*Status: Production Ready*
