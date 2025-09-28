from src.config.data_base import db

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    time_limit = db.Column(db.Integer, default=60)  
    points = db.Column(db.Integer, nullable=True)  

    theme = db.relationship('Theme', back_populates='questions')
    
    answers = db.relationship('Answer', back_populates='question', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "difficulty": self.difficulty,
            "theme_id": self.theme_id,
            "explanation": self.explanation,
            "time_limit": self.time_limit,
            "points": self.points,
            "answers": [answer.to_dict() for answer in self.answers] if self.answers else []
        }
