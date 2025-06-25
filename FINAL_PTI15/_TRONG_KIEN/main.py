import sys
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QButtonGroup
import data

LOGIN_FILE = os.path.join(os.path.dirname(__file__), "ui", "login.ui")
REGISTER_FILE = os.path.join(os.path.dirname(__file__), "ui", "register.ui")
MAIN_FILE = os.path.join(os.path.dirname(__file__), "ui", "main.ui")

class LoginWindow(QMainWindow):
    """Cửa sổ đăng nhập"""
    def __init__(self):
        super().__init__()
        
        # Load UI trực tiếp vào QMainWindow
        uic.loadUi(LOGIN_FILE, self)
        
        # Kết nối signals với slots
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_register.clicked.connect(self.show_register)
        
        # Biến lưu thông tin user hiện tại
        self.current_user = None
        self.register_window = None
    
    def login(self):
        """Xử lý đăng nhập"""
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        
        if not username or not password:
            self.label_message.setText("Vui lòng nhập đầy đủ thông tin!")
            return
        
        success, message = data.login_user(username, password)
        
        if success:
            self.current_user = data.find_user(username)
            # Mở cửa sổ chính
            self.main_window = MainWindow(self.current_user)
            self.main_window.show()
            self.close()  # Đóng cửa sổ đăng nhập
        else:
            self.label_message.setText(message)
    
    def show_register(self):
        """Hiển thị cửa sổ đăng ký"""
        if self.register_window is None:
            self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()  # Ẩn cửa sổ đăng nhập

class RegisterWindow(QMainWindow):
    """Cửa sổ đăng ký"""
    def __init__(self, login_window):
        super().__init__()
        
        # Load UI trực tiếp vào QMainWindow
        uic.loadUi(REGISTER_FILE, self)
        
        # Lưu reference đến login window
        self.login_window = login_window
        
        # Kết nối signals với slots
        self.pushButton_register.clicked.connect(self.register)
        self.pushButton_cancel.clicked.connect(self.cancel)
    
    def register(self):
        """Xử lý đăng ký"""
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        confirm_password = self.lineEdit_confirm_password.text().strip()
        
        if not username or not password or not confirm_password:
            self.label_message.setText("Vui lòng nhập đầy đủ thông tin!")
            return
        
        if password != confirm_password:
            self.label_message.setText("Mật khẩu xác nhận không khớp!")
            return
        
        if len(password) < 3:
            self.label_message.setText("Mật khẩu phải có ít nhất 3 ký tự!")
            return
        
        success, message = data.register_user(username, password)
        
        if success:
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bạn có thể đăng nhập.")
            self.close()  # Đóng cửa sổ đăng ký
            self.login_window.show()  # Hiển thị lại cửa sổ đăng nhập
        else:
            self.label_message.setText(message)
    
    def cancel(self):
        """Hủy đăng ký và quay về cửa sổ đăng nhập"""
        self.close()
        self.login_window.show()

class MainWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng"""
    def __init__(self, user_info):
        super().__init__()
        # Load UI từ file
        uic.loadUi(MAIN_FILE, self)
        
        # Thông tin user hiện tại
        self.current_user = user_info
        self.questions = []
        self.current_question_index = 0
        self.user_answers = {}
        
        # Hiển thị thông tin user
        self.update_user_info()
        
        # Ẩn group câu hỏi ban đầu
        self.groupBox_question.setVisible(False)
        
        # Tạo button group cho radio buttons
        self.answer_group = QButtonGroup()
        self.answer_group.addButton(self.radioButton_option1, 0)
        self.answer_group.addButton(self.radioButton_option2, 1)
        self.answer_group.addButton(self.radioButton_option3, 2)
        self.answer_group.addButton(self.radioButton_option4, 3)
        
        # Kết nối signals với slots
        self.pushButton_start_test.clicked.connect(self.start_test)
        self.pushButton_next.clicked.connect(self.next_question)
        self.pushButton_previous.clicked.connect(self.previous_question)
        self.pushButton_submit.clicked.connect(self.submit_test)
        self.pushButton_logout.clicked.connect(self.logout)
        
        # Kết nối signal cho việc chọn đáp án
        self.answer_group.buttonClicked.connect(self.save_answer)
    
    def update_user_info(self):
        """Cập nhật thông tin user trên giao diện"""
        self.label_user_info.setText(f"Người dùng: {self.current_user['username']}")
        self.label_highest_score.setText(f"Điểm cao nhất: {self.current_user['highest_score']}")
    
    def start_test(self):
        """Bắt đầu bài kiểm tra"""
        # Load câu hỏi từ file
        self.questions = data.load_questions()
        
        if not self.questions:
            QMessageBox.warning(self, "Lỗi", "Không thể tải câu hỏi!")
            return
        
        # Reset dữ liệu
        self.current_question_index = 0
        self.user_answers = {}
        
        # Hiển thị group câu hỏi và ẩn nút bắt đầu
        self.groupBox_question.setVisible(True)
        self.pushButton_start_test.setVisible(False)
        
        # Hiển thị câu hỏi đầu tiên
        self.display_question()
    
    def display_question(self):
        """Hiển thị câu hỏi hiện tại"""
        if not self.questions:
            return
        
        question = self.questions[self.current_question_index]
        
        # Cập nhật số câu hỏi
        self.label_question_number.setText(f"Câu {self.current_question_index + 1}/{len(self.questions)}:")
        
        # Hiển thị câu hỏi
        self.label_question.setText(question['question'])
        
        # Hiển thị các đáp án
        options = question['options']
        self.radioButton_option1.setText(f"A. {options[0]}")
        self.radioButton_option2.setText(f"B. {options[1]}")
        self.radioButton_option3.setText(f"C. {options[2]}")
        self.radioButton_option4.setText(f"D. {options[3]}")
        
        # Xóa lựa chọn trước đó
        self.answer_group.setExclusive(False)
        for button in self.answer_group.buttons():
            button.setChecked(False)
        self.answer_group.setExclusive(True)
        
        # Hiển thị đáp án đã chọn trước đó (nếu có)
        if self.current_question_index in self.user_answers:
            answer_index = self.user_answers[self.current_question_index]
            self.answer_group.button(answer_index).setChecked(True)
        
        # Cập nhật trạng thái các nút
        self.pushButton_previous.setEnabled(self.current_question_index > 0)
        self.pushButton_next.setEnabled(self.current_question_index < len(self.questions) - 1)
    
    def save_answer(self, button):
        """Lưu đáp án người dùng chọn"""
        answer_index = self.answer_group.id(button)
        self.user_answers[self.current_question_index] = answer_index
    
    def next_question(self):
        """Chuyển đến câu hỏi tiếp theo"""
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question()
    
    def previous_question(self):
        """Quay lại câu hỏi trước"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question()
    
    def submit_test(self):
        """Nộp bài và tính điểm"""
        # Kiểm tra xem đã trả lời hết câu hỏi chưa
        if len(self.user_answers) < len(self.questions):
            reply = QMessageBox.question(self, "Xác nhận", 
                                       f"Bạn chỉ trả lời {len(self.user_answers)}/{len(self.questions)} câu hỏi.\n"
                                       "Bạn có muốn nộp bài không?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        
        # Tính điểm
        score = 0
        for i, question in enumerate(self.questions):
            if i in self.user_answers:
                if self.user_answers[i] == question['correct_answer']:
                    score += 1
        
        # Hiển thị kết quả
        QMessageBox.information(self, "Kết quả", 
                              f"Bạn đã trả lời đúng {score}/{len(self.questions)} câu hỏi.\n"
                              f"Điểm số: {score}")
        
        # Cập nhật điểm cao nhất
        if score > self.current_user['highest_score']:
            data.update_highest_score(self.current_user['username'], score)
            self.current_user['highest_score'] = score
            self.update_user_info()
            QMessageBox.information(self, "Chúc mừng!", "Bạn đã lập kỷ lục mới!")
        
        # Reset về trạng thái ban đầu
        self.reset_test()
    
    def reset_test(self):
        """Reset về trạng thái ban đầu"""
        self.groupBox_question.setVisible(False)
        self.pushButton_start_test.setVisible(True)
        self.current_question_index = 0
        self.user_answers = {}
    
    def logout(self):
        """Đăng xuất"""
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có muốn đăng xuất không?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

app = QApplication(sys.argv)
# Hiển thị cửa sổ đăng nhập
login_window = LoginWindow()
login_window.show()
sys.exit(app.exec())


