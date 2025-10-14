# 🚀 Deploy Proutman to PythonAnywhere

## Overview

This guide will help you deploy Proutman as a **web-based game** on PythonAnywhere, making it playable from anywhere in the world!

**Your PythonAnywhere Account**: https://www.pythonanywhere.com/user/callensxavier/

---

## 🎯 Deployment Strategy

Since Proutman is a **Pygame-based desktop game**, we'll deploy it as a **web application** using one of these approaches:

### Option 1: Pygame in Browser (Recommended)
Convert Proutman to run in the browser using **Pygbag** (Pygame for WebAssembly)

### Option 2: Flask Web Demo
Deploy the existing `web_demo` as a Flask application

### Option 3: Game Streaming
Stream the game using a web-based VNC/remote desktop

---

## 📋 Prerequisites

- ✅ PythonAnywhere account: `callensxavier`
- ✅ GitHub repository with Proutman code
- ✅ Basic knowledge of terminal commands

---

## 🚀 Option 1: Pygbag Deployment (Best for Gaming)

### Step 1: Prepare the Game for Web

**On your local machine:**

```bash
cd /home/kalxav/CascadeProjects/windsurf-project-2

# Install pygbag
pip install pygbag

# Create web-compatible version
mkdir -p web_build
cp play_bomberman.py web_build/main.py
cp -r bomber_game web_build/
```

### Step 2: Modify for Web Compatibility

Create `web_build/main.py`:

```python
#!/usr/bin/env python3
"""
Proutman - Web Version
Optimized for browser play via Pygbag
"""

import asyncio
import pygame
import sys
import os

# Add bomber_game to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bomber_game.game_engine import BombermanGame

async def main():
    """Main game loop for web."""
    game = BombermanGame(show_splash=True)
    
    while game.running:
        game.handle_events()
        
        if not game.paused:
            dt = game.clock.tick(60) / 1000.0
            game.update(dt)
        
        game.render()
        
        # Yield control to browser
        await asyncio.sleep(0)
    
    pygame.quit()

# Start the game
asyncio.run(main())
```

### Step 3: Build for Web

```bash
cd web_build
pygbag main.py --build
```

This creates a `build/web` directory with HTML/JS files.

### Step 4: Deploy to PythonAnywhere

**Login to PythonAnywhere:**
1. Go to https://www.pythonanywhere.com/
2. Login with username: `callensxavier`
3. Go to **Files** tab

**Upload the web build:**
```bash
# On your local machine, create a zip
cd web_build/build/web
zip -r proutman_web.zip *

# Upload via PythonAnywhere Files interface
# Or use rsync/scp
```

**Serve as static files:**
1. Go to **Web** tab
2. Add a new web app
3. Choose **Static files only**
4. Set URL: `/proutman`
5. Set Directory: `/home/callensxavier/proutman_web`
6. Click **Reload**

**Access your game:**
```
https://callensxavier.pythonanywhere.com/proutman/
```

---

## 🚀 Option 2: Flask Web Demo (Easier, Limited Features)

This deploys the existing `web_demo` directory.

### Step 1: Push Code to GitHub

**On your local machine:**

```bash
cd /home/kalxav/CascadeProjects/windsurf-project-2

# Ensure code is committed
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git push origin main
```

### Step 2: Clone on PythonAnywhere

**Login to PythonAnywhere Console:**

1. Go to https://www.pythonanywhere.com/user/callensxavier/
2. Open a **Bash console**
3. Run these commands:

```bash
# Clone your repository
git clone https://github.com/xaviercallens/xgames.git proutman
cd proutman

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask pygame numpy torch
```

### Step 3: Create Flask App

Create `/home/callensxavier/proutman/flask_app.py`:

```python
"""
Proutman Flask Web Application
Serves the web demo on PythonAnywhere
"""

from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DEMO_DIR = os.path.join(BASE_DIR, 'web_demo')

@app.route('/')
def index():
    """Main page."""
    return send_from_directory(WEB_DEMO_DIR, 'index.html')

@app.route('/demo.html')
def demo():
    """Demo page."""
    return send_from_directory(WEB_DEMO_DIR, 'demo.html')

@app.route('/play.html')
def play():
    """Play page."""
    return send_from_directory(WEB_DEMO_DIR, 'play.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(WEB_DEMO_DIR, filename)

@app.route('/bomber_game/<path:filename>')
def serve_game_files(filename):
    """Serve game files."""
    game_dir = os.path.join(WEB_DEMO_DIR, 'bomber_game')
    return send_from_directory(game_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 4: Configure PythonAnywhere Web App

**In PythonAnywhere Web tab:**

1. Click **Add a new web app**
2. Choose **Flask**
3. Python version: **Python 3.10**
4. Path: `/home/callensxavier/proutman/flask_app.py`

**Configure WSGI file** (`/var/www/callensxavier_pythonanywhere_com_wsgi.py`):

```python
import sys
import os

