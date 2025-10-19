# 🎨 Visual Reference Guide

## Game Visual Elements

### 🟢 Player Character (Green)
```
        👀
       /  \
      |    |
       \  /
       /  \
      |    |
      |    |
```
**Features:**
- Head with expressive eyes
- Body with outline
- Animated bobbing legs
- Shine highlight
- Smooth movement

**Animation:**
- Eyes follow direction
- Legs bob up and down
- Smooth sub-pixel positioning

---

### 🔴 AI Character (Red)
```
        👀
       /  \
      |    |
       \  /
       /  \
      |    |
      |    |
```
**Features:**
- Same as player but red
- Controlled by AI
- Same animation system

---

### 💨 Prout Bomb (Smelly Cloud)
```
     ~~~
    (   )
   (  ◯  )
    (   )
     ~~~
```
**Features:**
- Green main cloud
- Yellow secondary puffs
- Animated stink lines (wavy)
- Pulsing effect
- Brown caca marks
- Timer: 3 seconds

**Animation:**
- Pulsing size (grows as timer runs out)
- Wavy stink lines (4 directions)
- Stink intensity increases

**Concept:** Smelly fart bomb!

---

### 💩 Caca Obstacle (Poop Pile)
```
      ~~~
     (   )
    (  ◯  )
     (   )
    -------
```
**Features:**
- 3 stacked brown piles
- Animated stink lines
- Shine highlight
- Pulsing visibility
- Duration: 5 seconds

**Animation:**
- Wavy stink lines (3 rising)
- Pulsing visibility effect
- Smooth animations

**Concept:** Poop obstacle to avoid!

---

### 💥 Explosion (Expanding Cloud)
```
      ~~~
     (   )
    (  ◯  )
     (   )
      ~~~
```
**Features:**
- Green outer cloud
- Yellow-brown middle
- Brown inner core
- Expanding particles
- Fade-out effect
- Duration: 0.5 seconds

**Animation:**
- Expands outward
- Stink particles radiate (6 directions)
- Smooth fade-out
- Color progression

**Concept:** Smelly explosion!

---

### ⭐ Power-ups (Rotating Squares)

#### 💣 Bomb+ (Yellow)
```
    ◇◇◇
    ◇◇◇
    ◇◇◇
```
**Effect:** More bombs
**Color:** Yellow
**Animation:** Rotating square + pulsing glow

#### 🔥 Fire+ (Orange)
```
    ◇◇◇
    ◇◇◇
    ◇◇◇
```
**Effect:** Bigger explosions
**Color:** Orange
**Animation:** Rotating square + pulsing glow

#### ⚡ Speed+ (Blue)
```
    ◇◇◇
    ◇◇◇
    ◇◇◇
```
**Effect:** Move faster
**Color:** Blue
**Animation:** Rotating square + pulsing glow

#### 🛡️ Shield (Purple)
```
    ◇◇◇
    ◇◇◇
    ◇◇◇
```
**Effect:** Survive one hit
**Color:** Purple
**Animation:** Rotating square + pulsing glow

#### 📡 Remote (Pink)
```
    ◇◇◇
    ◇◇◇
    ◇◇◇
```
**Effect:** Detonate on command
**Color:** Pink
**Animation:** Rotating square + pulsing glow

#### ⚔️ Pierce (Green)
```
    ◇◇◇
    ◇◇◇
    ◇◇◇
```
**Effect:** Bombs pierce walls
**Color:** Green
**Animation:** Rotating square + pulsing glow

---

### 🧱 Walls

#### Hard Wall (Indestructible)
```
┌─────┐
│ ╱╲  │
│╱  ╲ │
│ ╲╱  │
└─────┘
```
**Features:**
- Stone texture
- Cracks pattern
- Dark gray color
- Cannot be destroyed

#### Soft Wall (Destructible)
```
┌─────┐
│ ║║║ │
│ ║║║ │
│ ║║║ │
└─────┘
```
**Features:**
- Wood grain texture
- Shine highlight
- Brown color
- Can be destroyed by bombs

---

### 🟩 Game Board

```
┌─────────────────────────────────┐
│ 🟢 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ │
│ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │
│ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ │
│ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │
│ 🧱 ░ 🧱 ░ 💨 ░ 🧱 ░ 🧱 ░ 🧱 ░ │
│ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │
│ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 💩 ░ 🧱 ░ │
│ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │
│ 🧱 ░ 🧱 ░ 🧱 ░ ⭐ ░ 🧱 ░ 🔴 │
└─────────────────────────────────┘
```

**Elements:**
- 🟢 = Green player
- 🔴 = Red AI player
- 🧱 = Walls (gray/brown)
- ░ = Empty floor (checkerboard)
- 💨 = Prout bomb
- 💩 = Caca obstacle
- ⭐ = Power-up
- 💥 = Explosion (temporary)

---

