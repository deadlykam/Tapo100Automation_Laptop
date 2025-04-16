"""
tapo_manager.py

This script connects to the Tapo account and turn's on/off the Tapo device.

Dependencies:
- PyP100

Author: Kamran Wali
"""

from PyP100 import PyP100

tapo = None

def connect_tapo(ip, email, password):
    """
    This method connects to the Tapo account.
    :param ip: The local IP address of the Tapo device.
    :param email: The email address of the Tapo account.
    :param password: The password for the Tapo account.
    """
    global tapo
    tapo = PyP100.P100(ip, email, password)
    tapo.handshake()

def set_tapo(is_on):
    """
    This method turn's the Tapo device on/off
    :param is_on: If True, then the Tapo device is turned on. If False, then the Tapo device is turned off.
    :return:
    """
    if is_on: tapo.turnOn()
    else: tapo.turnOff()