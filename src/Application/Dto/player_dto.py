from apiflask import Schema
from apiflask.fields import String, Email
from apiflask.validators import Length

class PlayerRegisterSchema(Schema):
    id = String(dump_only=True)
    username = String(required=True, validate=Length(1))
    email = Email(required=True)
    password = String(required=True, validate=Length(min=6))

player_schema = PlayerRegisterSchema()
players_schema = PlayerRegisterSchema(many=True)