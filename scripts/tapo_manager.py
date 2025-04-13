from PyP100 import PyP100

tapo = None

def connect_tapo(ip, email, password):
    global tapo
    tapo = PyP100.P100(ip, email, password)
    tapo.handshake()

def set_tapo(is_on):
    if is_on: tapo.turnOn()
    else: tapo.turnOff()