## Color Palette

### Primary Colors
```
PROUT_GREEN    = RGB(100, 200, 50)    ■ Green cloud
PROUT_YELLOW   = RGB(200, 200, 50)    ■ Yellow puff
PROUT_BROWN    = RGB(139, 90, 43)     ■ Caca brown
DARK_BROWN     = RGB(101, 67, 33)     ■ Dark caca
STINK_GREEN    = RGB(150, 220, 100)   ■ Stink lines
```

### Player Colors
```
PLAYER_GREEN   = RGB(0, 255, 0)       ■ Player
PLAYER_RED     = RGB(255, 0, 0)       ■ AI
```

### Background
```
FOREST_GREEN   = RGB(34, 139, 34)     ■ Dark floor
LIME_GREEN     = RGB(50, 205, 50)     ■ Light floor
```

---

## Animation Cycles

### Character Bobbing
```
Frame 0: ▄▄ (legs down)
Frame 1: ▀▀ (legs up)
→ Repeats smoothly
```

### Bomb Pulsing
```
Timer 3.0s: ◯ (normal)
Timer 2.0s: ◯ (slight pulse)
Timer 1.0s: ◉ (medium pulse)
Timer 0.5s: ◉ (large pulse - about to explode!)
```

### Stink Lines
```
Frame 0: ~~~
Frame 1: ~~~
Frame 2: ~~~
→ Wavy animation
```

### Power-up Rotation
```
0°:   ◇
45°:  ◆
90°:  ◇
135°: ◆
→ Continuous rotation
```

### Explosion Expansion
```
Start:  ◯ (small)
Middle: ◉ (medium)
End:    ◎ (large, fading)
```

---

## Visual Feedback

### What Each Visual Means

| Visual | Meaning | Action |
|--------|---------|--------|
| 🟢 Eyes looking | Player direction | Moving in that direction |
| 💨 Pulsing cloud | Bomb about to explode | Run away! |
| 💩 Stink rising | Caca obstacle | Can't walk through |
| 💥 Expanding cloud | Explosion happening | Damage zone |
| ⭐ Rotating square | Power-up available | Collect it! |
| 🧱 Gray wall | Hard wall | Can't break |
| 🧱 Brown wall | Soft wall | Can destroy |
| 🟢 Dead | Player eliminated | Game over |

---

## Screen Layout

```
┌─────────────────────────────────────────────────────┐
│                   GAME BOARD                        │
│                  (13x13 grid)                       │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ 🟢 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ │  │
│  │ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │  │
│  │ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ │  │
│  │ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │  │
│  │ 🧱 ░ 🧱 ░ 💨 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ │  │
│  │ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │  │
│  │ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 💩 ░ 🧱 ░ 🧱 ░ 🧱 ░ │  │
│  │ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 ░ 🧱 │  │
│  │ 🧱 ░ 🧱 ░ 🧱 ░ ⭐ ░ 🧱 ░ 🧱 ░ 🧱 ░ 🔴 │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Player: Trumps:2 Cacas:3 Range:2                 │
│  AI (PPO): Bombs:2 Range:2                        │
│  Controls: WASD=Move Space=Trump C=Caca P=Pause  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Animation Speeds

| Animation | Speed | Effect |
|-----------|-------|--------|
| Character bobbing | 0.15s per frame | Natural walking |
| Bomb pulsing | 8 Hz | Urgent feeling |
| Stink lines | 3 Hz | Flowing motion |
| Power-up rotation | 360°/10s | Smooth rotation |
| Explosion expansion | 0.5s total | Quick burst |
| Floating effect | 3 units/s | Gentle bobbing |

---

## Visual Hierarchy

### Rendering Order (Bottom to Top)
1. **Background** - Green checkerboard floor
2. **Walls** - Stone and wood textures
3. **Cacas** - Poop obstacles
4. **Bombs** - Smelly clouds
5. **Explosions** - Expanding clouds
6. **Power-ups** - Rotating squares
7. **Players** - Characters on top
8. **UI** - Stats and controls

---

## Professional Touches

### Depth Effects
- Outlines on characters
- Shine highlights
- Shadow effects
- Layered colors

### Smooth Animations
- Sine wave motion
- No jerky movements
- Continuous transitions
- Natural feel

### Visual Clarity
- Color coding
- Size variation
- Animation cues
- Clear feedback

### Professional Appearance
- Consistent theming
- Polished effects
- Smooth transitions
- Engaging visuals

---

## Summary

The enhanced graphics create a **visually cohesive, engaging game** with:
- ✅ Detailed characters
- ✅ Smelly prout clouds
- ✅ Poop obstacles
- ✅ Dramatic explosions
- ✅ Rotating power-ups
- ✅ Textured walls
- ✅ Smooth animations
- ✅ Professional appearance

**The visual theme perfectly represents the PROUTMAN concept!** 💨🎮💩

