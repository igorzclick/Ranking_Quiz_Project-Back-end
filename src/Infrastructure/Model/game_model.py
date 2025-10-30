from src.config.data_base import db

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    game_title = db.Column(db.String(100), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='inactive')#types: inactive, active, completed
    points = db.Column(db.Integer, nullable=True)
    def to_dict(self):

        return {
            "id": self.id,
            "game_name": self.game_name,
            "theme_id": self.theme_id,
            "player_id": self.player_id,
            "status": self.status,
            "points": self.points
        }