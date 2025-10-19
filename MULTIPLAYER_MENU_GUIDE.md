# 🎮 Multiplayer Menu System Guide

## Overview

Comprehensive menu system for configuring multiplayer games with support for:
- Multiple game modes (1v1, 2-4 players)
- Human and AI player selection
- AI difficulty/mode selection
- Player name customization
- Game configuration summary

---

## 🎯 Features

### Game Mode Selection
- ✅ 1v1 (Human vs AI)
- ✅ 2 Players (Local)
- ✅ 3 Players (Local)
- ✅ 4 Players (Local)
- ✅ 2 Human + 1 AI
- ✅ 2 Human + 2 AI
- ✅ 3 Human + 1 AI

### Player Configuration
- ✅ Human player name input
- ✅ AI mode selection
- ✅ Player color assignment
- ✅ Configuration summary

### AI Modes
- ✅ Beginner Bot (10% WR)
- ✅ Intermediate Bot (35% WR)
- ✅ Advanced Bot (Smart) (60% WR)

---

## 📊 Menu Flow

```
Main Menu
    ↓
Game Mode Selection
    ├─ 1v1 (Human vs AI)
    ├─ 2 Players (Local)
    ├─ 3 Players (Local)
    ├─ 4 Players (Local)
    ├─ 2 Human + 1 AI
    ├─ 2 Human + 2 AI
    └─ 3 Human + 1 AI
    ↓
Player Configuration
    ├─ Human Player 1: Name Input
    ├─ Human Player 2: Name Input (if applicable)
    ├─ AI Player 1: Mode Selection
    ├─ AI Player 2: Mode Selection (if applicable)
    └─ ...
    ↓
Configuration Summary
    ├─ Review all players
    ├─ START GAME
    └─ GO BACK
    ↓
Game Start
```

---

## 🎮 User Interface

### Game Mode Selection Screen

```
┌─────────────────────────────────────────┐
│         🎮 Select Game Mode             │
│      Choose how many players            │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 1v1 (Human vs AI)      👤 1 🤖 1 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 2 Players (Local)      👤 2 🤖 0 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 3 Players (Local)      👤 3 🤖 0 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ 4 Players (Local)      👤 4 🤖 0 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ↑↓ or W/S to select | ENTER to confirm│
│  ESC to go back                         │
└─────────────────────────────────────────┘
```

### Player Name Input Screen

```
┌─────────────────────────────────────────┐
│          👤 Player Name                 │
├─────────────────────────────────────────┤
│                                         │
│           Player 1                      │
│                                         │
│    ┌─────────────────────────────┐     │
│    │ Player Name_                │     │
│    └─────────────────────────────┘     │
│                                         │
│    Type name and press ENTER            │
│                                         │
└─────────────────────────────────────────┘
```

### AI Mode Selection Screen

```
┌─────────────────────────────────────────┐
│        🤖 Select AI Mode                │
│         AI Player 1                     │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Beginner Bot                    │   │
│  │ Expected Win Rate: 10%          │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Intermediate Bot                │   │
│  │ Expected Win Rate: 35%          │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Advanced Bot (Smart)            │   │
│  │ Expected Win Rate: 60%          │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ↑↓ or W/S to select | ENTER to confirm│
│  ESC to go back                         │
└─────────────────────────────────────────┘
```

### Configuration Summary Screen

```
┌─────────────────────────────────────────┐
│      🎮 Game Configuration              │
├─────────────────────────────────────────┤
│                                         │
│  👤 Player 1 (Human)                    │
│  👤 Player 2 (Human)                    │
│  🤖 AI 1 (intermediate_heuristic)       │
│                                         │
│                                         │
│      [START GAME]    [GO BACK]          │
│                                         │
│  ↑↓ or W/S to select | ENTER to confirm│
│  ESC to go back                         │
└─────────────────────────────────────────┘
```

---

## 🎮 Controls

### Navigation
- **↑↓ or W/S**: Move up/down
- **ENTER or SPACE**: Confirm selection
- **ESC**: Go back
- **MOUSE**: Click to select

### Text Input
- **Type**: Enter player name
- **BACKSPACE**: Delete character
- **ENTER**: Confirm name
- **ESC**: Cancel

---

## 💻 Code Usage

### Basic Usage

```python
from bomber_game.multiplayer_menu import MultiplayerMenu

# Create menu
menu = MultiplayerMenu(screen)

# Show game mode selection
game_mode = menu.show_game_mode_selection()
if game_mode is None:
    return  # User cancelled

# Show player configuration
players_config = menu.show_player_configuration(game_mode)
if players_config is None:
    return  # User cancelled

# Show summary
if menu.show_summary(players_config):
    # Start game with players_config
    start_game(players_config)
```

### Game Configuration

```python
from bomber_game.multiplayer_config import (
    GameConfig, PlayerConfig, GameConfigBuilder,
    create_1v1_config, create_4player_local_config
)

# Create configuration manually
config = GameConfig()
config.add_player(PlayerConfig(1, 'Player 1', 'human', None, (0, 255, 0)))
config.add_player(PlayerConfig(2, 'AI 1', 'ai', 'intermediate_heuristic', (255, 0, 0)))

# Or use builder
builder = GameConfigBuilder()
builder.add_human_player('Player 1', (0, 255, 0))
builder.add_ai_player('AI 1', 'intermediate_heuristic', (255, 0, 0))
config = builder.build()

# Or use presets
config = create_1v1_config('Player', 'advanced_heuristic')
config = create_4player_local_config(['P1', 'P2', 'P3', 'P4'])

# Access configuration
print(f"Total players: {config.get_player_count()}")
print(f"Human players: {config.get_human_count()}")
print(f"AI players: {config.get_ai_count()}")

for player in config.players:
    print(f"{player.name}: {player.type}")
```

