# models.py - Định nghĩa các lớp dữ liệu đơn giản

class Task:
    """Lớp Task - mô tả một công việc"""
    def __init__(self, ten_task, han_chot, trang_thai="Chưa xong"):
        self.ten_task = ten_task        # Tên công việc
        self.han_chot = han_chot        # Ngày hết hạn
        self.trang_thai = trang_thai    # "Chưa xong" hoặc "Xong rồi"

class User:
    """Lớp User - mô tả một người dùng"""
    def __init__(self, ten_dang_nhap, mat_khau):
        self.ten_dang_nhap = ten_dang_nhap  # Tên đăng nhập
        self.mat_khau = mat_khau            # Mật khẩu
        self.danh_sach_task = []            # Danh sách các task
        