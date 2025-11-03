from src.Infrastructure.Model.theme_model import Theme
from src.Infrastructure.Model.player_model import Player
from src.Infrastructure.Model.question_model import Question
from src.Infrastructure.Model.answer_model import Answer
from src.config.data_base import db

class ThemeService:
    @staticmethod
    def get_default_points(difficulty):
        difficulty_points = {
            'easy': 10,
            'medium': 20,
            'hard': 30
        }

        return difficulty_points.get(difficulty.lower(), 10)

    @staticmethod
    def create_theme(theme):
        
        new_theme = theme.to_dict()
        try:
        
            player = Player.query.filter_by(id=new_theme['created_by']).first()
            if not player:
                return None, "Player not found"

            if Theme.query.filter_by(name=new_theme['name']).first():
                return None, "Theme name already registered"
            
            if 'is_active' not in new_theme:
                new_theme['is_active'] = True
            
            theme = Theme(
                **new_theme
            )

            db.session.add(theme)
            db.session.commit()

            return theme, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def get_all_themes():
        try:
            themes = Theme.query.filter_by(is_active=True).all()    
            return [theme.to_dict() for theme in themes]
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_theme_by_id(id):
        try:
            theme = Theme.query.filter_by(id=id).first()        
            return theme.to_dict()
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def get_theme_by_name(name):
        try:
            theme = Theme.query.filter_by(name=name).first()        
            return theme.to_dict()
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def update_theme(theme):
        new_theme = theme.to_dict()

        try:
            theme = Theme.query.filter_by(id=new_theme['id']).first()

            theme_by_name = Theme.query.filter_by(name=new_theme['name']).first()
            if theme_by_name != None and theme_by_name.id != theme.id:
                return None, "Theme name already registered"

            if not theme:
                return None, "Theme not found"

            theme.name = new_theme['name']
            theme.description = new_theme['description']
            theme.is_active = new_theme['is_active']

            db.session.commit()

            return theme, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_theme(id):
        try:
            theme = Theme.query.filter_by(id=id).first()

            if not theme:
                return None, "Theme not found"

            theme.is_active = False

            db.session.commit()

            return theme, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def get_theme_integrated(theme_id):
        theme = Theme.query.filter_by(id=theme_id, is_active=True).first()
        if not theme:
            return make_response(jsonify({"error": "Theme não encontrado"}), 404)
        
        questions = Question.query.filter_by(theme_id=theme_id).all()
        
        result = {
            "id": theme.id,
            "name": theme.name,
            "description": theme.description,
            "is_active": theme.is_active,
            "created_by": theme.created_by,
            "created_at": theme.created_at.isoformat() if hasattr(theme, 'created_at') else None,
            "updated_at": theme.updated_at.isoformat() if hasattr(theme, 'updated_at') else None,
            "questions": []
        }
        
        for question in questions:
            answers = Answer.query.filter_by(question_id=question.id).all()
            
            question_data = {
                "id": question.id,
                "text": question.text,
                "difficulty": question.difficulty,
                "explanation": question.explanation,
                "points": question.points,
                "answers": []
            }
            
            for answer in answers:
                answer_data = {
                    "id": answer.id,
                    "text": answer.text,
                    "is_correct": answer.is_correct,
                    "order": answer.order
                }
                question_data["answers"].append(answer_data)
            
            result["questions"].append(question_data)

        return result
        