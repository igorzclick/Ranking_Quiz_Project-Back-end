from flask import jsonify, make_response
from src.Infrastructure.Model.player_model import Player
from src.config.data_base import db
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def login(data):
        username = data["username"]
        password = data["password"]

        if not username or not password:
            return None, "username and password are required", 400

        player = Player.query.filter_by(username=username).first()

        if not player or player.password != password:
            return None, "Invalid credentials", 401

        access_token = create_access_token(identity=player.id)
        
        return access_token, None, 200