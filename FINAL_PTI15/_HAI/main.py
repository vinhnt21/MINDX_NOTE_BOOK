# main.py - Ứng dụng chính tóm tắt tài liệu DOCX
# Ứng dụng này cho phép người dùng đăng ký, đăng nhập và tóm tắt tài liệu DOCX

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import uic
import sys
import os
import docx  # Để đọc file DOCX
from data import load_data, save_data, find_user
from models import User
from ai import summarize_text

# Đường dẫn tới các file giao diện
UI_FILE_1 = os.path.join(os.path.dirname(__file__), "ui/main.ui")
UI_FILE_2 = os.path.join(os.path.dirname(__file__), "ui/dangki.ui")
UI_FILE_3 = os.path.join(os.path.dirname(__file__), "ui/dangnhap.ui")

class MainWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng"""
    
    def __init__(self, current_user=None):
        super().__init__()
        # Load UI
        uic.loadUi(UI_FILE_1, self)
        
        # Khởi tạo biến cần thiết
        self.current_user = current_user
        self.users = load_data()
        self.current_file_path = ""
        self.current_document_text = ""
        self.current_summary = ""
        
        # Thiết lập tiêu đề
        if self.current_user:
            self.setWindowTitle(f"Tóm Tắt DOCX - Xin chào {self.current_user.username}")
        else:
            self.setWindowTitle("Tóm Tắt DOCX - Hỗ Trợ Bởi Gemini AI")
        
        # Connect signals
        self.btn_browse.clicked.connect(self.browse_file)
        self.btn_summarize.clicked.connect(self.summarize_document)
        self.btn_copy_summary.clicked.connect(self.copy_summary)
        self.btn_save_summary.clicked.connect(self.save_summary_to_file)
    
    def browse_file(self):
        """Mở hộp thoại chọn file DOCX"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Chọn file DOCX",
                "",
                "Word Documents (*.docx);;All Files (*)"
            )
            
            if file_path:
                self.current_file_path = file_path
                # Hiển thị đường dẫn file đã chọn
                self.lineEdit_filePath.setText(file_path)
                
                # Đọc nội dung file
                self.read_docx_file(file_path)
                
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể mở file: {str(e)}")
    
    def read_docx_file(self, file_path):
        """Đọc nội dung file DOCX"""
        try:
            # Mở file DOCX
            doc = docx.Document(file_path)
            
            # Đọc tất cả đoạn văn
            text_content = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():  # Chỉ lấy đoạn văn có nội dung
                    text_content.append(paragraph.text.strip())
            
            # Nối tất cả đoạn văn thành một chuỗi
            self.current_document_text = "\n".join(text_content)
            
            # Hiển thị văn bản gốc trong tab
            self.textEdit_original.setPlainText(self.current_document_text)
            
            if self.current_document_text:
                QMessageBox.information(
                    self, 
                    "Thành công", 
                    f"Đã đọc file thành công!\nSố ký tự: {len(self.current_document_text)}"
                )
            else:
                QMessageBox.warning(self, "Cảnh báo", "File không có nội dung văn bản!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc file DOCX: {str(e)}")
    
    def summarize_document(self):
        """Tóm tắt tài liệu"""
        try:
            # Kiểm tra xem đã chọn file chưa
            if not self.current_document_text:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file DOCX trước!")
                return
            
            # Lấy thông tin từ giao diện
            length = "Trung bình"  # Mặc định
            format_type = "Đoạn Văn"  # Mặc định
            
            length = self.comboBox_length.currentText()
            format_type = self.comboBox_format.currentText()
            
            # Hiển thị thông báo đang xử lý
            progress_dialog = QProgressDialog("Đang tóm tắt tài liệu...", "Hủy", 0, 0, self)
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.show()
            
            # Tóm tắt văn bản
            QApplication.processEvents()  # Cập nhật giao diện
            summary = summarize_text(self.current_document_text, length, format_type)
            
            progress_dialog.close()
            
            # Hiển thị kết quả
            if summary:
                self.current_summary = summary
                # Hiển thị tóm tắt trong tab thay vì dialog
                self.textEdit_summary.setPlainText(summary)
                
                # Chuyển sang tab tóm tắt
                self.tabWidget.setCurrentIndex(0)  # Tab đầu tiên là tóm tắt
                
                QMessageBox.information(self, "Thành công", "Tóm tắt hoàn thành!")
                
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể tóm tắt tài liệu!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tóm tắt: {str(e)}")
    
    def copy_summary(self):
        """Sao chép nội dung tóm tắt vào clipboard"""
        try:
            if not self.current_summary:
                QMessageBox.warning(self, "Cảnh báo", "Chưa có nội dung tóm tắt để sao chép!")
                return
            
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_summary)
            QMessageBox.information(self, "Thành công", "Đã sao chép nội dung tóm tắt!")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi sao chép: {str(e)}")
    
    def save_summary_to_file(self):
        """Lưu nội dung tóm tắt ra file"""
        try:
            if not self.current_summary:
                QMessageBox.warning(self, "Cảnh báo", "Chưa có nội dung tóm tắt để lưu!")
                return
            
            # Mở hộp thoại lưu file
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Lưu tóm tắt",
                "tom_tat.txt",
                "Text Files (*.txt);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.current_summary)
                
                QMessageBox.information(self, "Thành công", f"Đã lưu tóm tắt vào file: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu file: {str(e)}")

