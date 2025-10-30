from src.config.data_base import db
from src.Infrastructure.Model.game_model import Game
from src.Infrastructure.Model.theme_model import Theme
from src.Application.Controllers.theme_integrated_controller import ThemeIntegratedController

class GameService:
    @staticmethod
    def create_game(game):
        new_game = game.to_dict()
        try:
            game = Game(
                **new_game #O operador ** em Python desempacota 
                            #um dicionário e passa suas chaves/valores 
                            #como argumentos nomeados para uma função,
                            # método ou construtor.
            )

            db.session.add(game)
            db.session.commit()
            
            return game, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_game_by_id(id):
        try:
            game = Game.query.filter_by(id=id).first()
            game_dict = game.to_dict()
            questions = ThemeIntegratedController.get_theme_integrated(game_dict['theme_id'])
            return game_dict, questions if game else (None, None)
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_all_games():
        try:
            games = Game.query.all()        
            return [game.to_dict() for game in games]
        except Exception as e:
            return None, str(e)  

    @staticmethod
    def update_game(game):
        new_game = game.to_dict()
        
        try:
            game = Game.query.filter_by(id=new_game['id']).first()

            if not game:
                return None, "Game not found"

            for key, value in new_game.items():
                setattr(game, key, value)# e usa setattr para atualizar dinamicamente os atributos do objeto game.
                                        # Exemplo: setattr(game, "status", "playing") é o mesmo que game.status = "playing"

            db.session.commit()
            return game, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    @staticmethod
    def delete_game(id): 
        try:
            game = Game.query.filter_by(id=id).first()

            if not game:
                return "Game not found"

            db.session.delete(game)
            db.session.commit()
            return None
        except Exception as e:
            db.session.rollback()
            return str(e)

    @staticmethod
    def get_games_by_player(player_id):
        try:
            games = Game.query.filter_by(player_id=player_id).all()        
            return [game.to_dict() for game in games]
        except Exception as e:
            return None, str(e)   
    @staticmethod
    def get_games_by_status(status):
        try:
            games = Game.query.filter_by(status=status).all()        
            return [game.to_dict() for game in games]
        except Exception as e:
            return None, str(e)
    @staticmethod
    def get_games_by_theme(theme_id):
        try:
            games = Game.query.filter_by(theme_id=theme_id).all()        
            return [game.to_dict() for game in games]
        except Exception as e:
            return None, str(e)  

    @staticmethod
    def show_points(game_id,):
        try:
            game = Game.query.filter_by(id=game_id).first()        
            if game:
                return game.points
            return None
        except Exception as e:
            return None, str(e)
            
    @staticmethod
    def update_points(game_id, points):
        try:
            game = Game.query.filter_by(id=game_id).first()        
            if not game:
                return None, "Game not found"

            game.points = points
            db.session.commit()
            return game, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_status(game_id, status):
        try:
            game = Game.query.filter_by(id=game_id).first()        
            if not game:
                return None, "Game not found"

            game.status = status
            db.session.commit()
            return game, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    @staticmethod
    def start_game(game_id):
        try:
            game = Game.query.filter_by(id=game_id).first()        
            if not game:
                return None, "Game not found"

            game.status = 'active'
            db.session.commit()
            return game, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)        
