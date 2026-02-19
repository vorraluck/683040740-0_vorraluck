import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QRadioButton, QButtonGroup, QDateEdit
)
from PyQt5.QtCore import QDate


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registration Form")
        self.setFixedSize(400, 600)

        layout = QVBoxLayout()

        # ===== Full Name =====
        name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addSpacing(15)

        # ===== Email =====
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()

        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addSpacing(15)

        # ===== Gender =====
        gender_label = QLabel("Gender:")
        layout.addWidget(gender_label)

        self.gender_group = QButtonGroup()

        gender_layout = QHBoxLayout()
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")

        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)

        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)

        layout.addLayout(gender_layout)
        layout.addSpacing(15)

        # ===== Date of Birth =====
        dob_label = QLabel("Date of Birth:")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("M/dd/yy")
        self.date_edit.setDate(QDate(2000, 1, 1))  # January 1, 2000

        layout.addWidget(dob_label)
        layout.addWidget(self.date_edit)
        layout.addSpacing(15)

        # ===== Program =====
        program_label = QLabel("Program:")
        self.program_combo = QComboBox()

        programs = [
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
        ]

        self.program_combo.addItems(programs)

        layout.addWidget(program_label)
        layout.addWidget(self.program_combo)
        layout.addSpacing(15)

        # ===== Address =====
        address_label = QLabel("Address:")
        self.address_text = QTextEdit()
        self.address_text.setMaximumHeight(100)

        layout.addWidget(address_label)
        layout.addWidget(self.address_text)
        layout.addSpacing(20)

        # ===== Submit Button =====
        self.submit_button = QPushButton("Submit")
        layout.addWidget(self.submit_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())
