from flask import jsonify, make_response
from src.Domain.theme import ThemeDomain
from src.Domain.question import QuestionDomain
from src.Domain.answer import AnswerDomain
from src.Infrastructure.Model.theme_model import Theme
from src.Infrastructure.Model.question_model import Question
from src.Infrastructure.Model.answer_model import Answer
from src.config.data_base import db
from src.Application.Service.theme_service import ThemeService
from flask_jwt_extended import get_jwt_identity

class ThemeIntegratedController:
    @staticmethod
    def create_theme_integrated(data):
        try:
            user_id = get_jwt_identity()
            
            theme_domain = ThemeDomain(
                name=data['name'],
                description=data['description'],
                is_active=data['is_active'],
                created_by=user_id
            )
            
            theme = Theme(**theme_domain.to_dict())
            db.session.add(theme)
            db.session.flush()
            
            for question_data in data['questions']:
                points = ThemeIntegratedController._calculate_points_by_difficulty(question_data['difficulty'])
                
                question_domain = QuestionDomain(
                    text=question_data['text'],
                    difficulty=question_data['difficulty'],
                    theme_id=theme.id,
                    explanation=question_data.get('explanation'),
                    points=points
                )
                
                question = Question(**question_domain.to_dict())
                db.session.add(question)
                db.session.flush()
                
                for answer_data in question_data['answers']:
                    answer_domain = AnswerDomain(
                        text=answer_data['text'],
                        is_correct=answer_data['is_correct'],
                        order=answer_data['order'],
                        question_id=question.id
                    )
                    
                    answer = Answer(**answer_domain.to_dict())
                    db.session.add(answer)
            
            db.session.commit()
            
            return make_response(jsonify({
                "message": "Theme com questions e answers criado com sucesso",
                "theme_id": theme.id
            }), 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({
                "error": str(e)
            }), 500)
    
    @staticmethod
    def update_theme_integrated(theme_id, data):
        try:
            theme = Theme.query.get(theme_id)
            if not theme:
                return make_response(jsonify({"error": "Theme não encontrado"}), 404)
            
            theme.name = data['name']
            theme.description = data['description']
            theme.is_active = data['is_active']
            
            questions = Question.query.filter_by(theme_id=theme_id).all()
            for question in questions:
                Answer.query.filter_by(question_id=question.id).delete()
            Question.query.filter_by(theme_id=theme_id).delete()
            
            for question_data in data['questions']:
                points = ThemeIntegratedController._calculate_points_by_difficulty(question_data['difficulty'])
                
                question_domain = QuestionDomain(
                    text=question_data['text'],
                    difficulty=question_data['difficulty'],
                    theme_id=theme.id,
                    explanation=question_data.get('explanation'),
                    points=points
                )
                
                question = Question(**question_domain.to_dict())
                db.session.add(question)
                db.session.flush()  
                
                for answer_data in question_data['answers']:
                    answer_domain = AnswerDomain(
                        text=answer_data['text'],
                        is_correct=answer_data['is_correct'],
                        order=answer_data['order'],
                        question_id=question.id
                    )
                    
                    answer = Answer(**answer_domain.to_dict())
                    db.session.add(answer)
            
            db.session.commit()
            
            return make_response(jsonify({
                "message": "Theme com questions e answers atualizado com sucesso",
                "theme_id": theme.id
            }), 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({
                "error": str(e)
            }), 500)
    
    @staticmethod
    def get_theme_integrated(theme_id):
        try:
            result = ThemeService.get_theme_integrated(theme_id)
            return make_response(jsonify(result), 200)
            
        except Exception as e:
            return make_response(jsonify({
                "error": str(e)
            }), 500)
    
    @staticmethod
    def _calculate_points_by_difficulty(difficulty):
        if difficulty == "easy":
            return 10
        elif difficulty == "medium":
            return 20
        elif difficulty == "hard":
            return 30
        else:
            return 10