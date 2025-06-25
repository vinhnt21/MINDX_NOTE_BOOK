# data.py - Xử lý dữ liệu người dùng và phiên thi
# File này chứa các hàm để lưu trữ và tải dữ liệu từ file JSON

import json
import os
from datetime import datetime
from models import User, QuizSession

# Đường dẫn tới các file lưu trữ dữ liệu
DATA_DIR = os.path.dirname(__file__)
USERS_FILE = os.path.join(DATA_DIR, "users.json")
QUIZ_SESSIONS_FILE = os.path.join(DATA_DIR, "quiz_sessions.json")

def load_users():
    """
    Tải dữ liệu người dùng từ file JSON
    Returns: danh sách các đối tượng User
    """
    try:
        # Kiểm tra xem file có tồn tại không
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
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
        print(f"Lỗi khi tải dữ liệu người dùng: {e}")
        return []

def save_users(users):
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
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("Đã lưu dữ liệu người dùng thành công!")
    
    except Exception as e:
        # Nếu có lỗi, in ra thông báo
        print(f"Lỗi khi lưu dữ liệu người dùng: {e}")

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

def register_user(username, password, confirm_password):
    """
    Đăng ký người dùng mới
    Args: username, password, confirm_password
    Returns: tuple (success: bool, message: str)
    """
    # Kiểm tra mật khẩu xác nhận
    if password != confirm_password:
        return False, "Mật khẩu xác nhận không khớp!"
    
    # Kiểm tra độ dài
    if len(username) < 3:
        return False, "Tên đăng nhập phải có ít nhất 3 ký tự!"
    
    if len(password) < 3:
        return False, "Mật khẩu phải có ít nhất 3 ký tự!"
    
    # Tải danh sách người dùng hiện tại
    users = load_users()
    
    # Kiểm tra xem tên đăng nhập đã tồn tại chưa
    if find_user(username, users):
        return False, "Tên đăng nhập đã tồn tại!"
    
    # Tạo người dùng mới
    new_user = User(username, password)
    users.append(new_user)
    
    # Lưu vào file
    save_users(users)
    
    return True, "Đăng ký thành công!"

def login_user(username, password):
    """
    Đăng nhập người dùng
    Args: username, password
    Returns: tuple (success: bool, message: str, user: User or None)
    """
    # Tải danh sách người dùng
    users = load_users()
    
    # Tìm người dùng
    user = find_user(username, users)
    
    if user is None:
        return False, "Tên đăng nhập không tồn tại!", None
    
    if user.password != password:
        return False, "Mật khẩu không đúng!", None
    
    return True, "Đăng nhập thành công!", user

def save_quiz_session(quiz_session):
    """
    Lưu phiên thi vào file JSON
    Args: quiz_session - đối tượng QuizSession
    """
    try:
        # Tải dữ liệu hiện tại
        sessions = load_quiz_sessions()
        
        # Thêm timestamp
        quiz_session.timestamp = datetime.now().isoformat()
        
        # Chuyển đổi thành dictionary
        session_data = {
            "user_id": quiz_session.user_id,
            "questions": quiz_session.questions,
            "answers": quiz_session.answers,
            "score": quiz_session.score,
            "timestamp": quiz_session.timestamp
        }
        
        sessions.append(session_data)
        
        # Lưu vào file
        with open(QUIZ_SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=4)
        
        print("Đã lưu phiên thi thành công!")
    
    except Exception as e:
        print(f"Lỗi khi lưu phiên thi: {e}")

def load_quiz_sessions():
    """
    Tải dữ liệu phiên thi từ file JSON
    Returns: danh sách các dictionary phiên thi
    """
    try:
        if os.path.exists(QUIZ_SESSIONS_FILE):
            with open(QUIZ_SESSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
    
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu phiên thi: {e}")
        return []

# Hàm tương thích với code cũ
def load_data():
    """Hàm tương thích với code cũ"""
    return load_users()

def save_data(users):
    """Hàm tương thích với code cũ"""
    save_users(users)


