# PythonAnywhere Deployment - Fix Port Issue

## ✅ Good News!

Your installation was **successful**! The "port in use" error is normal and expected.

## 🎯 Next Steps

You don't need to run `python flask_app.py` manually. Instead, configure the web app through PythonAnywhere's web interface.

### Step 1: Stop the Test Server

In your PythonAnywhere bash console, press **Ctrl+C** to stop the Flask test server.

### Step 2: Configure Web App

1. Go to the **Web** tab: https://www.pythonanywhere.com/user/callensxavier/webapps/

2. Click **"Add a new web app"**

3. Configuration:
   - Domain: `callensxavier.pythonanywhere.com`
   - Framework: **Manual configuration** (not Flask wizard)
   - Python version: **3.10**

### Step 3: Configure WSGI File

1. In the Web tab, click on the **WSGI configuration file** link
   (It will be something like `/var/www/callensxavier_pythonanywhere_com_wsgi.py`)

2. **Delete all content** and replace with:

```python
import sys
import os

# Add project directory to path
project_home = '/home/callensxavier/proutman'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add virtualenv site-packages
venv_path = '/home/callensxavier/proutman/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Import Flask app
from flask_app import app as application
```

3. Click **Save**

### Step 4: Set Virtual Environment

1. In the Web tab, scroll to **"Virtualenv"** section

2. Enter the path:
   ```
   /home/callensxavier/proutman/venv
   ```

3. The path should turn blue/green (indicating it's valid)

### Step 5: Configure Static Files (Optional but Recommended)

1. In the Web tab, scroll to **"Static files"** section

2. Click **"Enter URL"** and add:
   - URL: `/static`
   - Directory: `/home/callensxavier/proutman/web_demo`

3. Click the checkmark to save

### Step 6: Reload Web App

1. Scroll to the top of the Web tab

2. Click the big green **"Reload callensxavier.pythonanywhere.com"** button

3. Wait for the reload to complete

### Step 7: Test Your Site

Visit: **https://callensxavier.pythonanywhere.com/**

You should see the Proutman landing page!

---

## 🐛 If You See Errors

### Check Error Log

```bash
# In PythonAnywhere bash console
tail -50 /var/log/callensxavier.pythonanywhere.com.error.log
```

### Common Issues and Fixes

#### 1. "ImportError: No module named flask_app"

**Fix**: Check WSGI file paths are correct
```bash
# Verify files exist
ls -la /home/callensxavier/proutman/flask_app.py
ls -la /home/callensxavier/proutman/venv/
```

#### 2. "No module named 'flask'"

**Fix**: Virtualenv not activated in WSGI
- Make sure the venv path in WSGI file is correct
- Check: `/home/callensxavier/proutman/venv/lib/python3.10/site-packages`

#### 3. "404 Not Found"

**Fix**: Check static files mapping
- Ensure `web_demo` directory exists
- Verify static files path is correct

---

## ✅ Quick Verification Checklist

- [ ] Flask and dependencies installed (✅ Already done!)
- [ ] WSGI file configured with correct paths
- [ ] Virtual environment path set in Web tab
- [ ] Static files mapping added (optional)
- [ ] Web app reloaded
- [ ] Site accessible at callensxavier.pythonanywhere.com

---

## 📝 Complete WSGI Configuration

Here's the complete WSGI file content (copy-paste ready):

```python
# /var/www/callensxavier_pythonanywhere_com_wsgi.py

import sys
import os

# Project directory
project_home = '/home/callensxavier/proutman'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtual environment site-packages
venv_path = '/home/callensxavier/proutman/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Import Flask application
from flask_app import app as application

# Optional: Enable logging
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Proutman Flask app loaded successfully")
```

---

## 🎯 What Each URL Will Show

After successful deployment:

- **/** → Main landing page with game info
- **/demo.html** → Game demo page
- **/play.html** → Play page
- **/api/status** → JSON status endpoint

---

## 🔄 Update Deployment Later

When you make changes to the code:

```bash
# In PythonAnywhere bash console
cd ~/proutman
git pull origin main
# Then click "Reload" in Web tab
```

---

## 📊 Monitor Your App

### View Logs

```bash
# Error log
tail -f /var/log/callensxavier.pythonanywhere.com.error.log

# Server log
tail -f /var/log/callensxavier.pythonanywhere.com.server.log
```

### Check Status

Visit: https://callensxavier.pythonanywhere.com/api/status

Should return:
```json
{
  "status": "online",
  "game": "Proutman",
  "version": "2.0",
  "deployment": "PythonAnywhere"
}
```

---

## 🎉 Success Indicators

You'll know it's working when:

1. ✅ Web tab shows green "Reload" button (not red)
2. ✅ No errors in error log
3. ✅ Site loads at callensxavier.pythonanywhere.com
4. ✅ API status returns JSON response

---

## 💡 Pro Tips

### 1. Don't Run Flask Manually

On PythonAnywhere, **never** run `python flask_app.py` for production. The web app runs automatically through the WSGI server.

### 2. Use the Web Interface

All configuration should be done through the Web tab, not by running commands.

### 3. Check Logs First

If something doesn't work, always check the error log first before making changes.

### 4. Reload After Changes

Always click "Reload" in the Web tab after making any changes to code or configuration.

---

## 📞 Need Help?

If you're still stuck:

1. **Check error log**: Most issues show up there
2. **PythonAnywhere Help**: https://help.pythonanywhere.com/
3. **Forums**: https://www.pythonanywhere.com/forums/

---

**Your deployment is 90% complete!** Just follow the steps above to finish the configuration through the Web interface.

Good luck! 🚀
