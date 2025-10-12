# 🎮 WebAssembly Demo Guide - Make Proutman Playable in Browser!

## 🌐 Current Status

✅ **GitHub Pages Live:**
- Main site: https://xaviercallens.github.io/xgames/
- Demo page: https://xaviercallens.github.io/xgames/demo.html

📄 **Current Demo:**
- Static page with screenshots
- Download instructions
- Game controls
- Quick start guide

🎯 **Goal:**
- Add fully playable browser version
- No installation required
- Play directly on website

---

## 🚀 Option 1: Pygbag (Recommended)

**Pygbag** converts Pygame games to WebAssembly for browser play!

### **Installation:**

```bash
# Activate your environment
source game_dev_env/bin/activate

# Install pygbag
pip install pygbag
```

### **Prepare Your Game:**

1. **Create a web-ready version:**

```bash
# Create web directory
mkdir -p web_demo
cp play_bomberman.py web_demo/main.py
```

2. **Modify main.py for web:**

Add this at the top of `web_demo/main.py`:

```python
import asyncio
import platform

# Web compatibility
if platform.system() == "Emscripten":
    import asyncio
    RUNNING_IN_BROWSER = True
else:
    RUNNING_IN_BROWSER = False
```

3. **Make game loop async:**

```python
async def main():
    # Your game code here
    while running:
        # Game loop
        if RUNNING_IN_BROWSER:
            await asyncio.sleep(0)  # Yield to browser

if __name__ == "__main__":
    if RUNNING_IN_BROWSER:
        asyncio.run(main())
    else:
        main()
```

### **Build for Web:**

```bash
# Build the game
pygbag web_demo/main.py

# This creates a build/ directory with:
# - index.html
# - Python WebAssembly files
# - Your game assets
```

### **Deploy to GitHub Pages:**

```bash
# Copy build to docs/play/
mkdir -p docs/play
cp -r build/web/* docs/play/

# Commit and push
git add docs/play/
git commit -m "Add playable WebAssembly demo"
git push
```

### **Update demo.html:**

Replace "Coming Soon" section with:

```html
<div style="text-align: center; margin: 40px 0;">
    <h2>🎮 Play Now in Your Browser!</h2>
    <iframe 
        src="play/index.html" 
        width="800" 
        height="600" 
        style="border: 2px solid #667eea; border-radius: 15px;"
        allowfullscreen>
    </iframe>
    <p style="margin-top: 20px;">
        <strong>Controls:</strong> WASD or Arrow Keys to move, SPACE for bombs!
    </p>
</div>
```

---

## 🚀 Option 2: Brython (Python in Browser)

**Brython** runs Python directly in the browser using JavaScript.

### **Installation:**

```bash
pip install brython
```

### **Setup:**

1. **Create Brython version:**

```bash
mkdir -p docs/brython_demo
cd docs/brython_demo
brython-cli --install
```

2. **Create HTML file:**

```html
<!DOCTYPE html>
<html>
<head>
    <script src="brython.js"></script>
    <script src="brython_stdlib.js"></script>
</head>
<body onload="brython()">
    <canvas id="game-canvas" width="800" height="600"></canvas>
    <script type="text/python">
        # Your Proutman game code here
        # Simplified version for browser
    </script>
</body>
</html>
```

**Note:** Brython has limitations with Pygame. Better for simple games.

---

## 🚀 Option 3: HTML5/JavaScript Rewrite

**Rewrite the game in JavaScript** for native browser support.

### **Technologies:**

- **Phaser.js** - Popular HTML5 game framework
- **PixiJS** - 2D rendering engine
- **Vanilla JavaScript** - No framework

### **Example with Phaser:**

```javascript
// game.js
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

function preload() {
    // Load Proutman assets
    this.load.image('player', 'assets/prout_man_player.png');
    this.load.image('bomb', 'assets/bomb.png');
}

function create() {
    // Create game objects
    this.player = this.add.sprite(100, 100, 'player');
}

function update() {
    // Game loop
    // Handle input, update positions, check collisions
}
```

---

## 🎯 Recommended Approach

### **Quick Win: Pygbag**

**Pros:**
- ✅ Keep Python code
- ✅ Minimal changes needed
- ✅ Works with Pygame
- ✅ Fast to implement

**Cons:**
- ⚠️ Larger file size
- ⚠️ Loading time
- ⚠️ Some Pygame features limited

### **Best Quality: JavaScript Rewrite**

**Pros:**
- ✅ Native browser support
- ✅ Fast loading
- ✅ Full control
- ✅ Best performance

