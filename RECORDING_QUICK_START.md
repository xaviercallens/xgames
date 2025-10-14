# 🎬 Video Recording - Quick Start

## 3-Step Setup

### 1️⃣ Install FFmpeg
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/
```

### 2️⃣ Play Game
```bash
./play_bomberman.py
```

### 3️⃣ Record
- Press **'R'** to start recording
- Play your game
- Press **'R'** again to stop

---

## Output Files

All saved to `recordings/` directory:
- **`.webm`** - Web-optimized video (best for GitHub Pages)
- **`.mp4`** - Compatible video (works everywhere)
- **`.gif`** - Preview (first 5 seconds)
- **`.html`** - Ready-to-use embed page

---

## GitHub Pages Usage

### Embed Video in README
```markdown
<video width="100%" controls>
  <source src="recordings/your_video.webm" type="video/webm">
</video>
```

### Use GIF Preview
```markdown
![Gameplay](recordings/your_video_preview.gif)
```

---

## Tips

✅ **Keep recordings short** (30-60 seconds)  
✅ **Use WebM for web** (smaller files)  
✅ **Use GIF for previews** (universal compatibility)  
⚠️ **Stop before game over** (cleaner ending)  

---

📚 **Full Guide**: See [VIDEO_RECORDING_GUIDE.md](VIDEO_RECORDING_GUIDE.md)
