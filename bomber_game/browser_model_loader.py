"""
Browser-Adaptive Model Loader
Automatically adjusts model complexity based on browser capabilities.
"""

import os
import json
from datetime import datetime


class BrowserModelLoader:
    """
    Loads appropriate AI model based on browser capabilities.
    
    Adapts model selection for:
    - WebAssembly performance
    - Memory constraints
    - CPU limitations
    - Mobile vs Desktop
    """
    
    def __init__(self, models_dir):
        """
        Initialize browser-adaptive loader.
        
        Args:
            models_dir: Directory containing models
        """
        self.models_dir = models_dir
        self.config_file = os.path.join(models_dir, "browser_config.json")
        
        # Performance profiles
        self.profiles = {
            'high_performance': {
                'name': 'High Performance',
                'description': 'Desktop browsers with good CPU/memory',
                'model': 'enhanced_heuristic',
                'max_search_depth': 5,
                'beam_width': 20,
                'think_time': 0.1,
            },
            'medium_performance': {
                'name': 'Medium Performance',
                'description': 'Older desktops or tablets',
                'model': 'improved_heuristic',
                'max_search_depth': 3,
                'beam_width': 10,
                'think_time': 0.15,
            },
            'low_performance': {
                'name': 'Low Performance',
                'description': 'Mobile devices or slow connections',
                'model': 'simple_heuristic',
                'max_search_depth': 1,
                'beam_width': 5,
                'think_time': 0.2,
            },
            'auto': {
                'name': 'Auto-Detect',
                'description': 'Automatically detect browser capabilities',
                'model': 'auto',
                'max_search_depth': 'auto',
                'beam_width': 'auto',
                'think_time': 'auto',
            }
        }
    
    def detect_browser_capabilities(self):
        """
        Detect browser capabilities from environment.
        
        Returns:
            Dictionary with detected capabilities
        """
        capabilities = {
            'wasm_support': True,  # Assume WASM support
            'memory_mb': 512,      # Conservative estimate
            'cpu_cores': 2,        # Conservative estimate
            'is_mobile': False,    # Default to desktop
            'connection_speed': 'good',  # Assume good connection
        }
        
        # Try to detect from environment variables or user agent
        # (In web context, this would be done via JavaScript)
        
        return capabilities
    
    def select_profile(self, capabilities=None):
        """
        Select appropriate performance profile.
        
        Args:
            capabilities: Browser capabilities dict (or None for auto-detect)
            
        Returns:
            Profile dictionary
        """
        if capabilities is None:
            capabilities = self.detect_browser_capabilities()
        
        # Decision logic
        memory_mb = capabilities.get('memory_mb', 512)
        cpu_cores = capabilities.get('cpu_cores', 2)
        is_mobile = capabilities.get('is_mobile', False)
        
        # Mobile devices - use low performance
        if is_mobile:
            return self.profiles['low_performance']
        
        # Desktop with good specs - use high performance
        if memory_mb >= 1024 and cpu_cores >= 4:
            return self.profiles['high_performance']
        
        # Desktop with medium specs - use medium performance
        if memory_mb >= 512 and cpu_cores >= 2:
            return self.profiles['medium_performance']
        
        # Everything else - use low performance
        return self.profiles['low_performance']
    
    def get_model_config(self, profile_name='auto'):
        """
        Get model configuration for specified profile.
        
        Args:
            profile_name: Name of profile ('auto', 'high_performance', etc.)
            
        Returns:
            Configuration dictionary
        """
        if profile_name == 'auto':
            profile = self.select_profile()
        else:
            profile = self.profiles.get(profile_name, self.profiles['medium_performance'])
        
        config = {
            'profile': profile['name'],
            'model_type': profile['model'],
            'search_depth': profile['max_search_depth'],
            'beam_width': profile['beam_width'],
            'think_time': profile['think_time'],
            'timestamp': datetime.now().isoformat(),
        }
        
        # Save configuration
        self._save_config(config)
        
        return config
    
    def _save_config(self, config):
        """Save browser configuration."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save browser config: {e}")
    
    def load_config(self):
        """Load saved browser configuration."""
        if not os.path.exists(self.config_file):
            return None
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load browser config: {e}")
            return None
    
    def get_recommended_settings(self):
        """
        Get recommended settings for current browser.
        
        Returns:
            Dictionary with recommendations
        """
        capabilities = self.detect_browser_capabilities()
        profile = self.select_profile(capabilities)
        
        return {
            'capabilities': capabilities,
            'profile': profile,
            'recommendations': {
                'model': profile['model'],
                'search_depth': profile['max_search_depth'],
                'beam_width': profile['beam_width'],
                'think_time': profile['think_time'],
            }
        }
    
    def generate_report(self):
        """Generate browser compatibility report."""
        capabilities = self.detect_browser_capabilities()
        profile = self.select_profile(capabilities)
        
        report = []
        report.append("\n" + "=" * 70)
        report.append("🌐 BROWSER MODEL LOADER")
        report.append("=" * 70)
        
        report.append(f"\n📊 Detected Capabilities:")
        report.append(f"   Memory: {capabilities['memory_mb']} MB")
        report.append(f"   CPU Cores: {capabilities['cpu_cores']}")
        report.append(f"   Device: {'Mobile' if capabilities['is_mobile'] else 'Desktop'}")
        report.append(f"   Connection: {capabilities['connection_speed']}")
        
        report.append(f"\n🎯 Selected Profile: {profile['name']}")
        report.append(f"   Description: {profile['description']}")
        report.append(f"   Model: {profile['model']}")
        report.append(f"   Search Depth: {profile['max_search_depth']}")
        report.append(f"   Beam Width: {profile['beam_width']}")
        report.append(f"   Think Time: {profile['think_time']}s")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)


# JavaScript integration code for web deployment
BROWSER_DETECTION_JS = """
// Browser capability detection for Python integration
function detectBrowserCapabilities() {
    const capabilities = {
        wasm_support: typeof WebAssembly !== 'undefined',
        memory_mb: navigator.deviceMemory ? navigator.deviceMemory * 1024 : 512,
        cpu_cores: navigator.hardwareConcurrency || 2,
        is_mobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
        connection_speed: navigator.connection ? navigator.connection.effectiveType : 'good',
        screen_width: window.screen.width,
        screen_height: window.screen.height,
    };
    
    // Send to Python via custom event or API
    window.browserCapabilities = capabilities;
    
    return capabilities;
}

// Auto-detect on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', detectBrowserCapabilities);
} else {
    detectBrowserCapabilities();
}

// Expose globally
window.detectBrowserCapabilities = detectBrowserCapabilities;
"""


def save_browser_detection_script(output_dir='docs/play'):
    """Save browser detection JavaScript."""
    script_path = os.path.join(output_dir, 'browser_detect.js')
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(script_path, 'w') as f:
            f.write(BROWSER_DETECTION_JS)
        print(f"✅ Saved browser detection script to: {script_path}")
        return script_path
    except Exception as e:
        print(f"⚠️  Could not save browser detection script: {e}")
        return None


if __name__ == '__main__':
    # Test browser model loader
    loader = BrowserModelLoader('bomber_game/models')
    print(loader.generate_report())
    
    # Save JavaScript detection script
    save_browser_detection_script()
