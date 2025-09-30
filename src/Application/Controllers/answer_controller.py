from flask import jsonify, make_response
from src.Application.Service.answer_service import AnswerService
from src.Domain.answer import AnswerDomain

class AnswerController:
    @staticmethod
    def register_answer(body):
        answer_domain = AnswerDomain(
            text=body['text'],
            is_correct=body['is_correct'],
            order=body['order'],
            question_id=body['question_id']
        )
        answer, error_message = AnswerService.create_answer(answer_domain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        return make_response(jsonify({
            "message": "Answer registered successfully",
            "answer": answer.to_dict()
        }), 201)

    @staticmethod
    def get_all_answers():
        answers = AnswerService.get_all_answers()
        if answers is None:
            return make_response(jsonify({"message": "Could not retrieve answers"}), 500)
        return make_response(jsonify({
            "answers": answers
        }), 200)

    @staticmethod
    def get_answer_by_id(answer_id):
        answer = AnswerService.get_answer_by_id(answer_id)
        if not answer:
             return make_response(jsonify({"message": "Answer not found"}), 404)
        return make_response(jsonify({
            "answer": answer
        }), 200)

    @staticmethod
    def get_answers_by_question(question_id):
        answers = AnswerService.get_answers_by_question(question_id)
        if answers is None:
             return make_response(jsonify({"message": "Could not retrieve answers"}), 500)
        return make_response(jsonify({
            "answers": answers
        }), 200)

    @staticmethod
    def get_correct_answer_by_question(question_id):
        answer = AnswerService.get_correct_answer_by_question(question_id)
        if not answer:
             return make_response(jsonify({"message": "Correct answer not found for this question"}), 404)
        return make_response(jsonify({
            "answer": answer
        }), 200)

    @staticmethod
    def update_answer(body):
        answer, error_message = AnswerService.update_answer(body)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not answer:
            return make_response(jsonify({"message": "Answer not found or update failed"}), 404)

        return make_response(jsonify({
            "message": "Answer updated successfully",
            "answer": answer.to_dict()
        }), 200)
    
    @staticmethod
    def delete_answer(answer_id):
        answer, error_message = AnswerService.delete_answer(answer_id)
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not answer:
            return make_response(jsonify({"message": "Answer not found"}), 404)

        return make_response(jsonify({
            "message": "Answer deleted successfully",
            "answer": answer.to_dict()
        }), 200)
