#Vorraluck Taladon
#683040740-0

import sys
import os
import pyqtgraph as pg
from pyqtgraph import BarGraphItem
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton,
    QGroupBox, QMessageBox, QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QBrush, QPen, QPixmap


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

CATEGORIES = ["Electronics", "Clothing", "Food", "Others"]

# (R, G, B, A)
CATEGORY_COLORS = {
    "Electronics": (91,  155, 213, 220),
    "Clothing":    (237, 125,  49, 220),
    "Food":        (112, 173,  71, 220),
    "Others":      (255, 192,   0, 220),
}

PANEL_WIDTH = 225
BAR_WIDTH   = 0.18   # width of each individual bar
GROUP_GAP   = 1.0    # spacing between month groups



def field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #555; font-size: 12px;")
    return lbl


def rgba_to_hex(r, g, b, a=255) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"


class SalesChartApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Data Chart")
        self.setMinimumSize(1080, 660)

        # data[category][month_index] = total sales
        self.data: dict[str, list[float]] = {
            cat: [0.0] * 12 for cat in CATEGORIES
        }

        # pyqtgraph global style
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "#333")

        self._build_ui()
        self._refresh_chart()


    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(PANEL_WIDTH)
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            QWidget#sidebar {
                background: #F4F4F4;
                border-right: 1px solid #DDD;
            }
        """)
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(12, 14, 12, 14)
        sl.setSpacing(10)
        sl.addWidget(self._build_import_group())
        sl.addWidget(self._build_add_data_group())

        clear_btn = QPushButton("✕  Clear Chart")
        clear_btn.setFixedHeight(34)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: white; border: 1px solid #CCC;
                border-radius: 4px; color: #444; font-size: 12px;
            }
            QPushButton:hover   { background:#FFE8E8; border-color:#E07070; color:#C00; }
            QPushButton:pressed { background:#FFCECE; }
        """)
        clear_btn.clicked.connect(self._on_clear)
        sl.addWidget(clear_btn)
        sl.addStretch()
        root.addWidget(sidebar)

        # Chart area
        chart_container = QWidget()
        chart_container.setStyleSheet("background: white;")
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(10, 10, 10, 10)
        chart_layout.setSpacing(6)

        # Title label
        self.title_lbl = QLabel("Monthly Sales by Product Category")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        self.title_lbl.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #222; padding: 4px;"
        )
        chart_layout.addWidget(self.title_lbl)

        # pyqtgraph PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")
        self.plot_widget.showGrid(x=False, y=True, alpha=0.3)
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chart_layout.addWidget(self.plot_widget, 1)

        # Legend
        self.legend_widget = self._build_legend()
        chart_layout.addWidget(self.legend_widget, 0, Qt.AlignCenter)

        root.addWidget(chart_container, 1)

    def _build_import_group(self) -> QGroupBox:
        grp = QGroupBox("Import Data")
        grp.setStyleSheet(self._grp_style())
        layout = QVBoxLayout(grp)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(4)
        row.addWidget(QLabel("📄"))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("sales_data.txt")
        self.filename_input.setFixedHeight(26)
        self.filename_input.setStyleSheet(self._le_style())
        row.addWidget(self.filename_input)
        layout.addLayout(row)

        btn = QPushButton("🗀  Import Data")
        btn.setFixedHeight(32)
        btn.setStyleSheet("""
            QPushButton {
                background:#E8A020; color:white; border:none;
                border-radius:4px; font-size:12px; font-weight:bold;
            }
            QPushButton:hover   { background:#C8821A; }
            QPushButton:pressed { background:#A86510; }
        """)
        btn.clicked.connect(self._on_import)
        layout.addWidget(btn)
        return grp

    def _build_add_data_group(self) -> QGroupBox:
        grp = QGroupBox("Add Data")
        grp.setStyleSheet(self._grp_style())
        layout = QVBoxLayout(grp)
        layout.setSpacing(8)

        layout.addWidget(field_label("Month"))
        self.month_cb = QComboBox()
        self.month_cb.addItems(MONTHS)
        self.month_cb.setFixedHeight(28)
        self.month_cb.setStyleSheet(self._cb_style())
        layout.addWidget(self.month_cb)

        layout.addWidget(field_label("Sales Amount (฿)"))
        self.sales_input = QDoubleSpinBox()
        self.sales_input.setRange(0, 99_999_999)
        self.sales_input.setDecimals(0)
        self.sales_input.setSingleStep(1000)
        self.sales_input.setValue(10000)
        self.sales_input.setFixedHeight(28)
        self.sales_input.setStyleSheet("""
            QDoubleSpinBox {
                border:1px solid #CCC; border-radius:3px;
                padding:2px 6px; background:white; font-size:12px;
            }
            QDoubleSpinBox:focus { border-color:#5B9BD5; }
        """)
        layout.addWidget(self.sales_input)

        layout.addWidget(field_label("Product Category"))
        self.category_cb = QComboBox()
        self.category_cb.addItems(CATEGORIES)
        self.category_cb.setFixedHeight(28)
        self.category_cb.setStyleSheet(self._cb_style())
        layout.addWidget(self.category_cb)

        add_btn = QPushButton("＋  Add Data")
        add_btn.setFixedHeight(34)
        add_btn.setStyleSheet("""
            QPushButton {
                background:white; border:1px solid #CCC;
                border-radius:4px; color:#333; font-size:12px;
            }
            QPushButton:hover   { background:#EAF4FF; border-color:#5B9BD5; color:#2060A0; }
            QPushButton:pressed { background:#D0E8FF; }
        """)
        add_btn.clicked.connect(self._on_add_data)
        layout.addWidget(add_btn)
        return grp

    def _build_legend(self) -> QWidget:
        """Build a simple horizontal colour legend."""
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)
        for cat in CATEGORIES:
            r, g, b, _ = CATEGORY_COLORS[cat]
            hex_color = rgba_to_hex(r, g, b)
            swatch = QLabel()
            swatch.setFixedSize(14, 14)
            swatch.setStyleSheet(
                f"background:{hex_color}; border:1px solid #aaa; border-radius:2px;"
            )
            lbl = QLabel(cat)
            lbl.setStyleSheet("font-size:11px; color:#333;")
            row = QHBoxLayout()
            row.setSpacing(4)
            row.setContentsMargins(0, 0, 0, 0)
            row.addWidget(swatch)
            row.addWidget(lbl)
            container = QWidget()
            container.setLayout(row)
            layout.addWidget(container)
        return w

    def _refresh_chart(self):
        pw = self.plot_widget
        pw.clear()

        n_cats = len(CATEGORIES)
        offsets = np.array([(i - (n_cats - 1) / 2) * BAR_WIDTH
                            for i in range(n_cats)])

        x_centers = np.arange(12, dtype=float)  # 0..11

        for i, cat in enumerate(CATEGORIES):
            r, g, b, a = CATEGORY_COLORS[cat]
            values = np.array(self.data[cat])
            x_pos  = x_centers + offsets[i]

            bar = BarGraphItem(
                x=x_pos,
                height=values,
                width=BAR_WIDTH * 0.92,
                brush=pg.mkBrush(r, g, b, a),
                pen=pg.mkPen(color=(max(r-30,0), max(g-30,0), max(b-30,0)), width=0.8),
            )
            pw.addItem(bar)

        # X axis: month labels
        ax = pw.getAxis("bottom")
        ax.setTicks([list(enumerate(MONTHS))])
        ax.setLabel("Month", **{"font-size": "11pt"})

        # Y axis
        pw.getAxis("left").setLabel("Sales Amount (฿)", **{"font-size": "11pt"})

        # Y range
        max_val = max(
            (self.data[cat][m] for cat in CATEGORIES for m in range(12)),
            default=0,
        )
        pw.setYRange(0, max(max_val * 1.2, 5000))
        pw.setXRange(-0.6, 11.6)

        # Style axes
        for axis_name in ("bottom", "left"):
            axis = pw.getAxis(axis_name)
            axis.setStyle(tickFont=QFont("Segoe UI", 9))
            axis.setPen(pg.mkPen(color="#999", width=1))
            axis.setTextPen(pg.mkPen(color="#333"))


    def _on_add_data(self):
        month_idx = self.month_cb.currentIndex()
        category  = self.category_cb.currentText()
        amount    = self.sales_input.value()
        if amount <= 0:
            QMessageBox.warning(self, "Input Error",
                                "Sales amount must be greater than 0.")
            return
        self.data[category][month_idx] += amount
        self._refresh_chart()

    def _on_clear(self):
        if QMessageBox.question(
            self, "Clear Chart", "Clear all data?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        ) == QMessageBox.Yes:
            self.data = {cat: [0.0] * 12 for cat in CATEGORIES}
            self._refresh_chart()

    def _on_import(self):
        filename = self.filename_input.text().strip()
        if not filename:
            QMessageBox.warning(self, "Import Error", "Please enter a filename.")
            return
        if not os.path.exists(filename):
            QMessageBox.warning(
                self, "File Not Found",
                f'"{filename}" does not exist.\n\n'
                "Expected CSV format:\n  Month,Category,Amount\n\n"
                "Example:\n  Jan,Electronics,15000\n  Mar,Food,4500"
            )
            return

        errors, count = [], 0
        with open(filename, "r", encoding="utf-8") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    errors.append(f"Line {lineno}: expected 3 fields")
                    continue
                month, category, amount_str = parts
                if month not in MONTHS:
                    errors.append(f"Line {lineno}: unknown month '{month}'")
                    continue
                if category not in CATEGORIES:
                    errors.append(f"Line {lineno}: unknown category '{category}'")
                    continue
                try:
                    amount = float(amount_str)
                except ValueError:
                    errors.append(f"Line {lineno}: invalid amount '{amount_str}'")
                    continue
                self.data[category][MONTHS.index(month)] += amount
                count += 1

        self._refresh_chart()
        msg = f"Imported {count} record(s) from '{filename}'."
        if errors:
            msg += f"\n\nSkipped {len(errors)} line(s):\n" + "\n".join(errors[:10])
        QMessageBox.information(self, "Import Complete", msg)


    @staticmethod
    def _grp_style() -> str:
        return """
            QGroupBox {
                font-weight:bold; font-size:12px;
                border:1px solid #DDD; border-radius:6px;
                margin-top:8px; background:white; padding:4px;
            }
            QGroupBox::title {
                subcontrol-origin:margin; subcontrol-position:top left;
                left:8px; padding:0 4px; color:#333;
            }
        """

    @staticmethod
    def _le_style() -> str:
        return """
            QLineEdit {
                border:1px solid #CCC; border-radius:3px;
                padding:2px 6px; background:white; font-size:12px;
            }
            QLineEdit:focus { border-color:#5B9BD5; }
        """

    @staticmethod
    def _cb_style() -> str:
        return """
            QComboBox {
                border:1px solid #CCC; border-radius:3px;
                padding:2px 6px; background:white; font-size:12px;
            }
            QComboBox:focus { border-color:#5B9BD5; }
            QComboBox::drop-down { border:none; width:20px; }
        """


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    window = SalesChartApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()