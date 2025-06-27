import os
import json
from model import User
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def load_users():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    users = []
    for item in data:
        user = User(item["username"], item["password"])
        users.append(user)
    return users


def save_users(users):
    data = []
    for user in users:
        data.append(user.__dict__)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    




