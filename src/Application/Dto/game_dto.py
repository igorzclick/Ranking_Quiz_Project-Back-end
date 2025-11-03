from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length

class GameDto(Schema):
    id = String(dump_only=True)
    theme_id = String(required=True)
    game_name = String(required=True, validate=Length(min=1, max=100))
    player_id = String(required=True)
    status = String(required=True)
    points = Integer(required=False)