import json
import pandas as pd
import pyqtgraph as pg
import numpy as np

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    To do 1 — Read a CSV file and return a clean DataFrame.

    - Read the CSV file into a pandas DataFrame
    - If the file is empty, raise a ValueError
    - If any required columns are missing, raise a ValueError
    - Return the DataFrame
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(f"ไฟล์ '{path}' ว่างเปล่า")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"ขาดคอลัมน์: {', '.join(sorted(missing))}")

    return df


def read_json(path: str) -> pd.DataFrame:
    """
    To do 2 — Read a JSON file and return a DataFrame.

    - Read the JSON file into a pandas DataFrame
    - If the file is empty, raise a ValueError
    - If any required columns are missing, raise a ValueError
    - Return the DataFrame
    """
    df = pd.read_json(path)

    if df.empty:
        raise ValueError(f"ไฟล์ '{path}' ว่างเปล่า")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"ขาดคอลัมน์: {', '.join(sorted(missing))}")

    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    To do 3 — Save a DataFrame to a CSV file.

    - If the DataFrame is empty, raise a ValueError
    - Try writing to the file; if an error occurs, raise an IOError
    """
    if df.empty:
        raise ValueError("ไม่มีข้อมูลให้บันทึก")

    try:
        df.to_csv(path, index=False)
    except Exception as exc:
        raise IOError(f"บันทึก CSV ไม่สำเร็จ: {exc}") from exc


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    To do 4 — Save a DataFrame to a JSON file.

    - If the DataFrame is empty, raise a ValueError
    - Try writing to the file; if an error occurs, raise an IOError
    """
    if df.empty:
        raise ValueError("ไม่มีข้อมูลให้บันทึก")

    try:
        df.to_json(path, orient="records", indent=2)
    except Exception as exc:
        raise IOError(f"บันทึก JSON ไม่สำเร็จ: {exc}") from exc


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    To do 5 — Return a QTableWidget shown in the Statistics panel.

    Per-city stats:
      - Number of records
      - Average temperature  (1 d.p.)
      - Hottest day          (1 d.p.)
      - Coldest day          (1 d.p.)
      - Total rainfall (mm)  (1 d.p.)
      - Average humidity (%) (1 d.p.)

    - If the DataFrame is empty, raise a ValueError
    - If any required columns are missing, raise a ValueError
    - Build and return a QTableWidget
    """
    if df.empty:
        raise ValueError("ไม่มีข้อมูลสำหรับคำนวณสถิติ")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"ขาดคอลัมน์: {', '.join(sorted(missing))}")

    cities = sorted(df["city"].unique())

    row_labels = [
        "Records",
        "Avg Temp (°C)",
        "Hottest Day (°C)",
        "Coldest Day (°C)",
        "Total Rainfall (mm)",
        "Avg Humidity (%)",
    ]

    table = QTableWidget(len(row_labels), len(cities))
    table.setVerticalHeaderLabels(row_labels)
    table.setHorizontalHeaderLabels(cities)

    bold = QFont()
    bold.setBold(True)
    table.horizontalHeader().setFont(bold)
    table.verticalHeader().setFont(bold)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setAlternatingRowColors(True)

    alt_color = QColor(220, 235, 255)

    for col_idx, city in enumerate(cities):
        cdf = df[df["city"] == city]

        values = [
            str(len(cdf)),
            f"{cdf['temp_c'].mean():.1f}",
            f"{cdf['temp_c'].max():.1f}",
            f"{cdf['temp_c'].min():.1f}",
            f"{cdf['rainfall_mm'].sum():.1f}",
            f"{cdf['humidity'].mean():.1f}",
        ]

        for row_idx, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            if row_idx % 2 == 1:
                item.setBackground(alt_color)
            table.setItem(row_idx, col_idx, item)

    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    To do 6 — Draw a Rainfall Histogram using pyqtgraph and return a PlotWidget.

    - If the DataFrame has no data, raise a ValueError
    - If 'rainfall_mm' column is missing, raise a ValueError
    - Compute a histogram of the rainfall data
    - Return a pg.PlotWidget with labelled axes
    """
    if df is None or df.empty:
        raise ValueError("ไม่มีข้อมูลสำหรับสร้างกราฟ")

    if "rainfall_mm" not in df.columns:
        raise ValueError("ไม่พบคอลัมน์ 'rainfall_mm'")

    rainfall = df["rainfall_mm"].dropna().values
    counts, bin_edges = np.histogram(rainfall, bins=20)

    plot_widget = pg.PlotWidget()
    plot_widget.setBackground("w")

    bar_width = float(bin_edges[1] - bin_edges[0])
    bar_item = pg.BarGraphItem(
        x=bin_edges[:-1],
        height=counts,
        width=bar_width * 0.85,
        brush=pg.mkBrush(30, 120, 220, 180),
        pen=pg.mkPen("w", width=0.5),
    )
    plot_widget.addItem(bar_item)

    plot_widget.setLabel("left",   "Frequency")
    plot_widget.setLabel("bottom", "Rainfall (mm)")
    plot_widget.setTitle("Rainfall Distribution")
    plot_widget.showGrid(x=True, y=True, alpha=0.3)

    return plot_widget