import sys
import os
import psutil
import time
import qdarktheme
from scripts.tapo_manager import connect_tapo
from scripts.tapo_manager import set_tapo
from scripts.save_load_manager import is_data
from scripts.save_load_manager import data_save
from scripts.save_load_manager import data_load
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget,
                             QProgressBar, QGridLayout, QLineEdit,
                             QPushButton, QCheckBox)
from PyQt5.QtGui import QPixmap, QIcon


class MainWindow (QMainWindow):

    _window_title = "Tapo 100 Automation For Laptop"
    _version = "1.0.0"
    _window_icon = "TAL_Logo_199x256.png"
    _window_position = [0, 0, 400, 200] # X, Y, Width, Height
    _range_pb_battery = [0, 100] # Min, Max
    _range_charge = [20, 80] # Min, Max
    _refresh_rate = 1 # Per Second
    _is_plugged = False
    _is_charging = False
    _is_dark_theme = False
    _is_auto_connect = False
    battery_charge = 0
    ip = ""
    email = ""
    password = ""
    is_connected = False

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self._window_title + " - " + self._version)
        self.setGeometry(self._window_position[0],
                         self._window_position[1],
                         self._window_position[2],
                         self._window_position[3])
        self.setWindowIcon(QIcon(self.resource_path("images/logo/TAL_Logo_256x256.ico")))

        self._is_charging = psutil.sensors_battery().power_plugged # Getting the first charge value

        self.init_ui()
        if is_data(): self.load_values(data_load())
        if self._is_auto_connect: self.connect_tapo()
        self.set_theme()
        self.thread_update = UpdateWorker(self._refresh_rate)
        self.thread_update.battery_update.connect(self.update_battery_charge_value)
        self.thread_update.charging_status.connect(self.handle_charging_status)
        self.thread_update.start()

    def init_ui(self):
        layout_grid = QGridLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.img_battery_discharging = QLabel(self)
        self.img_battery_discharging.setGeometry(0, 0, 50, 25)
        self.img_battery_discharging.setPixmap(QPixmap(self.resource_path("images/uis/Battery_Discharging_50x25.png")))
        self.img_battery_discharging.show()
        layout_grid.addWidget(self.img_battery_discharging, 0, 1)

        self.img_battery_discharging_d = QLabel(self)
        self.img_battery_discharging_d.setGeometry(0, 0, 50, 25)
        self.img_battery_discharging_d.setPixmap(QPixmap(self.resource_path("images/uis/Battery_Discharging_D_50x25.png")))
        self.img_battery_discharging_d.hide()
        layout_grid.addWidget(self.img_battery_discharging_d, 0, 1)

        self.img_battery_charging = QLabel(self)
        self.img_battery_charging.setGeometry(0, 0, 50, 25)
        self.img_battery_charging.setPixmap(QPixmap(self.resource_path("images/uis/Battery_Charging_50x25.png")))
        self.img_battery_charging.hide()
        layout_grid.addWidget(self.img_battery_charging, 0, 1)

        self.img_battery_charging_d = QLabel(self)
        self.img_battery_charging_d.setGeometry(0, 0, 50, 25)
        self.img_battery_charging_d.setPixmap(QPixmap(self.resource_path("images/uis/Battery_Charging_D_50x25.png")))
        self.img_battery_charging_d.hide()
        layout_grid.addWidget(self.img_battery_charging_d, 0, 1)

        self.img_tapo_icon = QLabel(self)
        self.img_tapo_icon.setPixmap(QPixmap(self.resource_path("images/uis/TapoPlug_x25.png")))
        self.img_tapo_icon.hide()
        layout_grid.addWidget(self.img_tapo_icon, 0, 2)

        self.img_tapo_icon_d = QLabel(self)
        self.img_tapo_icon_d.setPixmap(QPixmap(self.resource_path("images/uis/TapoPlug_D_x25.png")))
        self.img_tapo_icon_d.hide()
        layout_grid.addWidget(self.img_tapo_icon_d, 0, 2)

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

        self.cb_toggle_auto_connect = QCheckBox("Auto Connect", self)
        self.cb_toggle_auto_connect.clicked.connect(self.toggle_auto_connect)
        layout_grid.addWidget(self.cb_toggle_auto_connect, 8, 0)

        self.cb_toggle_theme = QCheckBox("Dark Theme", self)
        self.cb_toggle_theme.clicked.connect(self.toggle_theme)
        layout_grid.addWidget(self.cb_toggle_theme, 8, 1)

        central_widget.setLayout(layout_grid)

    def set_charging_image(self, is_charging):
        if not self._is_dark_theme:
            self.img_battery_charging.setVisible(is_charging)
            self.img_battery_discharging.setVisible(not is_charging)
        else:
            self.img_battery_charging_d.setVisible(is_charging)
            self.img_battery_discharging_d.setVisible(not is_charging)

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
                  self.ip, self.email, self.password, self._is_dark_theme,
                  self._is_auto_connect)

    def load_values(self, data):
        self._range_charge[0] = data["min"]
        self.le_min.setText(str(data["min"]))
        self.lbl_min.setText("Min (%) -> " + str(self._range_charge[0]) + "%")
        self._range_charge[1] = data["max"]
        self.le_max.setText(str(data["max"]))
        self.lbl_max.setText("Max (%) -> " + str(self._range_charge[1]) + "%")
        self.ip = data["ip"]
        self.le_ip.setText(data["ip"])
        self.lbl_ip.setText("IP: " + self.ip)
        self.email = data["email"]
        self.le_email.setText(data["email"])
        self.lbl_email.setText("Email: " + self.email)
        self.password = data["password"]
        self.le_password.setText(data["password"])
        self._is_dark_theme = data["is_dark_theme"]
        self._is_auto_connect = data["is_auto_connect"]
        self.cb_toggle_theme.setChecked(self._is_dark_theme)
        self.cb_toggle_auto_connect.setChecked(self._is_auto_connect)

    def connect_tapo(self):
        connect_tapo(self.ip, self.email, self.password)
        self.is_connected = True
        if not self._is_dark_theme: self.img_tapo_icon.show()
        else: self.img_tapo_icon_d.show()
        self.btn_connect.hide()

    def handle_charging_status(self, is_plugged):
        self._is_plugged = is_plugged
        self.validate_charging()
        self.set_charging_image(is_plugged)

    def toggle_theme(self):
        self._is_dark_theme = self.cb_toggle_theme.isChecked()
        self.set_theme()

    def set_theme(self):
        if self._is_dark_theme:
            self.img_tapo_icon_d.setVisible(self.is_connected)
            self.img_battery_charging_d.setVisible(self.img_battery_charging.isVisible())
            self.img_battery_discharging_d.setVisible(self.img_battery_discharging.isVisible())
            self.img_tapo_icon.hide()
            self.img_battery_charging.hide()
            self.img_battery_discharging.hide()
            qdarktheme.setup_theme()
        else:
            self.img_tapo_icon.setVisible(self.is_connected)
            self.img_battery_charging.setVisible(self.img_battery_charging_d.isVisible())
            self.img_battery_discharging.setVisible(self.img_battery_discharging_d.isVisible())
            self.img_tapo_icon_d.hide()
            self.img_battery_charging_d.hide()
            self.img_battery_discharging_d.hide()
            qdarktheme.setup_theme("light")

    def toggle_auto_connect(self):
        self._is_auto_connect = self.cb_toggle_auto_connect.isChecked()

    def closeEvent(self, event):
        if hasattr(self, 'thread_update'):
            self.thread_update.stop()
            self.thread_update.wait()
        event.accept()

    def update_battery_charge_value(self, value):
        self.pb_battery.setValue(value)
        self.battery_charge = value

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)

class UpdateWorker(QThread):
    battery_update = pyqtSignal(int)
    charging_status = pyqtSignal(bool)

    def __init__(self, refresh_rate=1, parent=None):
        super().__init__(parent)
        self.refresh_rate = refresh_rate
        self._running = True

    def run(self):
        while self._running:
            battery = psutil.sensors_battery()
            self.battery_update.emit(int(battery.percent))
            self.charging_status.emit(battery.power_plugged)
            time.sleep(self.refresh_rate)

    def stop(self): self._running = False