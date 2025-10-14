# 🎯 PythonAnywhere Web Configuration - Step by Step

## Current Situation

You're looking at the wrong directory! The virtualenv section in the Web tab is different from the Files tab.

---

## ✅ Correct Steps

### Step 1: Go to Web Tab

**Don't use the Files tab for this!**

1. Click on **"Web"** in the top navigation
2. URL: https://www.pythonanywhere.com/user/callensxavier/webapps/

### Step 2: You Should See This

```
┌─────────────────────────────────────────────────────────────┐
│  Web apps                                                   │
├─────────────────────────────────────────────────────────────┤
│  You don't have any web apps yet.                          │
│                                                             │
│  [Add a new web app]  ← CLICK THIS BUTTON                 │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Create Web App

Click **"Add a new web app"** and follow the wizard:

**Screen 1: Domain**
```
Your web app's domain name will be:
callensxavier.pythonanywhere.com

[Next] ← Click
```

**Screen 2: Framework**
```
Select a Python Web framework:
○ Flask
○ Django  
○ web2py
● Manual configuration  ← SELECT THIS
○ Bottle

[Next] ← Click
```

**Screen 3: Python Version**
```
Select a Python version:
○ Python 3.8
○ Python 3.9
● Python 3.10  ← SELECT THIS
○ Python 3.11

[Next] ← Click
```

### Step 4: Configure the Web App

After creation, you'll see a configuration page with several sections:

```
┌─────────────────────────────────────────────────────────────┐
│  Configuration for callensxavier.pythonanywhere.com         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Code:                                                      │
│  ─────────────────────────────────────────────────────────  │
│  Source code:                                               │
│  /home/callensxavier/                                       │
│  [Edit] ← Change to: /home/callensxavier/proutman         │
│                                                             │
│  Working directory:                                         │
│  /home/callensxavier/                                       │
│  [Edit] ← Change to: /home/callensxavier/proutman         │
│                                                             │
│  WSGI configuration file:                                   │
│  /var/www/callensxavier_pythonanywhere_com_wsgi.py        │
│  [Edit] ← CLICK THIS                                       │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  Virtualenv:                                                │
│  ─────────────────────────────────────────────────────────  │
│  Enter path to a virtualenv, if desired                    │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  └───────────────────────────────────────────────────────┘ │
│  ↑ TYPE HERE: /home/callensxavier/proutman/venv           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Detailed Configuration

### A. Edit WSGI File

1. Click on **WSGI configuration file** link
2. You'll see a text editor with default content
3. **DELETE EVERYTHING** in the file
4. **PASTE THIS:**

```python
import sys
import os

# Add project directory to Python path
project_home = '/home/callensxavier/proutman'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add virtualenv site-packages to Python path
venv_path = '/home/callensxavier/proutman/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Import Flask application
from flask_app import app as application
```

5. Click **"Save"** (top right)

### B. Set Virtualenv Path

1. Scroll down to **"Virtualenv"** section
2. In the text box, type:
   ```
   /home/callensxavier/proutman/venv
   ```
3. Press **Enter** or click outside the box
4. The path should turn **blue/green** (valid) or **red** (invalid)

**If it turns RED:**
- Check the path is correct
- Verify the venv exists by running in bash console:
  ```bash
  ls -la /home/callensxavier/proutman/venv/
  ```

### C. Set Source Code Path (Optional)

1. Click **"Edit"** next to "Source code:"
2. Change to: `/home/callensxavier/proutman`
3. Click **"✓"** to save

### D. Set Working Directory (Optional)

1. Click **"Edit"** next to "Working directory:"
2. Change to: `/home/callensxavier/proutman`
3. Click **"✓"** to save

### E. Add Static Files (Optional)

1. Scroll down to **"Static files"** section
2. Click **"Enter URL"**
3. Enter:
   - URL: `/static`
   - Directory: `/home/callensxavier/proutman/web_demo`
4. Click **"✓"** to save

---

## 🔄 Reload Web App

After all configuration:

1. Scroll to the **top** of the page
2. Find the big green button that says:
   ```
   [Reload callensxavier.pythonanywhere.com]
   ```
3. Click it
4. Wait for the reload to complete (button will briefly turn gray)

---

## ✅ Test Your Site

Open a new browser tab and visit:

```
https://callensxavier.pythonanywhere.com/
```

You should see the Proutman landing page!

---

## 🐛 If You See Errors

### Check Error Log

In bash console:
```bash
tail -50 /var/log/callensxavier.pythonanywhere.com.error.log
```

### Common Issues

**1. "Something went wrong :("**
- Check error log for specific error
- Verify WSGI file paths are correct
- Ensure virtualenv path is valid

**2. "ImportError: No module named 'flask_app'"**
```bash
# Verify file exists
ls -la /home/callensxavier/proutman/flask_app.py
```

**3. "ImportError: No module named 'flask'"**
```bash
# Check Flask is installed in venv
source /home/callensxavier/proutman/venv/bin/activate
python -c "import flask; print(flask.__version__)"
```

**4. Virtualenv path turns RED**
```bash
# Verify venv exists
ls -la /home/callensxavier/proutman/venv/
# Should show: bin/ lib/ include/ etc.
```

---

## 📊 Visual Guide: Where to Find Virtualenv Section

```
TOP NAVIGATION:
┌──────────────────────────────────────────────────────────┐
│ Dashboard | Consoles | Files | Web | Tasks | Databases  │
│                                  ↑                        │
│                            CLICK HERE                     │
└──────────────────────────────────────────────────────────┘

Then scroll down on the Web page to find:

┌──────────────────────────────────────────────────────────┐
│  Virtualenv:                                             │
│  ──────────────────────────────────────────────────────  │
│  Enter path to a virtualenv, if desired                 │
│  ┌────────────────────────────────────────────────────┐ │
│  │ /home/callensxavier/proutman/venv                  │ │
│  └────────────────────────────────────────────────────┘ │
│     ↑ TYPE THE PATH HERE                                │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Quick Checklist

- [ ] Go to **Web** tab (not Files tab)
- [ ] Click **"Add a new web app"**
- [ ] Choose **Manual configuration**
- [ ] Select **Python 3.10**
- [ ] Edit **WSGI file** with correct paths
- [ ] Set **Virtualenv** to `/home/callensxavier/proutman/venv`
- [ ] Click **Reload** button
- [ ] Test site at callensxavier.pythonanywhere.com

---

## 💡 Important Notes

1. **Don't confuse Files tab with Web tab**
   - Files tab: Browse files
   - Web tab: Configure web apps

2. **The virtualenv section is on the Web configuration page**
   - Not in the Files browser
   - Not in the Consoles tab
   - It's in the Web tab, after creating a web app

3. **Your venv is at: `/home/callensxavier/proutman/venv`**
   - NOT in `/home/callensxavier/.virtualenvs/`
   - It's inside your project directory

---

## 🚀 Next Steps

1. **Navigate to Web tab** (top menu)
2. **Create web app** if you haven't already
3. **Configure** using the steps above
4. **Reload** the web app
5. **Test** your site!

---

**You're looking in the wrong place!** The virtualenv configuration is in the **Web tab**, not the Files tab. Follow the steps above! 🎯
