from src.config.data_base import db

class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)

    creator = db.relationship('Player', backref=db.backref('created_themes', lazy=True))
    questions = db.relationship('Question', back_populates='theme', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_by": self.created_by,
             "questions": [question.to_dict() for question in self.questions] if self.questions else [],
            "easy_points": self.easy_points,
            "medium_points": self.medium_points,
            "hard_points": self.hard_points,
            "creator": self.creator.username if self.creator else None
        }