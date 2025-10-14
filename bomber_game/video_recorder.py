"""
Video Recording System for Proutman
Records gameplay sessions and exports to web-friendly formats.

Features:
- Press 'R' to start/stop recording
- Exports to WebM format (best for web)
- Automatic GIF generation for previews
- Metadata tracking (duration, FPS, resolution)
- GitHub Pages compatible output
"""

import pygame
import os
import json
from datetime import datetime
from pathlib import Path
import subprocess
import tempfile
from typing import Optional, List


class VideoRecorder:
    """
    Records pygame screen to video files.
    Supports WebM (for web) and MP4 (for compatibility).
    """
    
    def __init__(self, output_dir: str = "recordings", fps: int = 60):
        """
        Initialize video recorder.
        
        Args:
            output_dir: Directory to save recordings
            fps: Frames per second for recording
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.fps = fps
        self.is_recording = False
        self.frames: List[pygame.Surface] = []
        self.start_time: Optional[datetime] = None
        self.recording_name: Optional[str] = None
        
        # Check for ffmpeg (required for video encoding)
        self.ffmpeg_available = self._check_ffmpeg()
        
        # Recording stats
        self.frame_count = 0
        self.dropped_frames = 0
        
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available."""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def start_recording(self, session_name: Optional[str] = None):
        """
        Start recording gameplay.
        
        Args:
            session_name: Optional custom name for the recording
        """
        if self.is_recording:
            print("⚠️  Already recording!")
            return
        
        if not self.ffmpeg_available:
            print("❌ FFmpeg not found! Install it to enable video recording:")
            print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   macOS: brew install ffmpeg")
            print("   Windows: Download from https://ffmpeg.org/")
            return
        
        self.is_recording = True
        self.frames = []
        self.start_time = datetime.now()
        self.frame_count = 0
        self.dropped_frames = 0
        
        # Generate recording name
        if session_name:
            timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
            self.recording_name = f"{session_name}_{timestamp}"
        else:
            self.recording_name = self.start_time.strftime("proutman_%Y%m%d_%H%M%S")
        
        print(f"🎬 Recording started: {self.recording_name}")
        print(f"   Press 'R' again to stop recording")
    
    def capture_frame(self, screen: pygame.Surface):
        """
        Capture a single frame from the pygame screen.
        
        Args:
            screen: Pygame surface to capture
        """
        if not self.is_recording:
            return
        
        try:
            # Create a copy of the screen surface
            frame = screen.copy()
            self.frames.append(frame)
            self.frame_count += 1
            
            # Memory management: warn if too many frames
            if len(self.frames) > 3600:  # ~1 minute at 60 FPS
                print(f"⚠️  Recording {len(self.frames)} frames ({len(self.frames)/self.fps:.1f}s)")
                print(f"   Memory usage may be high. Consider stopping recording.")
        
        except Exception as e:
            self.dropped_frames += 1
            if self.dropped_frames % 100 == 0:
                print(f"⚠️  Dropped {self.dropped_frames} frames due to errors")
    
    def stop_recording(self, game_stats: Optional[dict] = None) -> Optional[dict]:
        """
        Stop recording and save video file with optional game statistics.
        
        Args:
            game_stats: Optional dictionary with game performance data
        
        Returns:
            Dictionary with recording metadata, or None if failed
        """
        if not self.is_recording:
            print("⚠️  Not currently recording!")
            return None
        
        self.is_recording = False
        
        if len(self.frames) == 0:
            print("❌ No frames captured!")
            return None
        
        print(f"\n🎬 Stopping recording...")
        print(f"   Captured {self.frame_count} frames")
        print(f"   Duration: {len(self.frames)/self.fps:.2f} seconds")
        print(f"   Dropped frames: {self.dropped_frames}")
        
        # Store game stats for later use
        self._game_stats = game_stats
        
        # Save frames to temporary directory
        temp_dir = Path(tempfile.mkdtemp())
        
        try:
            print(f"💾 Saving frames to temporary directory...")
            for i, frame in enumerate(self.frames):
                frame_path = temp_dir / f"frame_{i:06d}.png"
                pygame.image.save(frame, str(frame_path))
                
                if (i + 1) % 100 == 0:
                    print(f"   Saved {i + 1}/{len(self.frames)} frames...")
            
            # Encode video
            metadata = self._encode_video(temp_dir)
            
            # Clean up temporary files
            self._cleanup_temp_files(temp_dir)
            
            # Clear frames from memory
            self.frames.clear()
            
            return metadata
        
        except Exception as e:
            print(f"❌ Error saving recording: {e}")
            self._cleanup_temp_files(temp_dir)
            return None
    
    def _encode_video(self, frames_dir: Path) -> dict:
        """
        Encode frames to video files using ffmpeg.
        
        Args:
            frames_dir: Directory containing frame images
            
        Returns:
            Metadata dictionary
        """
        print(f"\n🎞️  Encoding video...")
        
        # Output paths
        webm_path = self.output_dir / f"{self.recording_name}.webm"
        mp4_path = self.output_dir / f"{self.recording_name}.mp4"
        gif_path = self.output_dir / f"{self.recording_name}_preview.gif"
        metadata_path = self.output_dir / f"{self.recording_name}_metadata.json"
        
        # Get frame dimensions from first frame
        first_frame = pygame.image.load(str(frames_dir / "frame_000000.png"))
        width, height = first_frame.get_size()
        
        # 1. Create WebM (best for web, smaller file size)
        print(f"   Creating WebM (web-optimized)...")
        webm_cmd = [
            'ffmpeg',
            '-framerate', str(self.fps),
            '-i', str(frames_dir / 'frame_%06d.png'),
            '-c:v', 'libvpx-vp9',  # VP9 codec (better quality)
            '-crf', '30',  # Quality (0-63, lower = better)
            '-b:v', '0',  # Variable bitrate
            '-pix_fmt', 'yuv420p',
            '-y',  # Overwrite output
            str(webm_path)
        ]
        
        try:
            subprocess.run(webm_cmd, check=True, capture_output=True)
            print(f"   ✅ WebM created: {webm_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  WebM encoding failed: {e}")
        
        # 2. Create MP4 (better compatibility)
        print(f"   Creating MP4 (compatibility)...")
        mp4_cmd = [
            'ffmpeg',
            '-framerate', str(self.fps),
            '-i', str(frames_dir / 'frame_%06d.png'),
            '-c:v', 'libx264',  # H.264 codec
            '-preset', 'medium',
            '-crf', '23',  # Quality (0-51, lower = better)
            '-pix_fmt', 'yuv420p',
            '-y',
            str(mp4_path)
        ]
        
        try:
            subprocess.run(mp4_cmd, check=True, capture_output=True)
            print(f"   ✅ MP4 created: {mp4_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  MP4 encoding failed: {e}")
        
        # 3. Create GIF preview (first 5 seconds, lower quality)
        print(f"   Creating GIF preview...")
        max_frames = min(len(self.frames), self.fps * 5)  # Max 5 seconds
        gif_cmd = [
            'ffmpeg',
            '-framerate', str(self.fps),
            '-i', str(frames_dir / 'frame_%06d.png'),
            '-vf', f'fps={self.fps//2},scale=640:-1:flags=lanczos',  # Half FPS, 640px width
            '-frames:v', str(max_frames),
            '-y',
            str(gif_path)
        ]
        
        try:
            subprocess.run(gif_cmd, check=True, capture_output=True)
            print(f"   ✅ GIF preview created: {gif_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  GIF encoding failed: {e}")
        
        # Create metadata
        metadata = {
            'recording_name': self.recording_name,
            'timestamp': self.start_time.isoformat(),
            'duration_seconds': len(self.frames) / self.fps,
            'fps': self.fps,
            'frame_count': len(self.frames),
            'dropped_frames': self.dropped_frames,
            'resolution': {
                'width': width,
                'height': height
            },
            'files': {
                'webm': webm_path.name if webm_path.exists() else None,
                'mp4': mp4_path.name if mp4_path.exists() else None,
                'gif_preview': gif_path.name if gif_path.exists() else None
            },
            'file_sizes': {
                'webm_mb': webm_path.stat().st_size / (1024*1024) if webm_path.exists() else 0,
                'mp4_mb': mp4_path.stat().st_size / (1024*1024) if mp4_path.exists() else 0,
                'gif_mb': gif_path.stat().st_size / (1024*1024) if gif_path.exists() else 0
            }
        }
        
        # Add game statistics if provided
        if hasattr(self, '_game_stats') and self._game_stats:
            metadata['game_statistics'] = self._game_stats
        
        # Save metadata
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save game statistics as separate text file
        if hasattr(self, '_game_stats') and self._game_stats:
            self._save_game_stats_txt(metadata)
        
        print(f"\n✅ Recording saved successfully!")
        print(f"   📁 Location: {self.output_dir}")
        print(f"   🎬 WebM: {metadata['file_sizes']['webm_mb']:.2f} MB")
        print(f"   🎬 MP4: {metadata['file_sizes']['mp4_mb']:.2f} MB")
        print(f"   🖼️  GIF: {metadata['file_sizes']['gif_mb']:.2f} MB")
        print(f"   ⏱️  Duration: {metadata['duration_seconds']:.2f}s")
        if hasattr(self, '_game_stats') and self._game_stats:
            print(f"   📊 Game stats: {self.recording_name}_stats.txt")
        
        # Generate HTML embed code
        self._generate_html_embed(metadata)
        
        return metadata
    
    def _save_game_stats_txt(self, metadata: dict):
        """Save game statistics as a formatted text file."""
        stats_path = self.output_dir / f"{self.recording_name}_stats.txt"
        game_stats = metadata.get('game_statistics', {})
        
        with open(stats_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("PROUTMAN GAMEPLAY STATISTICS\n")
            f.write("=" * 80 + "\n\n")
            
            # Recording Information
            f.write("📹 RECORDING INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"Recording Name:  {self.recording_name}\n")
            f.write(f"Date/Time:       {metadata.get('timestamp', 'N/A')}\n")
            f.write(f"Duration:        {metadata.get('duration_seconds', 0):.2f} seconds\n")
            f.write(f"FPS:             {metadata.get('fps', 0)}\n")
            f.write(f"Frames Captured: {metadata.get('frame_count', 0)}\n")
            f.write(f"Resolution:      {metadata.get('resolution', {}).get('width', 0)}x{metadata.get('resolution', {}).get('height', 0)}\n")
            f.write("\n")
            
            # AI Information
            if 'ai_info' in game_stats:
                ai_info = game_stats['ai_info']
                f.write("🤖 AI OPPONENT INFORMATION\n")
                f.write("-" * 80 + "\n")
                f.write(f"AI Type:         {ai_info.get('type', 'Unknown')}\n")
                f.write(f"Model Path:      {ai_info.get('model_path', 'N/A')}\n")
                f.write(f"Skill Level:     {ai_info.get('skill_level', 'Unknown')}\n")
                f.write("\n")
            
            # Game Results
            if 'game_result' in game_stats:
                result = game_stats['game_result']
                f.write("🏆 GAME RESULT\n")
                f.write("-" * 80 + "\n")
                f.write(f"Winner:          {result.get('winner', 'Unknown')}\n")
                f.write(f"Game Duration:   {result.get('duration', 0):.2f} seconds\n")
                f.write(f"Total Turns:     {result.get('turns', 0)}\n")
                f.write("\n")
            
            # Performance Statistics
            if 'performance' in game_stats:
                perf = game_stats['performance']
                
                f.write("📊 PERFORMANCE STATISTICS\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total Games:     {perf.get('total_games', 0)}\n")
                f.write(f"Human Wins:      {perf.get('human_wins', 0)}\n")
                f.write(f"AI Wins:         {perf.get('ai_wins', 0)}\n")
                f.write(f"Draws:           {perf.get('draws', 0)}\n")
                f.write(f"Human Win Rate:  {perf.get('human_win_rate', 0):.1f}%\n")
                f.write(f"AI Win Rate:     {perf.get('ai_win_rate', 0):.1f}%\n")
                f.write("\n")
                
                # Win streaks
                f.write("🔥 WIN STREAKS\n")
                f.write("-" * 80 + "\n")
                f.write(f"Human Current:   {perf.get('human_current_streak', 0)}\n")
                f.write(f"Human Best:      {perf.get('human_best_streak', 0)}\n")
                f.write(f"AI Current:      {perf.get('ai_current_streak', 0)}\n")
                f.write(f"AI Best:         {perf.get('ai_best_streak', 0)}\n")
                f.write("\n")
            
            # Current Game Stats
            if 'current_game' in game_stats:
                current = game_stats['current_game']
                
                f.write("🎮 CURRENT GAME STATISTICS\n")
                f.write("-" * 80 + "\n")
                
                # Human stats
                if 'human' in current:
                    human = current['human']
                    f.write("\nPlayer (Human):\n")
                    f.write(f"  Moves:         {human.get('moves', 0)}\n")
                    f.write(f"  Bombs Placed:  {human.get('bombs', 0)}\n")
                    f.write(f"  Walls Broken:  {human.get('walls', 0)}\n")
                    f.write(f"  Powerups:      {human.get('powerups', 0)}\n")
                    f.write(f"  Near Deaths:   {human.get('near_death', 0)}\n")
                    f.write(f"  Strategy:      {human.get('strategy', 'Unknown')}\n")
                    f.write(f"  Avg Risk:      {human.get('avg_risk', 0):.1f}\n")
                    f.write(f"  Performance:   {human.get('performance', 0):.1f}/100\n")
                
                # AI stats
                if 'ai' in current:
                    ai = current['ai']
                    f.write("\nAI Opponent:\n")
                    f.write(f"  Moves:         {ai.get('moves', 0)}\n")
                    f.write(f"  Bombs Placed:  {ai.get('bombs', 0)}\n")
                    f.write(f"  Walls Broken:  {ai.get('walls', 0)}\n")
                    f.write(f"  Powerups:      {ai.get('powerups', 0)}\n")
                    f.write(f"  Near Deaths:   {ai.get('near_death', 0)}\n")
                    f.write(f"  Strategy:      {ai.get('strategy', 'Unknown')}\n")
                    f.write(f"  Avg Risk:      {ai.get('avg_risk', 0):.1f}\n")
                    f.write(f"  Performance:   {ai.get('performance', 0):.1f}/100\n")
                f.write("\n")
            
            # Recommendations
            if 'recommendations' in game_stats:
                f.write("💡 RECOMMENDATIONS\n")
                f.write("-" * 80 + "\n")
                for i, rec in enumerate(game_stats['recommendations'], 1):
                    f.write(f"{i}. {rec}\n")
                f.write("\n")
            
            # Footer
            f.write("=" * 80 + "\n")
            f.write("Generated by Proutman Video Recorder\n")
            f.write(f"Video files: {self.recording_name}.webm, .mp4, .gif\n")
            f.write("=" * 80 + "\n")
    
    def _generate_html_embed(self, metadata: dict):
        """Generate HTML code for embedding video on GitHub Pages."""
        html_path = self.output_dir / f"{self.recording_name}_embed.html"
        
        webm_file = metadata['files']['webm']
        mp4_file = metadata['files']['mp4']
        gif_file = metadata['files']['gif_preview']
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proutman Gameplay - {metadata['recording_name']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .video-container {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        video {{
            width: 100%;
            max-width: 100%;
            border-radius: 4px;
        }}
        .metadata {{
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .metadata h3 {{
            margin-top: 0;
        }}
        .metadata p {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="video-container">
        <h1>💨 Proutman Gameplay Recording</h1>
        
        <!-- Video Player -->
        <video controls preload="metadata" poster="{gif_file}">
            {f'<source src="{webm_file}" type="video/webm">' if webm_file else ''}
            {f'<source src="{mp4_file}" type="video/mp4">' if mp4_file else ''}
            Your browser does not support the video tag.
        </video>
        
        <!-- Metadata -->
        <div class="metadata">
            <h3>📊 Recording Information</h3>
            <p><strong>Date:</strong> {metadata['timestamp']}</p>
            <p><strong>Duration:</strong> {metadata['duration_seconds']:.2f} seconds</p>
            <p><strong>FPS:</strong> {metadata['fps']}</p>
            <p><strong>Resolution:</strong> {metadata['resolution']['width']}x{metadata['resolution']['height']}</p>
            <p><strong>Frames:</strong> {metadata['frame_count']}</p>
        </div>
        
        <!-- Download Links -->
        <div class="metadata">
            <h3>📥 Download</h3>
            {f'<p><a href="{webm_file}" download>Download WebM ({metadata["file_sizes"]["webm_mb"]:.2f} MB)</a></p>' if webm_file else ''}
            {f'<p><a href="{mp4_file}" download>Download MP4 ({metadata["file_sizes"]["mp4_mb"]:.2f} MB)</a></p>' if mp4_file else ''}
            {f'<p><a href="{gif_file}" download>Download GIF Preview ({metadata["file_sizes"]["gif_mb"]:.2f} MB)</a></p>' if gif_file else ''}
        </div>
    </div>
    
    <!-- Markdown Embed Code -->
    <div class="video-container" style="margin-top: 20px;">
        <h3>📝 Embed Code for GitHub README</h3>
        <pre style="background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto;">
&lt;video width="100%" controls&gt;
  &lt;source src="recordings/{webm_file}" type="video/webm"&gt;
  &lt;source src="recordings/{mp4_file}" type="video/mp4"&gt;
&lt;/video&gt;

Or use GIF:
![Proutman Gameplay](recordings/{gif_file})
        </pre>
    </div>
</body>
</html>
"""
        
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        print(f"   📄 HTML embed: {html_path.name}")
    
    def _cleanup_temp_files(self, temp_dir: Path):
        """Clean up temporary frame files."""
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"⚠️  Could not clean up temp files: {e}")
    
    def get_status_text(self) -> str:
        """Get current recording status for display."""
        if not self.is_recording:
            return ""
        
        duration = len(self.frames) / self.fps
        return f"🔴 REC {duration:.1f}s ({len(self.frames)} frames)"
    
    def toggle_recording(self, session_name: Optional[str] = None) -> bool:
        """
        Toggle recording on/off.
        
        Args:
            session_name: Optional custom name for the recording
            
        Returns:
            True if now recording, False if stopped
        """
        if self.is_recording:
            self.stop_recording()
            return False
        else:
            self.start_recording(session_name)
            return True
