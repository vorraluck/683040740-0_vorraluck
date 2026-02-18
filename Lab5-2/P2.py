import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtWidgets import QPushButton, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
m = "meters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        owTitle("P1: BMI Calself.setWindculator")
        self.setGeometry(100, 100, 300, 450)

        # Create central widget and layout
        

        # Create an input section object
        input_section = InputSection()
        
        # create an output section object
        output_section = OutputSection()

        result_container = QWidget()
        result_container.setStyleSheet("background-color: #FAF0E6;")  # Linen color
        result_container.setLayout(output_section)

        # connect signals from clicking submit and clear buttons
        


class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()


    def show_adult_table(self):
        table_layout = QGridLayout()
        label = QLabel("BMI")
        label.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout.addWidget(label, 0, 0, Qt.AlignCenter)
        label = QLabel("Condition")
        label.setFont(QFont("Arial", 10, QFont.Bold))
        table_layout.addWidget(label, 0, 1)
        
        self.addLayout(table_layout)

    def show_child_link(self):
        
        link_layout = QHBoxLayout()
        boy_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf?sfvrsn=4007e921_4">BMI graph for BOYS</a>')
        girl_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf?sfvrsn=c708a56b_4">BMI graph for GIRLS</a>')
        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)
        

    def update_results(self, bmi, age_group):
        pass
    
    def clear_result(self):
        
        while self.count() > 3:
            item = self.takeAt(3)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

class InputSection(QWidget):

    def __init__(self):
        super().__init__()

        

    def clear_form(self, output_section):
        # clear input form

        # clear output section
        output_section.clear_result()

    def submit_reg(self, output_section):
        pass

    def calculate_BMI(self):
        pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()