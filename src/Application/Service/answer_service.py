from src.Infrastructure.Model.answer_model import Answer
from src.Infrastructure.Model.question_model import Question
from src.config.data_base import db

class AnswerService:
    @staticmethod
    def create_answer(answer):
        new_answer = answer.to_dict()
        try:

            question = Question.query.filter_by(id=new_answer['question_id']).first()
            if not question:
                return None, "Question not found"
            
            existing_answer = Answer.query.filter_by(
                question_id=new_answer['question_id'], 
                order=new_answer['order']
            ).first()
            if existing_answer:
                return None, f"Answer with order {new_answer['order']} already exists for this question"
            
            answer = Answer(**new_answer)
            db.session.add(answer)
            db.session.commit()

            return answer, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def get_all_answers():
        try:
            answers = Answer.query.all()        
            return [answer.to_dict() for answer in answers]
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_answer_by_id(id):
        try:
            answer = Answer.query.filter_by(id=id).first()        
            return answer.to_dict() if answer else None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_answers_by_question(question_id):
        try:
            answers = Answer.query.filter_by(question_id=question_id).order_by(Answer.order).all()        
            return [answer.to_dict() for answer in answers]
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_correct_answer_by_question(question_id):
        try:
            answer = Answer.query.filter_by(question_id=question_id, is_correct=True).first()        
            return answer.to_dict() if answer else None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def update_answer(answer_data):
        try:
            answer = Answer.query.filter_by(id=answer_data['id']).first()

            if not answer:
                return None, "Answer not found"

            if 'question_id' in answer_data:
                question = Question.query.filter_by(id=answer_data['question_id']).first()
                if not question:
                    return None, "Question not found"

            if 'order' in answer_data and answer_data['order'] != answer.order:
                existing_answer = Answer.query.filter_by(
                    question_id=answer.question_id, 
                    order=answer_data['order']
                ).first()
                if existing_answer and existing_answer.id != answer.id:
                    return None, f"Answer with order {answer_data['order']} already exists for this question"

            for field, value in answer_data.items():
                if field != 'id' and hasattr(answer, field):
                    setattr(answer, field, value)

            db.session.commit()
            return answer, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_answer(id):
        try:
            answer = Answer.query.filter_by(id=id).first()

            if not answer:
                return None, "Answer not found"

            db.session.delete(answer)
            db.session.commit()

            return answer, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
