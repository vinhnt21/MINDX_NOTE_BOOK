# data.py - Xử lý dữ liệu người dùng
# File này chứa các hàm để lưu trữ và tải dữ liệu từ file JSON

import json
import os
from models import User

# Đường dẫn tới file lưu trữ dữ liệu
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load_data():
    """
    Tải dữ liệu người dùng từ file JSON
    Returns: danh sách các đối tượng User
    """
    try:
        # Kiểm tra xem file có tồn tại không
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            # Nếu file không tồn tại, trả về danh sách rỗng
            return []
        
        # Nếu file rỗng, trả về danh sách rỗng
        if len(data) == 0:
            return []
        
        # Chuyển đổi dữ liệu JSON thành các đối tượng Python
        users = []
        for user_data in data:
            # Tạo đối tượng User
            user = User(user_data["username"], user_data["password"])
            users.append(user)
        
        return users
    
    except Exception as e:
        # Nếu có lỗi, in ra thông báo và trả về danh sách rỗng
        print(f"Lỗi khi tải dữ liệu: {e}")
        return []

def save_data(users):
    """
    Lưu dữ liệu người dùng vào file JSON
    Args: users - danh sách các đối tượng User
    """
    try:
        # Chuyển đổi các đối tượng Python thành dữ liệu JSON
        data = []
        for user in users:
            # Chuyển đổi đối tượng User thành dictionary
            user_data = {
                "username": user.username,
                "password": user.password
            }
            data.append(user_data)
        
        # Lưu vào file JSON
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("Đã lưu dữ liệu thành công!")
    
    except Exception as e:
        # Nếu có lỗi, in ra thông báo
        print(f"Lỗi khi lưu dữ liệu: {e}")

def find_user(username, users):
    """
    Tìm người dùng theo tên đăng nhập
    Args: username - tên đăng nhập, users - danh sách người dùng
    Returns: đối tượng User nếu tìm thấy, None nếu không tìm thấy
    """
    for user in users:
        if user.username == username:
            return user
    return None


