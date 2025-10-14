from src.Application.Service.theme_service import ThemeService
from src.Infrastructure.Model.question_model import Question
from src.Infrastructure.Model.theme_model import Theme
from src.config.data_base import db

class QuestionService:
    @staticmethod
    def create_question(question):
        new_question = question.to_dict()
        try:
            theme = Theme.query.filter_by(id=new_question['theme_id']).first()
            if not theme:
                return None, "Theme not found"
            
            difficulty = new_question['difficulty'].lower()

            points_map = {
                'easy': getattr(theme, 'easy_points', None),
                'medium': getattr(theme, 'medium_points', None),
                'hard': getattr(theme, 'hard_points', None)
            }
            new_question['points'] = points_map.get(difficulty) or ThemeService.get_default_points(difficulty)
            
            question = Question(**new_question)
            db.session.add(question)
            db.session.commit()

            return question, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def get_all_questions():
        try:
            questions = Question.query.all()        
            return [question.to_dict() for question in questions]
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_question_by_id(id):
        try:
            question = Question.query.filter_by(id=id).first()        
            return question.to_dict() if question else None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_questions_by_theme(theme_id):
        try:
            questions = Question.query.filter_by(theme_id=theme_id).all()        
            return [question.to_dict() for question in questions]
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_questions_by_difficulty(difficulty):
        try:
            questions = Question.query.filter_by(difficulty=difficulty).all()        
            return [question.to_dict() for question in questions]
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def update_question(question_data):
        try:
            question = Question.query.filter_by(id=question_data['id']).first()

            if not question:
                return None, "Question not found"

            if 'theme_id' in question_data:
                theme = Theme.query.filter_by(id=question_data['theme_id']).first()
                if not theme:
                    return None, "Theme not found"
                
            for field, value in question_data.items():
                if field != 'id' and hasattr(question, field):
                    setattr(question, field, value)

            db.session.commit()
            return question, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).first()

            if not question:
                return None, "Question not found"

            db.session.delete(question)
            db.session.commit()

            return question, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
