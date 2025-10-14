"""
Proutman Flask Web Application
Serves the web demo on PythonAnywhere and other hosting platforms
"""

from flask import Flask, render_template, send_from_directory, jsonify
import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DEMO_DIR = os.path.join(BASE_DIR, 'web_demo')

@app.route('/')
def index():
    """Main landing page."""
    try:
        return send_from_directory(WEB_DEMO_DIR, 'index.html')
    except:
        return """
        <html>
        <head><title>Proutman - Educational Bomberman Game</title></head>
        <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
            <h1>💨 Proutman - Educational Bomberman Game 💩</h1>
            <p>Welcome to Proutman! An educational game for learning Python, AI, and Reinforcement Learning.</p>
            <h2>Available Pages:</h2>
            <ul>
                <li><a href="/demo.html">Game Demo</a></li>
                <li><a href="/play.html">Play Now</a></li>
                <li><a href="/api/status">API Status</a></li>
            </ul>
            <h2>Features:</h2>
            <ul>
                <li>🎮 Classic Bomberman gameplay with a funny twist</li>
                <li>🤖 AI opponents using Reinforcement Learning</li>
                <li>🎓 Educational content for learning Python</li>
                <li>🎬 Video recording feature</li>
                <li>📊 Performance tracking and statistics</li>
            </ul>
            <p><a href="https://github.com/xaviercallens/xgames">View on GitHub</a></p>
        </body>
        </html>
        """

@app.route('/demo.html')
def demo():
    """Demo page."""
    return send_from_directory(WEB_DEMO_DIR, 'demo.html')

@app.route('/play.html')
def play():
    """Play page."""
    return send_from_directory(WEB_DEMO_DIR, 'play.html')

@app.route('/api/status')
def api_status():
    """API status endpoint."""
    return jsonify({
        'status': 'online',
        'game': 'Proutman',
        'version': '2.0',
        'features': [
            'Web Demo',
            'AI Opponents',
            'Video Recording',
            'Statistics Tracking'
        ],
        'deployment': 'PythonAnywhere',
        'repository': 'https://github.com/xaviercallens/xgames'
    })

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from web_demo directory."""
    try:
        return send_from_directory(WEB_DEMO_DIR, filename)
    except:
        return f"File not found: {filename}", 404

@app.route('/bomber_game/<path:filename>')
def serve_game_files(filename):
    """Serve game files."""
    game_dir = os.path.join(WEB_DEMO_DIR, 'bomber_game')
    try:
        return send_from_directory(game_dir, filename)
    except:
        return f"Game file not found: {filename}", 404

@app.route('/recordings/<path:filename>')
def serve_recordings(filename):
    """Serve recording files."""
    recordings_dir = os.path.join(BASE_DIR, 'recordings')
    try:
        return send_from_directory(recordings_dir, filename)
    except:
        return f"Recording not found: {filename}", 404

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return """
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <p><a href="/">Go to Home Page</a></p>
    </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(e):
    """Custom 500 page."""
    return """
    <html>
    <head><title>500 - Internal Server Error</title></head>
    <body style="font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1>500 - Internal Server Error</h1>
        <p>Something went wrong on our end.</p>
        <p><a href="/">Go to Home Page</a></p>
    </body>
    </html>
    """, 500

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
