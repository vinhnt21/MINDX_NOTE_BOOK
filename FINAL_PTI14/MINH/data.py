import os
import json
from model import Essay

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def load_essays():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    essays = []
    for item in data:
        essay = Essay(item["user_essay"], item["ai_feedback"])
        essays.append(essay)
    return essays

def save_essays(essays):
    data = []
    for essay in essays:
        data.append(essay.__dict__)    
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
