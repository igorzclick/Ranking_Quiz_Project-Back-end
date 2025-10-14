from marshmallow import Schema, fields, validate

class AnswerSchema(Schema):
    text = fields.Str(required=True)
    is_correct = fields.Bool(required=True)
    order = fields.Int(required=True)

class QuestionSchema(Schema):
    text = fields.Str(required=True)
    difficulty = fields.Str(required=True, validate=validate.OneOf(["easy", "medium", "hard"]))
    explanation = fields.Str(required=False)
    answers = fields.List(fields.Nested(AnswerSchema), required=True, validate=validate.Length(min=2))

class ThemeIntegratedSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    is_active = fields.Bool(required=True)
    questions = fields.List(fields.Nested(QuestionSchema), required=True, validate=validate.Length(min=1))

theme_integrated_schema = ThemeIntegratedSchema()