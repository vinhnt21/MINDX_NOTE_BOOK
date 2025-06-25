class User:
    """Class đại diện cho người dùng"""
    def __init__(self, username, password, highest_score=0):
        self.username = username
        self.password = password
        self.highest_score = highest_score
    
    def __str__(self):
        return f"User: {self.username}, Score: {self.highest_score}"

class Question:
    """Class đại diện cho câu hỏi"""
    def __init__(self, id, question, options, correct_answer):
        self.id = id
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
    
    def __str__(self):
        return f"Question {self.id}: {self.question}"
