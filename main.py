from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout, QMainWindow
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        add_student = QAction("Add Student", self)
        file_menu.addAction(add_student)

        about = QAction("About", self)
        help_menu.addAction(about)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())