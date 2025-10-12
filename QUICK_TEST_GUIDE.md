# 🎮 Quick Test Guide - Enhanced Gameplay Features

## ✅ Bug Fixed!
The `grid_x` and `grid_y` attribute error has been fixed. Game should now run properly!

---

## 🚀 **Game is Running - Test These Features:**

### **1. 🗺️ Open Map (5% Walls)**
**Look for:**
- Very few brown/toilet walls
- Lots of empty space
- Easy to move around

**Status:** [ ] Visible

---

### **2. 🚪 Teleport Doors**
**Look for:**
- 8 colored squares on map borders
- Pulsing animation
- Different colors

**Test:**
1. Walk to a door on the border
2. Step on it
3. Should teleport instantly to paired door

**Colors to find:**
- [ ] Magenta (Door 1)
- [ ] Cyan (Door 2)
- [ ] Yellow (Door 3)
- [ ] Orange (Door 4)

**Status:** [ ] Working

---

### **3. 💣 Bomb Machine**
**Look for:**
- Gray/red machine at center of map
- Timer counting down from 10.0s
- Animated bomb icon

**Watch for:**
- Timer: 10s → 9s → ... → 0s
- Warning at 2s (red flash)
- Bomb drops at 0s
- Explosion 10s later

**Status:** [ ] Working

---

### **4. 🎁 New Power-Ups**
**Destroy walls to find:**

**🛡️ Shield (Green):**
- Collect it
- Walk into explosion
- Should survive 1 hit
- [ ] Tested

**📡 Remote (Yellow):**
- Collect it
- Place bomb (SPACE)
- Press **R** key
- Bomb explodes immediately
- [ ] Tested

**⚡ Pierce (Purple):**
- Collect it
- Place bomb near wall
- Explosion goes through wall
- [ ] Tested

---

## 🎮 **Controls:**
- **WASD / Arrow Keys** - Move
- **SPACE** - Drop bomb
- **C** - Drop caca block
- **R** - Remote detonate (if you have Remote power-up)
- **P** - Pause
- **ESC** - Quit

---

## ✅ **Quick Checklist:**
- [ ] Map is open (5% walls)
- [ ] Teleport doors visible on borders
- [ ] Bomb machine at center with timer
- [ ] Can collect new power-ups
- [ ] All features working
- [ ] No crashes or errors

---

## 🐛 **If You See Errors:**
Report them with:
- Error message
- What you were doing
- Which feature caused it

---

## 🎉 **Have Fun Testing!**

**All features should now be working!** 🚀✨

**Play a few games and test everything!** 🎮
