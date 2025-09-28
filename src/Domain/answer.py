class AnswerDomain:
    def __init__(self, text, is_correct, order, question_id):
        self.text = text
        self.is_correct = is_correct
        self.order = order
        self.question_id = question_id

    def to_dict(self):
        return {
            "text": self.text,
            "is_correct": self.is_correct,
            "order": self.order,
            "question_id": self.question_id
        }
