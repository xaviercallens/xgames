# 🎯 PythonAnywhere Deployment - Visual Step-by-Step Guide

## ✅ Current Status

```
✅ Code cloned to: /home/callensxavier/proutman
✅ Virtual environment created
✅ Dependencies installed (Flask, etc.)
```

**The "port in use" error is NORMAL and EXPECTED!**

---

## 🚫 STOP! Don't Do This

```bash
❌ python flask_app.py  # DON'T RUN THIS ON PYTHONANYWHERE
```

**Why?** PythonAnywhere uses a web server (WSGI), not the Flask development server.

---

## ✅ Do This Instead

### Step 1: Go to Web Tab

```
https://www.pythonanywhere.com/user/callensxavier/
                    ↓
            Click "Web" tab
```

### Step 2: Add New Web App

```
┌─────────────────────────────────────────┐
│  Web Apps                               │
├─────────────────────────────────────────┤
│  [Add a new web app]  ← CLICK THIS     │
└─────────────────────────────────────────┘
```

### Step 3: Choose Configuration

```
┌─────────────────────────────────────────┐
│  Select a Python Web Framework         │
├─────────────────────────────────────────┤
│  ○ Flask                                │
│  ○ Django                               │
│  ● Manual configuration  ← SELECT THIS │
└─────────────────────────────────────────┘

Next screen:
┌─────────────────────────────────────────┐
│  Select Python Version                  │
├─────────────────────────────────────────┤
│  ○ Python 3.8                           │
│  ○ Python 3.9                           │
│  ● Python 3.10          ← SELECT THIS  │
└─────────────────────────────────────────┘
```

### Step 4: Configure WSGI File

```
┌─────────────────────────────────────────────────────────┐
│  Configuration for callensxavier.pythonanywhere.com     │
├─────────────────────────────────────────────────────────┤
│  Code:                                                  │
│    Source code:  /home/callensxavier/proutman          │
│    Working directory: /home/callensxavier/proutman     │
│                                                         │
│  WSGI configuration file:                              │
│    /var/www/callensxavier_pythonanywhere_com_wsgi.py  │
│    ↑ CLICK THIS LINK                                   │
└─────────────────────────────────────────────────────────┘
```

**In the WSGI file editor:**

1. **DELETE ALL EXISTING CONTENT**
2. **PASTE THIS:**

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

3. **CLICK "SAVE"**

### Step 5: Set Virtual Environment

```
┌─────────────────────────────────────────────────────────┐
│  Virtualenv:                                            │
├─────────────────────────────────────────────────────────┤
│  Enter path to a virtualenv, if desired                │
│  ┌───────────────────────────────────────────────────┐ │
│  │ /home/callensxavier/proutman/venv                 │ │
│  └───────────────────────────────────────────────────┘ │
│     ↑ TYPE THIS PATH                                   │
│                                                         │
│  Path should turn BLUE/GREEN when valid ✓              │
└─────────────────────────────────────────────────────────┘
```

### Step 6: Add Static Files (Optional)

```
┌─────────────────────────────────────────────────────────┐
│  Static files:                                          │
├─────────────────────────────────────────────────────────┤
│  URL                          Directory                 │
│  ┌─────────┐                 ┌────────────────────────┐│
│  │ /static │                 │ /home/callensxavier/   ││
│  └─────────┘                 │ proutman/web_demo      ││
│                               └────────────────────────┘│
│  [✓] ← Click checkmark to save                         │
└─────────────────────────────────────────────────────────┘
```

### Step 7: Reload Web App

```
┌─────────────────────────────────────────────────────────┐
│  ┌───────────────────────────────────────────────────┐ │
│  │  [Reload callensxavier.pythonanywhere.com]        │ │
│  │         ↑ CLICK THIS BIG GREEN BUTTON             │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Step 8: Test Your Site

```
Open browser and visit:
┌─────────────────────────────────────────────────────────┐
│  https://callensxavier.pythonanywhere.com/              │
└─────────────────────────────────────────────────────────┘

