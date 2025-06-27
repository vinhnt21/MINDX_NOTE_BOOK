from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap  # Import thêm QPixmap
from PyQt6 import uic
import sys

# Không cần import resources_rc.py nữa nếu bạn dùng cách này

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/main.ui", self)
        self.setWindowTitle("Question Generator")
       
class DangKi(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/dangki.ui", self)
        self.setWindowTitle("Đăng Kí")
        
        # --- THÊM CODE TẢI ẢNH VÀO ĐÂY ---
        # 1. Tạo một đối tượng QPixmap từ đường dẫn file
        pixmap = QPixmap("./ui/images/bg.jpg")  # Đường dẫn tương đối đến ảnh
    
        # 2. Tìm QLabel trong UI (tên là imageLabel trong file .ui tôi đã gửi)
        # 3. Đặt pixmap cho QLabel đó
        self.imageLabel.setPixmap(pixmap)
        
class DangNhap(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/dangnhap.ui", self)
        self.setWindowTitle("Đăng Nhập")
        
        # --- THÊM CODE TẢI ẢNH VÀO ĐÂY ---
        pixmap = QPixmap("./ui/images/bg.jpg")
        self.imageLabel.setPixmap(pixmap)
        
        # (Tùy chọn) Để ảnh co giãn theo kích thước của Label
        # self.imageLabel.setScaledContents(True)

app = QApplication(sys.argv)
main = MainWindow()
dangki = DangKi()
dangnhap = DangNhap()
main.show()
dangki.show()
dangnhap.show()
sys.exit(app.exec())