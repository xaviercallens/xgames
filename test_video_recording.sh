#!/bin/bash
# Test Video Recording Feature

echo "========================================"
echo "🎬 Video Recording Feature Test"
echo "========================================"
echo ""

# Check FFmpeg
echo "1️⃣ Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "   ✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
else
    echo "   ❌ FFmpeg not found!"
    echo ""
    echo "   Install FFmpeg:"
    echo "   Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   macOS: brew install ffmpeg"
    echo ""
    exit 1
fi

echo ""
echo "2️⃣ Checking Python dependencies..."
python3 -c "import pygame" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Pygame installed"
else
    echo "   ❌ Pygame not found!"
    echo "   Install: pip install pygame"
    exit 1
fi

echo ""
echo "3️⃣ Creating recordings directory..."
mkdir -p recordings
echo "   ✅ Directory ready: recordings/"

echo ""
echo "4️⃣ Checking video recorder module..."
python3 -c "from bomber_game.video_recorder import VideoRecorder; print('   ✅ VideoRecorder module OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "   ❌ VideoRecorder module error"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ All checks passed!"
echo "========================================"
echo ""
echo "🎮 Ready to record gameplay!"
echo ""
echo "Instructions:"
echo "  1. Run: ./play_bomberman.py"
echo "  2. Press 'R' to start recording"
echo "  3. Play your game"
echo "  4. Press 'R' to stop and save"
echo ""
echo "Output files will be in: recordings/"
echo ""
