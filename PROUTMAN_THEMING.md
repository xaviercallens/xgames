# 💨 PROUTMAN Theming Guide 💩

## 🎨 **Overview**

Your game now features the **PROUTMAN** theme with fun, educational French-inspired branding!

---

## ✨ **What's New**

### **1. Splash Screen System**
- **3-second intro** with beautiful Proutman artwork
- **Skip with any key** or mouse click
- **Pulsing animation** for "Press any key"
- **Fallback text splash** if image not available
- **Professional presentation**

### **2. Enhanced Branding**
```
Window Title: 💨 PROUTMAN - L'aventure Codée! 💩
Game Theme: Fun, educational, humor-based learning
Language: French-inspired (Prout = Trump/Fart, Caca = Poop)
```

### **3. New Assets Integration**
- ✅ `sprite_player_versionproutman.png` - Enhanced player sprites
- ✅ `tiles_bomberman_versionproutman.png` - Themed tiles
- ✅ `proutman_splash.jpg` - Splash screen image
- ✅ Automatic fallback to standard assets

---

## 🖼️ **Splash Screen Image**

### **To Add Your Custom Splash:**

1. **Save the Proutman splash image** you provided to:
   ```
   bomber_game/assets/images/proutman_splash.jpg
   ```

2. **The image should show:**
   - PROUTMAN title logo
   - "L'aventure Codée!" subtitle
   - Proutman character with green mask
   - Caca (💩) obstacles on game board
   - "START GAME" and "OPTIONS" buttons
   - Educational tagline

3. **Image will automatically:**
   - Scale to fit screen
   - Maintain aspect ratio
   - Center on display
   - Show for 3 seconds

### **Current Fallback:**
If image is missing, shows text-based splash:
```
💨 PROUTMAN 💨
L'aventure Codée!

💩 Decorative cacas 💩

Pour Apprendre à Coder et S'Amuser!
Création de Jeu & Apprentissage Renforcé

💨 Drop Prouts (Trumps) to destroy walls
💩 Place Cacas to block enemies
🎯 Collect power-ups and defeat AI

Press any key to start...
```

---

## 🎮 **How It Works**

### **Game Start Sequence:**

1. **Launch game:**
   ```bash
   ./launch_bomberman.sh
   ```

2. **Splash screen appears:**
   - Shows for 3 seconds
   - Press any key to skip
   - Pulsing "Press any key" text

3. **Game starts:**
   - Loads with Proutman theme
   - Uses enhanced sprites
   - Fun educational experience

---

## 🎨 **Theming Details**

### **Visual Theme:**
- **Colors**: Green (Proutman), Brown (Caca), Bright & Fun
- **Style**: Cartoon, Educational, Humorous
- **Emojis**: 💨 💩 🎯 🏆 ⚡ 👑

### **Language:**
- **French-inspired** terminology
- **Prout** = Trump/Fart (bomb)
- **Caca** = Poop (obstacle)
- **Educational** focus

### **Branding Elements:**
```python
Window Title: "💨 PROUTMAN - L'aventure Codée! 💩"
Splash Title: "PROUTMAN"
Subtitle: "L'aventure Codée!"
Tagline: "Pour Apprendre à Coder et S'Amuser!"
```

---

## 📁 **File Structure**

```
bomber_game/
├── menu.py                          # NEW: Menu system
├── game_engine.py                   # UPDATED: Splash integration
├── assets.py                        # UPDATED: Proutman assets
└── assets/
    └── images/
        ├── proutman_splash.jpg      # NEW: Splash screen
        ├── sprite_player_versionproutman.png
        └── tiles_bomberman_versionproutman.png
```

---

## 🔧 **Customization**

### **Change Splash Duration:**

Edit `bomber_game/game_engine.py`:
```python
def run(self):
    if self.show_splash:
        quit_requested = self.menu.show_splash(duration=5.0)  # 5 seconds
```