# Add your project directory
project_home = '/home/callensxavier/proutman'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Flask app
from flask_app import app as application
```

**Set up virtual environment:**
- Virtualenv: `/home/callensxavier/proutman/venv`
- Python version: 3.10

**Static files mapping:**
- URL: `/static`
- Directory: `/home/callensxavier/proutman/web_demo`

### Step 5: Reload and Test

1. Click **Reload** button
2. Visit: `https://callensxavier.pythonanywhere.com/`

---

## 🚀 Option 3: GitHub Pages (Simplest)

Deploy static HTML/JS version to GitHub Pages.

### Step 1: Enable GitHub Pages

**On GitHub:**
1. Go to https://github.com/xaviercallens/xgames
2. Settings → Pages
3. Source: Deploy from branch
4. Branch: `main`
5. Folder: `/` (root)
6. Save

### Step 2: Access Your Game

Your game will be available at:
```
https://xaviercallens.github.io/xgames/demo.html
```

**Already working!** Your demo page is live.

---

## 📝 Detailed PythonAnywhere Setup Script

Save this as `deploy_to_pythonanywhere.sh`:

```bash
#!/bin/bash
# Automated PythonAnywhere Deployment Script

echo "========================================"
echo "🚀 Proutman PythonAnywhere Deployment"
echo "========================================"
echo ""

# Configuration
PYTHONANYWHERE_USER="callensxavier"
PROJECT_DIR="/home/$PYTHONANYWHERE_USER/proutman"
VENV_DIR="$PROJECT_DIR/venv"
REPO_URL="https://github.com/xaviercallens/xgames.git"

echo "📋 Deployment Configuration:"
echo "   User: $PYTHONANYWHERE_USER"
echo "   Project: $PROJECT_DIR"
echo "   Repository: $REPO_URL"
echo ""

# Step 1: Clone repository
echo "1️⃣ Cloning repository..."
if [ -d "$PROJECT_DIR" ]; then
    echo "   Directory exists, pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull
else
    echo "   Cloning fresh copy..."
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# Step 2: Create virtual environment
echo ""
echo "2️⃣ Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3.10 -m venv "$VENV_DIR"
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment exists"
fi

# Step 3: Activate and install dependencies
echo ""
echo "3️⃣ Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install flask pygame numpy torch

# Step 4: Create Flask app
echo ""
echo "4️⃣ Creating Flask application..."
cat > "$PROJECT_DIR/flask_app.py" << 'EOF'
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DEMO_DIR = os.path.join(BASE_DIR, 'web_demo')

@app.route('/')
def index():
    return send_from_directory(WEB_DEMO_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(WEB_DEMO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
EOF

echo "   ✅ Flask app created"

# Step 5: Instructions for web configuration
echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "📝 Next Steps (Manual):"
echo ""
echo "1. Go to PythonAnywhere Web tab:"
echo "   https://www.pythonanywhere.com/user/$PYTHONANYWHERE_USER/webapps/"
echo ""
echo "2. Click 'Add a new web app'"
echo ""
echo "3. Configure:"
echo "   - Framework: Flask"
echo "   - Python: 3.10"
echo "   - Path: $PROJECT_DIR/flask_app.py"
echo "   - Virtualenv: $VENV_DIR"
echo ""
echo "4. Edit WSGI file to include:"
echo "   project_home = '$PROJECT_DIR'"
echo ""
echo "5. Click 'Reload' and visit:"
echo "   https://$PYTHONANYWHERE_USER.pythonanywhere.com/"
echo ""
echo "========================================"
```

---

## 🔐 Security Best Practices

**IMPORTANT**: Never share passwords in plain text!

### Secure Deployment Methods

1. **Use SSH Keys** (Recommended)
   ```bash
   # Generate SSH key on PythonAnywhere
   ssh-keygen -t ed25519 -C "callensxavier@pythonanywhere"
   
   # Add to GitHub
   cat ~/.ssh/id_ed25519.pub
   # Copy and add to GitHub → Settings → SSH Keys
   ```

