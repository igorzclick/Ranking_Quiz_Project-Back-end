from src.config.data_base import db
from src.Infrastructure.Model.game_model import Game
from src.Infrastructure.Model.theme_model import Theme
from src.Infrastructure.Model.question_model import Question
from src.Infrastructure.Model.answer_model import Answer
from src.Infrastructure.Model.game_answer_model import GameAnswer
from src.Application.Service.theme_service import ThemeService
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
    def get_game_by_id(game_id):
        try:
            game = Game.query.filter_by(id=game_id).first()
            game_dict = game.to_dict()
            theme_dict = ThemeService.get_theme_integrated(game_dict['theme_id'])

            result = {
                "game": game_dict,
                "theme": theme_dict
            }
            return 200, result if game else (404, {"message": "Game not found"})
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
            if not game:
                return None, 'Game not found' 
            else:
                return game.to_dict()['points'], None
                
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

    @staticmethod
    def submit_answer(game_id, question_id, answer_id):
        try:
            game = Game.query.filter_by(id=game_id).first()
            if not game:
                return None, "Game not found"

            # Ensure game is active
            if game.status != 'active':
                return None, "Game is not active"

            question = Question.query.filter_by(id=question_id).first()
            if not question:
                return None, "Question not found"
            if question.theme_id != game.theme_id:
                return None, "Question does not belong to game's theme"

            answer = Answer.query.filter_by(id=answer_id, question_id=question_id).first()
            if not answer:
                return None, "Answer not found for this question"

            # Prevent duplicate answers for same question in the same game
            existing = GameAnswer.query.filter_by(game_id=game_id, question_id=question_id).first()
            if existing:
                return None, "Question already answered in this game"

            is_correct = bool(answer.is_correct)
            points_awarded = question.points or 0
            if not is_correct:
                points_awarded = 0

            record = GameAnswer(
                game_id=game_id,
                question_id=question_id,
                answer_id=answer_id,
                is_correct=is_correct,
                points_awarded=points_awarded,
            )
            db.session.add(record)

            # Update game points
            new_points = (game.points or 0) + points_awarded
            game.points = new_points

            db.session.commit()

            return {
                "answer": record.to_dict(),
                "game_points": new_points,
            }, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def finish_game(game_id):
        try:
            game = Game.query.filter_by(id=game_id).first()
            if not game:
                return None, "Game not found"

            # Fetch all questions for game's theme
            theme_data = ThemeService.get_theme_integrated(game.theme_id)
            if isinstance(theme_data, tuple):
                # In case service returned a response object
                return None, "Unable to fetch theme data"
            all_questions = theme_data.get('questions', [])
            total_questions = len(all_questions)

            # Fetch answered questions for this game
            answered_records = GameAnswer.query.filter_by(game_id=game_id).all()
            answered_by_qid = {rec.question_id: rec for rec in answered_records}

            # Check completion
            if len(answered_by_qid) < total_questions:
                return None, "Player has not answered all questions for this theme"

            summary = []
            correct_count = 0
            wrong_count = 0

            for q in all_questions:
                rec = answered_by_qid.get(q['id'])
                if not rec:
                    # Should not happen due to check above
                    continue
                item = {
                    "question_id": q['id'],
                    "question_text": q['text'],
                    "selected_answer_id": rec.answer_id,
                    "is_correct": rec.is_correct,
                    "points_awarded": rec.points_awarded,
                }
                summary.append(item)
                if rec.is_correct:
                    correct_count += 1
                else:
                    wrong_count += 1

            # Mark game as completed
            game.status = 'completed'
            db.session.commit()

            result = {
                "summary": summary,
                "correct": correct_count,
                "wrong": wrong_count,
                "final_points": game.points or 0,
                "total_questions": total_questions,
            }
            return result, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
