# main.py - Chương trình chính đơn giản

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import os
import sys

# Import các file data và models
from data import tai_du_lieu, luu_du_lieu, kiem_tra_dang_nhap, tim_user
from models import User, Task

# Đường dẫn đến các file UI
UI_DANG_NHAP = os.path.join(os.path.dirname(__file__), 'ui', 'DangNhap.ui')
UI_DANG_KY = os.path.join(os.path.dirname(__file__), 'ui', 'DangKy.ui')
UI_CHINH = os.path.join(os.path.dirname(__file__), 'ui', 'MAIN.ui')

class CuaSoDangNhap(QMainWindow):
    """Cửa sổ đăng nhập đơn giản"""
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_DANG_NHAP, self)
        
        # Đọc dữ liệu
        self.danh_sach_user = tai_du_lieu()
        
        # Kết nối các nút với hàm xử lý
        self.btn_login.clicked.connect(self.xu_ly_dang_nhap)
        self.btn_register.clicked.connect(self.mo_cua_so_dang_ky)
    
    def xu_ly_dang_nhap(self):
        """Xử lý khi nhấn nút đăng nhập"""
        # Lấy thông tin từ form
        ten_dang_nhap = self.lineEdit_username.text()
        mat_khau = self.lineEdit_password.text()
        
        # Kiểm tra rỗng
        if not ten_dang_nhap or not mat_khau:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra đăng nhập
        user = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau, self.danh_sach_user)
        if user:
            # Đăng nhập thành công
            self.hide()  # Ẩn cửa sổ đăng nhập
            self.cua_so_chinh = CuaSoChinh(user, self.danh_sach_user)
            self.cua_so_chinh.show()
        else:
            # Đăng nhập thất bại
            QMessageBox.warning(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
            self.lineEdit_password.clear()
    
    def mo_cua_so_dang_ky(self):
        """Mở cửa sổ đăng ký"""
        self.cua_so_dang_ky = CuaSoDangKy(self)
        self.cua_so_dang_ky.show()

class CuaSoDangKy(QMainWindow):
    """Cửa sổ đăng ký đơn giản"""
    def __init__(self, cua_so_cha):
        super().__init__()
        uic.loadUi(UI_DANG_KY, self)
        self.cua_so_cha = cua_so_cha  # Lưu tham chiếu đến cửa sổ đăng nhập
        
        # Kết nối các nút
        self.btn_register.clicked.connect(self.xu_ly_dang_ky)
        self.btn_back.clicked.connect(self.dong_cua_so)
    
    def xu_ly_dang_ky(self):
        """Xử lý khi nhấn nút đăng ký"""
        # Lấy thông tin từ form
        ten_dang_nhap = self.lineEdit_username.text()
        mat_khau = self.lineEdit_password.text()
        xac_nhan_mk = self.lineEdit_confirm.text()
        
        # Kiểm tra rỗng
        if not ten_dang_nhap or not mat_khau or not xac_nhan_mk:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra mật khẩu khớp
        if mat_khau != xac_nhan_mk:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        
        # Kiểm tra user đã tồn tại chưa
        if tim_user(ten_dang_nhap, self.cua_so_cha.danh_sach_user):
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại!")
            return
        
        # Tạo user mới
        user_moi = User(ten_dang_nhap, mat_khau)
        self.cua_so_cha.danh_sach_user.append(user_moi)
        
        # Lưu dữ liệu
        if luu_du_lieu(self.cua_so_cha.danh_sach_user):
            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
            self.dong_cua_so()
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể lưu dữ liệu!")
    
    def dong_cua_so(self):
        """Đóng cửa sổ đăng ký"""
        self.close()

class CuaSoChinh(QMainWindow):
    """Cửa sổ chính quản lý task"""
    def __init__(self, user, danh_sach_user):
        super().__init__()
        uic.loadUi(UI_CHINH, self)
        
        # Lưu thông tin
        self.user_hien_tai = user
        self.danh_sach_user = danh_sach_user
        
        # Thiết lập giao diện
        self.label_user.setText(f"Xin chào: {user.ten_dang_nhap}")
        
        # Kết nối các nút với hàm xử lý
        self.btn_dang_xuat.clicked.connect(self.dang_xuat)
        self.btn_them_task.clicked.connect(self.them_task)
        self.btn_sua_task.clicked.connect(self.sua_task)
        self.btn_xoa_task.clicked.connect(self.xoa_task)
        self.btn_doi_trang_thai.clicked.connect(self.doi_trang_thai)
        self.btn_them_nhanh.clicked.connect(self.them_task_nhanh)
        
        # Hiển thị danh sách task
        self.cap_nhat_danh_sach_task()
    
    def cap_nhat_danh_sach_task(self):
        """Cập nhật danh sách task trên giao diện"""
        self.list_task.clear()  # Xóa danh sách cũ
        
        for i, task in enumerate(self.user_hien_tai.danh_sach_task):
            # Tạo text hiển thị
            text = f"{task.ten_task} - Hạn: {task.han_chot} - {task.trang_thai}"
            
            # Thêm vào list
            item = QListWidgetItem(text)
            
            # Đổi màu theo trạng thái
            if task.trang_thai == "Xong rồi":
                item.setBackground(QColor(200, 200, 200))  # Màu xám cho task xong
            else:
                item.setBackground(QColor(255, 200, 200))  # Màu đỏ nhạt cho task chưa xong
            
            self.list_task.addItem(item)
    
    def them_task(self):
        """Thêm task mới bằng dialog"""
        # Hỏi thông tin task
        ten_task, ok1 = QInputDialog.getText(self, "Thêm Task", "Nhập tên task:")
        if not ok1 or not ten_task:
            return
        
        han_chot, ok2 = QInputDialog.getText(self, "Thêm Task", "Nhập hạn chót:")
        if not ok2 or not han_chot:
            return
        
        # Tạo task mới
        task_moi = Task(ten_task, han_chot)
        self.user_hien_tai.danh_sach_task.append(task_moi)
        
        # Lưu và cập nhật
        luu_du_lieu(self.danh_sach_user)
        self.cap_nhat_danh_sach_task()
        QMessageBox.information(self, "Thành công", "Đã thêm task mới!")
    
    def them_task_nhanh(self):
        """Thêm task nhanh từ form dưới"""
        ten_task = self.input_ten_task.text()
        han_chot = self.input_han_chot.text()
        
        if not ten_task:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên task!")
            return
        
        if not han_chot:
            han_chot = "Không có"
        
        # Tạo và thêm task
        task_moi = Task(ten_task, han_chot)
        self.user_hien_tai.danh_sach_task.append(task_moi)
        
        # Xóa form và cập nhật
        self.input_ten_task.clear()
        self.input_han_chot.clear()
        luu_du_lieu(self.danh_sach_user)
        self.cap_nhat_danh_sach_task()
    
    def sua_task(self):
        """Sửa task đã chọn"""
        # Kiểm tra có chọn task không
        dong_chon = self.list_task.currentRow()
        if dong_chon == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn task để sửa!")
            return
        
        # Lấy task cần sửa
        task = self.user_hien_tai.danh_sach_task[dong_chon]
        
        # Hỏi thông tin mới
        ten_moi, ok1 = QInputDialog.getText(self, "Sửa Task", "Tên task:", text=task.ten_task)
        if not ok1:
            return
        
        han_chot_moi, ok2 = QInputDialog.getText(self, "Sửa Task", "Hạn chót:", text=task.han_chot)
        if not ok2:
            return
        
        # Cập nhật task
        task.ten_task = ten_moi
        task.han_chot = han_chot_moi
        
        # Lưu và cập nhật
        luu_du_lieu(self.danh_sach_user)
        self.cap_nhat_danh_sach_task()
        QMessageBox.information(self, "Thành công", "Đã cập nhật task!")
    
    def xoa_task(self):
        """Xóa task đã chọn"""
        # Kiểm tra có chọn task không
        dong_chon = self.list_task.currentRow()
        if dong_chon == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn task để xóa!")
            return
        
        # Xác nhận xóa
        task = self.user_hien_tai.danh_sach_task[dong_chon]
        ket_qua = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa task '{task.ten_task}'?")
        
        if ket_qua == QMessageBox.StandardButton.Yes:
            # Xóa task
            del self.user_hien_tai.danh_sach_task[dong_chon]
            
            # Lưu và cập nhật
            luu_du_lieu(self.danh_sach_user)
            self.cap_nhat_danh_sach_task()
            QMessageBox.information(self, "Thành công", "Đã xóa task!")
    
    def doi_trang_thai(self):
        """Đổi trạng thái task (xong/chưa xong)"""
        # Kiểm tra có chọn task không
        dong_chon = self.list_task.currentRow()
        if dong_chon == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn task để đổi trạng thái!")
            return
        
        # Đổi trạng thái
        task = self.user_hien_tai.danh_sach_task[dong_chon]
        if task.trang_thai == "Chưa xong":
            task.trang_thai = "Xong rồi"
        else:
            task.trang_thai = "Chưa xong"
        
        # Lưu và cập nhật
        luu_du_lieu(self.danh_sach_user)
        self.cap_nhat_danh_sach_task()
        QMessageBox.information(self, "Thành công", f"Đã đổi trạng thái thành: {task.trang_thai}")
    
    def dang_xuat(self):
        """Đăng xuất về màn hình đăng nhập"""
        ket_qua = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn đăng xuất?")
        
        if ket_qua == QMessageBox.StandardButton.Yes:
            self.close()
            self.cua_so_dang_nhap = CuaSoDangNhap()
            self.cua_so_dang_nhap.show()

def main():
    """Hàm chính chạy chương trình"""
    app = QApplication(sys.argv)
    
    # Tạo và hiển thị cửa sổ đăng nhập
    cua_so_dang_nhap = CuaSoDangNhap()
    cua_so_dang_nhap.show()
    
    # Chạy ứng dụng
    sys.exit(app.exec())

# Chạy chương trình
if __name__ == "__main__":
    main()