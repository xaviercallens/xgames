# 🚀 PythonAnywhere Deployment - Quick Start

## ⚡ 5-Minute Deployment

### Step 1: Login to PythonAnywhere

1. Go to https://www.pythonanywhere.com/
2. Login with username: **callensxavier**
3. Open a **Bash console**

### Step 2: Clone and Setup (Copy-Paste This)

```bash
# Clone repository
cd ~
git clone https://github.com/xaviercallens/xgames.git proutman
cd proutman

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_web.txt

# Test Flask app
python flask_app.py
# Press Ctrl+C to stop
```

### Step 3: Configure Web App

1. Go to **Web** tab: https://www.pythonanywhere.com/user/callensxavier/webapps/
2. Click **"Add a new web app"**
3. Choose your domain: `callensxavier.pythonanywhere.com`
4. Select **"Flask"**
5. Python version: **3.10**
6. Path to Flask app: `/home/callensxavier/proutman/flask_app.py`

### Step 4: Configure WSGI File

1. In Web tab, click on **WSGI configuration file** link
2. **Replace entire content** with this:

```python
import sys
import os

# Project directory
project_home = '/home/callensxavier/proutman'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment
venv_path = '/home/callensxavier/proutman/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Import Flask app
from flask_app import app as application
```

3. Click **Save**

### Step 5: Configure Virtual Environment

1. In Web tab, find **"Virtualenv"** section
2. Enter: `/home/callensxavier/proutman/venv`
3. The path should turn blue/green (valid)

### Step 6: Configure Static Files (Optional)

1. In Web tab, find **"Static files"** section
2. Add mapping:
   - URL: `/static`
   - Directory: `/home/callensxavier/proutman/web_demo`

### Step 7: Reload and Test

1. Click the big green **"Reload"** button
2. Visit: **https://callensxavier.pythonanywhere.com/**

---

## ✅ Verification

Your site should show:
- ✅ Home page with Proutman info
- ✅ `/demo.html` - Game demo
- ✅ `/play.html` - Play page
- ✅ `/api/status` - API status (JSON)

---

## 🐛 Troubleshooting

### Error: "Something went wrong"

**Check error log:**
```bash
# In PythonAnywhere console
tail -50 /var/log/callensxavier.pythonanywhere.com.error.log
```

### Error: "ImportError: No module named flask"

**Fix:**
```bash
cd ~/proutman
source venv/bin/activate
pip install flask
# Then reload web app
```

### Error: "File not found"

**Check paths:**
```bash
ls -la ~/proutman/
ls -la ~/proutman/web_demo/
```

---

## 🔄 Update Deployment

When you make changes:

```bash
# In PythonAnywhere console
cd ~/proutman
git pull origin main
source venv/bin/activate
pip install -r requirements_web.txt
# Then click "Reload" in Web tab
```

---

## 📊 Monitoring

### View Logs

**Error log:**
```bash
tail -f /var/log/callensxavier.pythonanywhere.com.error.log
```

**Server log:**
```bash
tail -f /var/log/callensxavier.pythonanywhere.com.server.log
```

### Check Status

Visit: https://callensxavier.pythonanywhere.com/api/status

---

## 🎯 Next Steps

1. ✅ Deploy basic Flask app
2. ✅ Test all pages work
3. 📝 Customize web_demo content
4. 🎨 Add your own branding
5. 📊 Set up analytics (optional)
6. 🌐 Add custom domain (paid feature)

---

## 🔐 Security Notes

- **Never commit passwords** to Git
- Use **environment variables** for secrets
- Enable **HTTPS** (automatic on PythonAnywhere)
- Use **SSH keys** for Git authentication

---

## 📚 Resources

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Your Dashboard**: https://www.pythonanywhere.com/user/callensxavier/
- **GitHub Repo**: https://github.com/xaviercallens/xgames
- **Full Guide**: See PYTHONANYWHERE_DEPLOYMENT.md

---

**Deployment URL**: https://callensxavier.pythonanywhere.com/  
**Estimated Time**: 5-10 minutes  
**Difficulty**: Easy ⭐
