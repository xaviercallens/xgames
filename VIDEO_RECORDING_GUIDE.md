# 🎬 Video Recording Guide for Proutman

## Overview

Proutman now includes a **built-in video recording system** that allows you to capture and share your epic gameplay moments! Press the **'R' key** during gameplay to start/stop recording.

## Features

✅ **One-Key Recording**: Press 'R' to toggle recording on/off  
✅ **Web-Optimized Output**: Exports to WebM format (perfect for GitHub Pages)  
✅ **Multiple Formats**: WebM, MP4, and GIF preview  
✅ **Auto-Generated HTML**: Ready-to-use embed code for websites  
✅ **Metadata Tracking**: Duration, FPS, resolution, file sizes  
✅ **GitHub Pages Ready**: All outputs optimized for web sharing  

---

## Quick Start

### 1. Install FFmpeg (Required)

The video recorder uses FFmpeg for encoding. Install it first:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### 2. Start Playing

```bash
./play_bomberman.py
# or
python play_bomberman.py
```

### 3. Record Gameplay

1. **Start Recording**: Press **'R'** during gameplay
2. **Play Your Game**: The recording indicator will show in the top-right
3. **Stop Recording**: Press **'R'** again to stop and save

---

## Recording Controls

| Key | Action |
|-----|--------|
| **R** | Start/Stop recording (during gameplay) |
| **R** | Restart game (when game over) |

**Note**: The 'R' key has dual functionality:
- **During gameplay**: Toggle recording
- **After game over**: Restart the game

---

## Output Files

All recordings are saved to the `recordings/` directory:

```
recordings/
├── proutman_20251014_073000.webm           # WebM video (web-optimized)
├── proutman_20251014_073000.mp4            # MP4 video (compatibility)
├── proutman_20251014_073000_preview.gif    # GIF preview (first 5 seconds)
├── proutman_20251014_073000_metadata.json  # Recording metadata
└── proutman_20251014_073000_embed.html     # HTML embed code
```

### File Formats Explained

#### WebM (.webm)
- **Best for**: GitHub Pages, modern websites
- **Codec**: VP9 (excellent quality/size ratio)
- **Size**: Smallest file size
- **Compatibility**: All modern browsers

#### MP4 (.mp4)
- **Best for**: Maximum compatibility
- **Codec**: H.264
- **Size**: Medium file size
- **Compatibility**: All browsers, mobile devices

#### GIF Preview (.gif)
- **Best for**: README previews, quick sharing
- **Duration**: First 5 seconds only
- **Size**: Larger than video formats
- **Compatibility**: Universal (works everywhere)

---

## Using Recordings on GitHub Pages

### Option 1: Embed Video in README

```markdown
## Gameplay Demo

<video width="100%" controls>
  <source src="recordings/proutman_20251014_073000.webm" type="video/webm">
  <source src="recordings/proutman_20251014_073000.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

### Option 2: Use GIF Preview

```markdown
## Gameplay Demo

![Proutman Gameplay](recordings/proutman_20251014_073000_preview.gif)
```

### Option 3: Link to HTML Page

```markdown
## Gameplay Demo

