from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import uic
import sys
import os
from data import load_data, save_data, find_user
from models import User
from ai import create_outline

# Đường dẫn tới các file giao diện
UI_LOGIN_FILE = os.path.join(os.path.dirname(__file__), "ui/login.ui")
UI_MAIN_FILE = os.path.join(os.path.dirname(__file__), "ui/main.ui")

class MainWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng"""
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_MAIN_FILE, self)
        
        self.topic_input.setPlaceholderText("Nhập chủ đề bạn muốn tạo dàn ý...")
        self.outputTitleLabel.setText("Dàn ý sẽ hiển thị ở đây")
        
        self.generate_button.clicked.connect(self.generate_outline)
        self.logout_button.clicked.connect(self.logout)
    
    def generate_outline(self):
        """Tạo dàn ý từ chủ đề nhập vào"""
        topic = self.topic_input.toPlainText().strip()
        
        if not topic:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập chủ đề để tạo dàn ý!")
            return
        
        self.outputTitleLabel.setText("Đang tạo dàn ý...")
        
        self.generate_button.setEnabled(False)
        self.generate_button.setText("Đang xử lý...")

        try:
            outline = create_outline(topic)
            
            # Hiển thị kết quả
            self.result_output.setPlainText(outline)
            
            # Cập nhật tiêu đề
            self.outputTitleLabel.setText(f"Dàn ý cho chủ đề: {topic}")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi tạo dàn ý: {str(e)}")
        
        finally:
            # Khôi phục nút
            self.generate_button.setEnabled(True)
            self.generate_button.setText("Tạo Dàn Ý")
    
    def logout(self):
        """Đăng xuất và quay về màn hình đăng nhập"""
        reply = QMessageBox.question(
            self, 
            "Xác nhận", 
            "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            # Hiển thị lại cửa sổ đăng nhập
            login_window = LoginWindow()
            login_window.show()

class LoginWindow(QMainWindow):
    """Cửa sổ đăng nhập và đăng ký"""
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_LOGIN_FILE, self)
        
        # Tải dữ liệu người dùng
        self.users = load_data()
        
        # Thiết lập giao diện ban đầu
        self.stackedWidget.setCurrentIndex(0)
        
        
        # Kết nối các sự kiện

        
        # Nút đăng nhập
        self.login_button.clicked.connect(self.handle_login)
        
        # Nút đăng ký
        self.register_button.clicked.connect(self.handle_register)
        
        # Nút chuyển đổi giữa đăng nhập và đăng ký
        self.switchToRegisterButton.clicked.connect(self.switch_to_register)
        
        self.switchToLoginButton.clicked.connect(self.switch_to_login)
        
        # Enter để đăng nhập
        self.login_password_input.returnPressed.connect(self.handle_login)
    
    def switch_to_register(self):
        """Chuyển sang trang đăng ký"""
        self.stackedWidget.setCurrentIndex(1)
    
    def switch_to_login(self):
        """Chuyển sang trang đăng nhập"""
        self.stackedWidget.setCurrentIndex(0)
    
    def handle_login(self):
        """Xử lý đăng nhập"""
        # Lấy thông tin đăng nhập
        username = self.login_username_input.text().strip()
        password = self.login_password_input.text()
        
        # Kiểm tra thông tin nhập vào
        if not username or not password:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return
        
        # Tìm người dùng trong cơ sở dữ liệu
        user = find_user(username, self.users)
        
        if user and user.password == password:
            # Đăng nhập thành công
            QMessageBox.information(self, "Thành công", f"Chào mừng {username}!")
            
            # Mở cửa sổ chính
            self.main_window = MainWindow()
            self.main_window.show()
            
            # Đóng cửa sổ đăng nhập
            self.close()
        else:
            # Đăng nhập thất bại
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
            # Xóa mật khẩu
            self.login_password_input.clear()
    
    def handle_register(self):
        """Xử lý đăng ký"""
        # Lấy thông tin đăng ký
        username = self.register_username_input.text().strip()
        password = self.register_password_input.text()
        confirm_password = self.register_confirm_password_input.text()
        
        # Kiểm tra thông tin nhập vào
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra độ dài tên đăng nhập
        if len(username) < 3:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập phải có ít nhất 3 ký tự!")
            return
        
        # Kiểm tra độ dài mật khẩu
        if len(password) < 6:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        
        # Kiểm tra mật khẩu khớp nhau
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        # Kiểm tra tên đăng nhập đã tồn tại chưa
        if find_user(username, self.users):
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại!")
            return
        
        # Tạo người dùng mới
        new_user = User(username, password)
        self.users.append(new_user)
        
        # Lưu vào file
        save_data(self.users)
        
        # Thông báo thành công
        QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.")
        
        # Xóa form đăng ký
        self.register_username_input.clear()
        self.register_password_input.clear()
        self.register_confirm_password_input.clear()
        
        # Chuyển về tab đăng nhập
        self.switch_to_login()
        
        
        
app = QApplication(sys.argv)
app.setApplicationName("Ứng Dụng Tạo Dàn Ý")
login_window = LoginWindow()
login_window.show()
    
sys.exit(app.exec())