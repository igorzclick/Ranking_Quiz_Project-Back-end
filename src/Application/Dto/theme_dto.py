from apiflask import Schema
from apiflask.fields import String, Integer, Boolean
from apiflask.validators import Length

class ThemeRegisterSchema(Schema):
    id = Integer(dump_only=True)
    name = String(required=True, validate=Length(1))
    description = String()
    is_active = Boolean(load_default=True)
    created_by = Integer(dump_only=True)

class ThemeUpdateSchema(Schema):
    id = Integer(required=True)
    name = String(validate=Length(1))
    description = String()
    is_active = Boolean()
    created_by = Integer()

theme_schema = ThemeRegisterSchema()
themes_schema = ThemeRegisterSchema(many=True)
theme_update_schema = ThemeUpdateSchema()