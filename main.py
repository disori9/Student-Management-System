from tkinter.constants import INSERT

from PyQt6.QtCore import QLine
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        add_student = QAction("Add Student", self)
        add_student.triggered.connect(self.insert_student)
        file_menu.addAction(add_student)

        about = QAction("About", self)
        help_menu.addAction(about)

        search = QAction("Search", self)
        search.triggered.connect(self.search_student)
        edit_menu.addAction(search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert_student(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_student(self):
        dialog = SearchDialog()
        dialog.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.search_button = QPushButton("Search")
        #self.search_button.clicked.connect(self.search_student)
        layout.addWidget(self.search_button)

        self.setLayout(layout)


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_choices = QComboBox()
        self.course_choices.addItems(("Math", "Astronomy", "Biology", "Computer Science", "Physics"))
        self.course_choices.setPlaceholderText("Courses")
        layout.addWidget(self.course_choices)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone")
        layout.addWidget(self.phone_number)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.add_student)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        name = self.student_name.text()
        course = str(self.course_choices.itemText(self.course_choices.currentIndex()))
        phone = int(self.phone_number.text())

        cursor.execute("INSERT INTO students(name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, phone))
        connection.commit()

        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())