2. **Use Personal Access Tokens**
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Use instead of password: `git clone https://TOKEN@github.com/xaviercallens/xgames.git`

3. **Use PythonAnywhere API Token**
   - Account → API token
   - Use for automated deployments

---

## 📊 Step-by-Step Manual Deployment

### Phase 1: Prepare Locally

```bash
# 1. Ensure code is up to date
cd /home/kalxav/CascadeProjects/windsurf-project-2
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git push origin main

# 2. Test web demo locally
cd web_demo
python -m http.server 8000
# Visit http://localhost:8000
```

### Phase 2: PythonAnywhere Console

**Login to PythonAnywhere** (you'll need to do this manually):

1. Go to https://www.pythonanywhere.com/
2. Login with your credentials
3. Open **Bash console**

**Run these commands in the console:**

```bash
# Clone repository
git clone https://github.com/xaviercallens/xgames.git proutman
cd proutman

# Setup Python environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask

# Test Flask app
python flask_app.py
```

### Phase 3: Web App Configuration

**In PythonAnywhere Web tab:**

1. **Add new web app**
   - Click "Add a new web app"
   - Domain: `callensxavier.pythonanywhere.com`
   - Framework: Flask
   - Python: 3.10

2. **Configure paths**
   - Source code: `/home/callensxavier/proutman`
   - Working directory: `/home/callensxavier/proutman`
   - Virtualenv: `/home/callensxavier/proutman/venv`

3. **Edit WSGI file**
   - Path: `/var/www/callensxavier_pythonanywhere_com_wsgi.py`
   - Update to point to your Flask app

4. **Static files**
   - URL: `/static`
   - Directory: `/home/callensxavier/proutman/web_demo`

5. **Reload** the web app

---

## 🎮 Testing the Deployment

### Local Testing

```bash
# Test Flask app locally first
cd /home/kalxav/CascadeProjects/windsurf-project-2
python flask_app.py

# Visit http://localhost:5000
```

### PythonAnywhere Testing

After deployment, test these URLs:

- Main page: `https://callensxavier.pythonanywhere.com/`
- Demo: `https://callensxavier.pythonanywhere.com/demo.html`
- Play: `https://callensxavier.pythonanywhere.com/play.html`

---

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# In PythonAnywhere console
cd /home/callensxavier/proutman
source venv/bin/activate
python -c "import flask; print('Flask OK')"
```

**2. File Not Found**
- Check paths in WSGI file
- Verify files exist: `ls -la /home/callensxavier/proutman`

**3. Permission Errors**
```bash
# Fix permissions
chmod -R 755 /home/callensxavier/proutman
```

**4. Git Authentication**
```bash
# Use HTTPS with token instead of password
git clone https://YOUR_TOKEN@github.com/xaviercallens/xgames.git
```

### Error Logs

Check logs in PythonAnywhere:
- Web tab → Log files
- Error log: `/var/log/callensxavier.pythonanywhere.com.error.log`
- Server log: `/var/log/callensxavier.pythonanywhere.com.server.log`

---

## 📈 Next Steps After Deployment

1. **Test the game** thoroughly
2. **Share the URL** with friends
3. **Monitor performance** in PythonAnywhere dashboard
4. **Set up custom domain** (optional, paid feature)
5. **Enable HTTPS** (automatic on PythonAnywhere)

---

## 🎯 Quick Commands Reference

### Update Deployment

```bash
# SSH into PythonAnywhere or use console
cd /home/callensxavier/proutman
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # if you create one
# Reload web app via Web tab
```

### Check Status

```bash
# In PythonAnywhere console
cd /home/callensxavier/proutman
source venv/bin/activate
python -c "from flask_app import app; print('App OK')"
```

### View Logs

```bash
# In PythonAnywhere console
tail -f /var/log/callensxavier.pythonanywhere.com.error.log
```

---

## 📚 Additional Resources

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Pygbag Documentation**: https://pygame-web.github.io/
- **Your GitHub Repo**: https://github.com/xaviercallens/xgames

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] PythonAnywhere account ready
- [ ] SSH keys configured (recommended)
- [ ] Repository cloned on PythonAnywhere
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Flask app created
- [ ] Web app configured
- [ ] WSGI file updated
- [ ] Static files mapped
- [ ] Web app reloaded
- [ ] Tested and working!

---

**Created**: 2025-10-14  
**Account**: callensxavier  
**URL**: https://callensxavier.pythonanywhere.com/  
**Status**: Ready for deployment
