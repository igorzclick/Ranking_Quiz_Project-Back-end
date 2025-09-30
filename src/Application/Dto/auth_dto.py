from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import Length

class AuthRegisterSchema(Schema):
    id = String(dump_only=True)
    username = String(required=True, validate=Length(1))
    password = String(required=True, validate=Length(min=6))

auth_schema = AuthRegisterSchema()