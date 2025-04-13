import json
import os
from datetime import datetime

class PlayerStats:
    def __init__(self):
        self.stats_file = "player_stats.json"
        self.stats = self.load_stats()
        
    def load_stats(self):
        """Load player statistics from file, or create new if doesn't exist"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self.create_default_stats()
        else:
            return self.create_default_stats()
    
    def create_default_stats(self):
        """Create default statistics structure"""
        return {
            "player_name": "Player",
            "total_games": 0,
            "levels": {
                "1": {"name": "Iterative Deepening DFS (Professional)", "wins": 0, "losses": 0, "last_played": None},
                "2": {"name": "MonteCarlo (Challenging)", "wins": 0, "losses": 0, "last_played": None},
                "3": {"name": "Alpha-Beta Pruning (Hard)", "wins": 0, "losses": 0, "last_played": None},
                "4": {"name": "Minimax (Medium)", "wins": 0, "losses": 0, "last_played": None},
                "5": {"name": "ExpectiMax (Easy)", "wins": 0, "losses": 0, "last_played": None},
                "6": {"name": "Negamax (Beginner)", "wins": 0, "losses": 0, "last_played": None}
            },
            "recommended_level": "4"  # Start with medium difficulty
        }
    
    def update_stats(self, level, won):
        """Update statistics after a game"""
        level_str = str(level)
        self.stats["total_games"] += 1
        
        if level_str in self.stats["levels"]:
            if won:
                self.stats["levels"][level_str]["wins"] += 1
            else:
                self.stats["levels"][level_str]["losses"] += 1
            
            self.stats["levels"][level_str]["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            #update recommended level
            self.update_recommendation()
            
            # Save updated stats
            self.save_stats()
    
    def update_recommendation(self):
        """Determine the recommended level based on performance"""
        recommended = "4"  # Default: Medium
        
        # Calculate win rates for each level
        win_rates = {}
        for level, data in self.stats["levels"].items():
            total = data["wins"] + data["losses"]
            if total > 0:
                win_rate = data["wins"] / total
                win_rates[level] = win_rate
        
        if win_rates:
            # If winning too much at current level, suggest a harder one
            current_level = self.stats["recommended_level"]
            current_win_rate = win_rates.get(current_level, 0.5)
            
            if current_win_rate > 0.7 and int(current_level) > 1:
                # Player is winning a lot, suggest a harder level
                recommended = str(int(current_level) - 1)
            elif current_win_rate < 0.3 and int(current_level) < 6:
                # Player is losing a lot, suggest an easier level
                recommended = str(int(current_level) + 1)
            else:
                # Keep the current level
                recommended = current_level
        
        self.stats["recommended_level"] = recommended
    
    def save_stats(self):
        """Save statistics to file"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=4)
    
    #gets the statistics used for recommending level to player
    def get_stats_summary(self):
        """Get a formatted summary of player statistics"""
        summary += f"Total Games: {self.stats['total_games']}\n\n"
        
        summary += "Performance by Level:\n"
        for level, data in self.stats["levels"].items():
            total = data["wins"] + data["losses"]
            win_rate = (data["wins"] / total * 100) if total > 0 else 0
            summary += f"{level}. {data['name']}: {data['wins']}W/{data['losses']}L ({win_rate:.1f}%)\n"
        
        recommended = self.stats["recommended_level"]
        summary += f"\nRecommended Level: {recommended}. {self.stats['levels'][recommended]['name']}"
        return summary
    
    # gets the recommended level for the player based on preformance
    def get_recommended_level(self):
        """Get the recommended difficulty level"""
        return self.stats["recommended_level"]
    
    def set_player_name(self, name):
        """Set the player's name"""
        self.stats["player_name"] = name
        self.save_stats()