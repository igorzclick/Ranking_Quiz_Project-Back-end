from flask import jsonify, make_response
from src.Application.Service.question_service import QuestionService
from src.Domain.question import QuestionDomain


COULD_NOT_RETRIEVE_QUESTIONS = "Could not retrieve questions"

class QuestionController:
    @staticmethod
    def register_question(body):
        question_domain = QuestionDomain(
            text=body['text'],
            difficulty=body['difficulty'],
            theme_id=body['theme_id'],
            explanation=body.get('explanation'),
            time_limit=body.get('time_limit', 60),
            points=body.get('points')
        )
        question, error_message = QuestionService.create_question(question_domain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        return make_response(jsonify({
            "message": "Question registered successfully",
            "question": question.to_dict()
        }), 201)

    @staticmethod
    def get_all_questions():
        questions = QuestionService.get_all_questions()
        if questions is None:
            return make_response(jsonify({"message": COULD_NOT_RETRIEVE_QUESTIONS}), 500)
        return make_response(jsonify({
            "questions": questions
        }), 200)

    @staticmethod
    def get_question_by_id(question_id):
        question = QuestionService.get_question_by_id(question_id)
        if not question:
             return make_response(jsonify({"message": "Question not found"}), 404)
        return make_response(jsonify({
            "question": question
        }), 200)

    @staticmethod
    def get_questions_by_theme(theme_id):
        questions = QuestionService.get_questions_by_theme(theme_id)
        if questions is None:
             return make_response(jsonify({"message": COULD_NOT_RETRIEVE_QUESTIONS}), 500)
        return make_response(jsonify({
            "questions": questions
        }), 200)

    @staticmethod
    def get_questions_by_difficulty(difficulty):
        questions = QuestionService.get_questions_by_difficulty(difficulty)
        if questions is None:
             return make_response(jsonify({"message": COULD_NOT_RETRIEVE_QUESTIONS}), 500)
        return make_response(jsonify({
            "questions": questions
        }), 200)

    @staticmethod
    def update_question(body):
        question, error_message = QuestionService.update_question(body)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not question:
            return make_response(jsonify({"message": "Question not found or update failed"}), 404)

        return make_response(jsonify({
            "message": "Question updated successfully",
            "question": question.to_dict()
        }), 200)
    
    @staticmethod
    def delete_question(question_id):
        question, error_message = QuestionService.delete_question(question_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not question:
            return make_response(jsonify({"message": "Question not found"}), 404)

        return make_response(jsonify({
            "message": "Question deleted successfully",
            "question": question.to_dict()
        }), 200)
