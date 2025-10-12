# Overnight Training - Quick Reference

**TL;DR: Complete overnight PPO training system for Bomberman AI**

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Start training (easiest way)
./start_overnight_training.sh

# 2. Monitor progress (in another terminal)
python3 monitor_training.py

# 3. Check results in the morning
python3 monitor_training.py --summary
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `overnight_training.py` | Main training script with auto-checkpointing |
| `monitor_training.py` | Real-time progress monitoring & visualization |
| `start_overnight_training.sh` | Easy launcher with multiple modes |
| `OVERNIGHT_TRAINING_GUIDE.md` | Complete documentation |

---

## ⚙️ Training Modes

### 1. Quick Test (1 hour)
```bash
./start_overnight_training.sh
# Select option 1
# ~1,000 episodes, test configuration
```

### 2. Overnight (8 hours) - Default
```bash
./start_overnight_training.sh
# Select option 2 or press Enter
# ~10,000 episodes, full training
```

### 3. Weekend (48 hours)
```bash
./start_overnight_training.sh
# Select option 3
# ~50,000 episodes, maximum training
```

---

## 📊 Key Features

### Automatic Checkpointing ✅
- Saves every 100 episodes
- Autosaves every 30 minutes
- Keeps best performing model
- Resume from any checkpoint

### Progress Tracking ✅
- Real-time win rate monitoring
- Reward tracking over time
- Performance visualization
- Detailed logging

### Adaptive Learning ✅
- Learning rate decay (3e-4 → 1e-5)
- Early stopping on plateau
- Performance-based saves
- Optimized hyperparameters

### Safety Features ✅
- Graceful Ctrl+C handling
- Time limit enforcement
- Automatic state saving
- Error recovery

---

## 📈 Expected Results

### After 8 Hours Overnight Training

| Metric | Expected Value |
|--------|----------------|
| Episodes Completed | 8,000 - 10,000 |
| Win Rate vs Heuristic | 40% - 55% |
| Average Reward | 50 - 100+ |
| Best Win Rate | 50% - 60%+ |

### Performance Timeline

```
Hour 1:  Win Rate ~15-20% (learning basics)
Hour 2:  Win Rate ~20-30% (developing strategy)
Hour 4:  Win Rate ~30-40% (tactical improvements)
Hour 8:  Win Rate ~40-55% (refined play)
```

---

## 🔍 Monitoring

### Real-time Monitor
```bash
python3 monitor_training.py
# Refreshes every 30 seconds
# Shows: episode, win rate, rewards, ETA
```

### Quick Status Check
```bash
python3 monitor_training.py --summary
# One-time summary, no continuous monitoring
```

### Generate Plots
```bash
python3 monitor_training.py --plots
# Creates: win_rate.png, avg_reward.png, etc.
# Saved to: bomber_game/models/plots/
```

### View Logs
```bash
# Training log
tail -f bomber_game/models/training_log.txt

# Output log (if using nohup)
tail -f training_output.log
```

---

## 📂 Output Files

```
bomber_game/models/
├── ppo_agent.pth              ← Final trained model (use this!)
├── training_stats.json        ← Complete statistics
├── overnight_progress.json    ← Current progress
├── training_log.txt          ← Detailed log
├── checkpoints/
│   ├── latest_checkpoint.pth ← Resume from here
│   ├── checkpoint_ep*_best_*.pth
│   └── checkpoint_ep*_periodic_*.pth
└── plots/
    ├── win_rate.png
    ├── avg_reward.png
    └── combined_progress.png
```

---

## 🎮 Using Trained Model

### Play Against AI
```bash
python3 play_bomberman.py
# Automatically uses best trained model
```

### Test Performance
```bash
python3 quick_test_agent.py
# Benchmark against heuristic
```

### Check Model Stats
```bash
python3 -c "
from bomber_game.model_selector import ModelSelector
selector = ModelSelector('bomber_game/models')
print(selector.get_performance_report())
"
```

---

## 🔄 Resume Training

Training automatically resumes from latest checkpoint:

```bash
# Just run again - it finds the checkpoint automatically
./start_overnight_training.sh
```

Or manually:
```bash
python3 overnight_training.py
# Looks for: bomber_game/models/checkpoints/latest_checkpoint.pth
```

---

## 🛠️ Troubleshooting

