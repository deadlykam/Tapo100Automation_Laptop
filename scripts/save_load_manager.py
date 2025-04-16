"""
save_load_manager.py

This script saves and loads the application's setting data using JSON.

Dependencies:
- json
- pathlib

Author: Kamran Wali
"""

import json
from pathlib import Path

data_name = "data.json"

def is_data():
    """
    Checks if the data file exists.
    :return: If True, then data file exists. If False, then data file does NOT exist.
    """
    file_path = Path(data_name)
    return file_path.exists()

def data_load():
    """
    This method loads the application's setting data from saved data file.
    """
    with open(data_name, "r") as f:
        data = json.load(f)
    return data

def data_save(min, max, ip, email, password, is_dark_theme,
              is_auto_connect):
    """
    This method saves the application's setting to the JSON data file.
    :param min: The minimum threshold of the laptop battery value.
    :param max: The maximum threshold of the laptop battery value.
    :param ip: The local IP address of the Tapo device.
    :param email: The email address for Tapo account
    :param password: The password for the Tapo account
    :param is_dark_theme: If True, then dark theme has been set. If False, then light theme has been set.
    :param is_auto_connect: If True, then auto connect at start up has been set. If False, then auto connect
                            has been disabled at start up.
    """
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