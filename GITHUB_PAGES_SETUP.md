# 🌐 GitHub Pages Setup Guide

## Enable GitHub Pages for Proutman

Follow these steps to enable the live demo website:

---

## 📋 **Prerequisites**

- ✅ GitHub repository: `xaviercallens/xgames`
- ✅ Files in `docs/` directory
- ✅ Repository pushed to GitHub

---

## 🚀 **Setup Steps**

### **1. Go to Repository Settings**

1. Navigate to: https://github.com/xaviercallens/xgames
2. Click **Settings** tab (top right)

### **2. Enable GitHub Pages**

1. Scroll down to **Pages** section (left sidebar)
2. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
3. Click **Save**

### **3. Wait for Deployment**

- GitHub will build your site (takes 1-2 minutes)
- You'll see a message: "Your site is published at..."

### **4. Access Your Site**

Your Proutman website will be live at:
```
https://xaviercallens.github.io/xgames/
```

**Pages:**
- **Home**: https://xaviercallens.github.io/xgames/
- **Demo**: https://xaviercallens.github.io/xgames/demo.html

---

## 📁 **Files Structure**

```
docs/
├── index.html          # Main landing page
└── demo.html           # Live demo page (coming soon)
```

---

## 🎨 **What's Included**

### **Main Page (index.html)**
- 🌟 Story behind Proutman
- 🎮 Feature showcase
- 📸 Screenshots
- 🎨 Visual gallery
- 📚 Learning path
- 👨‍👩‍👧‍👦 Parent/teacher resources

### **Demo Page (demo.html)**
- 🎮 Live demo information
- 📥 Download instructions
- 🎯 Game controls
- 📸 Gameplay screenshots
- 🚀 Quick start guide

---

## 🔧 **Customization**

### **Update Content**

1. Edit files in `docs/` directory
2. Commit and push changes:
   ```bash
   git add docs/
   git commit -m "Update website"
   git push
   ```
3. GitHub Pages will auto-update (1-2 minutes)

### **Add New Pages**

1. Create new `.html` file in `docs/`
2. Link from existing pages
3. Push to GitHub

---

## 🎯 **Future Enhancements**

### **WebAssembly Demo (Coming Soon)**

To add a playable browser version:

1. **Use Pygbag** (Pygame to WebAssembly):
   ```bash
   pip install pygbag
   pygbag play_bomberman.py
   ```

2. **Or use Brython** (Python in browser):
   - Convert Python to JavaScript
   - Embed in HTML page

3. **Or create HTML5 version**:
   - Rewrite game logic in JavaScript
   - Use HTML5 Canvas
   - Keep same gameplay

### **Video Demo**

Add gameplay video:
1. Record gameplay
2. Upload to YouTube
3. Embed in demo.html

---

## 📊 **Analytics (Optional)**

Add Google Analytics to track visitors:

```html
<!-- Add to <head> in index.html and demo.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-ID');
</script>
```

---

## 🐛 **Troubleshooting**

### **Site Not Loading**

1. Check GitHub Pages is enabled
2. Verify `docs/` folder selected
3. Wait 2-3 minutes for deployment
4. Clear browser cache

### **Images Not Showing**

1. Check image paths are relative: `../bomber_game/assets/images/`
2. Ensure images are committed to repo
3. Verify file names match exactly (case-sensitive)

### **Links Not Working**

1. Use relative paths: `./demo.html` or `../README.md`
2. For external links, use full URLs
3. Test locally first

---

## ✅ **Verification**

After setup, verify:

- ✅ Main page loads: https://xaviercallens.github.io/xgames/
- ✅ Demo page loads: https://xaviercallens.github.io/xgames/demo.html
- ✅ Images display correctly
- ✅ Links work properly
- ✅ Mobile responsive

---

## 🎉 **Success!**

Your Proutman website is now live!

**Share it:**
- 📱 Social media
- 📧 Email to friends
- 🎓 Show in class
- 👨‍👩‍👧‍👦 Share with parents

**Promote it:**
- 🌟 Add to GitHub README
- 📝 Blog about it
- 🎮 Gaming forums
- 🎓 Educational sites

---

## 📚 **Resources**

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Pygbag (Pygame to Web)](https://pygame-web.github.io/)
- [HTML5 Game Development](https://developer.mozilla.org/en-US/docs/Games)

---

**Made with ❤️ for Proutman!** 💨🤖
