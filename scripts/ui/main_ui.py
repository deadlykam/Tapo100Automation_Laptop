import threading
import sys
import os
import psutil
import time
from scripts.tapo_manager import connect_tapo
from scripts.tapo_manager import set_tapo
from scripts.save_load_manager import is_data
from scripts.save_load_manager import data_save
from scripts.save_load_manager import data_load
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget,
                             QProgressBar, QGridLayout, QLineEdit,
                             QPushButton)
from PyQt5.QtGui import QPixmap


class MainWindow (QMainWindow):

    _window_title = "Tapo 100 Automation For Laptop"
    _window_icon = "TODO: Create an icon and link here"
    _window_position = [0, 0, 400, 200] # X, Y, Width, Height
    _range_pb_battery = [0, 100] # Min, Max
    _range_charge = [20, 80] # Min, Max
    _refresh_rate = 1 # Per Second
    _is_plugged = False
    _is_charging = False
    battery_charge = 0
    ip = ""
    email = ""
    password = ""
    is_connected = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self._window_title)
        self.setGeometry(self._window_position[0],
                         self._window_position[1],
                         self._window_position[2],
                         self._window_position[3])

        self._is_charging = psutil.sensors_battery().power_plugged # Getting the first charge value

        self.init_ui()
        if is_data(): self.load_values(data_load())
        self.thread_update = threading.Thread(target=self.update_loop, daemon=True)
        self.thread_update.start()

    def init_ui(self):
        layout_grid = QGridLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.img_battery_discharging = QLabel(self)
        self.img_battery_discharging.setGeometry(0, 0, 50, 25)
        self.img_battery_discharging.setPixmap(QPixmap(self.resource_path(os.path.join('images', 'uis', 'Battery_Discharging_50x25.png'))))
        self.img_battery_discharging.show()
        layout_grid.addWidget(self.img_battery_discharging, 0, 1)

        self.img_battery_charging = QLabel(self)
        self.img_battery_charging.setGeometry(0, 0, 50, 25)
        self.img_battery_charging.setPixmap(QPixmap(self.resource_path(os.path.join('images', 'uis', 'Battery_Charging_50x25.png'))))
        self.img_battery_charging.hide()
        layout_grid.addWidget(self.img_battery_charging, 0, 1)

        self.img_tapo_icon = QLabel(self)
        self.img_tapo_icon.setPixmap(QPixmap(self.resource_path(os.path.join('images', 'uis', 'TapoPlug_x25.png'))))
        self.img_tapo_icon.hide()
        layout_grid.addWidget(self.img_tapo_icon, 0, 2)

        self.pb_battery = QProgressBar()
        self.pb_battery.setRange(self._range_pb_battery[0], self._range_pb_battery[1])
        self.pb_battery.setValue(0)
        layout_grid.addWidget(self.pb_battery, 0, 0)

        self.lbl_min = QLabel(self)
        self.lbl_min.setText("Min (%) -> 20%")
        layout_grid.addWidget(self.lbl_min, 2, 0)

        self.le_min = QLineEdit(self)
        self.le_min.setInputMask("000")
        self.le_min.setText("20")
        layout_grid.addWidget(self.le_min, 2, 1)

        self.lbl_max = QLabel(self)
        self.lbl_max.setText("Max (%) -> 80%")
        layout_grid.addWidget(self.lbl_max, 3, 0)

        self.le_max = QLineEdit(self)
        self.le_max.setInputMask("000")
        self.le_max.setText("80")
        layout_grid.addWidget(self.le_max, 3, 1)

        self.lbl_ip = QLabel(self)
        self.lbl_ip.setText("IP:")
        layout_grid.addWidget(self.lbl_ip, 4, 0)

        self.le_ip = QLineEdit(self)
        layout_grid.addWidget(self.le_ip, 4, 1)

        self.lbl_email = QLabel(self)
        self.lbl_email.setText("Email:")
        layout_grid.addWidget(self.lbl_email, 5, 0)

        self.le_email = QLineEdit(self)
        layout_grid.addWidget(self.le_email, 5, 1)

        self.lbl_password = QLabel(self)
        self.lbl_password.setText("Password")
        layout_grid.addWidget(self.lbl_password, 6, 0)

        self.le_password = QLineEdit(self)
        self.le_password.setEchoMode(QLineEdit.Password)
        layout_grid.addWidget(self.le_password, 6, 1)

        self.btn_connect = QPushButton("Connect", self)
        self.btn_connect.clicked.connect(self.connect_tapo)
        layout_grid.addWidget(self.btn_connect, 7, 0)

        self.btn_save = QPushButton("Save", self)
        self.btn_save.clicked.connect(self.save_values)
        layout_grid.addWidget(self.btn_save, 7, 1)

        central_widget.setLayout(layout_grid)

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
        return os.path.join(base_path, relative_path)

    def set_charging_image(self, is_charging):
        self.img_battery_charging.setVisible(is_charging)
        self.img_battery_discharging.setVisible(not is_charging)

    def validate_charging(self):
        if self.is_connected:
            if self._is_plugged and self._is_charging and self.battery_charge >= self._range_charge[1]:
                set_tapo(False)
                self._is_charging = False
            elif not self._is_plugged and not self._is_charging and self.battery_charge <= self._range_charge[0]:
                set_tapo(True)
                self._is_charging = True

    def save_values(self):
        self._range_charge[0] = int(self.le_min.text())
        self.lbl_min.setText("Min (%) -> " + str(self._range_charge[0]) + "%")
        self._range_charge[1] = int(self.le_max.text())
        self.lbl_max.setText("Max (%) -> " + str(self._range_charge[1]) + "%")
        self.ip = self.le_ip.text()
        self.lbl_ip.setText("IP: " + self.ip)
        self.email = self.le_email.text()
        self.lbl_email.setText("Email: " + self.email)
        self.password = self.le_password.text()
        data_save(self._range_charge[0], self._range_charge[1],
                  self.ip, self.email, self.password)

    def load_values(self, data):
        self._range_charge[0] = data["min"]
        self.le_min.setText(str(data["min"]))
        self._range_charge[1] = data["max"]
        self.le_max.setText(str(data["max"]))
        self.ip = data["ip"]
        self.le_ip.setText(data["ip"])
        self.email = data["email"]
        self.le_email.setText(data["email"])
        self.password = data["password"]
        self.le_password.setText(data["password"])

    def connect_tapo(self):
        connect_tapo(self.ip, self.email, self.password)
        self.is_connected = True
        self.img_tapo_icon.show()

    def update_loop(self):
        while True:
            time.sleep(self._refresh_rate)
            self.battery_charge = int(psutil.sensors_battery().percent)
            self._is_plugged = psutil.sensors_battery().power_plugged
            self.validate_charging()
            self.pb_battery.setValue(self.battery_charge)
            self.set_charging_image(self._is_plugged)
