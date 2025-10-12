# Training Quick Start Guide

**Fixed the PyTorch issue! Ready to train.** 🚀

---

## ✅ Issue Fixed

**Problem:** Script was checking system Python instead of virtual environment
**Solution:** Updated `start_overnight_training.sh` to auto-detect and activate `.venv`

---

## 🚀 Three Ways to Start Training

### Option 1: Interactive Launcher (Recommended)
```bash
./start_overnight_training.sh
```
- Choose training mode (1h test, 8h overnight, 48h weekend)
- Choose execution mode (foreground, background, screen, tmux)
- Full control over settings

### Option 2: Quick Start (No Prompts)
```bash
./quick_train.sh
```
- Starts immediately in background
- Default 8-hour overnight training
- Saves PID to `training.pid`

### Option 3: Direct Python
```bash
source .venv/bin/activate
python overnight_training.py
```
- Run directly with Python
- Full control, no wrapper script

---

## 📊 Monitor Training

### Real-time Monitor
```bash
source .venv/bin/activate
python monitor_training.py
```

### View Logs
```bash
# Training output
tail -f training_output.log

# Detailed log
tail -f bomber_game/models/training_log.txt
```

### Check Progress
```bash
source .venv/bin/activate
python monitor_training.py --summary
```

---

## 🛑 Stop Training

### If you saved the PID:
```bash
kill $(cat training.pid)
```

### Or find the process:
```bash
ps aux | grep overnight_training
kill <PID>
```

### Graceful stop (saves checkpoint):
Press `Ctrl+C` if running in foreground

---

## 🔧 Troubleshooting

### PyTorch Not Found
```bash
# Activate virtual environment first
source .venv/bin/activate

# Verify PyTorch
python -c "import torch; print(torch.__version__)"

# If missing, install:
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Script Won't Run
```bash
# Make executable
chmod +x start_overnight_training.sh quick_train.sh

# Check virtual environment exists
ls -la .venv/
```

### Training Crashes
```bash
# Check logs
tail -50 bomber_game/models/training_log.txt

# Check output
tail -50 training_output.log
```

---

## 📁 Virtual Environment

Your project uses a virtual environment (`.venv/`):

**Activate it:**
```bash
source .venv/bin/activate
```

**Deactivate:**
```bash
deactivate
```

**Why?** Debian/Ubuntu uses "externally managed" Python, so we need a venv for packages.

---

## ✅ Pre-flight Checklist

Before starting overnight training:

- [x] Virtual environment exists (`.venv/`)
- [x] PyTorch installed in venv
- [x] Scripts are executable
- [x] Sufficient disk space (>1GB)
- [ ] System won't sleep/hibernate
- [ ] Ready to leave running overnight

---

## 🎯 Quick Commands

```bash
# Start training (easiest)
./quick_train.sh

# Monitor
source .venv/bin/activate && python monitor_training.py

# Check status
tail -f training_output.log

# Stop
kill $(cat training.pid)

# Resume (if stopped)
./quick_train.sh
```

---

## 📊 Expected Results

After 8 hours:
- **Episodes:** 8,000-10,000
- **Win Rate:** 40-55% (vs 30% heuristic)
- **Model saved:** `bomber_game/models/ppo_agent.pth`

---

## 💡 Tips

1. **Use `quick_train.sh`** for simplest start
2. **Monitor in another terminal** while training
3. **Check logs** if something seems wrong
4. **Be patient** - first hour shows slow progress
5. **Don't close terminal** if running in foreground

---

**Ready to train!** Run: `./quick_train.sh` 🚀
