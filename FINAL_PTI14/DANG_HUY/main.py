from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap  # Import thêm QPixmap
from PyQt6 import uic
import sys
import os
from ai import generate_content, csv_to_excel
from data import load_users, save_users
from model import User

users = load_users()

DANGKI_UI_FILE = os.path.join(os.path.dirname(__file__),"ui" ,"dangki.ui")
DANGNHAP_UI_FILE = os.path.join(os.path.dirname(__file__),"ui" ,"dangnhap.ui")
MAIN_UI_FILE = os.path.join(os.path.dirname(__file__),"ui" ,"main.ui")
BG_IMAGE_FILE = os.path.join(os.path.dirname(__file__),"ui" ,"images/bg.jpg")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(MAIN_UI_FILE, self)
        self.setWindowTitle("Question Generator")
        self.generateButton.clicked.connect(self.create_excel_file)
        self.titleLabel.setText("Tạo Câu hỏi Tự động bằng AI")
        
    def create_excel_file(self):
        # tạo câu hỏi dưới dạng csv
        topic = self.topicLineEdit.text()
        content = self.contentTextEdit.toPlainText()
        
        if not topic or not content:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập cả chủ đề và nội dung.")
            return
        QMessageBox.information(self, "Thông báo", "Đang tạo câu hỏi, đại ca đợi em tí nhé")
        csv_content = generate_content(topic, content)
        
        # tạo file excel
        output_filename = self.outputFileNameLineEdit.text()
        output_filename = os.path.join(os.path.dirname(__file__), "output", output_filename)
        csv_to_excel(csv_content, output_filename)
        # self.titleLabel.setText("Tạo Câu hỏi Tự động bằng AI")
        QMessageBox.information(self, "Thành công", f"File excel đã được tạo thành công: {output_filename}")
        
        
        
        
        
        
       
class DangKi(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(DANGKI_UI_FILE, self)
        self.setWindowTitle("Đăng Kí")
        
        # --- THÊM CODE TẢI ẢNH VÀO ĐÂY ---
        # 1. Tạo một đối tượng QPixmap từ đường dẫn file
        pixmap = QPixmap(BG_IMAGE_FILE)  # Đường dẫn tương đối đến ảnh
        # 2. Tìm QLabel trong UI (tên là imageLabel trong file .ui tôi đã gửi)
        # 3. Đặt pixmap cho QLabel đó
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setFixedSize(400, 400)
        
        self.imageLabel.setScaledContents(True)
        
        self.pushButton.clicked.connect(self.open_dangnhap)
        self.registerButton.clicked.connect(self.dang_ki)
        
    def open_dangnhap(self):
        dangnhap.show()
        self.close()
    
    def dang_ki(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirm_password = self.confirmPasswordLineEdit.text()
        
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Cảnh báo", "Mật khẩu không khớp.")
            return
        for user in users:
            if user.username == username:
                QMessageBox.warning(self, "Cảnh báo", "Tên đăng nhập đã tồn tại.")
                return
        users.append(User(username, password))
        save_users(users)
        QMessageBox.information(self, "Thành công", "Đăng kí thành công.")
        self.close()
        dangnhap.show()
    
    
class DangNhap(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(DANGNHAP_UI_FILE, self)
        self.setWindowTitle("Đăng Nhập")
        
        # --- THÊM CODE TẢI ẢNH VÀO ĐÂY ---
        pixmap = QPixmap(BG_IMAGE_FILE)
        self.imageLabel.setPixmap(pixmap)
        # set fixed size cho imageLabel
        self.imageLabel.setFixedSize(400, 400)
        # (Tùy chọn) Để ảnh co giãn theo kích thước của Label
        self.imageLabel.setScaledContents(True)
        
        self.pushButton.clicked.connect(self.open_dangki)
        self.loginButton.clicked.connect(self.dang_nhap)
    
    def open_dangki(self):
        dangki.show()
        self.close()

    def dang_nhap(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if not username or not password:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return
        for user in users:
            if user.username == username and user.password == password:
                main.show()
                self.close()
                return
        QMessageBox.warning(self, "Cảnh báo", "Tên đăng nhập hoặc mật khẩu không đúng.")
        
        
        
        
       

app = QApplication(sys.argv)
main = MainWindow()
dangki = DangKi()
dangnhap = DangNhap()
dangnhap.show()
sys.exit(app.exec())