class DangKy(QMainWindow):
    """Cửa sổ đăng ký tài khoản"""
    
    def __init__(self):
        super().__init__()
        # Load UI
        uic.loadUi(UI_FILE_2, self)
        self.setWindowTitle("Đăng Ký Tài Khoản")
        
        # Connect signals
        self.registerButton.clicked.connect(self.register_user)
    
    def register_user(self):
        """Đăng ký người dùng mới"""
        try:
            # Lấy thông tin từ giao diện
            username = self.usernameLineEdit.text().strip()
            password = self.passwordLineEdit.text()
            confirm_password = self.verifyPasswordLineEdit.text()
            
            # Kiểm tra thông tin
            if not username or not password or not confirm_password:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
                return
            
            if password != confirm_password:
                QMessageBox.warning(self, "Cảnh báo", "Mật khẩu xác nhận không khớp!")
                return
            
            if len(password) < 6:
                QMessageBox.warning(self, "Cảnh báo", "Mật khẩu phải có ít nhất 6 ký tự!")
                return
            
            # Kiểm tra tên đăng nhập đã tồn tại
            users = load_data()
            if find_user(username, users):
                QMessageBox.warning(self, "Cảnh báo", "Tên đăng nhập đã tồn tại!")
                return
            
            # Tạo user mới
            new_user = User(username, password)
            users.append(new_user)
            
            # Lưu dữ liệu
            save_data(users)
            
            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
            
            # Chuyển sang đăng nhập
            self.open_login()
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi đăng ký: {str(e)}")
    
    def open_login(self):
        """Mở cửa sổ đăng nhập"""
        self.hide()
        self.login_window = DangNhap()
        self.login_window.show()

class DangNhap(QMainWindow):
    """Cửa sổ đăng nhập"""
    
    def __init__(self):
        super().__init__()
        # Load UI
        uic.loadUi(UI_FILE_3, self)
        self.setWindowTitle("Đăng Nhập")
        
        # Connect signals
        self.loginButton.clicked.connect(self.login_user)
        self.registerButton.clicked.connect(self.open_register)

    def login_user(self):
        """Đăng nhập người dùng"""
        try:
            # Lấy thông tin từ giao diện
            username = self.usernameLineEdit.text().strip()
            password = self.passwordLineEdit.text()
            
            # Kiểm tra thông tin
            if not username or not password:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
                return
            
            # Tìm user trong dữ liệu
            users = load_data()
            user = find_user(username, users)
            
            if not user:
                QMessageBox.warning(self, "Cảnh báo", "Tên đăng nhập không tồn tại!")
                return
            
            if user.password != password:
                QMessageBox.warning(self, "Cảnh báo", "Mật khẩu không đúng!")
                return
            
            # Đăng nhập thành công
            QMessageBox.information(self, "Thành công", f"Chào mừng {username}!")
            
            # Mở ứng dụng chính
            self.login_success(user)
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi đăng nhập: {str(e)}")
    
    def login_success(self, user):
        """Khi đăng nhập thành công"""
        self.hide()
        self.main_window = MainWindow(current_user=user)
        self.main_window.show()
    
    def open_register(self):
        """Mở cửa sổ đăng ký"""
        self.hide()
        self.register_window = DangKy()
        self.register_window.show()

app = QApplication(sys.argv)
login_window = DangNhap()
login_window.show()
sys.exit(app.exec())