You should see:
┌─────────────────────────────────────────────────────────┐
│  💨 Proutman - Educational Bomberman Game 💩            │
│                                                         │
│  Welcome to Proutman! An educational game for          │
│  learning Python, AI, and Reinforcement Learning.      │
│                                                         │
│  Available Pages:                                      │
│  • Game Demo                                           │
│  • Play Now                                            │
│  • API Status                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Troubleshooting Visual Guide

### If You See "Something went wrong"

```
Step 1: Check Error Log
┌─────────────────────────────────────────────────────────┐
│  In PythonAnywhere Bash Console:                       │
│  $ tail -50 /var/log/callensxavier.pythonanywhere.com.error.log
└─────────────────────────────────────────────────────────┘

Step 2: Look for Error Messages
┌─────────────────────────────────────────────────────────┐
│  Common errors:                                         │
│  • ImportError: No module named 'flask_app'            │
│    → Check WSGI file paths                             │
│                                                         │
│  • ImportError: No module named 'flask'                │
│    → Check virtualenv path                             │
│                                                         │
│  • FileNotFoundError                                   │
│    → Check files exist in /home/callensxavier/proutman │
└─────────────────────────────────────────────────────────┘
```

### Verify Files Exist

```bash
$ ls -la ~/proutman/flask_app.py
-rw-r--r-- 1 callensxavier registered_users 3456 Oct 14 08:00 flask_app.py
                                              ↑ Should see this

$ ls -la ~/proutman/venv/
drwxr-xr-x 5 callensxavier registered_users 4096 Oct 14 08:00 .
                                              ↑ Should see this
```

---

## 📊 Configuration Summary

```
┌──────────────────────────────────────────────────────────────┐
│  CONFIGURATION CHECKLIST                                     │
├──────────────────────────────────────────────────────────────┤
│  ✅ Web app created (Manual configuration, Python 3.10)     │
│  ✅ WSGI file edited with correct paths                     │
│  ✅ Virtual environment path set                            │
│  ✅ Static files mapped (optional)                          │
│  ✅ Web app reloaded                                        │
│  ✅ Site accessible at callensxavier.pythonanywhere.com    │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 Quick Reference

### Paths to Remember

```
Project:     /home/callensxavier/proutman
Virtualenv:  /home/callensxavier/proutman/venv
Flask App:   /home/callensxavier/proutman/flask_app.py
Web Demo:    /home/callensxavier/proutman/web_demo
```

### URLs to Test

```
Main:        https://callensxavier.pythonanywhere.com/
Demo:        https://callensxavier.pythonanywhere.com/demo.html
API Status:  https://callensxavier.pythonanywhere.com/api/status
```

### Logs to Check

```
Error Log:   /var/log/callensxavier.pythonanywhere.com.error.log
Server Log:  /var/log/callensxavier.pythonanywhere.com.server.log
```

---

## ✅ Success Indicators

```
┌──────────────────────────────────────────────────────────────┐
│  YOU'LL KNOW IT'S WORKING WHEN:                             │
├──────────────────────────────────────────────────────────────┤
│  1. ✅ Web tab shows green "Reload" button (not red)        │
│  2. ✅ No errors in error log                               │
│  3. ✅ Site loads at callensxavier.pythonanywhere.com       │
│  4. ✅ API status returns JSON:                             │
│        {"status":"online","game":"Proutman",...}            │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Final Steps

```
1. Stop Flask test server (Ctrl+C in bash console)
2. Go to Web tab
3. Configure WSGI file
4. Set virtualenv path
5. Click Reload
6. Visit your site!
```

---

## 💡 Remember

```
┌──────────────────────────────────────────────────────────────┐
│  DO NOT run "python flask_app.py" on PythonAnywhere!       │
│                                                              │
│  ✅ Use Web tab configuration instead                       │
│  ✅ WSGI server runs your app automatically                 │
│  ✅ Just configure and reload                               │
└──────────────────────────────────────────────────────────────┘
```

---

**You're 90% done!** Just follow the visual steps above and your site will be live! 🎉
