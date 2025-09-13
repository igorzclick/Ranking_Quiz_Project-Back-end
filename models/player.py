from models.db import db
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    
    def __repr__(self):
        return f"<Player {self.name} - Score: {self.score}>"