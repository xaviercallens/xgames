"""
Setup script for Python Game Development Environment.
Run this to install all dependencies and set up the development environment.
"""

import subprocess
import sys
import os


def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_requirements():
    """Install all required packages."""
    print("\n📦 Installing required packages...")
    
    success, output = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    if success:
        print("✅ All packages installed successfully!")
        return True
    else:
        print("❌ Failed to install packages:")
        print(output)
        return False


def test_imports():
    """Test if all major libraries can be imported."""
    print("\n🧪 Testing library imports...")
    
    libraries = [
        ("pygame", "Pygame (2D games)"),
        ("panda3d.core", "Panda3D (3D games)"),
        ("numpy", "NumPy (mathematical operations)"),
        ("PIL", "Pillow (image processing)"),
    ]
    
    failed_imports = []
    
    for lib, description in libraries:
        try:
            __import__(lib)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description}")
            failed_imports.append(lib)
    
    if failed_imports:
        print(f"\n⚠️  Some libraries failed to import: {', '.join(failed_imports)}")
        print("   You may need to install them manually or check for system dependencies.")
        return False
    
    print("\n🎉 All libraries imported successfully!")
    return True


def create_example_assets():
    """Create some basic asset files for testing."""
    print("\n🎨 Creating example assets...")
    
    # Create a simple test image using PIL
    try:
        from PIL import Image, ImageDraw
        
        # Create images directory if it doesn't exist
        os.makedirs("assets/images", exist_ok=True)
        
        # Create a simple player sprite
        img = Image.new('RGBA', (32, 32), (0, 255, 0, 255))  # Green square
        draw = ImageDraw.Draw(img)
        draw.rectangle([8, 8, 24, 24], fill=(0, 200, 0, 255))  # Darker green center
        img.save("assets/images/player.png")
        
        # Create a simple enemy sprite
        img = Image.new('RGBA', (32, 32), (255, 0, 0, 255))  # Red square
        draw = ImageDraw.Draw(img)
        draw.rectangle([8, 8, 24, 24], fill=(200, 0, 0, 255))  # Darker red center
        img.save("assets/images/enemy.png")
        
        print("✅ Example sprites created in assets/images/")
        
    except ImportError:
        print("⚠️  Could not create example images (PIL not available)")


def run_quick_test():
    """Run a quick test to make sure everything works."""
    print("\n🚀 Running quick functionality test...")
    
    # Test pygame initialization
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((100, 100))
        pygame.quit()
        print("✅ Pygame initialization test passed")
    except Exception as e:
        print(f"❌ Pygame test failed: {e}")
        return False
    
    # Test utility modules
    try:
        from utils.game_math import Vector2D, circle_collision
        from utils.input_handler import InputManager
        
        # Test Vector2D
        v1 = Vector2D(3, 4)
        v2 = Vector2D(1, 1)
        result = v1 + v2
        assert result.x == 4 and result.y == 5
        
        # Test collision detection
        collision = circle_collision((0, 0), 5, (3, 4), 5)
        assert collision == True
        
        print("✅ Utility modules test passed")
        
    except Exception as e:
        print(f"❌ Utility modules test failed: {e}")
        return False
    
    return True


def main():
    """Main setup function."""
    print("🎮 Python Game Development Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation.")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n⚠️  Setup completed with warnings. Some features may not work.")
    
    # Create example assets
    create_example_assets()
    
    # Run quick test
    if run_quick_test():
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 You can now run the example games:")
        print("   python games_2d/space_shooter.py")
        print("   python games_3d/cube_runner.py")
        print("   python snake_game.py")
    else:
        print("\n⚠️  Setup completed but some tests failed.")
        print("   Check the error messages above for troubleshooting.")


if __name__ == "__main__":
    main()
