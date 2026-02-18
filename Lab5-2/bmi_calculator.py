import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QGridLayout,
                             QWidget, QLabel, QLineEdit, QPushButton, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
inch = "inches"

adult = "Adults 20+"
child = "Children and Teenagers (5-19)"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 400, 500)

        # Create central widget and layout


        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Sections
        self.input_section = InputSection()
        self.output_section = OutputSection()

        result_container = QWidget()
        result_container.setStyleSheet("background-color: #FAF0E6;")
        result_container.setLayout(self.output_section.layout)

        main_layout.addWidget(self.input_section)
        main_layout.addWidget(result_container)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect buttons
        self.input_section.submit_btn.clicked.connect(
            lambda: self.input_section.submit_reg(self.output_section)
        )

        self.input_section.clear_btn.clicked.connect(
            lambda: self.input_section.clear_form(self.output_section)
        )


class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.result_title = QLabel("Your BMI")
        self.result_title.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("0.00")
        self.result_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.result_title)
        self.layout.addWidget(self.result_label)

    def show_adult_table(self):
        table = QLabel(
            "\nBMI\t\tCondition\n"
            "< 18.5\t\tThin\n"
            "18.5 - 25.0\tNormal\n"
            "25.1 - 30.0\tOverweight\n"
            "> 30.0\t\tObese"
        )
        table.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(table)

    def show_child_link(self):
        boy_link = QLabel(
            '<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf">BMI graph for BOYS</a>'
        )
        girl_link = QLabel(
            '<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf">BMI graph for GIRLS</a>'
        )

        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)

        boy_link.setAlignment(Qt.AlignCenter)
        girl_link.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(boy_link)
        self.layout.addWidget(girl_link)

    def update_results(self, bmi, age_group):
        self.clear_result()
        self.result_label.setText(f"{bmi:.2f}")

        if age_group == adult:
            self.show_adult_table()
        else:
            self.show_child_link()

    def clear_result(self):
        while self.layout.count() > 2:
            item = self.layout.takeAt(2)
            if item.widget():
                item.widget().deleteLater()

        self.result_label.setText("0.00")


class InputSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        layout.addWidget(QLabel("BMI age group:"), 0, 0)
        self.age_combo = QComboBox()
        self.age_combo.addItems([adult, child])
        layout.addWidget(self.age_combo, 0, 1)

        layout.addWidget(QLabel("Weight:"), 1, 0)
        self.weight_input = QLineEdit()
        layout.addWidget(self.weight_input, 1, 1)

        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])
        layout.addWidget(self.weight_unit, 1, 2)

        layout.addWidget(QLabel("Height:"), 2, 0)
        self.height_input = QLineEdit()
        layout.addWidget(self.height_input, 2, 1)

        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, inch])
        layout.addWidget(self.height_unit, 2, 2)

        self.submit_btn = QPushButton("Submit")
        self.clear_btn = QPushButton("Clear")

        layout.addWidget(self.submit_btn, 3, 1)
        layout.addWidget(self.clear_btn, 3, 2)

        self.setLayout(layout)

    def clear_form(self, output_section):
        self.weight_input.clear()
        self.height_input.clear()
        output_section.clear_result()

    def submit_reg(self, output_section):
        bmi = self.calculate_BMI()
        if bmi:
            output_section.update_results(bmi, self.age_combo.currentText())

    def calculate_BMI(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())

            if self.weight_unit.currentText() == lb:
                weight *= 0.453592

            if self.height_unit.currentText() == inch:
                height *= 2.54

            height_m = height / 100
            bmi = weight / (height_m ** 2)

            return round(bmi, 2)

        except:
            return None


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
