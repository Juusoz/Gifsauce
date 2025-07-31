from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit, QCheckBox,
    QSpinBox
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt
from ui.left_layout import left_layout
from ui.right_layout import right_layout


def build_main_layout(self: QWidget) -> QHBoxLayout:
    # ─── Layout Assembly ────────────────────────────────────────────────
    main_layout = QHBoxLayout()
    main_layout.addLayout(left_layout(self), 2)
    main_layout.addLayout(right_layout(self), 1)
    return main_layout