---

## 📊 Game Modes

### 1v1 (Human vs AI)
```
Players: 1 Human + 1 AI
Setup: Human player vs selected AI opponent
Best for: Single player experience
```

### 2 Players (Local)
```
Players: 2 Humans
Setup: Two human players on same machine
Controls: Player 1 (WASD), Player 2 (Arrow Keys)
Best for: Local multiplayer
```

### 3 Players (Local)
```
Players: 3 Humans
Setup: Three human players on same machine
Controls: P1 (WASD), P2 (Arrow Keys), P3 (IJKL)
Best for: Local multiplayer
```

### 4 Players (Local)
```
Players: 4 Humans
Setup: Four human players on same machine
Controls: P1 (WASD), P2 (Arrow Keys), P3 (IJKL), P4 (Numpad)
Best for: Local multiplayer
```

### 2 Human + 1 AI
```
Players: 2 Humans + 1 AI
Setup: Two human players vs one AI
Best for: Cooperative gameplay
```

### 2 Human + 2 AI
```
Players: 2 Humans + 2 AI
Setup: Two human players vs two AI
Best for: Team gameplay
```

### 3 Human + 1 AI
```
Players: 3 Humans + 1 AI
Setup: Three human players vs one AI
Best for: Cooperative gameplay
```

---

## 🤖 AI Modes

### Beginner Bot
- **Type**: `simple`
- **Win Rate**: 10%
- **Difficulty**: Easy
- **Features**: Basic danger avoidance
- **Best for**: Learning

### Intermediate Bot
- **Type**: `heuristic`
- **Win Rate**: 35%
- **Difficulty**: Medium
- **Features**: A* pathfinding, strategic planning
- **Best for**: Balanced challenge

### Advanced Bot (Smart)
- **Type**: `advanced_heuristic`
- **Win Rate**: 60%
- **Difficulty**: Hard
- **Features**: Predictive analysis, game tree evaluation
- **Best for**: Expert challenge

---

## 🎨 Player Colors

```
Player 1: Green   (0, 255, 0)
Player 2: Red     (255, 0, 0)
Player 3: Blue    (0, 0, 255)
Player 4: Yellow  (255, 255, 0)
```

---

## 📋 Configuration Structure

### PlayerConfig
```python
{
    'player_id': 1,
    'name': 'Player 1',
    'type': 'human',  # or 'ai'
    'ai_mode': None,  # or 'beginner', 'intermediate', 'advanced'
    'color': (0, 255, 0)
}
```

### GameConfig
```python
{
    'players': [
        {'player_id': 1, 'name': 'Player 1', 'type': 'human', ...},
        {'player_id': 2, 'name': 'AI 1', 'type': 'ai', ...}
    ],
    'game_mode': 'local',
    'max_players': 4,
    'grid_size': 13
}
```

---

## 🔄 Integration with Game Engine

### In game_engine.py

```python
from bomber_game.multiplayer_menu import MultiplayerMenu
from bomber_game.multiplayer_config import GameConfig

# In game initialization
menu = MultiplayerMenu(self.screen)

# Show game mode selection
game_mode = menu.show_game_mode_selection()

# Show player configuration
players_config = menu.show_player_configuration(game_mode)

# Show summary
if menu.show_summary(players_config):
    # Create game with configuration
    self.setup_multiplayer_game(players_config)
```

---

## ✅ Features Implemented

### Menu System
- ✅ Game mode selection (7 modes)
- ✅ Player name input
- ✅ AI mode selection (3 modes)
- ✅ Configuration summary
- ✅ Keyboard navigation
- ✅ Mouse support
- ✅ Pulsing animations

### Configuration System
- ✅ PlayerConfig class
- ✅ GameConfig class
- ✅ GameConfigBuilder
- ✅ Preset configurations
- ✅ Serialization (to/from dict)
- ✅ Validation

### User Experience
- ✅ Clear instructions
- ✅ Visual feedback
- ✅ Smooth transitions
- ✅ Error handling
- ✅ Intuitive controls

---

## 🎯 Next Steps

### Integration
1. Update game_engine.py to use multiplayer menu
2. Update main menu to show multiplayer option
3. Implement 4-player game state
4. Update player controllers

### Enhancement
1. Add network multiplayer menu
2. Add server/client selection
3. Add connection settings
4. Add player name validation

### Testing
1. Test all game modes
2. Test player configuration
3. Test AI mode selection
4. Test edge cases

---

## 📚 Files

### Created
- `bomber_game/multiplayer_menu.py` (400+ lines)
- `bomber_game/multiplayer_config.py` (300+ lines)
- `MULTIPLAYER_MENU_GUIDE.md` (this file)

### Total
- **Lines**: 700+
- **Classes**: 5
- **Methods**: 30+

---

## 🎉 Summary

The multiplayer menu system provides:
- ✅ 7 game mode options
- ✅ Flexible player configuration
- ✅ 3 AI difficulty levels
- ✅ Intuitive user interface
- ✅ Comprehensive configuration system
- ✅ Easy integration

**Ready for game engine integration!** 🚀

