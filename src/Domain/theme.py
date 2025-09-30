class ThemeDomain:
    def __init__(self, name, description, is_active, created_by):
        self.name = name
        self.description = description
        self.is_active = is_active
        self.created_by = created_by

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_by": self.created_by
        }