**Cons:**
- ⚠️ Complete rewrite needed
- ⚠️ Time-consuming
- ⚠️ Different language

---

## 📋 Step-by-Step: Pygbag Implementation

### **1. Install Pygbag (5 minutes)**

```bash
source game_dev_env/bin/activate
pip install pygbag
```

### **2. Prepare Game (15 minutes)**

```bash
# Create web version
mkdir -p web_demo
cp play_bomberman.py web_demo/main.py

# Copy assets
cp -r bomber_game web_demo/
```

### **3. Modify for Web (20 minutes)**

Edit `web_demo/main.py`:

```python
import asyncio
import platform

# Check if running in browser
RUNNING_IN_BROWSER = platform.system() == "Emscripten"

async def main():
    """Main game loop - async for web compatibility"""
    # Your existing game code
    from bomber_game.game_engine import main as game_main
    
    if RUNNING_IN_BROWSER:
        # Web-compatible version
        while True:
            game_main()
            await asyncio.sleep(0)
    else:
        # Desktop version
        game_main()

if __name__ == "__main__":
    if RUNNING_IN_BROWSER:
        asyncio.run(main())
    else:
        main()
```

### **4. Build (5 minutes)**

```bash
cd web_demo
pygbag main.py --build

# Wait for build to complete
# Creates build/web/ directory
```

### **5. Deploy (5 minutes)**

```bash
# Copy to docs
cd ..
mkdir -p docs/play
cp -r web_demo/build/web/* docs/play/

# Commit and push
git add docs/play/
git commit -m "Add playable WebAssembly demo with Pygbag"
git push
```

### **6. Update Website (10 minutes)**

Edit `docs/demo.html` - replace "Coming Soon" with:

```html
<div class="playable-demo">
    <h2 style="color: #667eea; font-size: 2.5em; margin: 30px 0;">
        🎮 Play Proutman Now!
    </h2>
    <iframe 
        src="play/index.html" 
        width="800" 
        height="600" 
        style="border: 3px solid #667eea; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);"
        allowfullscreen>
    </iframe>
    <p style="margin-top: 20px; font-size: 1.2em;">
        <strong>Controls:</strong> 
        WASD or Arrow Keys = Move | 
        SPACE = Drop Bomb 💨 | 
        C = Place Caca 💩
    </p>
</div>
```

### **7. Test (5 minutes)**

- Visit: https://xaviercallens.github.io/xgames/demo.html
- Game should load in iframe
- Test controls work
- Verify gameplay

**Total Time: ~1 hour**

---

## 🐛 Troubleshooting

### **Pygbag Build Fails:**

```bash
# Update pygbag
pip install --upgrade pygbag

# Check Python version (needs 3.9+)
python --version

# Try with verbose output
pygbag main.py --build --verbose
```

### **Game Doesn't Load:**

1. Check browser console for errors (F12)
2. Verify all assets are included
3. Check file paths are correct
4. Try different browser

### **Performance Issues:**

1. Reduce game resolution
2. Optimize asset sizes
3. Simplify graphics
4. Reduce AI complexity

---

## 📊 Comparison

| Feature | Pygbag | Brython | JavaScript |
|---------|--------|---------|------------|
| **Setup Time** | 1 hour | 2 hours | 1 week |
| **Code Reuse** | 90% | 70% | 0% |
| **Performance** | Good | Fair | Excellent |
| **File Size** | Large | Medium | Small |
| **Compatibility** | Good | Limited | Excellent |
| **Pygame Support** | Yes | No | N/A |

**Recommendation:** Start with **Pygbag** for quick results!

---

## ✅ Success Checklist

After implementation:

- [ ] Game loads in browser
- [ ] Controls work (WASD, SPACE, C)
- [ ] Graphics display correctly
- [ ] AI opponent works
- [ ] Bombs explode properly
- [ ] Collisions detect correctly
- [ ] Game over/restart works
- [ ] Mobile responsive (optional)

---

## 🎉 Next Steps

1. **Try Pygbag** (recommended)
2. **Test thoroughly**
3. **Share playable demo**
4. **Get feedback**
5. **Iterate and improve**

---

## 📚 Resources

- [Pygbag Documentation](https://pygame-web.github.io/)
- [Pygame WebAssembly Guide](https://pygame-web.github.io/wiki/pygbag/)
- [Brython Documentation](https://brython.info/)
- [Phaser.js](https://phaser.io/)

---

**Ready to make Proutman playable in the browser!** 🎮🌐✨

**Start with Pygbag for fastest results!** 🚀
