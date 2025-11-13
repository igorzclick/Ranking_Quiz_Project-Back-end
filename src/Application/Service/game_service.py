from src.config.data_base import db
from src.Infrastructure.Model.game_model import Game
from src.Infrastructure.Model.theme_model import Theme
from src.Infrastructure.Model.question_model import Question
from src.Infrastructure.Model.answer_model import Answer
from src.Application.Service.theme_service import ThemeService
from src.Application.Service.question_service import QuestionService
import random
class GameService:
    @staticmethod
    def create_game(game):
        new_game = game.to_dict()
        try:
            game = Game(
                **new_game
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
                setattr(game, key, value)

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
    def start_game(game_id, player_id):
        try:
            game = Game.query.filter_by(id=game_id).first()        
            if not game:
                return None, "Game not found"
            
            if int(game.player_id) != int(player_id):
                return None, "Only the game owner can start and play this game. Single player mode."
            
            if game.status == 'completed':
                return None, "Game is already completed. Cannot start a completed game."
            
            if game.status != 'active':
                game.status = 'active'
                db.session.commit()
            
            return game, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_current_question(game_id, player_id, question_index=0):
        try:
            game = Game.query.filter_by(id=game_id).first()
            if not game:
                return None, "Game not found"
            
            if int(game.player_id) != int(player_id):
                return None, "Only the game owner can access this game. Single player mode."
            
            if game.status != 'active':
                return None, "Game is not active"
            
            questions = Question.query.filter_by(theme_id=game.theme_id).all()
            
            if not questions:
                return None, "No questions found for this theme"
            
            questions_list = list(questions)
            rng = random.Random(game_id)
            rng.shuffle(questions_list)
            
            if question_index >= len(questions_list):
                return None, "No more questions available"
            
            question = questions_list[question_index]
            
            question_dict = {
                "id": question.id,
                "text": question.text,
                "difficulty": question.difficulty,
                "theme_id": question.theme_id,
                "points": question.points,
                "answers": []
            }
            
            answers = Answer.query.filter_by(question_id=question.id).order_by(Answer.order).all()
            for answer in answers:
                answer_dict = {
                    "id": answer.id,
                    "text": answer.text,
                    "order": answer.order,
                    "question_id": answer.question_id
                }
                question_dict["answers"].append(answer_dict)
            
            rng = random.Random(game_id + question.id)
            rng.shuffle(question_dict["answers"])
            
            return {
                "question": question_dict,
                "question_index": question_index,
                "total_questions": len(questions_list),
                "game_id": game_id
            }, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def submit_answer(game_id, question_id, answer_id, player_id):
        try:
            game = Game.query.filter_by(id=game_id).first()
            if not game:
                return None, "Game not found"
            
            if int(game.player_id) != int(player_id):
                return None, "Only the game owner can submit answers. Single player mode."
            
            if game.status != 'active':
                return None, "Game is not active"
            
            answer = Answer.query.filter_by(id=answer_id, question_id=question_id).first()
            if not answer:
                return None, "Answer not found or does not belong to this question"
            
            correct_answer = Answer.query.filter_by(question_id=question_id, is_correct=True).first()
            if not correct_answer:
                return None, "Correct answer not found for this question"
            
            is_correct = answer.is_correct
            
            question = Question.query.filter_by(id=question_id).first()
            points_earned = 0
            
            if is_correct and question:
                points_earned = question.points or 0
                current_points = game.points or 0
                game.points = current_points + points_earned
                db.session.commit()
            
            result = {
                "is_correct": is_correct,
                "points_earned": points_earned,
                "total_points": game.points or 0,
                "correct_answer_id": correct_answer.id,
                "correct_answer_text": correct_answer.text,
                "explanation": question.explanation if question else None
            }
            
            return result, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def finish_game(game_id, player_id):
        try:
            game = Game.query.filter_by(id=game_id).first()
            if not game:
                return None, "Game not found"
            
            if int(game.player_id) != int(player_id):
                return None, "Only the game owner can finish this game. Single player mode."
            
            game.status = 'completed'
            db.session.commit()
            
            return game.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)        
