from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QGridLayout, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(430, 290)

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        add_student = QAction(QIcon("./icons/add.png"), "Add Student", self)
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)

        about = QAction("About", self)
        help_menu.addAction(about)
        about.triggered.connect(self.about)

        search = QAction(QIcon("./icons/search.png"),"Search", self)
        search.triggered.connect(self.search)
        edit_menu.addAction(search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.addAction(add_student)
        toolbar.addAction(search)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app is created to test my knowledge about CRUD in databases"""

        self.setText(content)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        self.cell_index = main_window.table.currentRow()

        self.confirmation_text = QLabel("Are you sure you want to delete?")
        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        layout.addWidget(self.confirmation_text, 0, 0, 1, 2)
        layout.addWidget(self.yes_button, 1, 0)
        layout.addWidget(self.no_button, 1, 1)
        self.setLayout(layout)

        self.yes_button.clicked.connect(self.delete_student)
        self.no_button.clicked.connect(self.close)

    def delete_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cell_id = int(main_window.table.item(self.cell_index, 0).text())

        cursor.execute("DELETE FROM students WHERE id = ?",(cell_id,))

        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.cell_index = main_window.table.currentRow()
        self.name_cell = main_window.table.item(self.cell_index, 1).text()

        self.student_name = QLineEdit(self.name_cell)
        layout.addWidget(self.student_name)

        self.course_choices = QComboBox()
        self.course_choices.addItems(("Math", "Astronomy", "Biology", "Computer Science", "Physics"))
        self.course_cell = main_window.table.item(self.cell_index, 2).text()
        self.course_choices.setCurrentText(self.course_cell)
        layout.addWidget(self.course_choices)

        self.number_cell = main_window.table.item(self.cell_index, 3).text()
        self.phone_number = QLineEdit(self.number_cell)
        layout.addWidget(self.phone_number)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        name = self.student_name.text()
        course = self.course_choices.currentText()
        number = int(self.phone_number.text())
        cell_id = int(main_window.table.item(self.cell_index, 0).text())

        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (name, course, number, cell_id))
        connection.commit()

        cursor.close()
        connection.close()

        main_window.load_data()


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
        self.search_button.clicked.connect(self.search_student)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        name = self.student_name.text().lower().title()
        # result = cursor.execute(f"SELECT name FROM students WHERE name=?", (name,))
        # result_row = list(result)[0]

        items = main_window.table.findItems(name, Qt.MatchFlag.MatchContains)
        # basically, this is a generator that searches for the items that matches the given condition (name)

        # we iterate over this iterator/generator
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
            # we select the specific cell, item.row() is the index of row where the item was found and 1 is the name
            # column. .setSelected(True) highights the cell.

        cursor.close()
        connection.close()


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
        connection = DatabaseConnection().connect()
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