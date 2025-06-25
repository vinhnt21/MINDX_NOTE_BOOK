import json
import os

# Tên file dữ liệu
USER_FILE = os.path.join(os.path.dirname(__file__), "user.json")
QUESTION_FILE = os.path.join(os.path.dirname(__file__), "question.json")

def load_users():
    """Đọc dữ liệu người dùng từ file JSON"""
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Tạo file mới nếu chưa có
            default_data = {"users": []}
            save_users(default_data)
            return default_data
    except Exception as e:
        print(f"Lỗi khi đọc file user: {e}")
        return {"users": []}

def save_users(data):
    """Lưu dữ liệu người dùng vào file JSON"""
    try:
        with open(USER_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Lỗi khi lưu file user: {e}")
        return False

def load_questions():
    """Đọc câu hỏi từ file JSON"""
    try:
        if os.path.exists(QUESTION_FILE):
            with open(QUESTION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Không tìm thấy file {QUESTION_FILE}")
            return []
    except Exception as e:
        print(f"Lỗi khi đọc file câu hỏi: {e}")
        return []

def find_user(username):
    """Tìm người dùng theo tên đăng nhập"""
    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            return user
    return None

def register_user(username, password):
    """Đăng ký người dùng mới"""
    data = load_users()
    
    # Kiểm tra xem user đã tồn tại chưa
    if find_user(username):
        return False, "Tên đăng nhập đã tồn tại!"
    
    # Thêm user mới
    new_user = {
        "username": username,
        "password": password,
        "highest_score": 0
    }
    data["users"].append(new_user)
    
    if save_users(data):
        return True, "Đăng ký thành công!"
    else:
        return False, "Lỗi khi lưu dữ liệu!"

def login_user(username, password):
    """Đăng nhập người dùng"""
    user = find_user(username)
    if user and user["password"] == password:
        return True, "Đăng nhập thành công!"
    else:
        return False, "Tên đăng nhập hoặc mật khẩu không đúng!"

def update_highest_score(username, new_score):
    """Cập nhật điểm cao nhất của người dùng"""
    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            if new_score > user["highest_score"]:
                user["highest_score"] = new_score
                save_users(data)
                return True
            break
    return False


