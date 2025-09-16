from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from src.Infrastructure.Model.player_model import Player
from src.config.data_base import db
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return make_response(jsonify({"message": "username and password are required"}), 400)

        player = Player.query.filter_by(username=username).first()

        if not player or player.password != password:
            return make_response(jsonify({"message": "Invalid credentials"}), 401)

        access_token = create_access_token(identity=player.id)
        refresh_token = create_refresh_token(identity=player.id)

        return make_response(jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token 
        }), 200)