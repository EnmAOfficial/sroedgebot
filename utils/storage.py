import json
import os

def load(path, default):
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path, "r", encoding="utf-8"))
    except:
        return default

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
