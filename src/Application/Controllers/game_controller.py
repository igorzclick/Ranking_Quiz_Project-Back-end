from flask import jsonify,make_response
from src.Application.Service.game_service import GameService
from src.Domain.game import GameDomain
from flask_jwt_extended import get_jwt_identity


class GameController:
    @staticmethod
    def create_game(body):
        gameDomain = GameDomain(
            theme_id=body['theme_id'],
            game_name=body['game_name'],
            player_id=body['player_id'],
            points=body['points'],
            status='inactive'
        )
        game, error_message = GameService.create_game(gameDomain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        return make_response(jsonify({
            "game": game.to_dict()
        }), 201)


    @staticmethod
    def get_all_games():
        games = GameService.get_all_games()
        if games is None:
            return make_response(jsonify({"message": "Could not retrieve games"}), 500)
        return make_response(jsonify({
            "games": games
        }), 200)

    @staticmethod
    def get_game_by_id(game_id):
        code, result = GameService.get_game_by_id(game_id)
        if code != 200:
             return make_response(jsonify(result), code)
        return make_response(jsonify(result), 200)

    @staticmethod
    def update_game(body):
        gameDomain = GameDomain(
            id=body['id'],
            theme_id=body['theme_id'],
            game_title=body['game_title'],
            player_id=body['player_id'],
            status=body['status'],
            points=body['points']
        )
        game, error_message = GameService.update_game(gameDomain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not game:
            return make_response(jsonify({"message": "Game not found or update failed"}), 404)

        return make_response(jsonify({
            "message": "Game updated successfully",
            "game": game.to_dict()
        }), 200)
    @staticmethod
    def delete_game(game_id):
        deleted_game = GameService.delete_game(game_id)

        if deleted_game:
            return make_response(jsonify({"message": deleted_game}), 400)

        return make_response(jsonify({
            "message": "Game deleted successfully"
        }), 200)     


    @staticmethod
    def   get_games_by_player(player_id):
        games, error_message = GameService.get_games_by_player(player_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        return make_response(jsonify({
            "games": games
        }), 200)

    @staticmethod
    def   get_games_by_status(status):
        games, error_message = GameService.get_games_by_status(status)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        return make_response(jsonify({
            "games": games
        }), 200)

    @staticmethod
    def  get_games_by_theme(theme_id):
        games, error_message = GameService.get_games_by_theme(theme_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        return make_response(jsonify({
            "games": games
        }), 200)
    @staticmethod
    def show_points(game_id):
        points, error_message = GameService.show_points(game_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        return make_response(jsonify({
            "points": points
        }), 200)
    
    @staticmethod
    def start_game_and_get_question(game_id, player_id):
        player_id = int(player_id)
        
        game, error_message = GameService.start_game(game_id, player_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not game:
            return make_response(jsonify({"message": "Game not found"}), 404)
        
        result, error_message = GameService.get_current_question(game_id, player_id, question_index=0)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not result:
            return make_response(jsonify({"message": "Could not retrieve question"}), 500)
        
        return make_response(jsonify(result), 200)
    
    @staticmethod
    def get_current_question(game_id, question_index, player_id):
        player_id = int(player_id)
        
        result, error_message = GameService.get_current_question(game_id, player_id, question_index)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not result:
            return make_response(jsonify({"message": "Could not retrieve question"}), 500)
        
        return make_response(jsonify(result), 200)
    
    @staticmethod
    def submit_answer(game_id, body, player_id):
        player_id = int(player_id)
        
        question_id = body.get('question_id')
        answer_id = body.get('answer_id')
        
        if not question_id or not answer_id:
            return make_response(jsonify({
                "message": "question_id and answer_id are required"
            }), 400)
        
        result, error_message = GameService.submit_answer(game_id, question_id, answer_id, player_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not result:
            return make_response(jsonify({"message": "Could not submit answer"}), 500)
        
        return make_response(jsonify(result), 200)
    
    @staticmethod
    def finish_game(game_id, player_id):
        player_id = int(player_id)
        
        result, error_message = GameService.finish_game(game_id, player_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not result:
            return make_response(jsonify({"message": "Could not finish game"}), 500)
        
        return make_response(jsonify({
            "message": "Game finished successfully",
            "game": result
        }), 200)

