from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
from PyQt6 import uic
import sys
import os
from google import genai
import google.generativeai as genai
from data import load_essays, save_essays
from model import Essay
from history import HistoryWindow
# API key cho Gemini
# Lưu ý: Bạn nên quản lý API key của mình một cách an toàn, ví dụ như sử dụng biến môi trường.
API_KEY = "---"

MAIN_UI_FILE = os.path.join(os.path.dirname(__file__), "nhatminh.ui")

essays = load_essays()

def get_answer(text, level):
    """
    Gửi bài viết đến Gemini API để đánh giá

    Args:
        text (str): Bài viết cần đánh giá
        level (str): Trình độ học sinh (Beginner/Intermediate/Advanced)

    Returns:
        str: Phản hồi từ AI
    """
    try:
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel('gemini-2.5-flash')

        role_info = f"""
        Bạn là giáo viên chấm bài viết tiếng Anh.
        Bạn sẽ nhận được một bài viết tiếng Anh của học sinh trình độ {level}.
        Mong bạn hãy chấm điểm rất chặt chẽ nếu người dùng là Advanced, chấm điểm ít chặt chẽ hơn đối với Intermediate, 
        chấm điểm rất nhẹ tay đối với Beginner.
        Hãy đánh giá dựa trên level của học sinh và nhận xét theo các tiêu chí:
        - Ngữ pháp (Grammar)
        - Từ vựng (Vocabulary)
        - Cấu trúc (Structure) 
        - Ý tưởng (Ideas)
        - Gợi ý cải thiện (Suggestions for improvement)
        - Phân tích từ vựng (cái này có thể cho ngắn)
        - Trả về bài viết được viết lại tốt hơn cho người dùng tham khảo
        - Cho các Video Youtube cho người dùng để giúp người dùng cải thiện.

        Cuối cùng, hãy cho điểm bài viết trên thang điểm 10.

        Trả về định dạng text cơ bản, chia các ý theo gạch đầu dòng, không dùng markdown.
        """

        question = (
            f"Đánh giá bài viết tiếng Anh này của học sinh trình độ {level}:\n\n{text}"
        )

        # Gemini sử dụng một định dạng hơi khác cho các cuộc hội thoại nhiều lượt
        # Ở đây chúng ta sẽ bắt đầu một cuộc trò chuyện mới mỗi lần để đơn giản.
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": [role_info]
            },
            {
                "role": "model",
                "parts": ["Tôi đã sẵn sàng để chấm bài."]
            }
        ])

        response = chat.send_message(question)

        return response.text

    except Exception as e:
        return f"Lỗi khi kết nối với AI: {str(e)}"


