# models.py - Định nghĩa các lớp dữ liệu
# File này chứa các lớp dữ liệu cho ứng dụng tạo câu hỏi trắc nghiệm

class User:
    """Lớp User đại diện cho một người dùng"""
    def __init__(self, username, password):
        self.username = username    # Tên đăng nhập
        self.password = password    # Mật khẩu

class QuizSession:
    """Lớp QuizSession đại diện cho một phiên thi trắc nghiệm"""
    def __init__(self, user_id, questions, answers=None, score=None):
        self.user_id = user_id      # ID người dùng
        self.questions = questions  # Câu hỏi (chuỗi text)
        self.answers = answers      # Đáp án người dùng nhập
        self.score = score         # Điểm số
        self.timestamp = None      # Thời gian làm bài

class QuizResult:
    """Lớp QuizResult đại diện cho kết quả chấm điểm"""
    def __init__(self, score, total_questions, details):
        self.score = score                  # Điểm đạt được
        self.total_questions = total_questions  # Tổng số câu
        self.details = details              # Chi tiết kết quả từ AI
