from src.config.data_base import db

class GameAnswer(db.Model):
    __tablename__ = 'game_answers'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    points_awarded = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint('game_id', 'question_id', name='uq_game_question'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "question_id": self.question_id,
            "answer_id": self.answer_id,
            "is_correct": self.is_correct,
            "points_awarded": self.points_awarded,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }