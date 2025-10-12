---
layout: default
title: Home
---

<div class="hero">
  <h1>💨 Proutman - AI Bomberman Game</h1>
  <p class="lead">Educational Bomberman game with reinforcement learning AI</p>
  <div class="hero-buttons">
    <a href="{{ site.baseurl }}/docs/play/" class="btn btn-primary btn-lg">🎮 Play Demo</a>
    <a href="{{ site.baseurl }}/docs/getting-started" class="btn btn-secondary btn-lg">📚 Get Started</a>
    <a href="https://github.com/xaviercallens/xgames" class="btn btn-outline btn-lg">💻 GitHub</a>
  </div>
</div>

## 🎯 Features

<div class="features-grid">
  <div class="feature">
    <h3>🎮 Web Demo</h3>
    <p>Play directly in your browser using WebAssembly. No installation required!</p>
    <a href="{{ site.baseurl }}/docs/play/">Try it now →</a>
  </div>

  <div class="feature">
    <h3>🤖 AI Opponents</h3>
    <p>Battle against trained PPO agents or enhanced heuristic AI with 40-66% win rates.</p>
    <a href="{{ site.baseurl }}/docs/ai-agents">Learn more →</a>
  </div>

  <div class="feature">
    <h3>🧠 Reinforcement Learning</h3>
    <p>Train your own AI using PPO, DQN, or custom algorithms. Overnight training included!</p>
    <a href="{{ site.baseurl }}/docs/training">Start training →</a>
  </div>

  <div class="feature">
    <h3>📊 Performance Tracking</h3>
    <p>Real-time statistics, win rate monitoring, and performance visualization.</p>
    <a href="{{ site.baseurl }}/docs/statistics">View stats →</a>
  </div>

  <div class="feature">
    <h3>🎓 Educational</h3>
    <p>Learn Python, game development, and AI through hands-on coding.</p>
    <a href="{{ site.baseurl }}/docs/tutorials">Tutorials →</a>
  </div>

  <div class="feature">
    <h3>🔧 Customizable</h3>
    <p>Modify game rules, create custom maps, and implement your own AI strategies.</p>
    <a href="{{ site.baseurl }}/docs/customization">Customize →</a>
  </div>
</div>

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/xaviercallens/xgames.git
cd xgames

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Play the game
python play_bomberman.py

# Train AI overnight
./quick_train.sh
```

## 📊 AI Performance

Our trained agents achieve impressive results:

| Agent Type | Win Rate | Training Time | Description |
|------------|----------|---------------|-------------|
| **Enhanced Heuristic** | 66% | N/A | Expert-level rule-based AI |
| **PPO (Trained)** | 40-55% | 8 hours | Reinforcement learning |
| **Pretrained Model** | 25% | Instant | Bootstrap model |
| **Simple Heuristic** | 30% | N/A | Baseline |

## 🎮 Game Modes

- **🆚 Player vs AI**: Test your skills against trained agents
- **🤖 AI vs AI**: Watch agents battle each other
- **🎓 Training Mode**: Train your own reinforcement learning agents
- **🌐 Web Demo**: Play in your browser with WebAssembly

## 🛠️ Technology Stack

- **Game Engine**: Pygame
- **AI Framework**: PyTorch
- **RL Algorithms**: PPO, DQN
- **Web**: Pygbag (Python to WebAssembly)
- **Visualization**: Matplotlib
- **Documentation**: Jekyll, GitHub Pages

## 📚 Documentation

- [Getting Started]({{ site.baseurl }}/docs/getting-started) - Installation and setup
- [Game Controls]({{ site.baseurl }}/docs/controls) - How to play
- [AI Training Guide]({{ site.baseurl }}/docs/training) - Train your own agents
- [API Reference]({{ site.baseurl }}/docs/api) - Code documentation
- [Tutorials]({{ site.baseurl }}/docs/tutorials) - Step-by-step guides

## 🎯 Project Goals

1. **Educational**: Teach Python, game development, and AI concepts
2. **Practical**: Provide working examples of RL algorithms
3. **Accessible**: Easy to use, well-documented, beginner-friendly
4. **Extensible**: Modular design for easy customization

## 🤝 Contributing

Contributions are welcome! Check out our [contribution guidelines](https://github.com/xaviercallens/xgames/blob/main/CONTRIBUTING.md).

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [GitHub Repository](https://github.com/xaviercallens/xgames)
- [Play Web Demo]({{ site.baseurl }}/docs/play/)
- [Report Issues](https://github.com/xaviercallens/xgames/issues)
- [Discussions](https://github.com/xaviercallens/xgames/discussions)

---

<div class="cta-section">
  <h2>Ready to Play?</h2>
  <p>Try the web demo or download and run locally</p>
  <a href="{{ site.baseurl }}/docs/play/" class="btn btn-primary btn-lg">🎮 Play Now</a>
  <a href="{{ site.baseurl }}/docs/getting-started" class="btn btn-secondary btn-lg">📥 Download</a>
</div>

<style>
.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 3em;
  margin-bottom: 20px;
}

.hero .lead {
  font-size: 1.5em;
  margin-bottom: 30px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-block;
  padding: 12px 30px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #fff;
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

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-outline:hover {
  background: white;
  color: #667eea;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin: 40px 0;
}

.feature {
  padding: 30px;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.feature:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transform: translateY(-5px);
}

.feature h3 {
  margin-top: 0;
  color: #667eea;
}

.feature a {
  color: #667eea;
  text-decoration: none;
  font-weight: bold;
}

.feature a:hover {
  text-decoration: underline;
}

.cta-section {
  text-align: center;
  padding: 60px 20px;
  background: #f6f8fa;
  border-radius: 10px;
  margin-top: 60px;
}

.cta-section h2 {
  margin-top: 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

table th,
table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e1e4e8;
}

table th {
  background: #f6f8fa;
  font-weight: bold;
}

table tr:hover {
  background: #f6f8fa;
}
</style>