def ask_question(essay, feedback, question, level):
    """
    Gửi câu hỏi thêm về bài viết đến Gemini API

    Args:
        essay (str): Bài viết gốc
        feedback (str): Phản hồi đã có
        question (str): Câu hỏi của học sinh
        level (str): Trình độ học sinh

    Returns:
        str: Phản hồi từ AI
    """
    try:
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel('gemini-2.5-flash')

        # Xây dựng lại lịch sử trò chuyện để cung cấp ngữ cảnh
        history = [
            {
                "role": "user",
                "parts": [f"Bạn là giáo viên tiếng Anh đang hỗ trợ học sinh trình độ {level}."]
            },
            {
                "role": "model",
                "parts": ["Được thôi, tôi sẽ giúp."]
            },
            {
                "role": "user",
                "parts": [f"Bài viết của học sinh:\n{essay}\n\nĐánh giá của bạn:\n{feedback}"]
            },
            {
                "role": "model",
                "parts": ["Tôi đã xem lại bài viết và phản hồi của mình."]
            }
        ]
        
        chat = model.start_chat(history=history)
        response = chat.send_message(question)

        return response.text

    except Exception as e:
        return f"Lỗi khi kết nối với AI: {str(e)}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(MAIN_UI_FILE, self)

        self.btnToggleMode.setText("☀️")
        self.btnToggleMode.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                background-color: transparent;
                border: none;
            }
        """
        )
        self.dark_mode = False


        self.btnEvaluate.clicked.connect(self.evaluate_text)
        self.btnToggleMode.clicked.connect(self.toggle_dark_mode)
        self.btnAsk.clicked.connect(self.ask_additional_question)
        self.btnHistory.clicked.connect(self.open_history_window)

        # chế độ tối và lưu trữ bài viết/phản hồi
        self.dark_mode = False
        self.current_essay = ""
        self.current_feedback = ""
        self.history_window = None

        self.labelQuestion.setVisible(False)
        self.lineQuestion.setVisible(False)
        self.btnAsk.setVisible(False)

        self.toggle_dark_mode()

    def evaluate_text(self):
        """Xử lý khi người dùng nhấn nút đánh giá"""
        # Lấy nội dung bài viết
        text = self.textInput.toPlainText().strip()

        if not text:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng nhập bài viết cần đánh giá!"
            )
            return

        # Lấy trình độ từ combobox
        level = self.comboLevel.currentText()

        # Hiển thị thông báo đang xử lý
        self.textOutput.setPlainText("Đang đánh giá bài viết, vui lòng đợi...")
        QApplication.processEvents()  # Cập nhật giao diện

        # đánh giá
        result = get_answer(text, level)

        # Lưu bài viết 
        self.current_essay = text
        self.current_feedback = result

        # Hiển thị kq
        self.textOutput.setPlainText(result)

        # Hiển thị reply
        self.labelQuestion.setVisible(True)
        self.lineQuestion.setVisible(True)
        self.btnAsk.setVisible(True)
        
        # Lưu bài viết
        essays.append(Essay(self.current_essay, self.current_feedback))
        save_essays(essays)
        
    def ask_additional_question(self):
        """Xử lý khi người dùng đặt câu hỏi thêm"""
        # Kiểm tra xem đã có bài viết và phản hồi chưa
        if not self.current_essay or not self.current_feedback:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng đánh giá bài viết trước khi đặt câu hỏi!"
            )
            return

        # Lấy câu hỏi
        question = self.lineQuestion.text().strip()
        if not question:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập câu hỏi!")
            return

        # Lấy trình độ
        level = self.comboLevel.currentText()

        # Hiển thị thông báo đang xử lý
        current_text = self.textOutput.toPlainText()
        self.textOutput.setPlainText(
            current_text + "\n\nĐang xử lý câu hỏi, vui lòng đợi..."
        )
        QApplication.processEvents()  # Cập nhật giao diện

        # Gọi API để trả lời câu hỏi
        answer = ask_question(
            self.current_essay, self.current_feedback, question, level
        )

        # Hiển thị câu hỏi và câu trả lời
        self.textOutput.setPlainText(
            current_text + f"\n\nCâu hỏi: {question}\n\nTrả lời: {answer}"
        )

        # Xóa nội dung câu hỏi
        self.lineQuestion.clear()

    def open_history_window(self):
        """Mở cửa sổ lịch sử bài viết"""
        try:
            if self.history_window is None or not self.history_window.isVisible():
                self.history_window = HistoryWindow()
                # Đồng bộ dark mode
                if self.dark_mode != self.history_window.dark_mode:
                    self.history_window.toggle_dark_mode()
            
            self.history_window.show()
            self.history_window.activateWindow()
            self.history_window.raise_()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở cửa sổ lịch sử: {str(e)}")

    def toggle_dark_mode(self):
        """Chuyển đổi giữa chế độ sáng và tối"""
        self.dark_mode = not self.dark_mode

        # Thay đổi emoji
        if self.dark_mode:
            self.btnToggleMode.setText("🌙")

            # Áp dụng dark mode
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #1E1E1E;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QLabel#labelTitle {
                    font-size: 28px;
                    font-weight: bold;
                    color: #64B5F6;
                }
                QPushButton {
                    background-color: #2979FF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
                QTextEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QComboBox {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QWidget#mainContent {
                    background-color: #2D2D2D;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """
            )
        else:
            self.btnToggleMode.setText("☀️")

            # Áp dụng light mode
            self.setStyleSheet(
                """
                QMainWindow {
                    background-color: #FFFFFF;
                }
                QLabel {
                    color: #333333;
                }
                QLabel#labelTitle {
                    font-size: 28px;
                    font-weight: bold;
                    color: #1976D2;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QTextEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 10px;
                    font-size: 14px;
                }
                QComboBox {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QLineEdit {
                    background-color: #F5F5F5;
                    color: #333333;
                    border: 1px solid #DDDDDD;
                    border-radius: 5px;
                    padding: 8px;
                    font-size: 14px;
                }
                QWidget#mainContent {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton#btnToggleMode {
                    font-size: 18px;
                    background-color: transparent;
                    border: none;
                }
            """
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
