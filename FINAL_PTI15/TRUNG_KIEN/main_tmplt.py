from PyQt6.QtWidgets import *
from PyQt6 import uic

UI_FILE = "ui/main.ui"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()