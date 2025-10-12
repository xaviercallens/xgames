---
layout: default
title: Getting Started
permalink: /docs/getting-started/
---

# 🚀 Getting Started

Get up and running with Proutman in minutes!

## 📋 Prerequisites

- **Python 3.8+** (3.11 recommended)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **1GB+ disk space**

## 🔧 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/xaviercallens/xgames.git
cd xgames
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Pygame** - Game engine
- **PyTorch** - AI/ML framework
- **NumPy** - Numerical computing
- **Matplotlib** - Visualization

## 🎮 Quick Start

### Play the Game

```bash
python play_bomberman.py
```

**Controls:**
- WASD or Arrow Keys - Move
- SPACE - Place bomb
- ESC - Pause
- R - Restart (when game over)

### Train AI Overnight

```bash
./quick_train.sh
```

Monitor progress:
```bash
python monitor_training.py
```

### Test AI Performance

```bash
python quick_test_agent.py
```

## 📁 Project Structure

```
xgames/
├── bomber_game/          # Core game engine
│   ├── agents/          # AI agents (PPO, DQN, Heuristic)
│   ├── entities/        # Game entities (Player, Bomb, etc.)
│   ├── models/          # Trained AI models
│   └── game_engine.py   # Main game loop
├── docs/                # Documentation & web demo
│   └── play/           # WebAssembly demo
├── examples/            # Example games
├── play_bomberman.py    # Main game launcher
├── overnight_training.py # AI training script
└── requirements.txt     # Dependencies
```

## 🎯 Next Steps

<div class="next-steps-grid">
  <div class="step-card">
    <h3>🎮 Play the Game</h3>
    <p>Try the web demo or run locally</p>
    <a href="{{ site.baseurl }}/docs/play/">Play Now →</a>
  </div>

  <div class="step-card">
    <h3>🤖 Understand AI</h3>
    <p>Learn about the AI opponents</p>
    <a href="{{ site.baseurl }}/docs/ai-agents/">AI Agents →</a>
  </div>

  <div class="step-card">
    <h3>🧠 Train Your AI</h3>
    <p>Create custom AI agents</p>
    <a href="{{ site.baseurl }}/docs/training/">Training Guide →</a>
  </div>

  <div class="step-card">
    <h3>📚 Read Tutorials</h3>
    <p>Step-by-step guides</p>
    <a href="{{ site.baseurl }}/docs/tutorials/">Tutorials →</a>
  </div>
</div>

## 🐛 Troubleshooting

### PyTorch Installation Issues

**On Debian/Ubuntu:**
```bash
# Use virtual environment (required)
python3 -m venv .venv
source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Pygame Not Working

```bash
# Install system dependencies (Linux)
sudo apt-get install python3-pygame

# Or reinstall in venv
pip install --force-reinstall pygame
```

### Permission Errors

```bash
# Make scripts executable
chmod +x *.sh

# Or run with bash
bash quick_train.sh
```

## 💡 Tips

1. **Always activate virtual environment** before running scripts
2. **Use `quick_train.sh`** for easiest AI training
3. **Monitor training** in a separate terminal
4. **Check logs** if something goes wrong
5. **Start with web demo** to see what's possible

## 📊 System Requirements

### Minimum
- **CPU**: Dual-core 2GHz
- **RAM**: 2GB
- **Storage**: 500MB
- **OS**: Linux, macOS, Windows

### Recommended
- **CPU**: Quad-core 2.5GHz+
- **RAM**: 4GB+
- **Storage**: 2GB
- **OS**: Linux (best performance)

## 🔗 Useful Links

- [GitHub Repository](https://github.com/xaviercallens/xgames)
- [Report Issues](https://github.com/xaviercallens/xgames/issues)
- [Discussions](https://github.com/xaviercallens/xgames/discussions)
- [Contributing Guide](https://github.com/xaviercallens/xgames/blob/main/CONTRIBUTING.md)

## 📞 Need Help?

- **Check the docs** - Most questions are answered here
- **Search issues** - Someone might have had the same problem
- **Ask on Discussions** - Community support
- **Open an issue** - For bugs or feature requests

---

<div class="success-section">
  <h2>✅ Ready to Go!</h2>
  <p>You're all set! Start playing or training your AI.</p>
  <a href="{{ site.baseurl }}/docs/play/" class="btn btn-primary">Play Demo</a>
  <a href="{{ site.baseurl }}/docs/training/" class="btn btn-secondary">Train AI</a>
</div>

<style>
.next-steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.step-card {
  background: #f6f8fa;
  padding: 25px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.step-card h3 {
  margin-top: 0;
  color: #667eea;
}

.step-card a {
  color: #667eea;
  text-decoration: none;
  font-weight: bold;
}

.step-card a:hover {
  text-decoration: underline;
}

.success-section {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  margin-top: 40px;
}

.success-section h2 {
  margin-top: 0;
}

.btn {
  display: inline-block;
  padding: 12px 30px;
  margin: 5px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.btn-secondary {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: rgba(255,255,255,0.3);
}
</style>
