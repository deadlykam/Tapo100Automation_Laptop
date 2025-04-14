import json
from pathlib import Path

data_name = "data.json"

def is_data():
    file_path = Path(data_name)
    return file_path.exists()

def data_load():
    with open(data_name, "r") as f:
        data = json.load(f)
    return data

def data_save(min, max, ip, email, password, is_dark_theme,
              is_auto_connect):
    data = {
        "min": min,
        "max": max,
        "ip": ip,
        "email": email,
        "password": password,
        "is_dark_theme": is_dark_theme,
        "is_auto_connect": is_auto_connect
    }

    with open(data_name, "w") as f:
        json.dump(data, f, indent=4)