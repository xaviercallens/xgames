#!/bin/bash
# Activation script for Python Game Development Environment

echo "🎮 Activating Python Game Development Environment..."
echo "=================================================="

# Activate virtual environment
source game_dev_env/bin/activate

# Check Python version
echo "✅ Python version: $(python --version)"

# Check key libraries
echo "✅ Pygame version: $(python -c 'import pygame; print(pygame.version.ver)' 2>/dev/null || echo 'Not installed')"
echo "✅ NumPy version: $(python -c 'import numpy; print(numpy.__version__)' 2>/dev/null || echo 'Not installed')"
echo "✅ Pymunk version: $(python -c 'import pymunk; print(pymunk.version)' 2>/dev/null || echo 'Not installed')"

echo ""
echo "🚀 Available Games:"
echo "   python games_2d/space_shooter.py      # 2D Space Shooter"
echo "   python games_3d/cube_runner.py        # 3D Cube Runner (requires Panda3D)"
echo "   python examples/simple_platformer.py  # 2D Platformer"
echo "   python examples/physics_demo.py       # Physics Demo"
echo "   python snake_game.py                  # Original Snake Game"
echo ""
echo "📚 Documentation:"
echo "   cat docs/getting_started.md           # Getting started guide"
echo "   cat README.md                         # Full documentation"
echo ""
echo "Environment activated! Happy coding! 🎯"

# Start a new shell with the environment activated
exec bash
