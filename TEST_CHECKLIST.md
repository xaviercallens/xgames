# 🧪 Feature Testing Checklist

## How to Test the New Features

### **Prerequisites:**
```bash
# Make sure you're on the feature branch
git checkout feature/enhanced-gameplay

# Launch the game
./launch_bomberman.sh
```

---

## ✅ **Test 1: Reduced Wall Density (5%)**

### **What to Look For:**
- Map should be much more open
- Very few destructible walls (brown/toilet walls)
- Lots of empty space to move around

### **Expected Result:**
- Only ~5% of empty spaces have walls
- Easy to navigate
- Less crowded than before

### **Test Steps:**
1. Launch game
2. Observe the map layout
3. Count walls - should be minimal
4. Try moving around - should be easy

**Status:** [ ] PASS / [ ] FAIL

**Notes:**
```
_________________________________________________
_________________________________________________
```

---

## ✅ **Test 2: Teleport Doors**

### **What to Look For:**
- 8 colored squares on the map borders
- 4 different colors (4 pairs)
- Pulsing animation
- Numbers displayed on doors

### **Test Steps:**
1. Look at map borders (edges)
2. Find colored door squares
3. Walk onto a door
4. Should teleport to paired door instantly
5. Try all 4 door pairs

### **Expected Behavior:**
- Door 1 (Magenta) → Teleports to other Door 1
- Door 2 (Cyan) → Teleports to other Door 2
- Door 3 (Yellow) → Teleports to other Door 3
- Door 4 (Orange) → Teleports to other Door 4

**Status:** [ ] PASS / [ ] FAIL

**Notes:**
```
Door colors seen: _________________________________
Teleportation works: YES / NO
_________________________________________________
```

---

## ✅ **Test 3: Bomb Machine**

### **What to Look For:**
- Gray/red machine at center of map
- Timer counting down from 10.0s
- Warning flash (red) at 2 seconds
- Bomb drops at 0 seconds
- Bomb explodes 10 seconds after drop

### **Test Steps:**
1. Look at center of map
2. Watch the timer countdown
3. At 2 seconds, machine should flash red
4. At 0 seconds, bomb should drop
5. Wait 10 more seconds for explosion
6. Avoid the danger zone!

### **Expected Behavior:**
- Timer displays: 10.0s → 9.0s → ... → 0.0s
- Warning at 2.0s (red flash)
- Bomb drops at center
- Danger zone circle appears during warning
- Explosion after 10s

**Status:** [ ] PASS / [ ] FAIL

**Notes:**
```
Timer visible: YES / NO
Warning works: YES / NO
Bomb drops: YES / NO
Explosion happens: YES / NO
_________________________________________________
```

---

## ✅ **Test 4: New Power-Ups**

### **What to Look For:**
- 6 different power-up types
- New colors: Green (Shield), Yellow (Remote), Purple (Pierce)
- Power-ups under destroyed walls

### **Test Steps:**

#### **4A: Shield Power-Up (Green)**
1. Find and collect green power-up
2. Walk into an explosion
3. Should survive first hit
4. Second hit should kill you

**Status:** [ ] PASS / [ ] FAIL

#### **4B: Remote Detonator (Yellow)**
1. Find and collect yellow power-up
2. Place a bomb (SPACE)
3. Move away
4. Press R key to detonate
5. Bomb should explode immediately

**Status:** [ ] PASS / [ ] FAIL

#### **4C: Pierce Bombs (Purple)**
1. Find and collect purple power-up
2. Place bomb next to wall
3. Explosion should go through walls
4. Can hit enemies behind walls

**Status:** [ ] PASS / [ ] FAIL

**Notes:**
```
Power-ups found:
[ ] Bomb+ (Red)
[ ] Fire+ (Orange)
[ ] Speed+ (Blue)
[ ] Shield (Green) - NEW
[ ] Remote (Yellow) - NEW
[ ] Pierce (Purple) - NEW
_________________________________________________
```

