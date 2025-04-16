"""
main.py

This script starts the application.

Dependencies:
- PyQt5
- main_ui (custom module)

Author: Kamran Wali
Date: 23-03-2025
"""

import sys
from PyQt5.QtWidgets import QApplication
from scripts.ui.main_ui import MainWindow

def main():
    """
    Starts the application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    """
    Starting point of the script.
    """
    main()