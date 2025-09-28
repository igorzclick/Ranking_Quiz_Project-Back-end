class QuestionDomain:
    def __init__(self, text, difficulty, theme_id, explanation=None, time_limit=60, points=None):
        self.text = text
        self.difficulty = difficulty
        self.theme_id = theme_id
        self.explanation = explanation
        self.time_limit = time_limit
        self.points = points

    def to_dict(self):
        return {
            "text": self.text,
            "difficulty": self.difficulty,
            "theme_id": self.theme_id,
            "explanation": self.explanation,
            "time_limit": self.time_limit,
            "points": self.points
        }
