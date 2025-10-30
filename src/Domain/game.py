class GameDomain:
    def __init__(self, theme_id, game_title, player_id,points,status):
        self.theme_id = theme_id
        self.game_title = game_title
        self.player_id = player_id
        self.status = status
        self.points = points

    def to_dict(self):
        return {
            "theme_id": self.theme_id,
            "game_title": self.game_title,
            "player_id": self.player_id,
            "status": self.status,
            "points": self.points
        }