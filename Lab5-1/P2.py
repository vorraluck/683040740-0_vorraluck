import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QTextEdit, QRadioButton,
    QButtonGroup, QDateEdit, QCheckBox
)
from PySide6.QtCore import QDate, QLocale, Qt

class StudentRegistration(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P2: Student Registration")
        self.setFixedSize(400, 600)

        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Student Registration Form")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)
        main_layout.addSpacing(20)

        # Full Name
        main_layout.addWidget(QLabel("Full Name:"))
        main_layout.addWidget(QLineEdit())
        main_layout.addSpacing(10)

        # Email
        main_layout.addWidget(QLabel("Email:"))
        main_layout.addWidget(QLineEdit())
        main_layout.addSpacing(10)

        # Phone
        main_layout.addWidget(QLabel("Phone:"))
        main_layout.addWidget(QLineEdit())
        main_layout.addSpacing(15)

        # Date of Birth
        main_layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)

        # arabic
        date_edit.setLocale(QLocale.c())

        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setDate(QDate(2000, 1, 1))
        main_layout.addWidget(date_edit)
        main_layout.addSpacing(20)

        # Gender
        main_layout.addWidget(QLabel("Gender:"))
        gender_layout = QHBoxLayout()

        gender_group = QButtonGroup(self)
        male = QRadioButton("Male")
        female = QRadioButton("Female")

        gender_group.addButton(male)
        gender_group.addButton(female)

        gender_layout.addWidget(male)
        gender_layout.addWidget(female)

        main_layout.addLayout(gender_layout)
        main_layout.addSpacing(20)

        # Program
        main_layout.addWidget(QLabel("Program:"))
        program_combo = QComboBox()
        program_combo.addItems([
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electical Engineering",
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Power Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ])
        main_layout.addWidget(program_combo)
        main_layout.addSpacing(20)

        # About yourself
        main_layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        about = QTextEdit()
        about.setMaximumHeight(100)
        main_layout.addWidget(about)
        main_layout.addSpacing(20)

        # Terms
        main_layout.addWidget(QCheckBox("I accept the terms and conditions."))
        main_layout.addSpacing(20)

        # Submit button
        submit_btn = QPushButton("Submit Registration")
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(submit_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentRegistration()
    window.show()
    sys.exit(app.exec())
