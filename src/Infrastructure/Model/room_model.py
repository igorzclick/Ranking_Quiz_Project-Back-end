from src.config.data_base import db
from sqlalchemy.sql import func


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    theme = db.relationship('Theme', backref=db.backref('rooms', lazy=True))
    creator = db.relationship('Player', backref=db.backref('created_rooms', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "theme_id": self.theme_id,
            "theme_name": self.theme.name if self.theme else None,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


