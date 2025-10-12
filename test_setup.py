#!/usr/bin/env python3
"""
Quick test script to verify the game development environment is working.
"""

import sys
import os

def test_imports():
    """Test if all essential libraries can be imported."""
    print("🧪 Testing Python Game Development Environment")
    print("=" * 50)
    
    tests = [
        ("pygame", "Pygame (2D games)"),
        ("numpy", "NumPy (mathematical operations)"),
        ("PIL", "Pillow (image processing)"),
        ("pymunk", "Pymunk (2D physics)"),
        ("pydub", "Pydub (audio processing)"),
    ]
    
    passed = 0
    failed = 0
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {description}")
            passed += 1
        except ImportError as e:
            print(f"❌ {description} - {e}")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All core libraries are working!")
        return True
    else:
        print("⚠️  Some libraries are missing. Install them with:")
        print("   source game_dev_env/bin/activate")
        print("   pip install -r requirements.txt")
        return False

def test_pygame():
    """Test pygame initialization."""
    try:
        import pygame
        pygame.init()
        
        # Test creating a small window
        screen = pygame.display.set_mode((100, 100))
        pygame.display.set_caption("Test")
        
        # Clean up
        pygame.quit()
        
        print("✅ Pygame initialization test passed")
        return True
        
    except Exception as e:
        print(f"❌ Pygame test failed: {e}")
        return False

def test_utility_modules():
    """Test our custom utility modules."""
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from utils.game_math import Vector2D, circle_collision
        from utils.input_handler import InputManager
        
        # Test Vector2D
        v1 = Vector2D(3, 4)
        v2 = Vector2D(1, 1)
        result = v1 + v2
        assert result.x == 4 and result.y == 5, "Vector addition failed"
        
        # Test collision detection
        collision = circle_collision((0, 0), 5, (3, 4), 5)
        assert collision == True, "Circle collision detection failed"
        
        print("✅ Utility modules test passed")
        return True
        
    except Exception as e:
        print(f"❌ Utility modules test failed: {e}")
        return False

def main():
    """Run all tests."""
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}\n")
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    print()
    
    # Test pygame
    if not test_pygame():
        all_passed = False
    
    print()
    
    # Test utility modules
    if not test_utility_modules():
        all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All tests passed! Your environment is ready for game development!")
        print("\n🚀 Try running a game:")
        print("   python games_2d/space_shooter.py")
        print("   python examples/simple_platformer.py")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
