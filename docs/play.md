---
layout: default
title: Play Demo
permalink: /docs/play/
---

# 🎮 Play Proutman - Web Demo

<div class="demo-container">
  <div class="demo-info">
    <h2>Browser-Based Bomberman</h2>
    <p>Play directly in your browser using WebAssembly technology. No installation required!</p>
    
    <h3>🎯 Controls</h3>
    <ul>
      <li><strong>WASD</strong> or <strong>Arrow Keys</strong> - Move</li>
      <li><strong>SPACE</strong> - Place bomb</li>
      <li><strong>ESC</strong> - Pause/Menu</li>
      <li><strong>R</strong> - Restart (when game over)</li>
    </ul>

    <h3>🎲 Game Rules</h3>
    <ul>
      <li>Destroy soft walls to clear paths</li>
      <li>Collect power-ups for advantages</li>
      <li>Avoid explosions and enemy bombs</li>
      <li>Eliminate the AI opponent to win</li>
    </ul>

    <h3>💎 Power-ups</h3>
    <ul>
      <li><strong>Bomb+</strong> - Increase max bombs</li>
      <li><strong>Fire+</strong> - Increase explosion range</li>
      <li><strong>Speed+</strong> - Move faster</li>
    </ul>
  </div>

  <div class="demo-frame">
    <iframe 
      src="{{ site.baseurl }}/docs/play/index.html" 
      width="100%" 
      height="800px" 
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen>
    </iframe>
    <p class="demo-note">
      💡 <strong>Tip:</strong> Click inside the game area to enable keyboard controls
    </p>
  </div>
</div>

## 🤖 AI Opponent

You're playing against an **Enhanced Heuristic AI** with:
- **Win Rate**: ~66% (expert level)
- **Strategy**: A* pathfinding, danger prediction, strategic bomb placement
- **Difficulty**: Challenging but beatable!

## 🚀 Want More?

<div class="cta-grid">
  <div class="cta-card">
    <h3>📥 Download Desktop Version</h3>
    <p>Full-featured game with more AI opponents and training modes</p>
    <a href="{{ site.baseurl }}/docs/getting-started" class="btn btn-primary">Get Started</a>
  </div>

  <div class="cta-card">
    <h3>🧠 Train Your Own AI</h3>
    <p>Use reinforcement learning to create custom AI agents</p>
    <a href="{{ site.baseurl }}/docs/training" class="btn btn-primary">Learn How</a>
  </div>

  <div class="cta-card">
    <h3>💻 View Source Code</h3>
    <p>Explore the implementation and contribute</p>
    <a href="https://github.com/xaviercallens/xgames" class="btn btn-primary">GitHub</a>
  </div>
</div>

## 🐛 Troubleshooting

### Game Won't Load?
- **Clear browser cache** (Ctrl+Shift+R)
- **Try a different browser** (Chrome, Firefox, Edge recommended)
- **Check console** for errors (F12 → Console tab)

### Controls Not Working?
- **Click inside the game area** to focus
- **Refresh the page** if needed
- **Disable browser extensions** that might interfere

### Performance Issues?
- **Close other tabs** to free up memory
- **Use a modern browser** with WebAssembly support
- **Try the desktop version** for better performance

## 📊 Technical Details

- **Engine**: Pygame compiled to WebAssembly
- **Framework**: Pygbag 0.9.2
- **Python**: 3.12
- **Size**: ~7.3 MB (includes game + AI)
- **Platform**: Runs in any modern browser

---

<div class="feedback-section">
  <h2>💬 Feedback</h2>
  <p>Found a bug or have suggestions? <a href="https://github.com/xaviercallens/xgames/issues">Report it on GitHub</a></p>
</div>

<style>
.demo-container {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 30px;
  margin: 30px 0;
}

@media (max-width: 968px) {
  .demo-container {
    grid-template-columns: 1fr;
  }
}

.demo-info {
  background: #f6f8fa;
  padding: 20px;
  border-radius: 8px;
}

.demo-info h3 {
  margin-top: 20px;
  color: #667eea;
}

.demo-info ul {
  padding-left: 20px;
}

.demo-info li {
  margin: 8px 0;
}

.demo-frame {
  background: #fff;
  border: 2px solid #e1e4e8;
  border-radius: 8px;
  padding: 10px;
}

.demo-frame iframe {
  border-radius: 5px;
  display: block;
}

.demo-note {
  text-align: center;
  color: #666;
  margin-top: 10px;
  font-size: 0.9em;
}

.cta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.cta-card {
  background: #f6f8fa;
  padding: 25px;
  border-radius: 8px;
  text-align: center;
}

.cta-card h3 {
  margin-top: 0;
  color: #667eea;
}

.btn {
  display: inline-block;
  padding: 10px 25px;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn:hover {
  background: #5568d3;
  transform: translateY(-2px);
}

.feedback-section {
  text-align: center;
  padding: 40px 20px;
  background: #f6f8fa;
  border-radius: 8px;
  margin-top: 40px;
}

.feedback-section h2 {
  margin-top: 0;
}
</style>
