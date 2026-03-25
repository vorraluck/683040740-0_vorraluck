#Vorraluck Taladon
#683040740-0

import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QSlider, QPushButton,
    QProgressBar, QToolBar, QStatusBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
 
 
class CharacterBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Builder")
        self.resize(900, 520)
 
        self.initUI()
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
 
    # ================= UI =================
    def initUI(self):
        main = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(20)
 
        # ===== LEFT =====
        left = QVBoxLayout()
 
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter character name...")
 
        self.race = QComboBox()
        self.race.addItems(["Choose race", "Human", "Elf", "Dwarf", "Orc", "Undead"])
 
        self.cls = QComboBox()
        self.cls.addItems(["Choose class", "Warrior", "Mage", "Rogue", "Paladin", "Ranger"])
 
        self.gender = QComboBox()
        self.gender.addItems(["Choose gender", "Male", "Female", "Other"])
 
        left.addWidget(QLabel("Character Name"))
        left.addWidget(self.name)
        left.addWidget(QLabel("Race"))
        left.addWidget(self.race)
        left.addWidget(QLabel("Class"))
        left.addWidget(self.cls)
        left.addWidget(QLabel("Gender"))
        left.addWidget(self.gender)
 
        # ===== STAT =====
        title = QLabel("Stat Allocation")
        title.setStyleSheet("font-weight: bold; color:#7c5cff;")
        left.addWidget(title)
 
        self.sliders = {}
        self.values = {}
 
        # ✅ Bug 1 fixed: emoji strings on a single line (no mid-string newlines)
        icons = {
            "STR": "⚔ ",
            "DEX": "🏃 ",
            "INT": "🔮 ",
            "VIT": "❤ ",
        }
 
        for stat in ["STR", "DEX", "INT", "VIT"]:
            row = QHBoxLayout()
 
            label = QLabel(f"{icons[stat]} {stat}")
            slider = QSlider(Qt.Horizontal)
            slider.setRange(1, 20)
            slider.setValue(5)
 
            value = QLabel("5")
            value.setFixedWidth(20)
 
            slider.valueChanged.connect(self.update_points)
            slider.valueChanged.connect(lambda v, s=stat: self.values[s].setText(str(v)))
 
            self.sliders[stat] = slider
            self.values[stat] = value
 
            row.addWidget(label)
            row.addWidget(slider)
            row.addWidget(value)
 
            left.addLayout(row)
 
        self.point_label = QLabel("Points used: 20 / 40")
        left.addWidget(self.point_label)
 
        # ===== BUTTON =====
        # ✅ Bug 1 fixed: emoji on same line
        btn = QPushButton("🗡 Generate Character Sheet")
        btn.clicked.connect(self.generate)
        left.addWidget(btn)
 
        # ===== RIGHT PANEL =====
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignTop)
 
        self.title_label = QLabel("— Character Name —")
        self.sub_label = QLabel("Race • Class")
 
        self.title_label.setStyleSheet("color:#d7c8ff; font-size:18px; font-weight:bold;")
        self.sub_label.setStyleSheet("color:#aaa;")
 
        right.addWidget(self.title_label)
        right.addWidget(self.sub_label)
 
        self.bars = {}
        for stat in ["STR", "DEX", "INT", "VIT"]:
            bar = QProgressBar()
            bar.setRange(0, 20)
            bar.setTextVisible(False)
            self.bars[stat] = bar
 
            right.addWidget(QLabel(stat))
            right.addWidget(bar)
 
        right_widget = QWidget()
        right_widget.setLayout(right)
        right_widget.setFixedWidth(260)
        # ✅ Bug 4 fixed: added QWidget selector so styles actually apply
        right_widget.setStyleSheet("""
            QWidget {
                background-color: #1c1c2b;
                border-radius: 12px;
                padding: 12px;
            }
            QLabel {
                color: #aaa;
                background: transparent;
            }
        """)
 
        layout.addLayout(left, 2)
        layout.addWidget(right_widget, 1)
 
        main.setLayout(layout)
        self.setCentralWidget(main)
 
        self.apply_style()
 
    # ================= LOGIC =================
    def update_points(self):
        total = sum(sl.value() for sl in self.sliders.values())
        self.point_label.setText(f"Points used: {total} / 40")
 
        if total > 40:
            self.point_label.setStyleSheet("color:red; font-weight:bold;")
        else:
            self.point_label.setStyleSheet("color:black;")
 
    def generate(self):
        total = sum(sl.value() for sl in self.sliders.values())
        if total > 40:
            QMessageBox.warning(self, "Error", "Max 40 points!")
            return
 
        name = self.name.text() or "Unknown"
        self.title_label.setText(f"— {name} —")
 
        # ✅ Bug 2 fixed: f-string on a single line (no mid-string newline)
        self.sub_label.setText(f"{self.race.currentText()} • {self.cls.currentText()}")
 
        for stat in self.sliders:
            self.bars[stat].setValue(self.sliders[stat].value())
 
        self.status.showMessage("Character Generated!", 3000)
 
    def randomize(self):
        total = 0
        for stat in self.sliders:
            val = random.randint(1, 20)
            self.sliders[stat].setValue(val)
            total += val
 
        while total > 40:
            s = random.choice(list(self.sliders.keys()))
            if self.sliders[s].value() > 1:
                self.sliders[s].setValue(self.sliders[s].value() - 1)
                total -= 1
 
        self.status.showMessage("Randomized!", 3000)
 
    def reset_stats(self):
        for s in self.sliders.values():
            s.setValue(5)
        # ✅ Bug 5 fixed: update point_label after reset
        self.update_points()
 
    def new_character(self):
        self.name.clear()
        self.race.setCurrentIndex(0)
        self.cls.setCurrentIndex(0)
        self.gender.setCurrentIndex(0)
        self.reset_stats()
        # ✅ Bug 6 fixed: reset_stats now calls update_points, so label updates here too
 
    def save_sheet(self):
        # ✅ Bug 3 fixed: file filter string on one line (no mid-string newline)
        path, _ = QFileDialog.getSaveFileName(self, "Save", "", "Text Files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write(self.get_text())
            self.status.showMessage("Saved!", 3000)
 
    def get_text(self):
        txt = f"{self.name.text()}\n"
        txt += f"{self.race.currentText()} - {self.cls.currentText()}\n"
        for s in self.sliders:
            txt += f"{s}: {self.sliders[s].value()}\n"
        return txt
 
    # ================= MENU =================
    def create_menu(self):
        menu = self.menuBar()
 
        game = menu.addMenu("Game")
        game.addAction("New Character", self.new_character)
        game.addAction("Generate Sheet", self.generate)
        game.addAction("Save Sheet", self.save_sheet)
        game.addAction("Exit", self.close)
 
        edit = menu.addMenu("Edit")
        edit.addAction("Reset Stats", self.reset_stats)
        edit.addAction("Randomize", self.randomize)
 
    # ================= TOOLBAR =================
    def create_toolbar(self):
        tb = QToolBar()
        self.addToolBar(tb)
 
        tb.setMovable(False)
        tb.setStyleSheet("""
            QToolBar {
                spacing: 10px;
                padding: 5px;
            }
            QToolButton {
                padding: 5px 8px;
            }
        """)
 
        # ✅ Bug 1 fixed: all emoji labels on single lines
        tb.addAction("🆕 New", self.new_character)
        tb.addSeparator()
        tb.addAction("⚔ Generate", self.generate)
        tb.addSeparator()
        tb.addAction("🎲 Randomize", self.randomize)
        tb.addSeparator()
        tb.addAction("💾 Save", self.save_sheet)
 
    # ================= STATUS =================
    def create_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Created by YourName")
 
    # ================= STYLE =================
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 13px;
            }
 
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
 
            QPushButton {
                border: 2px solid #7c5cff;
                color: #7c5cff;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
 
            QPushButton:hover {
                background-color: #7c5cff;
                color: white;
            }
 
            QSlider::groove:horizontal {
                height: 6px;
                background: #ddd;
                border-radius: 3px;
            }
 
            QSlider::handle:horizontal {
                background: #4a90e2;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
 
            QProgressBar {
                background: #333;
                border-radius: 6px;
            }
 
            QProgressBar::chunk {
                background: #7c5cff;
                border-radius: 6px;
            }
        """)
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CharacterBuilder()
    window.show()
    sys.exit(app.exec())