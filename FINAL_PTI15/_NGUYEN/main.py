import sys
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QScrollArea, QFrame, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6 import uic
import data
import os

# Đường dẫn file UI
LOGIN_UI = os.path.join(os.path.dirname(__file__), 'ui', 'dangnhap.ui')
REGISTER_UI = os.path.join(os.path.dirname(__file__), 'ui', 'dangky.ui')
MAIN_UI = os.path.join(os.path.dirname(__file__), 'ui', 'main.ui')


class LoginWindow(QMainWindow):
    """Cửa sổ đăng nhập"""
    
    def __init__(self):
        super().__init__()
        # Load UI từ file
        uic.loadUi(LOGIN_UI, self)
    
        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.open_register)
    
    def login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        success, message = data.login_user(username, password)
        
        if success:
            QMessageBox.information(self, "Thành công", message)
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Lỗi", message)
    
    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
    
    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

class RegisterWindow(QMainWindow):
    """Cửa sổ đăng ký"""
    
    def __init__(self):
        super().__init__()
        # Load UI từ file
        uic.loadUi(REGISTER_UI, self)
    
        self.register_btn.clicked.connect(self.register)
        self.back_btn.clicked.connect(self.back_to_login)
    
    def register(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        confirm_password = self.confirm_password_edit.text().strip()
        
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return
        
        success, message = data.register_user(username, password)
        
        if success:
            QMessageBox.information(self, "Thành công", message)
            self.back_to_login()
        else:
            QMessageBox.warning(self, "Lỗi", message)
    
    def back_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class MainWindow(QMainWindow):
    """Cửa sổ chính hiển thị danh sách game"""
    
    def __init__(self):
        super().__init__()

        uic.loadUi(MAIN_UI, self)
        self.logout_btn.clicked.connect(self.logout)
        self.load_games()
        
        
    def load_games(self):
        games = data.load_games()
        if not games:
            no_games = QLabel("Không có game nào để hiển thị!")
            no_games.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_games.setFont(QFont("Arial", 16))
            no_games.setStyleSheet("color: #7f8c8d; margin: 50px;")
            self.games_layout.addWidget(no_games)
            return
        
        for game in games:
            self.create_game_card(game)
    
    def create_game_card(self, game):
        # Frame cho mỗi game
        game_frame = QFrame()
        game_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                margin: 10px;
                padding: 20px;
            }
            QFrame:hover {
                background-color: #f8f9fa;
            }
        """)
        game_frame.setFrameStyle(QFrame.Shape.Box)
        
        # Layout cho game card
        card_layout = QHBoxLayout()
        game_frame.setLayout(card_layout)
        
        # Thông tin game
        info_layout = QVBoxLayout()
        
        # Tên game
        name_label = QLabel(game.name)
        name_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        info_layout.addWidget(name_label)
        
        # Giá
        price_label = QLabel(f"Giá: {game.price}")
        price_label.setFont(QFont("Arial", 14))
        price_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        info_layout.addWidget(price_label)
        
        # Mô tả
        desc_text = QTextEdit()
        desc_text.setPlainText(game.description)
        desc_text.setMaximumHeight(80)
        desc_text.setReadOnly(True)
        desc_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                background-color: #f8f9fa;
            }
        """)
        info_layout.addWidget(desc_text)
        
        card_layout.addLayout(info_layout)
        
        # Button để mở website
        open_btn = QPushButton("Xem chi tiết")
        open_btn.clicked.connect(lambda: self.open_game_website(game.url))
        open_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 25px;
                font-size: 14px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        card_layout.addWidget(open_btn)
        
        self.games_layout.addWidget(game_frame)
    
    def open_game_website(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể mở trang web: {str(e)}")
    
    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    
    # Thiết lập font mặc định
    app.setStyleSheet("""
        QApplication {
            font-family: Arial, sans-serif;
        }
    """)
    

    
    login_window = LoginWindow()
    login_window.show()
  
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
