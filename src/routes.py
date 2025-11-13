from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Controllers.auth_controller import AuthController
from src.Application.Controllers.player_controller import PlayerController
from src.Application.Controllers.theme_controller import ThemeController
from src.Application.Controllers.question_controller import QuestionController
from src.Application.Controllers.answer_controller import AnswerController
from src.Application.Controllers.theme_integrated_controller import ThemeIntegratedController
from src.Application.Controllers.room_controller import RoomController
from flask import jsonify, make_response, request
from src.Application.Dto.player_dto import player_schema
from src.Application.Dto.auth_dto import auth_schema
from src.Application.Dto.theme_dto import theme_schema, theme_update_schema
from src.Application.Dto.question_dto import question_schema, question_update_schema
from src.Application.Dto.answer_dto import answer_schema, answer_update_schema
from src.Application.Dto.theme_integrated_dto import theme_integrated_schema
from src.Application.Dto.room_dto import room_register_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from src.Infrastructure.Model.player_model import Player
from src.Application.Controllers.game_controller import GameController
from src.config.data_base import db

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
        
    @app.route('/theme/integrated', methods=['POST'])
    @jwt_required()
    def create_theme_integrated():
        data = request.get_json()
        errors = theme_integrated_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return ThemeIntegratedController.create_theme_integrated(data)
        
    @app.route('/theme/integrated/<int:theme_id>', methods=['PUT'])
    @jwt_required()
    def update_theme_integrated(theme_id):
        data = request.get_json()
        errors = theme_integrated_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return ThemeIntegratedController.update_theme_integrated(theme_id, data)
        
    @app.route('/theme/integrated/<int:theme_id>', methods=['GET'])
    @jwt_required()
    def get_theme_integrated(theme_id):
        return ThemeIntegratedController.get_theme_integrated(theme_id)
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        errors = auth_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return AuthController.login(data)
    
    @app.route('/player/register', methods=['POST'])
    def register_player():
        data = request.get_json()
        errors = player_schema.validate(data)
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
    
    @app.route('/theme/register', methods=['POST'])
    @jwt_required()
    def register_theme_with_questions():
        data = request.get_json()

        try:
            with db.session.begin():
                theme = ThemeController.register_theme(data)

                for question_data in data.get("questions", []):
                    question_data["theme_id"] = theme.id
                    question = QuestionController.register_question(question_data)

                    for answer_data in question_data.get("answers", []):
                        answer_data["question_id"] = question.id
                        AnswerController.register_answer(answer_data)

            return make_response(jsonify({
                "message": "Theme registered successfully",
                "theme_id": theme.id
            }), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": str(e)}), 400)
    

    @app.route("/themes", methods=['GET'])
    @jwt_required()
    def get_all_themes():
        return ThemeController.get_all_themes()
    
    @app.route("/theme/<int:theme_id>", methods=['GET'])
    @jwt_required()
    def get_theme_by_id(theme_id):
        return ThemeController.get_theme_by_id(theme_id)
    
    @app.route("/theme/name/<string:theme_name>", methods=['GET'])
    @jwt_required()
    def get_theme_by_name(theme_name):
        return ThemeController.get_theme_by_name(theme_name)
    
    @app.route("/theme/<int:theme_id>", methods=['PUT'])
    @jwt_required()
    def update_theme(theme_id):
        data = request.get_json()
        data['id'] = theme_id
        errors = theme_update_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return ThemeController.update_theme(data)
    
    @app.route("/theme/<int:theme_id>", methods=['DELETE'])
    @jwt_required()
    def delete_theme(theme_id):
        return ThemeController.delete_theme(theme_id)
    
    @app.route("/questions", methods=['GET'])
    @jwt_required()
    def get_all_questions():
        return QuestionController.get_all_questions()
    
    @app.route("/question/<int:question_id>", methods=['GET'])
    @jwt_required()
    def get_question_by_id(question_id):
        return QuestionController.get_question_by_id(question_id)
    
    @app.route("/questions/theme/<int:theme_id>", methods=['GET'])
    @jwt_required()
    def get_questions_by_theme(theme_id):
        return QuestionController.get_questions_by_theme(theme_id)
    
    @app.route("/questions/difficulty/<string:difficulty>", methods=['GET'])
    @jwt_required()
    def get_questions_by_difficulty(difficulty):
        return QuestionController.get_questions_by_difficulty(difficulty)
    
    @app.route("/question/<int:question_id>", methods=['PUT'])
    @jwt_required()
    def update_question(question_id):
        data = request.get_json()
        data['id'] = question_id
        errors = question_update_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return QuestionController.update_question(data)
    
    @app.route("/question/<int:question_id>", methods=['DELETE'])
    @jwt_required()
    def delete_question(question_id):
        return QuestionController.delete_question(question_id)
    
    @app.route("/answers", methods=['GET'])
    @jwt_required()
    def get_all_answers():
        return AnswerController.get_all_answers()
    
    @app.route("/answer/<int:answer_id>", methods=['GET'])
    @jwt_required()
    def get_answer_by_id(answer_id):
        return AnswerController.get_answer_by_id(answer_id)
    
    @app.route("/answers/question/<int:question_id>", methods=['GET'])
    @jwt_required()
    def get_answers_by_question(question_id):
        return AnswerController.get_answers_by_question(question_id)
    
    @app.route("/answer/correct/question/<int:question_id>", methods=['GET'])
    @jwt_required()
    def get_correct_answer_by_question(question_id):
        return AnswerController.get_correct_answer_by_question(question_id)
    
    @app.route("/answer/<int:answer_id>", methods=['PUT'])
    @jwt_required()
    def update_answer(answer_id):
        data = request.get_json()
        data['id'] = answer_id
        errors = answer_update_schema.validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return AnswerController.update_answer(data)
    
    @app.route("/answer/<int:answer_id>", methods=['DELETE'])
    @jwt_required()
    def delete_answer(answer_id):
        return AnswerController.delete_answer(answer_id)


    @app.route("/game/create", methods=['POST'])
    # @jwt_required()
    def create_game():
        data = request.get_json()
        return GameController.create_game(data)
    @app.route("/games", methods=['GET'])
    @jwt_required()
    def get_all_games():
        return GameController.get_all_games()
    @app.route("/game/<int:game_id>", methods=['GET'])
    @jwt_required()
    def get_game_by_id(game_id):
        return GameController.get_game_by_id(game_id)
    @app.route("/game/<int:game_id>", methods=['PUT'])
    @jwt_required()
    def update_game(game_id):
        data = request.get_json()
        data['id'] = game_id
        return GameController.update_game(data)
    @app.route("/game/<int:game_id>", methods=['DELETE'])
    @jwt_required()
    def delete_game(game_id):
        return GameController.delete_game(game_id)

    @app.route("/games/player/<int:player_id>", methods=['GET'])
    @jwt_required()
    def get_games_by_player(player_id):
        return GameController.get_games_by_player(player_id)

    @app.route("/games/status/<string:status>", methods=['GET'])
    @jwt_required()
    def get_games_by_status(status):
        return GameController.get_games_by_status(status)

    @app.route("/games/theme/<int:theme_id>", methods=['GET'])
    @jwt_required()
    def get_games_by_theme(theme_id):
        return GameController.get_games_by_theme(theme_id)

    @app.route("/game/<int:game_id>/points", methods=['GET'])
    @jwt_required()
    def show_points(game_id):
        return GameController.show_points(game_id)

    @app.route("/game/<int:game_id>/start", methods=['POST'])
    @jwt_required()
    def start_game_and_get_question(game_id):
        player_id = get_jwt_identity()
        return GameController.start_game_and_get_question(game_id, player_id)
    
    @app.route("/game/<int:game_id>/question/<int:question_index>", methods=['GET'])
    @jwt_required()
    def get_current_question(game_id, question_index):
        player_id = get_jwt_identity()
        return GameController.get_current_question(game_id, question_index, player_id)
    
    @app.route("/game/<int:game_id>/answer", methods=['POST'])
    @jwt_required()
    def submit_answer(game_id):
        player_id = get_jwt_identity()
        data = request.get_json()
        return GameController.submit_answer(game_id, data, player_id)
    
    @app.route("/game/<int:game_id>/finish", methods=['POST'])
    @jwt_required()
    def finish_game(game_id):
        player_id = get_jwt_identity()
        return GameController.finish_game(game_id, player_id)


