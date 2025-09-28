from apiflask import Schema
from apiflask.fields import String, Integer, Boolean
from apiflask.validators import Length, Range

class QuestionRegisterSchema(Schema):
    id = Integer(dump_only=True)
    text = String(required=True, validate=Length(min=1, max=1000))
    difficulty = String(required=True, validate=Length(min=1))
    theme_id = Integer(required=True)
    explanation = String(validate=Length(max=1000))
    time_limit = Integer(load_default=60, validate=Range(min=10, max=300))
    points = Integer(validate=Range(min=1, max=100))

class QuestionUpdateSchema(Schema):
    id = Integer(required=True)
    text = String(validate=Length(min=1, max=1000))
    difficulty = String(validate=Length(min=1))
    theme_id = Integer()
    explanation = String(validate=Length(max=1000))
    time_limit = Integer(validate=Range(min=10, max=300))
    points = Integer(validate=Range(min=1, max=100))

question_schema = QuestionRegisterSchema()
questions_schema = QuestionRegisterSchema(many=True)
question_update_schema = QuestionUpdateSchema()