---

## 🎮 **Complete Gameplay Test**

### **Scenario: Full Feature Test**

1. **Start Game**
   - [ ] Map is open (5% walls)
   - [ ] Teleport doors visible on borders
   - [ ] Bomb machine at center with timer

2. **Movement**
   - [ ] Easy to move around (open space)
   - [ ] Can reach borders easily
   - [ ] No crowding

3. **Teleportation**
   - [ ] Walk to border door
   - [ ] Teleport to paired door
   - [ ] Use for quick escape

4. **Bomb Machine**
   - [ ] Watch timer countdown
   - [ ] See warning at 2s
   - [ ] Bomb drops at 0s
   - [ ] Avoid explosion

5. **Power-Ups**
   - [ ] Destroy walls to reveal power-ups
   - [ ] Collect different types
   - [ ] Test new power-ups (Shield, Remote, Pierce)

6. **Combat**
   - [ ] Fight AI opponent
   - [ ] Use teleport doors tactically
   - [ ] Avoid bomb machine
   - [ ] Use new power-ups strategically

**Overall Status:** [ ] PASS / [ ] FAIL

---

## 🐛 **Bug Report Template**

If you find any issues, document them here:

### **Bug 1:**
```
Feature: _____________________________________________
Issue: _______________________________________________
Steps to Reproduce:
1. ___________________________________________________
2. ___________________________________________________
3. ___________________________________________________

Expected: ____________________________________________
Actual: ______________________________________________
```

### **Bug 2:**
```
Feature: _____________________________________________
Issue: _______________________________________________
Steps to Reproduce:
1. ___________________________________________________
2. ___________________________________________________
3. ___________________________________________________

Expected: ____________________________________________
Actual: ______________________________________________
```

---

## 📊 **Performance Check**

### **Frame Rate:**
- [ ] Game runs smoothly (30 FPS)
- [ ] No lag with new features
- [ ] Animations are smooth

### **Visual Quality:**
- [ ] Teleport doors look good
- [ ] Bomb machine renders correctly
- [ ] New power-ups visible
- [ ] Timer text readable

**Status:** [ ] PASS / [ ] FAIL

---

## ✅ **Final Checklist**

Before marking features as complete:

- [ ] All 4 features implemented
- [ ] Wall density is 5%
- [ ] Teleport doors work (4 pairs)
- [ ] Bomb machine drops bombs every 10s
- [ ] 3 new power-ups collectible
- [ ] No game-breaking bugs
- [ ] Performance is good
- [ ] Visuals look professional

---

## 🎯 **Test Results Summary**

### **Features Tested:**
1. Wall Density (5%): [ ] PASS / [ ] FAIL
2. Teleport Doors: [ ] PASS / [ ] FAIL
3. Bomb Machine: [ ] PASS / [ ] FAIL
4. New Power-Ups: [ ] PASS / [ ] FAIL

### **Overall Result:**
[ ] ALL TESTS PASSED ✅
[ ] SOME ISSUES FOUND ⚠️
[ ] MAJOR BUGS 🐛

### **Ready for Merge:**
[ ] YES - All features working
[ ] NO - Bugs need fixing

---

## 📝 **Tester Notes**

```
Date: _______________
Tester: _____________

General Observations:
_____________________________________________________
_____________________________________________________
_____________________________________________________

Suggestions:
_____________________________________________________
_____________________________________________________
_____________________________________________________

Fun Factor (1-10): _____
Difficulty (1-10): _____
Visual Appeal (1-10): _____
```

---

## 🚀 **Quick Test Commands**

```bash
# Switch to feature branch
git checkout feature/enhanced-gameplay

# Launch game
./launch_bomberman.sh

# If issues, check logs
# Game output shows in terminal

# To test AI
# Just play normally - AI will use features too

# To reset and test again
# Press R when game over
# Or restart game
```

---

**Happy Testing!** 🎮✨

**Report any issues in the Bug Report section above.**
