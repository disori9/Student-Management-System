from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout, QMainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())