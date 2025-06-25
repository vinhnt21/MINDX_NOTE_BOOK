# models.py - Định nghĩa các lớp dữ liệu
# Lớp này dùng để lưu trữ thông tin về người dùng

class User:
    """Lớp User đại diện cho một người dùng"""
    def __init__(self, username, password):
        self.username = username    # Tên đăng nhập
        self.password = password    # Mật khẩu
