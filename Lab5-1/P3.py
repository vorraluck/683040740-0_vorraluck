# Name: Your Name
# Student ID: 12345678

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QGridLayout, QFrame
)
from PySide6.QtCore import Qt


class BMIUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.resize(420, 650)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # ===== Title =====
        title = QLabel("Adult and Child BMI Calculator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            background-color: #b64937;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 6px;
            border-radius: 5px;
        """)
        main_layout.addWidget(title)
        main_layout.addSpacing(20)

        # ===== Age Group =====
        age_layout = QHBoxLayout()
        age_label = QLabel("Calculate BMI for")
        age_combo = QComboBox()
        age_combo.addItems(["Adult Age 20+", "Child Age 2-19"])

        age_layout.addWidget(age_label)
        age_layout.addWidget(age_combo)
        age_layout.addStretch()
        main_layout.addLayout(age_layout)

        main_layout.addSpacing(20)

        # ===== Weight =====
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Weight:")
        weight_input = QLineEdit()
        weight_input.setFixedWidth(80)

        weight_unit = QComboBox()
        weight_unit.addItems(["pounds", "kilograms"])

        weight_layout.addWidget(weight_label)
        weight_layout.addSpacing(10)
        weight_layout.addWidget(weight_input)
        weight_layout.addWidget(weight_unit)
        weight_layout.addStretch()
        main_layout.addLayout(weight_layout)

        main_layout.addSpacing(15)

        # ===== Height (Feet row) =====
        height_layout1 = QHBoxLayout()
        height_label = QLabel("Height:")
        height_feet = QLineEdit()
        height_feet.setFixedWidth(80)

        height_unit = QComboBox()
        height_unit.addItems(["feet", "meters", "centimeters"])

        height_layout1.addWidget(height_label)
        height_layout1.addSpacing(10)
        height_layout1.addWidget(height_feet)
        height_layout1.addWidget(height_unit)
        height_layout1.addStretch()
        main_layout.addLayout(height_layout1)

        # ===== Height (Inches row) =====
        height_layout2 = QHBoxLayout()
        height_layout2.addSpacing(80)
        height_inches = QLineEdit()
        height_inches.setFixedWidth(80)
        inches_label = QLabel("inches")

        height_layout2.addWidget(height_inches)
        height_layout2.addWidget(inches_label)
        height_layout2.addStretch()
        main_layout.addLayout(height_layout2)

        main_layout.addSpacing(25)

        # ===== Buttons =====
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        calc_btn = QPushButton("Calculate")

        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(calc_btn)
        main_layout.addLayout(button_layout)

        main_layout.addSpacing(25)

        # ===== Answer Section =====
        answer_frame = QFrame()
        answer_frame.setFrameShape(QFrame.Box)

        answer_layout = QVBoxLayout()

        answer_label = QLabel("Answer:")
        bmi_label = QLabel("BMI =")
        bmi_label.setAlignment(Qt.AlignCenter)
        bmi_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        adult_label = QLabel("Adult BMI")
        adult_label.setAlignment(Qt.AlignCenter)
        adult_label.setStyleSheet("font-weight: bold;")

        # ===== BMI Table =====
        table = QGridLayout()

        table.addWidget(QLabel("BMI"), 0, 0)
        table.addWidget(QLabel("Status"), 0, 1)

        table.addWidget(QLabel("≤ 18.4"), 1, 0)
        table.addWidget(QLabel("Underweight"), 1, 1)

        table.addWidget(QLabel("18.5 - 24.9"), 2, 0)
        table.addWidget(QLabel("Normal"), 2, 1)

        table.addWidget(QLabel("25.0 - 39.9"), 3, 0)
        table.addWidget(QLabel("Overweight"), 3, 1)

        table.addWidget(QLabel("≥ 40.0"), 4, 0)
        table.addWidget(QLabel("Obese"), 4, 1)

        answer_layout.addWidget(answer_label)
        answer_layout.addSpacing(10)
        answer_layout.addWidget(bmi_label)
        answer_layout.addSpacing(15)
        answer_layout.addWidget(adult_label)
        answer_layout.addLayout(table)

        answer_frame.setLayout(answer_layout)
        main_layout.addWidget(answer_frame)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMIUI()
    window.show()
    sys.exit(app.exec())

