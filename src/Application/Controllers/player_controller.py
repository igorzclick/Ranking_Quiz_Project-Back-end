from flask import jsonify, make_response
from src.Application.Service.player_service import PlayerService
from src.Domain.player import PlayerDomain

class PlayerController:
    @staticmethod
    def register_player(body):
        playerDomain = PlayerDomain(
            username=body['name'],
            email=body['email'],
            password=body['password']
        )
        player, error_message = PlayerService.create_player(playerDomain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        return make_response(jsonify({
            "message": "Player registered successfully",
            "player": player.to_dict()
        }), 201)

    @staticmethod
    def get_all_players():
        players = PlayerService.get_all_players()
        if players is None:
            return make_response(jsonify({"message": "Could not retrieve players"}), 500)
        return make_response(jsonify({
            "players": players
        }), 200)

    @staticmethod
    def get_player_by_id(player_id):
        player = PlayerService.get_player_by_id(player_id)
        if not player:
             return make_response(jsonify({"message": "Player not found"}), 404)
        return make_response(jsonify({
            "player": player
        }), 200)

    @staticmethod
    def update_player(body, player_id):
        playerDomain = PlayerDomain(
            username=body['name'],
            email=body['email'],
            password=body['password']
        )
        player, error_message = PlayerService.update_player(playerDomain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not player:
            return make_response(jsonify({"message": "Player not found or update failed"}), 404)

        return make_response(jsonify({
            "message": "Player updated successfully",
            "player": player.to_dict()
        }), 200)

    @staticmethod
    def delete_player(player_id):
        player = PlayerService.delete_player(player_id)
        if not player:
            return make_response(jsonify({"message": "Player not found"}), 404)

        return make_response(jsonify({
            "message": "Player deleted successfully",
        }), 200)
