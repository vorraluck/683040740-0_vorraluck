#Vorraluck Taladon
#683040740-0

import sys
import math
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor

C_BG      = "#F3F3F3"
C_WHITE   = "#FFFFFF"
C_BTN     = "#F9F9F9"
C_BTN_HV  = "#E8E8E8"
C_BTN_PR  = "#D0D0D0"
C_TEXT    = "#1A1A1A"
C_MUTED   = "#888888"
C_BORDER  = "#DEDEDE"

def fnt(size=13, bold=False):
    f = QFont("Segoe UI", size)
    if bold:
        f.setWeight(QFont.Weight.Bold)
    return f

def center_window(win):
    geo = QApplication.primaryScreen().availableGeometry()
    win.move((geo.width() - win.width()) // 2, (geo.height() - win.height()) // 2)

def make_btn(text):
    btn = QPushButton(text)
    btn.setFixedSize(72, 56)
    btn.setFont(fnt(13))
    btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    btn.setStyleSheet(f"""
        QPushButton {{
            background: {C_BTN}; color: {C_TEXT};
            border: 1px solid {C_BORDER}; border-radius: 4px;
        }}
        QPushButton:hover   {{ background: {C_BTN_HV}; }}
        QPushButton:pressed {{ background: {C_BTN_PR}; }}
    """)
    return btn

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(340, 540)
        center_window(self)
        self.setStyleSheet(f"background: {C_BG};")
        self._expr = ""
        self._just_evaluated = False
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(0)

        heading = QLabel("Standard")
        heading.setFont(fnt(16, bold=True))
        heading.setStyleSheet(f"color: {C_TEXT}; background: transparent;")
        root.addWidget(heading)
        root.addSpacing(8)

        display = QWidget()
        display.setStyleSheet(f"background: {C_WHITE}; border-radius: 6px;")
        display.setFixedHeight(110)
        d_lay = QVBoxLayout(display)
        d_lay.setContentsMargins(12, 8, 12, 8)
        d_lay.setSpacing(2)

        self.expr_lbl = QLabel("")
        self.expr_lbl.setFont(fnt(14))
        self.expr_lbl.setStyleSheet(f"color: {C_MUTED}; background: transparent;")
        self.expr_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.result_lbl = QLabel("0")
        self.result_lbl.setFont(fnt(34, bold=True))
        self.result_lbl.setStyleSheet(f"color: {C_TEXT}; background: transparent;")
        self.result_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        d_lay.addWidget(self.expr_lbl)
        d_lay.addWidget(self.result_lbl)
        root.addWidget(display)
        root.addSpacing(12)

        grid = QGridLayout()
        grid.setSpacing(6)

        buttons = [
            [("%", self._pct),    ("CE", self._ce),       ("C", self._clear),    ("<-", self._backspace)],
            [("1/x", self._reciprocal), ("x^2", self._square), ("sqrt(x)", self._sqrt), ("/", lambda: self._op("/"))],
            [("7", lambda: self._digit("7")), ("8", lambda: self._digit("8")), ("9", lambda: self._digit("9")), ("x", lambda: self._op("*"))],
            [("4", lambda: self._digit("4")), ("5", lambda: self._digit("5")), ("6", lambda: self._digit("6")), ("-", lambda: self._op("-"))],
            [("1", lambda: self._digit("1")), ("2", lambda: self._digit("2")), ("3", lambda: self._digit("3")), ("+", lambda: self._op("+"))],
            [("+/-", self._negate), ("0", lambda: self._digit("0")), (".", lambda: self._digit(".")), ("=", self._evaluate)],
        ]

        for r, row in enumerate(buttons):
            for c, (label, action) in enumerate(row):
                btn = make_btn(label)
                btn.clicked.connect(action)
                grid.addWidget(btn, r, c)

        root.addLayout(grid)

    def _update(self):
        self.expr_lbl.setText(self._expr)
        if self._expr:
            try:
                val = eval(self._expr)
                self.result_lbl.setText(self._fmt(val))
            except Exception:
                self.result_lbl.setText(self._expr[-1] if self._expr else "0")
        else:
            self.result_lbl.setText("0")

    def _fmt(self, val):
        if isinstance(val, float):
            if val == int(val):
                return str(int(val))
            return f"{val:.10g}"
        return str(val)

    def _current_val(self):
        try:
            return float(eval(self._expr)) if self._expr else 0.0
        except Exception:
            return 0.0

    def _digit(self, d):
        if self._just_evaluated:
            self._expr = ""
            self._just_evaluated = False
        self._expr += d
        self._update()

    def _op(self, op):
        self._just_evaluated = False
        self._expr += op
        self._update()

    def _backspace(self):
        self._expr = self._expr[:-1]
        self._update()

    def _ce(self):
        self._expr = re.sub(r'[\d.]+$', '', self._expr)
        self._update()

    def _clear(self):
        self._expr = ""
        self._just_evaluated = False
        self.expr_lbl.setText("")
        self.result_lbl.setText("0")

    def _pct(self):
        try:
            val = self._current_val()
            result = val / 100
            self.expr_lbl.setText(f"{self._expr}%")
            self._expr = self._fmt(result)
            self.result_lbl.setText(self._expr)
            self._just_evaluated = True
        except Exception:
            self.result_lbl.setText("Error")

    def _negate(self):
        try:
            val = self._current_val()
            result = -val
            self.expr_lbl.setText(f"negate({self._expr})")
            self._expr = self._fmt(result)
            self.result_lbl.setText(self._expr)
            self._just_evaluated = True
        except Exception:
            self.result_lbl.setText("Error")

    def _reciprocal(self):
        try:
            val = self._current_val()
            if val == 0:
                self.result_lbl.setText("Cannot divide by zero")
                return
            result = 1 / val
            self.expr_lbl.setText(f"1/({self._expr})")
            self._expr = self._fmt(result)
            self.result_lbl.setText(self._expr)
            self._just_evaluated = True
        except Exception:
            self.result_lbl.setText("Error")

    def _square(self):
        try:
            val = self._current_val()
            result = val ** 2
            self.expr_lbl.setText(f"({self._expr})^2")
            self._expr = self._fmt(result)
            self.result_lbl.setText(self._expr)
            self._just_evaluated = True
        except Exception:
            self.result_lbl.setText("Error")

    def _sqrt(self):
        try:
            val = self._current_val()
            if val < 0:
                self.result_lbl.setText("Invalid input")
                return
            result = math.sqrt(val)
            self.expr_lbl.setText(f"sqrt({self._expr})")
            self._expr = self._fmt(result)
            self.result_lbl.setText(self._expr)
            self._just_evaluated = True
        except Exception:
            self.result_lbl.setText("Error")

    def _evaluate(self):
        if not self._expr:
            return
        try:
            result = eval(self._expr)
            self.expr_lbl.setText(self._expr + " =")
            self._expr = self._fmt(result)
            self.result_lbl.setText(self._expr)
            self._just_evaluated = True
        except ZeroDivisionError:
            self.result_lbl.setText("Cannot divide by zero")
            self._expr = ""
        except Exception:
            self.result_lbl.setText("Error")
            self._expr = ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Calculator")
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    w = Calculator()
    w.show()
    sys.exit(app.exec())