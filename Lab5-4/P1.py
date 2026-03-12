## For Master ##

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
                               QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
                               QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor, QIcon, QPixmap
import sys, os
import pyperclip 

default_color = "#C5D6BA"

class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(100, 100, 400, 500)

         # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.addSpacing(15)

        # input section
        self.input_layout = QFormLayout()
        self.input_layout.setVerticalSpacing(12)
        self.create_form()

        self.main_layout.addSpacing(5)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setLineWidth(1)
        line.setStyleSheet("background-color: #cccccc;")

        # Output section
        self.bg_widget = QWidget()
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.create_display()
        self.main_layout.addWidget(self.bg_widget)

        # menu
        self.create_menu()
        # toolbar
        self.create_toolbar()
        # status bar
        self.statusBar().showMessage("Fill in your details and click generate") 

    def create_form(self):
        form_container = QWidget()
        self.input_layout = QFormLayout(form_container)
        self.input_layout.setSpacing(12)
        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("First name and Lastname")
        
        self.age = QSpinBox()
        self.age.setRange(1, 120)
        self.age.setValue(25) 
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("username@domain.name")

        self.position = QComboBox()
        self.position.addItems(["Teaching Staff", "Supporting Staff", "Student", "Visitor"])
        self.position.setPlaceholderText("Choose your position")
        self.position.setCurrentIndex(-1)

        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        self.fav_color = QColor(default_color)
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(f"background-color: {self.fav_color.name()}; border: 1px solid #888;")
        color_layout.addWidget(self.color_swatch)
        color_btn = QPushButton("Pick New Color")
        color_btn.clicked.connect(self.pick_color)
        
        color_layout.addWidget(self.color_swatch)
        color_layout.addWidget(color_btn)
        color_layout.addStretch()

        self.input_layout.addRow("Full name:", self.full_name)
        self.input_layout.addRow("Age:", self.age)
        self.input_layout.addRow("Email:", self.email)
        self.input_layout.addRow("Position:", self.position)
        self.input_layout.addRow("Your favorite color:", color_row)
        
        self.main_layout.addWidget(form_container)

    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(f"background-color: {self.fav_color.name()}; border: 1px solid #888;")

    def create_display(self):
        self.bg_widget.setStyleSheet(f"background-color: {default_color}; border-radius: 12px;")
        self.bg_widget.setMinimumHeight(180)
        
        self.name_label = QLabel("Your name here")
        self.name_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.age_label = QLabel("(Age)")
        self.position_label = QLabel("Your position here")
        self.position_label.setStyleSheet("font-size: 14pt;")
        email_icon = QLabel()
        email_icon.setPixmap(QPixmap("mail.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.email_label = QLabel("your_username@domain.name")

        self.output_layout.addSpacing(10)
        self.output_layout.addWidget(self.name_label)
        self.output_layout.addWidget(self.age_label)
        self.output_layout.addSpacing(10)
        self.output_layout.addWidget(self.position_label)
        self.output_layout.addWidget(self.email_label)
        self.output_layout.addStretch()

    def update_display(self):
        name = self.full_name.text()
        age = self.age.value()
        email = self.email.text()
        position = self.position.currentText()

        if name == '':
            print("Please enter your name.")
            self.statusBar().showMessage("Please enter your name.")
            return
        if age < 18:
            print("Please enter your age.")
            self.statusBar().showMessage("Please enter your age.")
            return
        if email == '':
            print("Please enter your email.")
            self.statusBar().showMessage("Please enter your email.")
            return
        if position == '':
            print("Please select your position.")
            self.statusBar().showMessage("Please select your position.")
            return

        self.position_label.setText(position)
        
        
        self.name_label.setText(name)
        self.age_label.setText(f"({self.age.text()})")
        self.position_label.setText(position)
        self.email_label.setText(f"{email}") 
        
        self.bg_widget.setStyleSheet(f"background-color: {self.fav_color.name()}; border-radius: 12px;")
        self.statusBar().showMessage("Card copied to clipboard")

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Card", "my_card.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                content = f"{self.name_label.text()}\n({self.age.text()})\n{self.position_label.text()}\n{self.email_label.text()}"
                f.write(content)
            self.statusBar().showMessage(f"Save card, displaying {os.path.basename(filename)}")

    def copy_card(self):
        text = f"{self.name_label.text()}\n({self.age.text()})\n{self.position_label.text()}\n{self.email_label.text()}"
        pyperclip.copy(text)
        self.statusBar().showMessage("Copy card")

    def clear_all(self):
        self.full_name.clear()
        self.age.setValue(25)
        self.position.setCurrentIndex(-1)
        self.email.clear()
        self.name_label.setText("Your name here")
        self.age_label.setText("(Age)")
        self.position_label.setText("Your position here")
        self.email_label.setText("your_username@domain.name")
        self.bg_widget.setStyleSheet(f"background-color: {default_color}; border-radius: 12px;")
        self.statusBar().showMessage("Clear both form and display")

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("Generate Card", self.update_display)
        file_menu.addAction("Save Card", self.save_card)
        file_menu.addAction("Clear Display", lambda: [self.name_label.setText("Your name here"), self.statusBar().showMessage("Clear display")])
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        edit_menu = menubar.addMenu("&Edit") 
        edit_menu.addAction("Copy Card", self.copy_card)
        edit_menu.addAction("Clear Form", lambda: [self.full_name.clear(), self.statusBar().showMessage("Clear form")])


    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        action1 = QAction(QIcon("Lab5-4/next.png"),"next.png",self)
        action1.triggered.connect(self.update_display)
        toolbar.addAction(action1)
        action2 = QAction(QIcon("Lab5-4/save.png"),"Save",self)
        action2.triggered.connect(self.save_card)
        toolbar.addAction(action2)
        action3 = QAction(QIcon("Lab5-4/clear.png"),"Clear All",self)
        action3.triggered.connect(self.clear_all)
        toolbar.addAction(action3)

def main():
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
    QLineEdit {
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 4px 8px;
    background: #fafafa;
}
QLineEdit:focus {
    border: 1px solid #6c8ebf;
    background: #fff;
}

QComboBox {
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 4px 8px;
    background: #fafafa;
}
QComboBox:focus {
    border: 1px solid #6c8ebf;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}

QSpinBox {
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 4px 8px;
        background: #fafafa;
    }
    QSpinBox:focus {
        border: 1px solid #6c8ebf;
    }
QSpinBox::up-button:hover  { background: #e0e8f8; }
QSpinBox::up-button:pressed { background: #6c8ebf; }
QSpinBox::down-button:hover  { background: #e0e8f8; }
QSpinBox::down-button:pressed { background: #6c8ebf; }

QPushButton {
        border: 1px solid #6c8ebf;
        border-radius: 6px;
        padding: 5px 14px;
        background: #e8f0fb;
        color: #2c4a7c;
    }
    QPushButton:hover   { background: #d0e2f8; }
    QPushButton:pressed { background: #6c8ebf; color: #fff; }
    QPushButton:disabled { background: #eee; color: #aaa; border-color: #ddd; }

    """)

    window = PersonalCard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
