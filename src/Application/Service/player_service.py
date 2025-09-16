import random
from src.Infrastructure.Model.player_model import Player
from src.config.data_base import db

class PlayerService:
    @staticmethod
    def create_player(player):
        new_player = player.to_dict()
        try:

            if Player.query.filter_by(email=new_player.email).first():
                return None, "Email already registered"
            if Player.query.filter_by(username=new_player.username).first():
                return None, "Username already registered"
            
            player = Player(
                username=new_player.username,
                email=new_player.email,
                password=new_player.password
            )

            db.session.add(player)
            db.session.commit()
            
            return player, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_all_players():
        try:
            players = Player.query.all()        
            return [player.to_dict() for player in players]
        except Exception as e:
            return None
            
    @staticmethod
    def get_player_by_id(id):
        try:
            player = Player.query.filter_by(id=id).first()        
            return player.to_dict()
        except Exception as e:
            return None
        
    @staticmethod
    def update_player(player):
        new_player = player.to_dict()

        try:
            player = Player.query.filter_by(id=id).first()

            player_by_email = Player.query.filter_by(email=new_player.email).first()
            if player_by_email != None and player_by_email.id != player.id:
                return None, "Email already registered"
            
            player_by_username = Player.query.filter_by(username=new_player.username).first()
            if player_by_username != None and player_by_username.id != player.id:
                return None, "Username already registered"

            if not player:
                return None, "Player not found"
            
            player.username = new_player.username
            player.email = new_player.email
    
            db.session.commit()
            return player, None
        except Exception as e:
            return None, str(e)
         
    @staticmethod
    def delete_player(player_id):
        try:
            player = Player.query.filter_by(id=player_id).first()
            if not player:
                return None
            db.session.delete(player)
            db.session.commit()
            return True
        except Exception as e:
            return None