[▶️ Watch Full Gameplay](recordings/proutman_20251014_073000_embed.html)
```

### Option 4: Use Auto-Generated HTML

The recorder creates a ready-to-use HTML file with:
- Embedded video player
- Metadata display
- Download links
- Markdown embed code

Simply open `recordings/*_embed.html` in a browser or host it on GitHub Pages!

---

## Recording Settings

### Default Settings

```python
fps = 60              # Frames per second
output_dir = "recordings"
webm_quality = 30     # CRF (0-63, lower = better)
mp4_quality = 23      # CRF (0-51, lower = better)
gif_duration = 5      # Seconds for preview
```

### Customizing Settings

Edit `bomber_game/video_recorder.py` to change:

```python
# In _encode_video() method:

# Better quality (larger files)
'-crf', '20',  # Change from 30 to 20

# Lower quality (smaller files)
'-crf', '35',  # Change from 30 to 35

# Longer GIF preview
max_frames = min(len(self.frames), self.fps * 10)  # 10 seconds instead of 5
```

---

## Metadata File

Each recording includes a JSON metadata file:

```json
{
  "recording_name": "proutman_20251014_073000",
  "timestamp": "2025-10-14T07:30:00",
  "duration_seconds": 45.5,
  "fps": 60,
  "frame_count": 2730,
  "dropped_frames": 0,
  "resolution": {
    "width": 1116,
    "height": 640
  },
  "files": {
    "webm": "proutman_20251014_073000.webm",
    "mp4": "proutman_20251014_073000.mp4",
    "gif_preview": "proutman_20251014_073000_preview.gif"
  },
  "file_sizes": {
    "webm_mb": 2.5,
    "mp4_mb": 3.2,
    "gif_mb": 8.1
  }
}
```

---

## Best Practices

### 1. Keep Recordings Short

- ✅ **Recommended**: 30-60 seconds per recording
- ⚠️ **Warning**: 1-2 minutes (memory intensive)
- ❌ **Avoid**: 3+ minutes (may cause issues)

**Why?** Each frame is stored in memory until encoding. Longer recordings use more RAM.

### 2. Stop Recording Before Game Over

Stop recording before the game ends to capture the final moments without the game-over screen.

### 3. Name Your Sessions

The recorder automatically names files based on game number:
- `game_1_20251014_073000.webm`
- `game_2_20251014_073015.webm`

### 4. Organize Recordings

Create subdirectories for different types of recordings:

```bash
recordings/
├── epic_wins/
├── funny_moments/
├── ai_training/
└── tutorials/
```

---

## Troubleshooting

### "FFmpeg not found!"

**Problem**: FFmpeg is not installed or not in PATH.

**Solution**:
```bash
# Check if ffmpeg is installed
ffmpeg -version

# If not found, install it (see Quick Start section)
```

### Recording is Laggy

**Problem**: Recording at 60 FPS is CPU-intensive.

**Solutions**:
1. Lower the FPS:
   ```python
   # In game_engine.py __init__:
   self.video_recorder = VideoRecorder(output_dir="recordings", fps=30)
   ```

2. Close other applications

3. Record shorter sessions

### Large File Sizes

**Problem**: Video files are too large.

**Solutions**:
1. Use WebM instead of MP4 (smaller)
2. Increase CRF value (lower quality, smaller size)
3. Record at lower FPS
4. Keep recordings short

### Memory Warning During Recording

**Problem**: "Memory usage may be high" warning appears.

**Solution**: Stop recording (press 'R') to save the current recording, then start a new one if needed.

### Encoding Takes Too Long

**Problem**: FFmpeg encoding is slow.

**Solutions**:
1. Use faster preset:
   ```python
   '-preset', 'fast',  # Change from 'medium'
   ```

2. Skip MP4 generation (only create WebM)

3. Skip GIF generation

---

## Advanced Usage

### Programmatic Recording

You can control recording programmatically:

```python
from bomber_game.video_recorder import VideoRecorder

# Create recorder
recorder = VideoRecorder(output_dir="my_recordings", fps=60)

# Start recording
recorder.start_recording(session_name="epic_battle")

# In game loop:
recorder.capture_frame(screen)

# Stop and save
metadata = recorder.stop_recording()
print(f"Saved: {metadata['recording_name']}")
```

### Custom Session Names

```python
# In game_engine.py, modify the recording toggle:
session_name = "tutorial_level_1"  # Custom name
self.video_recorder.toggle_recording(session_name)
```

### Batch Processing

Convert all recordings to a different format:

```bash
# Convert all WebM to MP4
for file in recordings/*.webm; do
    ffmpeg -i "$file" "${file%.webm}.mp4"
done

# Create thumbnails
for file in recordings/*.webm; do
    ffmpeg -i "$file" -vframes 1 "${file%.webm}_thumb.jpg"
done
```

---

## GitHub Pages Integration

### Step 1: Upload Recordings

```bash
# Add recordings to git
git add recordings/*.webm recordings/*.gif recordings/*.html

# Commit
git commit -m "Add gameplay recordings"

# Push to GitHub
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to repository Settings
2. Navigate to Pages section
3. Select branch: `main`
4. Select folder: `/` (root)
5. Save

### Step 3: Access Your Videos

Your recordings will be available at:
```
https://yourusername.github.io/yourrepo/recordings/filename.webm
```

### Step 4: Embed in README

```markdown
## 🎮 Gameplay Videos

### Epic Win Against AI
<video width="100%" controls>
  <source src="https://yourusername.github.io/yourrepo/recordings/epic_win.webm" type="video/webm">
</video>

### Funny Moment
![Funny Gameplay](https://yourusername.github.io/yourrepo/recordings/funny_moment_preview.gif)
```

---

## Performance Tips

### Optimize for Web

1. **Use WebM**: Smaller files, better for web
2. **Limit Duration**: 30-60 seconds ideal
3. **Use GIF for Previews**: Quick loading, universal compatibility
4. **Compress Further**: Use online tools like [Handbrake](https://handbrake.fr/)

### Optimize for Quality

1. **Lower CRF**: Better quality, larger files
2. **Higher FPS**: Smoother playback
3. **Use MP4**: Better compatibility with editing software

---

## Examples

### Example 1: Quick Gameplay Clip

```bash
# 1. Start game
./play_bomberman.py

# 2. Press 'R' to start recording
# 3. Play for 30 seconds
# 4. Press 'R' to stop

# Result: recordings/game_1_TIMESTAMP.webm
```

### Example 2: Tutorial Video

```bash
# 1. Start game
./play_bomberman.py

# 2. Press 'R' to start recording
# 3. Demonstrate game mechanics
# 4. Press 'R' to stop

# 5. Rename for clarity
mv recordings/game_1_*.webm recordings/tutorial_basics.webm
```

### Example 3: AI Training Showcase

```bash
# Record multiple games to show AI improvement
# Game 1: Beginner AI
# Game 2: Intermediate AI  
# Game 3: Expert AI

# Create comparison video
```

---

## FAQ

**Q: Can I record multiple games in one session?**  
A: Yes! Each time you press 'R', a new recording starts with an incremented game number.

**Q: Does recording affect game performance?**  
A: Slightly. Recording at 60 FPS uses CPU for frame capture. Lower FPS if needed.

**Q: Can I edit the recordings?**  
A: Yes! Use any video editor that supports WebM/MP4 (e.g., DaVinci Resolve, Kdenlive, iMovie).

**Q: How do I delete old recordings?**  
A: Simply delete files from the `recordings/` directory.

**Q: Can I change the output directory?**  
A: Yes, edit `game_engine.py`:
```python
self.video_recorder = VideoRecorder(output_dir="my_videos", fps=60)
```

**Q: Why is the GIF so large?**  
A: GIFs are uncompressed. Use video formats for better compression. GIFs are best for short previews.

**Q: Can I record audio?**  
A: Not currently. The recorder only captures video frames. Audio support may be added in future versions.

---

## Technical Details

### Architecture

```
VideoRecorder
├── Frame Capture (pygame.Surface.copy())
├── Temporary Storage (in-memory list)
├── Frame Export (PNG files)
├── FFmpeg Encoding
│   ├── WebM (VP9 codec)
│   ├── MP4 (H.264 codec)
│   └── GIF (palette optimization)
└── Metadata Generation (JSON + HTML)
```

### Performance Characteristics

| Metric | Value |
|--------|-------|
| Frame Capture | ~0.5ms per frame |
| Memory Usage | ~2MB per second (60 FPS) |
| Encoding Time | ~10-30s for 60s video |
| WebM Compression | ~0.5MB per second |
| MP4 Compression | ~0.7MB per second |

---

## Future Enhancements

Planned features for future versions:

- [ ] Audio recording support
- [ ] Real-time encoding (no memory limit)
- [ ] Cloud upload integration
- [ ] Automatic highlight detection
- [ ] Slow-motion replay
- [ ] Picture-in-picture commentary
- [ ] Live streaming support

---

## Credits

- **FFmpeg**: Video encoding engine
- **Pygame**: Frame capture
- **VP9/H.264**: Video codecs

---

## Support

Having issues? Check:

1. **FFmpeg Installation**: `ffmpeg -version`
2. **Disk Space**: Ensure enough space in `recordings/`
3. **Memory**: Close other applications if recording long sessions
4. **Permissions**: Ensure write access to `recordings/` directory

For bugs or feature requests, open an issue on GitHub!

---

**Happy Recording! 🎬💨**
