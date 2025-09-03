from models.db import db

class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    secret_word = db.Column(db.String(100), nullable=False)

    questions = db.relationship("Question", backref="game", lazy=True)
    guesses = db.relationship("Guess", backref="game", lazy=True)
    players = db.relationship("User", backref="game", lazy=True)

    def __init__(self, secret_word):
        self.secret_word = secret_word