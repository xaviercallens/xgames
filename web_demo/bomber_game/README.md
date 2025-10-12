# 🎮 Bomberman Educational Game

A fun and educational Bomberman game for learning Python, AI, and Reinforcement Learning!

## 🚀 Quick Start

```bash
# Make sure you're in the virtual environment
source game_dev_env/bin/activate

# Run the game
python play_bomberman.py
```

## 🎯 Game Features

### Current Implementation (v0.1)
- ✅ **13x13 grid-based world**
- ✅ **Human player** (green) with smooth movement
- ✅ **AI opponent** (red) with simple heuristics
- ✅ **Bomb mechanics** with timed explosions
- ✅ **Destructible walls** (brown blocks)
- ✅ **Indestructible walls** (gray blocks)
- ✅ **Power-ups** hidden under walls:
  - 🔴 **Bomb+**: Increase max bombs
  - 🟠 **Fire+**: Increase explosion range
  - 🔵 **Speed+**: Move faster
- ✅ **Win/lose conditions**
- ✅ **Pause and restart**

## 🎮 Controls

| Key | Action |
|-----|--------|
| **WASD** or **Arrow Keys** | Move player |
| **Space** | Place bomb |
| **P** | Pause/Unpause |
| **R** | Restart (when game over) |
| **ESC** | Quit game |

## 🤖 AI Behavior

The current AI opponent uses simple heuristics:

1. **Priority 1**: Avoid explosions (run to safety)
2. **Priority 2**: Place bomb when near player
3. **Priority 3**: Move toward player
4. **Default**: Random movement

This AI is intentionally simple so your son can:
- Beat it and feel accomplished
- Understand how it works
- Improve it as a learning exercise

## 📚 Learning Path

This is **Week 1-4** of the educational plan. Your son will learn:

### Week 1-2: Python Basics
- Variables and data types
- Functions and classes
- Pygame basics
- Game loop concept

### Week 3-4: Game Mechanics
- Object-oriented programming
- Collision detection
- Entity management
- Game state handling

### Next Steps (Week 5+)
- Improve AI with pathfinding (A*)
- Add machine learning
- Implement reinforcement learning
- Train AI to learn from experience

## 🏗️ Code Structure

```
bomber_game/
├── __init__.py           # Game constants
├── config.py             # Configuration
├── game_engine.py        # Main game loop
├── game_state.py         # Game state management
├── entities/             # Game entities
│   ├── entity.py         # Base entity class
│   ├── player.py         # Player character
│   ├── bomb.py           # Bomb entity
│   ├── explosion.py      # Explosion effect
│   └── powerup.py        # Power-up items
└── agents/               # AI agents
    ├── agent_base.py     # Base agent class
    └── simple_agent.py   # Simple AI opponent
```

## 🎓 Teaching Moments

### For Parents/Mentors:

1. **Start Simple**: Let your son play the game first
2. **Explore Code**: Look at `player.py` together
3. **Make Changes**: Try changing colors, speeds, bomb timers
4. **Add Features**: Challenge him to add new power-ups
5. **Improve AI**: Make the AI smarter together

### Discussion Questions:

- How does the game loop work?
- What makes the AI "intelligent"?
- How could we make the AI harder to beat?
- What new features would be fun to add?

## 🔧 Customization Ideas

Easy modifications to try:

```python
# In config.py - Make bombs explode faster
GAME_CONFIG = {
    'bomb_timer': 2.0,  # Change from 3.0 to 2.0
}

# In player.py - Start with more bombs
self.max_bombs = 2  # Change from 1 to 2

# In game_state.py - More power-ups
if random.random() < 0.5:  # Change from 0.3 to 0.5
```

## 🐛 Troubleshooting

### Game won't start
```bash
# Make sure pygame is installed
pip install pygame

# Check you're in virtual environment
source game_dev_env/bin/activate
```

### Game is too slow
- Close other applications
- Reduce grid size in config.py
- Lower FPS if needed

### AI is too hard/easy
- Adjust `think_delay` in `simple_agent.py`
- Modify AI priorities
- Change starting positions

## 📈 Next Features (Coming Soon)

- [ ] Multiple difficulty levels
- [ ] Better AI with pathfinding
- [ ] More power-up types
- [ ] Custom maps
- [ ] Sound effects
- [ ] Score tracking
- [ ] Tutorial mode
- [ ] ML-based AI
- [ ] RL training mode

## 🎯 Learning Objectives Achieved

After playing and exploring this code, your son will understand:

✅ **Python Fundamentals**
- Classes and objects
- Lists and dictionaries
- Functions and methods
- Loops and conditionals

✅ **Game Development**
- Game loop structure
- Event handling
- Collision detection
- State management

✅ **Problem Solving**
- Breaking down complex problems
- Debugging code
- Testing and iteration

## 🤝 Contributing

This is an educational project! Encourage your son to:
- Experiment with the code
- Add new features
- Fix bugs
- Improve the AI
- Share what he learns

## 📚 Resources

- **Full Specification**: See `spec.md`
- **Learning Plan**: See `EDUCATION_PLAN.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`

## 🎉 Have Fun!

Remember: The goal is to **learn and have fun**!
- Experiment freely
- Break things (you can always restart)
- Ask questions
- Be creative

**Happy coding! 🚀**
