class GameStats():
    
    def __init__(self, settuns):
        self.settuns = settuns
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
        
    def reset_stats(self):
        self.ships_left = self.settuns.ship_limit
        self.score = 0
        self.level = 1
