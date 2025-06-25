import json
import os
from models import User, Game

# Đường dẫn file dữ liệu
USERS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'user.json')
GAMES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'game.json')

def load_users():
    """Tải danh sách người dùng từ file JSON"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            return [User(user['username'], user['password']) for user in users_data]
    except FileNotFoundError:
        return []

def save_users(users):
    """Lưu danh sách người dùng vào file JSON"""
    users_data = [{'username': user.username, 'password': user.password} for user in users]
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

def load_games():
    """Tải danh sách game từ file JSON"""
    try:
        with open(GAMES_FILE, 'r', encoding='utf-8') as f:
            games_data = json.load(f)
            return [Game(game['name'], game['price'], game['description'], 
                       game['url'], game['img_url']) for game in games_data]
    except FileNotFoundError:
        return []

def register_user(username, password):
    """Đăng ký người dùng mới"""
    users = load_users()
    
    # Kiểm tra username đã tồn tại chưa
    for user in users:
        if user.username == username:
            return False, "Tên đăng nhập đã tồn tại!"
    
    # Thêm user mới
    new_user = User(username, password)
    users.append(new_user)
    save_users(users)
    return True, "Đăng ký thành công!"

def login_user(username, password):
    """Đăng nhập người dùng"""
    users = load_users()
    
    for user in users:
        if user.username == username and user.password == password:
            return True, "Đăng nhập thành công!"
    
    return False, "Tên đăng nhập hoặc mật khẩu không đúng!"

def check_user_exists(username):
    """Kiểm tra người dùng có tồn tại không"""
    users = load_users()
    for user in users:
        if user.username == username:
            return True
    return False
