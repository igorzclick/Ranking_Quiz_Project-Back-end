class RoomDomain:
    def __init__(self, title, theme_id, created_by):
        self.title = title
        self.theme_id = theme_id
        self.created_by = created_by

    def to_dict(self):
        return {
            "title": self.title,
            "theme_id": self.theme_id,
            "created_by": self.created_by,
        }


