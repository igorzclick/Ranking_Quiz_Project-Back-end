from apiflask import Schema
from apiflask.fields import String, Integer, Boolean
from apiflask.validators import Length, Range

class AnswerRegisterSchema(Schema):
    id = Integer(dump_only=True)
    text = String(required=True, validate=Length(min=1, max=500))
    is_correct = Boolean(required=True)
    order = Integer(required=True, validate=Range(min=1, max=10))
    question_id = Integer(required=True)

class AnswerUpdateSchema(Schema):
    id = Integer(required=True)
    text = String(validate=Length(min=1, max=500))
    is_correct = Boolean()
    order = Integer(validate=Range(min=1, max=10))
    question_id = Integer()

answer_schema = AnswerRegisterSchema()
answers_schema = AnswerRegisterSchema(many=True)
answer_update_schema = AnswerUpdateSchema()
