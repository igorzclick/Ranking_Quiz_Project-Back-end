from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length


class RoomRegisterSchema(Schema):
    id = Integer(dump_only=True)
    title = String(required=True, validate=Length(1))
    theme_id = Integer(required=True)
    created_by = Integer(dump_only=True)


room_register_schema = RoomRegisterSchema()

