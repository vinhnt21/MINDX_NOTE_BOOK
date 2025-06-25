from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import os
import sys
from data import register_user, login_user, save_quiz_session
from models import QuizSession
from ai import generate_questions, grade_answers

# Đường dẫn đến các file UI
DANGKY_UI = os.path.join(os.path.dirname(__file__), "ui", "DangKy.ui")
DANGNHAP_UI = os.path.join(os.path.dirname(__file__), "ui", "DangNhap.ui")
MAIN_UI = os.path.join(os.path.dirname(__file__), "ui", "Main.ui")

class DangKy(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(DANGKY_UI, self)
        self.parent_app = parent
        self.setup_connections()
    
    def setup_connections(self):
        """Thiết lập kết nối signal-slot"""
        self.pushButton.clicked.connect(self.register)
        self.pushButton_2.clicked.connect(self.switch_to_login)
    
    def register(self):
        """Xử lý đăng ký"""
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        confirm_password = self.lineEdit_3.text().strip()
        
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        success, message = register_user(username, password, confirm_password)
        
        if success:
            QMessageBox.information(self, "Thành công", message)
            self.clear_fields()
            self.switch_to_login()
        else:
            QMessageBox.warning(self, "Lỗi", message)
    
    def switch_to_login(self):
        """Chuyển sang màn hình đăng nhập"""
        login_window.show()
        self.hide()
    
    def clear_fields(self):
        """Xóa nội dung các ô nhập"""
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()

class DangNhap(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(DANGNHAP_UI, self)
        self.setup_connections()
    
    def setup_connections(self):
        """Thiết lập kết nối signal-slot"""
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.switch_to_register)
        # Nhấn Enter cũng có thể đăng nhập
        self.lineEdit_2.returnPressed.connect(self.login)
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        success, message, user = login_user(username, password)
        
        if success:
            QMessageBox.information(self, "Thành công", message)
            main_window.set_user(user)
            main_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Lỗi", message)
    
    def switch_to_register(self):
        """Chuyển sang màn hình đăng ký"""
        register_window.show()
        self.hide()
    
    def clear_fields(self):
        """Xóa nội dung các ô nhập"""
        self.lineEdit.clear()
        self.lineEdit_2.clear()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(MAIN_UI, self)
        self.current_questions = ""
        self.setup_connections()
        self.setup_ui()
    
    def setup_connections(self):
        """Thiết lập kết nối signal-slot"""
        self.generateButton.clicked.connect(self.generate_questions_action)
        self.gradeButton.clicked.connect(self.grade_answers_action)
        self.logoutButton.clicked.connect(self.logout)
        
        # Nhấn Enter ở ô nhập đáp án sẽ chấm điểm
        self.answersLineEdit.returnPressed.connect(self.grade_answers_action)
    
    def setup_ui(self):
        """Thiết lập giao diện ban đầu"""
        self.gradeButton.setEnabled(False)
        self.answersLineEdit.setEnabled(False)
        self.resultsTextEdit.clear()
        self.questionsTextEdit.clear()
    
    def set_user(self, user):
        """Thiết lập người dùng hiện tại"""
        self.current_user = user
        self.userLabel.setText(f"Đã đăng nhập: {user.username}")
    
    def generate_questions_action(self):
        """Tạo câu hỏi từ AI"""
        if not self.current_user:
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập trước!")
            return
        
        content = self.inputTextEdit.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung để tạo câu hỏi!")
            return
        
        num_questions = self.numQuestionsSpinBox.value()
        
        # Hiển thị loading
        self.generateButton.setText("Đang tạo...")
        self.generateButton.setEnabled(False)
        QApplication.processEvents()
        
        try:
            # Gọi AI để tạo câu hỏi
            questions = generate_questions(content, num_questions)
            
            if questions and not questions.startswith("Lỗi"):
                self.current_questions = questions
                self.questionsTextEdit.setPlainText(questions)
                
                # Kích hoạt phần nhập đáp án
                self.gradeButton.setEnabled(True)
                self.answersLineEdit.setEnabled(True)
                self.answersLineEdit.clear()
                self.resultsTextEdit.clear()
                
                QMessageBox.information(self, "Thành công", "Đã tạo câu hỏi thành công!")
            else:
                QMessageBox.warning(self, "Lỗi", f"Không thể tạo câu hỏi: {questions}")
        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {str(e)}")
        
        finally:
            # Khôi phục nút
            self.generateButton.setText("Tạo Câu Hỏi")
            self.generateButton.setEnabled(True)
    
    def grade_answers_action(self):
        """Chấm điểm đáp án"""
        if not self.current_user:
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập trước!")
            return
        
        if not self.current_questions:
            QMessageBox.warning(self, "Lỗi", "Vui lòng tạo câu hỏi trước!")
            return
        
        user_answers = self.answersLineEdit.text().strip()
        if not user_answers:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đáp án!")
            return
        
        # Hiển thị loading
        self.gradeButton.setText("Đang chấm...")
        self.gradeButton.setEnabled(False)
        QApplication.processEvents()
        
        try:
            # Gọi AI để chấm điểm
            result = grade_answers(self.current_questions, user_answers)
            
            if result and not result.startswith("Lỗi"):
                self.resultsTextEdit.setPlainText(result)
                
                # Lưu phiên thi
                quiz_session = QuizSession(
                    user_id=self.current_user.username,
                    questions=self.current_questions,
                    answers=user_answers,
                    score=result
                )
                save_quiz_session(quiz_session)
                
                QMessageBox.information(self, "Thành công", "Đã chấm điểm và lưu kết quả!")
            else:
                QMessageBox.warning(self, "Lỗi", f"Không thể chấm điểm: {result}")
        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {str(e)}")
        
        finally:
            # Khôi phục nút
            self.gradeButton.setText("Chấm Điểm")
            self.gradeButton.setEnabled(True)
    
    def logout(self):
        """Đăng xuất"""
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn đăng xuất?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.current_questions = ""
            self.userLabel.setText("Chưa đăng nhập")
            
            # Xóa nội dung và vô hiệu hóa các tính năng
            self.inputTextEdit.clear()
            self.questionsTextEdit.clear()
            self.answersLineEdit.clear()
            self.resultsTextEdit.clear()
            self.gradeButton.setEnabled(False)
            self.answersLineEdit.setEnabled(False)
            
            login_window = DangNhap()
            login_window.show()
            self.hide()

app = QApplication(sys.argv)
        
main_window = Main()
login_window = DangNhap()
register_window = DangKy()

login_window.show()

sys.exit(app.exec())