### **Disable Splash:**

```python
game = BombermanGame(show_splash=False)
```

### **Customize Splash Text:**

Edit `bomber_game/menu.py`:
```python
def _draw_text_splash(self):
    # Modify title, subtitle, descriptions
    title = self.font_large.render("YOUR TITLE", True, GREEN)
```

---

## 🎯 **Menu System**

### **Features:**
- **Splash screen** with animation
- **Main menu** (future enhancement)
- **Keyboard navigation**
- **Smooth transitions**
- **Professional UI**

### **Menu Class:**
```python
from bomber_game.menu import MenuScreen

menu = MenuScreen(screen)
menu.show_splash(duration=3.0)  # Show splash
action = menu.show_menu()        # Show menu (future)
```

---

## 🚀 **Usage**

### **Play with Splash:**
```bash
./launch_bomberman.sh
```

**You'll see:**
1. ✅ Splash screen (3 seconds)
2. ✅ Game starts with Proutman theme
3. ✅ Enhanced sprites and tiles
4. ✅ Fun educational experience

### **Skip Splash:**
- Press **any key** during splash
- Or wait 3 seconds
- Game starts immediately

---

## 🎨 **Asset Integration**

### **Player Sprites:**
```python
# Automatically uses Proutman version if available
spritesheet = assets.get_player_spritesheet()
# Falls back to standard if not found
```

### **Tiles:**
```python
# Automatically uses Proutman tiles if available
tiles = assets.get_tiles_spritesheet()
# Falls back to standard if not found
```

### **Fallback System:**
- Tries Proutman assets first
- Falls back to standard assets
- No errors if assets missing
- Graceful degradation

---

## 📊 **Technical Details**

### **MenuScreen Class:**
```python
class MenuScreen:
    def __init__(self, screen)
    def show_splash(self, duration=3.0)
    def show_menu(self)  # Future
    def _draw_text_splash()
```

### **Features:**
- Image loading with scaling
- Aspect ratio preservation
- Pulsing animations
- Keyboard/mouse input
- Clean transitions

### **Animation:**
- Pulse speed: 2.0 Hz
- Alpha range: 128-255
- Smooth sine wave
- Professional feel

---

## 🎓 **Educational Value**

### **Learning Concepts:**
1. **Game Menus** - Professional UI design
2. **Asset Management** - Loading and caching
3. **Animation** - Pulsing effects
4. **State Management** - Menu states
5. **User Input** - Keyboard/mouse handling
6. **Fallback Systems** - Graceful degradation

### **French Language:**
- **Prout** (trump/fart) - Humorous learning
- **Caca** (poop) - Fun obstacles
- **L'aventure Codée** - The Coded Adventure
- **Pour Apprendre** - To Learn

---

## ✨ **Summary**

### **Implemented:**
- 🎨 **Splash screen** system
- 💨 **PROUTMAN** branding
- 🖼️ **Image loading** with fallback
- ✨ **Pulsing animations**
- 🎮 **Professional UI**
- 🇫🇷 **French-inspired** theme
- 💩 **Fun educational** approach

### **Benefits:**
- **Engaging** first impression
- **Professional** presentation
- **Educational** branding
- **Humorous** approach
- **Memorable** experience

---

## 📝 **Next Steps**

### **To Complete Setup:**

1. **Add splash image:**
   ```bash
   # Copy your Proutman splash image to:
   cp /path/to/proutman_image.jpg bomber_game/assets/images/proutman_splash.jpg
   ```

2. **Test the game:**
   ```bash
   ./launch_bomberman.sh
   ```

3. **Enjoy the splash screen!**
   - See Proutman intro
   - Skip with any key
   - Play the game

---

## 🎮 **Play Now!**

```bash
./launch_bomberman.sh
```

**Experience the fun PROUTMAN theme!** 💨🎮💩

---

**The game now has professional branding and a fun educational theme!** 🎉✨
