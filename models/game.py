from models.db import db
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secret_word = db.Column(db.String(80), nullable=False)

    def __init__(self, secret_word):
        self.secret_word = secret_word

    def to_dict(self):
        return {
            "id": self.id,
            "secret_word": self.secret_word
        }
