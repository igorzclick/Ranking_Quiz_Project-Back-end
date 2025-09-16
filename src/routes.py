from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Controllers.auth_controller import AuthController
from src.Application.Controllers.player_controller import PlayerController
from flask import jsonify, make_response, request
from src.Application.Dto.player_dto import PlayerRegisterSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from src.Infrastructure.Model.player_model import Player
from src.config.data_base import db



def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        return AuthController.login()
    
    @app.route('/player/register', methods=['POST'])
    def register_player():
        data = request.get_json()
        errors = PlayerRegisterSchema().validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return PlayerController.register_player(data)

    @app.route("/player", methods=['GET'])
    @jwt_required()
    def get_all_players():
        user_id = get_jwt_identity()
        print(f"Player autenticado ID: {user_id}")
        return PlayerController.get_all_players()
 
    @app.route("/player/<int:player_id>", methods=['GET'])
    @jwt_required()
    def get_player_by_id(player_id):
        return PlayerController.get_player_by_id(player_id)
    
    @app.route("/player/<int:player_id>", methods=['PUT'])
    @jwt_required()
    def update_player(player_id):
        data = request.get_json()
        return PlayerController.update_player(data, player_id)
    
    @app.route("/player/<int:player_id>", methods=['DELETE'])
    @jwt_required()
    def delete_player(player_id):
        return PlayerController.delete_player(player_id)
    
    @app.route("/auth/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        return jsonify(access_token=create_access_token(identity=get_jwt_identity()))
    