### Training Won't Start
```bash
# Install PyTorch
pip3 install torch

# Verify installation
python3 -c "import torch; print('OK')"
```

### Monitor Shows No Data
```bash
# Wait a few minutes for first checkpoint
# Or check if training is actually running
ps aux | grep overnight_training
```

### Low Win Rate After Training
- Normal if < 4 hours of training
- Check reward function tuning
- Verify heuristic baseline (~30%)
- Try longer training duration

### Out of Memory
```bash
# Edit overnight_training.py:
BATCH_SIZE = 64  # Reduce from 128
UPDATE_INTERVAL = 2048  # Reduce from 4096
```

---

## 💡 Pro Tips

### 1. System Preparation
```bash
# Prevent system sleep (Linux)
sudo systemctl mask sleep.target suspend.target

# Or use: caffeine, nosleep, etc.
```

### 2. Optimal Setup
```bash
# Terminal 1: Training
./start_overnight_training.sh

# Terminal 2: Monitor
python3 monitor_training.py

# Terminal 3: System resources
htop
```

### 3. Best Practices
- Start with default settings
- Monitor first hour closely
- Check progress every few hours
- Generate plots in the morning
- Backup best checkpoint

### 4. Performance Tuning
```python
# For faster training (less stable):
UPDATE_INTERVAL = 2048
LEARNING_RATE_START = 5e-4

# For more stable training (slower):
UPDATE_INTERVAL = 8192
LEARNING_RATE_START = 1e-4
```

---

## 📊 Training Configuration

### Default Hyperparameters

```python
TOTAL_EPISODES = 10000      # Target episodes
TRAINING_HOURS = 8          # Max duration
UPDATE_INTERVAL = 4096      # Steps per update
BATCH_SIZE = 128            # Training batch size
LEARNING_RATE_START = 3e-4  # Initial LR
LEARNING_RATE_END = 1e-5    # Final LR
CLIP_EPSILON = 0.2          # PPO clip parameter
GAMMA = 0.99                # Discount factor
GAE_LAMBDA = 0.95           # GAE parameter
```

### Reward Function

```python
+200  Win the game
-200  Lose the game
+20   Destroy soft wall
+15   Collect power-up
+20   Strategic bomb placement
+30   Survive dangerous situation
+10   Safe bomb placement
-25   Dangerous bomb placement
-0.5  Each step (efficiency)
```

---

## ✅ Success Checklist

### Before Starting
- [ ] PyTorch installed
- [ ] Sufficient disk space (>1GB)
- [ ] System won't sleep
- [ ] Configuration reviewed

### During Training
- [ ] Check after 1 hour
- [ ] Monitor system resources
- [ ] Verify checkpoints saving

### After Training
- [ ] Generate final plots
- [ ] Review summary
- [ ] Test trained model
- [ ] Backup best checkpoint

---

## 🎯 Success Criteria

Your training is successful if:

✅ **Win Rate > 40%** (vs 30% heuristic baseline)
✅ **Consistent improvement** over time
✅ **No crashes** or errors
✅ **Regular checkpoints** saved
✅ **Good gameplay** in actual matches

---

## 📞 Quick Commands Reference

```bash
# Start training
./start_overnight_training.sh

# Monitor progress
python3 monitor_training.py

# View summary
python3 monitor_training.py --summary

# Generate plots
python3 monitor_training.py --plots

# View logs
tail -f bomber_game/models/training_log.txt

# Check running processes
ps aux | grep overnight_training

# Stop training (gracefully)
# Press Ctrl+C in training terminal
# Or: kill <PID>

# Play with trained AI
python3 play_bomberman.py

# Test AI performance
python3 quick_test_agent.py
```

---

## 🚀 Next Steps

1. **Start Training**
   ```bash
   ./start_overnight_training.sh
   ```

2. **Monitor Progress**
   ```bash
   python3 monitor_training.py
   ```

3. **Check Results** (morning)
   ```bash
   python3 monitor_training.py --summary
   python3 monitor_training.py --plots
   ```

4. **Test the Model**
   ```bash
   python3 play_bomberman.py
   ```

5. **Continue Training** (if needed)
   ```bash
   ./start_overnight_training.sh
   # Will resume automatically
   ```

---

**Ready to train! 🌙🚀**

For detailed documentation, see `OVERNIGHT_TRAINING_GUIDE.md`
