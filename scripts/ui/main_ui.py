import threading
import psutil
import time
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget,
                             QVBoxLayout, QHBoxLayout, QProgressBar)
from PyQt5.QtGui import QPixmap

class MainWindow (QMainWindow):

    _window_title = "Tapo 100 Automation For Laptop"
    _window_icon = "TODO: Create an icon and link here"
    _window_position = [0, 0, 400, 200] # X, Y, Width, Height
    _range_charge = [0, 100] # Min, Max

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self._window_title)
        self.setGeometry(self._window_position[0],
                         self._window_position[1],
                         self._window_position[2],
                         self._window_position[3])

        self.initUI()

        self.thread_update = threading.Thread(target=self.update_loop, daemon=True)
        self.thread_update.start()

    def initUI(self):
        layout_main = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.img_battery_empty = QLabel(self)
        self.img_battery_empty.setGeometry(0, 0, 213, 105)
        pm = QPixmap("images/uis/Battery_Discharging.png")
        self.img_battery_empty.setPixmap(pm)
        self.img_battery_empty.setScaledContents(True)
        layout_main.addWidget(self.img_battery_empty)

        self.pb_battery = QProgressBar()
        self.pb_battery.setRange(self._range_charge[0], self._range_charge[1])
        self.pb_battery.setValue(0)
        layout_main.addWidget(self.pb_battery)

        central_widget.setLayout(layout_main)

    def update_loop(self):
        while True:
            time.sleep(1)
            self.pb_battery.setValue(psutil.sensors_battery().percent)
            if psutil.sensors_battery().power_plugged:
                print("Laptop Charging")
            else:
                print("Laptop NOT Charging")
