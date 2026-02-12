# Name: Your Name
# Student ID: 12345678

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QGridLayout
)
from PySide6.QtCore import Qt


class BMICalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # ===== Title =====
        title = QLabel("Adult and Child BMI Calculator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)

        # ===== Input Section =====
        grid = QGridLayout()

        grid.addWidget(QLabel("BMI age group:"), 0, 0)
        self.age_combo = QComboBox()
        self.age_combo.addItems(["Adults 20+", "Children (2-19)"])
        grid.addWidget(self.age_combo, 0, 1, 1, 2)

        grid.addWidget(QLabel("Weight:"), 1, 0)
        self.weight_input = QLineEdit()
        grid.addWidget(self.weight_input, 1, 1)

        self.weight_unit = QComboBox()
        self.weight_unit.addItems(["kilograms", "pounds"])
        grid.addWidget(self.weight_unit, 1, 2)

        grid.addWidget(QLabel("Height:"), 2, 0)
        self.height_input = QLineEdit()
        grid.addWidget(self.height_input, 2, 1)

        self.height_unit = QComboBox()
        self.height_unit.addItems(["centimeters", "inches"])
        grid.addWidget(self.height_unit, 2, 2)

        main_layout.addLayout(grid)

        # ===== Buttons =====
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("clear")
        self.submit_btn = QPushButton("Submit Registration")

        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.submit_btn)
        main_layout.addLayout(button_layout)

        # ===== Result Container (IMPORTANT PART) =====
        self.result_container = QWidget()
        self.result_container.setStyleSheet("background-color: #FAF0E6;")

        layout_output = QVBoxLayout()

        self.result_title = QLabel("Your BMI")
        self.result_title.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("0.00")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size:30px; font-weight:bold;")

        # BMI table text
        self.condition_label = QLabel(
            "\nBMI\t\tCondition\n"
            "< 18.5\t\tThin\n"
            "18.5 - 25.0\tNormal\n"
            "25.1 - 30.0\tOverweight\n"
            "> 30.0\t\tObese"
        )
        self.condition_label.setAlignment(Qt.AlignCenter)

        layout_output.addWidget(self.result_title)
        layout_output.addWidget(self.result_label)
        layout_output.addWidget(self.condition_label)
        layout_output.addStretch()

        self.result_container.setLayout(layout_output)

        main_layout.addWidget(self.result_container)

        self.setLayout(main_layout)

        # ===== Connections =====
        self.submit_btn.clicked.connect(self.calculate_bmi)
        self.clear_btn.clicked.connect(self.clear_fields)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())

            # Convert units
            if self.weight_unit.currentText() == "pounds":
                weight *= 0.453592

            if self.height_unit.currentText() == "inches":
                height *= 2.54

            height_m = height / 100
            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 2)

            self.result_label.setText(f"{bmi:.2f}")

        except ValueError:
            self.result_label.setText("0.00")

    def clear_fields(self):
        self.weight_input.clear()
        self.height_input.clear()
        self.result_label.setText("0.00")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.resize(450, 500)
    window.show()
    sys.exit(app.exec())
