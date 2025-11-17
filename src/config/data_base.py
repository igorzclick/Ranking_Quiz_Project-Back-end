from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
db = SQLAlchemy()

def init_db(app):
    DB_USER = os.getenv('MYSQL_USER', 'root')
    DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    DB_HOST = os.getenv('MYSQL_HOST', 'db')
    DB_NAME = os.getenv('MYSQL_DATABASE', 'RankingQuizDB')
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from src.Infrastructure.Model.player_model import Player
    from src.Infrastructure.Model.theme_model import Theme
    from src.Infrastructure.Model.question_model import Question
    from src.Infrastructure.Model.answer_model import Answer
    from src.Infrastructure.Model.room_model import Room
    from src.Infrastructure.Model.game_model import Game
    from src.Infrastructure.Model.game_answer_model import GameAnswer

    with app.app_context():
        db.create_all()
        