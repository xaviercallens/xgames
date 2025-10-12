"""
AI Level Manager - Manages multiple AI difficulty levels.
"""

import json
import shutil
from pathlib import Path
import torch


class AILevelManager:
    """
    Manages AI models at different difficulty levels.
    Automatically promotes models when they reach performance thresholds.
    """
    
    def __init__(self, models_dir="bomber_game/models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Define difficulty levels and their thresholds
        self.levels = {
            'beginner': {
                'name': 'Beginner Bot',
                'win_rate_min': 0,
                'win_rate_max': 20,
                'model_file': 'ppo_beginner.pth',
                'description': 'Easy opponent for learning',
                'icon': '🌱',
            },
            'intermediate': {
                'name': 'Intermediate Bot',
                'win_rate_min': 20,
                'win_rate_max': 40,
                'model_file': 'ppo_intermediate.pth',
                'description': 'Balanced challenge',
                'icon': '🎯',
            },
            'advanced': {
                'name': 'Advanced Bot',
                'win_rate_min': 40,
                'win_rate_max': 60,
                'model_file': 'ppo_advanced.pth',
                'description': 'Tough opponent',
                'icon': '🤖',
            },
            'expert': {
                'name': 'Expert Bot',
                'win_rate_min': 60,
                'win_rate_max': 80,
                'model_file': 'ppo_expert.pth',
                'description': 'Very challenging',
                'icon': '👑',
            },
            'master': {
                'name': 'Master Bot',
                'win_rate_min': 80,
                'win_rate_max': 100,
                'model_file': 'ppo_master.pth',
                'description': 'Nearly unbeatable',
                'icon': '🏆',
            },
        }
    
    def get_level_for_win_rate(self, win_rate):
        """Get appropriate level based on win rate."""
        for level, info in self.levels.items():
            if info['win_rate_min'] <= win_rate < info['win_rate_max']:
                return level
        return 'master'  # If above all thresholds
    
    def save_model_at_level(self, model_state, win_rate, episodes, metadata=None):
        """Save model at appropriate difficulty level."""
        level = self.get_level_for_win_rate(win_rate)
        level_info = self.levels[level]
        
        model_path = self.models_dir / level_info['model_file']
        
        # Save model
        save_data = {
            'model_state_dict': model_state,
            'level': level,
            'win_rate': win_rate,
            'episodes': episodes,
            'metadata': metadata or {},
        }
        
        torch.save(save_data, model_path)
        
        print(f"💾 Saved {level_info['icon']} {level_info['name']} (WR: {win_rate:.1f}%)")
        
        return level
    
    def load_model_at_level(self, level):
        """Load model at specific difficulty level."""
        if level not in self.levels:
            return None
        
        model_path = self.models_dir / self.levels[level]['model_file']
        
        if not model_path.exists():
            return None
        
        try:
            checkpoint = torch.load(model_path)
            return checkpoint
        except:
            return None
    
    def get_available_levels(self):
        """Get list of available difficulty levels."""
        available = []
        
        for level, info in self.levels.items():
            model_path = self.models_dir / info['model_file']
            
            if model_path.exists():
                try:
                    checkpoint = torch.load(model_path)
                    available.append({
                        'level': level,
                        'name': info['name'],
                        'icon': info['icon'],
                        'description': info['description'],
                        'win_rate': checkpoint.get('win_rate', 0),
                        'episodes': checkpoint.get('episodes', 0),
                        'model_path': str(model_path),
                    })
                except:
                    pass
        
        return available
    
    def promote_model(self, current_level, new_win_rate):
        """Promote model to higher level if it qualifies."""
        new_level = self.get_level_for_win_rate(new_win_rate)
        
        if new_level == current_level:
            return False
        
        # Check if it's a promotion (not demotion)
        level_order = list(self.levels.keys())
        if level_order.index(new_level) <= level_order.index(current_level):
            return False
        
        # Copy current model to new level
        current_path = self.models_dir / self.levels[current_level]['model_file']
        new_path = self.models_dir / self.levels[new_level]['model_file']
        
        if current_path.exists():
            shutil.copy(current_path, new_path)
            print(f"🎉 Model promoted from {current_level} to {new_level}!")
            return True
        
        return False
    
    def create_level_progression_report(self):
        """Create a report of AI progression across levels."""
        report = {
            'levels': {},
            'progression': [],
        }
        
        for level, info in self.levels.items():
            model_path = self.models_dir / info['model_file']
            
            if model_path.exists():
                try:
                    checkpoint = torch.load(model_path)
                    report['levels'][level] = {
                        'name': info['name'],
                        'win_rate': checkpoint.get('win_rate', 0),
                        'episodes': checkpoint.get('episodes', 0),
                        'exists': True,
                    }
                except:
                    report['levels'][level] = {
                        'name': info['name'],
                        'exists': False,
                    }
            else:
                report['levels'][level] = {
                    'name': info['name'],
                    'exists': False,
                }
        
        return report
    
    def initialize_beginner_model(self):
        """Initialize beginner model from pretrained or heuristic."""
        beginner_path = self.models_dir / self.levels['beginner']['model_file']
        
        if beginner_path.exists():
            print("✅ Beginner model already exists")
            return True
        
        # Try to copy from pretrained
        pretrained_path = self.models_dir / "ppo_agent_pretrained.pth"
        if pretrained_path.exists():
            shutil.copy(pretrained_path, beginner_path)
            print("✅ Initialized beginner model from pretrained")
            return True
        
        print("⚠️ No pretrained model found. Run bootstrap_ppo_training.py first.")
        return False
    
    def export_level_info(self, output_file="bomber_game/models/ai_levels.json"):
        """Export information about all AI levels."""
        info = {
            'levels': {},
            'available': [],
        }
        
        for level, level_info in self.levels.items():
            model_path = self.models_dir / level_info['model_file']
            
            info['levels'][level] = {
                'name': level_info['name'],
                'description': level_info['description'],
                'icon': level_info['icon'],
                'win_rate_range': [level_info['win_rate_min'], level_info['win_rate_max']],
                'exists': model_path.exists(),
            }
            
            if model_path.exists():
                try:
                    checkpoint = torch.load(model_path)
                    info['levels'][level]['current_win_rate'] = checkpoint.get('win_rate', 0)
                    info['levels'][level]['episodes'] = checkpoint.get('episodes', 0)
                    info['available'].append(level)
                except:
                    pass
        
        with open(output_file, 'w') as f:
            json.dump(info, f, indent=2)
        
        print(f"📝 Exported AI level info to {output_file}")


def main():
    """Test AI level manager."""
    manager = AILevelManager()
    
    print("🎮 AI Level Manager")
    print("=" * 50)
    
    # Get available levels
    available = manager.get_available_levels()
    
    if available:
        print(f"\n✅ Found {len(available)} AI levels:")
        for level_info in available:
            print(f"  {level_info['icon']} {level_info['name']}")
            print(f"     Win Rate: {level_info['win_rate']:.1f}%")
            print(f"     Episodes: {level_info['episodes']}")
    else:
        print("\n⚠️ No AI levels found")
        print("   Run: python bootstrap_ppo_training.py")
    
    # Export info
    manager.export_level_info()
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
