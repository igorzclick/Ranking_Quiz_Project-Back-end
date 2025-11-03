class GameDomain:
    def __init__(self, theme_id, game_name, player_id,points,status):
        self.theme_id = theme_id
        self.game_name = game_name
        self.player_id = player_id
        self.status = status
        self.points = points

    def to_dict(self):
        return {
            "theme_id": self.theme_id,
            "game_name": self.game_name,
            "player_id": self.player_id,
            "status": self.status,
            "points": self.points
        }