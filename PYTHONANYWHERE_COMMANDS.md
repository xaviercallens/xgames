# PythonAnywhere - Quick Command Reference

## ✅ What You've Done So Far

```bash
✅ git clone https://github.com/xaviercallens/xgames.git proutman
✅ cd proutman
✅ python3.10 -m venv venv
✅ source venv/bin/activate
✅ pip install -r requirements_web.txt
```

**Status**: Installation complete! ✅

---

## 🎯 What to Do Next

### 1. Stop the Test Server

Press **Ctrl+C** in your bash console (if Flask is still running)

### 2. Configure Through Web Interface

**Don't use command line for this part!** Use the PythonAnywhere Web tab instead.

Go to: https://www.pythonanywhere.com/user/callensxavier/webapps/

---

## 📋 Web Tab Configuration

### Add New Web App

1. Click **"Add a new web app"**
2. Choose: **Manual configuration**
3. Python: **3.10**

### WSGI File

Click on WSGI configuration file and paste this:

```python
import sys
import os

project_home = '/home/callensxavier/proutman'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

venv_path = '/home/callensxavier/proutman/venv/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

from flask_app import app as application
```

### Virtualenv Section

Enter: `/home/callensxavier/proutman/venv`

### Static Files (Optional)

- URL: `/static`
- Directory: `/home/callensxavier/proutman/web_demo`

### Reload

Click the big green **"Reload"** button

---

## 🔍 Verification Commands

Run these in bash console to verify everything:

```bash
# Check files exist
ls -la ~/proutman/flask_app.py
ls -la ~/proutman/venv/

# Check Flask is installed
source ~/proutman/venv/bin/activate
python -c "import flask; print('Flask version:', flask.__version__)"

# Check web_demo exists
ls -la ~/proutman/web_demo/
```

Expected output:
```
Flask version: 3.0.0
```

---

## 📊 Check Logs

```bash
# View error log (most useful)
tail -50 /var/log/callensxavier.pythonanywhere.com.error.log

# Follow error log in real-time
tail -f /var/log/callensxavier.pythonanywhere.com.error.log

# View server log
tail -50 /var/log/callensxavier.pythonanywhere.com.server.log
```

---

## 🧪 Test Your Deployment

### From Browser

Visit these URLs:

1. **Main page**: https://callensxavier.pythonanywhere.com/
2. **API status**: https://callensxavier.pythonanywhere.com/api/status
3. **Demo page**: https://callensxavier.pythonanywhere.com/demo.html

### From Command Line

```bash
# Test API endpoint
curl https://callensxavier.pythonanywhere.com/api/status

# Should return JSON like:
# {"status":"online","game":"Proutman",...}
```

---

## 🔄 Update Your Site Later

When you push changes to GitHub:

```bash
# In PythonAnywhere bash console
cd ~/proutman
git pull origin main

# Then go to Web tab and click "Reload"
```

---

## ❌ Common Errors and Fixes

### Error: "Address already in use"

**This is normal!** Don't run `python flask_app.py` on PythonAnywhere.
- Just configure through Web tab
- The WSGI server handles running the app

### Error: "ImportError: No module named flask_app"

**Fix**: Check WSGI file paths
```bash
# Verify file exists
ls -la ~/proutman/flask_app.py

# Should show: -rw-r--r-- ... flask_app.py
```

### Error: "No module named 'flask'"

**Fix**: Check virtualenv path in WSGI file
```bash
# Verify venv exists
ls -la ~/proutman/venv/lib/python3.10/site-packages/flask/

# Should show Flask directory
```

### Error: "Something went wrong :("

**Fix**: Check error log
```bash
tail -50 /var/log/callensxavier.pythonanywhere.com.error.log
```

---

## 📝 Quick Checklist

Before asking for help, verify:

- [ ] WSGI file has correct paths
- [ ] Virtualenv path is set in Web tab
- [ ] Web app has been reloaded
- [ ] Error log checked for specific errors
- [ ] Files exist at expected paths

---

## 🎯 Expected File Structure

```
/home/callensxavier/proutman/
├── flask_app.py          ← Main Flask app
├── requirements_web.txt  ← Dependencies
├── web_demo/            ← Static files
│   ├── index.html
│   ├── demo.html
│   └── ...
├── venv/                ← Virtual environment
│   └── lib/python3.10/site-packages/
└── bomber_game/         ← Game code
```

---

## 💡 Remember

1. **Don't run Flask manually** - Use Web tab configuration
2. **Always reload** after changes
3. **Check logs** for errors
4. **Use Web interface** for configuration

---

## ✅ Success Criteria

Your site is working when:

1. ✅ https://callensxavier.pythonanywhere.com/ loads
2. ✅ No errors in error log
3. ✅ API status returns JSON
4. ✅ Web tab shows green reload button

---

**You're almost there!** Just configure through the Web tab and you're done! 🚀
