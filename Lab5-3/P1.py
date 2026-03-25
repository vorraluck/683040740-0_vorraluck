#Vorraluck Taladon
#683040740-0

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QSpinBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import QLocale

class StudentGradeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Student scores and grades")
        self.setGeometry(300, 200, 900, 600)

        self.students = {}
        self.load_students()
        self.setup_ui()

    # Load students.txt 
    def load_students(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "students.txt")
            with open(file_path, "r") as f:
                for line in f:
                    sid, name = line.strip().split(",")
                    self.students[sid] = name
        except:
            QMessageBox.critical(self, "Error")
            sys.exit()

        #set
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        #Card
        card = QWidget()
        card.setObjectName("card")
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)

        # Student ID
        form_layout.addWidget(QLabel("Student ID:"), 0, 0)
        self.id_combo = QComboBox()
        self.id_combo.addItem("Select Student ID")
        for sid in sorted(self.students.keys()):
            self.id_combo.addItem(sid)
        self.id_combo.currentTextChanged.connect(self.update_name)
        form_layout.addWidget(self.id_combo, 0, 1)

        # Student Name
        form_layout.addWidget(QLabel("Student Name:"), 1, 0)
        self.name_label = QLabel("")
        self.name_label.setObjectName("nameLabel")
        form_layout.addWidget(self.name_label, 1, 1)

        # Scores
        self.math_input = QSpinBox()
        self.science_input = QSpinBox()
        self.english_input = QSpinBox()

        for spin in [self.math_input, self.science_input, self.english_input]:
            #set score 0-100
            spin.setRange(0, 100)
            #arabic
            spin.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        form_layout.addWidget(QLabel("Math Score:"), 2, 0)
        form_layout.addWidget(self.math_input, 2, 1)

        form_layout.addWidget(QLabel("Science Score:"), 3, 0)
        form_layout.addWidget(self.science_input, 3, 1)

        form_layout.addWidget(QLabel("English Score:"), 4, 0)
        form_layout.addWidget(self.english_input, 4, 1)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Student")
        reset_btn = QPushButton("Reset Input")
        clear_btn = QPushButton("Clear All")

        add_btn.clicked.connect(self.add_student)
        reset_btn.clicked.connect(self.reset_input)
        clear_btn.clicked.connect(self.clear_all)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(clear_btn)

        form_layout.addLayout(button_layout, 5, 0, 1, 2)

        card.setLayout(form_layout)
        main_layout.addWidget(card)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Student ID", "Student Name",
            "Math", "Science", "English",
            "Total", "Average", "Grade"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.apply_styles()

    # Styles
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QWidget#card {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
                border: 1px solid #dddddd;
            }

            QLabel {
                font-weight: 500;
            }

            QLabel#nameLabel {
                font-weight: bold;
                color: #9fa8da;
            }

            QComboBox, QSpinBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 8px;
                min-height: 30px;
                background-color: white;
            }

            QPushButton {
                background-color: #3f51b5;
                color: white;
                border-radius: 8px;
                padding: 8px 15px;
                           
            }
            QPushButton:hover {
                background-color: #3f51b5
                
;
            }

            QTableWidget {
                background-color: white;
                border-radius: 10px;
                gridline-color: #e0e0e0;
            }
        """)

    # ---------- Update Name ----------
    def update_name(self, text):
        if text == "Select Student ID":
            self.name_label.setText("")
        else:
            self.name_label.setText(self.students.get(text, ""))

    # Cal grade
    def get_grade(self, avg):
        if avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    #add student
    def add_student(self):
        student_id = self.id_combo.currentText()

        if student_id == "Select Student ID":
            QMessageBox.warning(self, "Warning", "Please select Student ID")
            return

        name = self.students[student_id]
        math = self.math_input.value()
        science = self.science_input.value()
        english = self.english_input.value()

        total = math + science + english
        average = total / 3
        grade = self.get_grade(average)

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(student_id))
        self.table.setItem(row, 1, QTableWidgetItem(name))
        self.table.setItem(row, 2, QTableWidgetItem(str(math)))
        self.table.setItem(row, 3, QTableWidgetItem(str(science)))
        self.table.setItem(row, 4, QTableWidgetItem(str(english)))
        self.table.setItem(row, 5, QTableWidgetItem(str(total)))
        self.table.setItem(row, 6, QTableWidgetItem(f"{average:.2f}"))
        self.table.setItem(row, 7, QTableWidgetItem(grade))

        self.sort_table()

    #Sort tabel
    def sort_table(self):
        self.table.sortItems(0)

    #Reset buttom
    def reset_input(self):
        self.id_combo.setCurrentIndex(0)
        self.name_label.setText("")
        self.math_input.setValue(0)
        self.science_input.setValue(0)
        self.english_input.setValue(0)

    #Clear buttom
    def clear_all(self):
        self.table.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    #Arabic
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

    window = StudentGradeCalculator()
    window.show()
    sys.exit(app.exec())
