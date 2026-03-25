import sys
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QRadioButton, QButtonGroup, QDateEdit
)
from PyQt5.QtCore import QDate


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P2: Student Registration")
        self.setFixedSize(500, 750)

        layout = QVBoxLayout()

        #Full name
        name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addSpacing(20)

        #Email
        email_label = QLabel("Email: ")
        self.email_input = QLineEdit()

        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addSpacing(20)

        #phone number
        phone_label = QLabel("Phone: ")
        self.phone_input = QLineEdit()

        layout.addWidget(phone_label)
        layout.addWidget(self.phone_input)
        layout.addSpacing(20)

        #Date of Birth(dd//MM/yyyy)
        day_label = QLabel("Date of Birth: ")
        layout.addWidget(day_label) 
        layout.addSpacing(20)

        # Create calendar field
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)  # Shows calendar dropdown
        date_edit.setDisplayFormat("M/dd/yy")  # Format like "2/19/00"
        date_edit.setDate(QDate(2000, 2, 19))  # Set default date
        layout.addWidget(date_edit)

        #Gender
        gender_label = QLabel("Gender: ")
        layout.addWidget(gender_label)

        # Button group ensures only one can be selected
        self.gender_group = QButtonGroup()
        
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.nonbi_radio = QRadioButton("Non-Binary")
        self.nottosay_radio = QRadioButton("Prefer not to say")

        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.nonbi_radio)
        self.gender_group.addButton(self.nottosay_radio)
        
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.male_radio)
        radio_layout.addWidget(self.female_radio)
        radio_layout.addWidget(self.nonbi_radio)
        radio_layout.addWidget(self.nottosay_radio)

        layout.addLayout(radio_layout)
        layout.addSpacing(20)

        #program
        program_label = QLabel("Program: ")
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
        layout.addSpacing(20)

        # Submit button
        self.submit_button = QPushButton("Submit")
        #Tell us
        tell_label = QLabel("Tell us about yourself: ")
        self.tell_input = QTextEdit()
        self.tell_input.setFixedHeight(100)

        layout.addWidget(tell_label)
        layout.addWidget(self.tell_input)

        # accept terms
        self.terms_checkbox = QCheckBox("I accept the terms and conditions.")
        layout.addWidget(self.terms_checkbox)
        layout.addSpacing(20)

        layout.addStretch()  

        layout.addWidget(self.submit_button)
        layout.addSpacing(20)
        
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())
