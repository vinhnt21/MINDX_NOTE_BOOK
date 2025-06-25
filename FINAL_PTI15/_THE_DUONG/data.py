# data.py - Xử lý dữ liệu đơn giản

import json
import os
from models import User, Task

# Tên file lưu dữ liệu
FILE_DU_LIEU = os.path.join(os.path.dirname(__file__), 'data.json')

def tai_du_lieu():
    """Đọc dữ liệu từ file"""
    try:
        if os.path.exists(FILE_DU_LIEU):
            with open(FILE_DU_LIEU, "r", encoding="utf-8") as file:
                data = json.load(file)
                
            # Chuyển từ dict thành User object
            danh_sach_user = []
            for user_info in data:
                user = User(user_info["ten_dang_nhap"], user_info["mat_khau"])
                
                # Thêm các task vào user
                for task_info in user_info["danh_sach_task"]:
                    task = Task(task_info["ten_task"], task_info["han_chot"], task_info["trang_thai"])
                    user.danh_sach_task.append(task)
                
                danh_sach_user.append(user)
            
            return danh_sach_user
        else:
            return []
    except:
        print("Lỗi khi đọc file!")
        return []

def luu_du_lieu(danh_sach_user):
    """Lưu dữ liệu vào file"""
    try:
        # Chuyển từ User object thành dict
        data = []
        for user in danh_sach_user:
            user_info = {
                "ten_dang_nhap": user.ten_dang_nhap,
                "mat_khau": user.mat_khau,
                "danh_sach_task": []
            }
            
            # Thêm thông tin task
            for task in user.danh_sach_task:
                task_info = {
                    "ten_task": task.ten_task,
                    "han_chot": task.han_chot,
                    "trang_thai": task.trang_thai
                }
                user_info["danh_sach_task"].append(task_info)
            
            data.append(user_info)
        
        # Ghi vào file
        with open(FILE_DU_LIEU, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        print("Đã lưu dữ liệu!")
        return True
    except:
        print("Lỗi khi lưu file!")
        return False

def tim_user(ten_dang_nhap, danh_sach_user):
    """Tìm user theo tên đăng nhập"""
    for user in danh_sach_user:
        if user.ten_dang_nhap == ten_dang_nhap:
            return user
    return None

def kiem_tra_dang_nhap(ten_dang_nhap, mat_khau, danh_sach_user):
    """Kiểm tra đăng nhập"""
    user = tim_user(ten_dang_nhap, danh_sach_user)
    if user and user.mat_khau == mat_khau:
        return user
    return None

