from PyQt6.QtWidgets import (
    QGridLayout, QLabel, QLineEdit, QWidget, QPushButton
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

def start_end_times(self):
    start_end_layout = QGridLayout()
    start_end_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

    # Clamp config: (min, max, digits, max width)
    field_specs = {
        "h": (0, 99, 2, 19),
        "m": (0, 59, 2, 19),
        "s": (0, 59, 2, 19),
        "ms": (0, 999, 3, 25)
    }

    # Helper to create and clamp a QLineEdit
    def create_clamped_field(spec_key: str) -> QLineEdit:
        min_val, max_val, digits, max_width = field_specs[spec_key]
        line_edit = QLineEdit(f"{min_val:0{digits}d}")
        line_edit.setMaximumWidth(max_width)
        line_edit.setValidator(QIntValidator(min_val, 9999))  # Allow over-input, we handle clamping

        def clamp_text():
            text = line_edit.text()
            try:
                value = int(text)
                if value > max_val:
                    value = max_val
                elif value < min_val:
                    value = min_val
                line_edit.setText(f"{value:0{digits}d}")
            except ValueError:
                # Reset to minimum value if invalid
                line_edit.setText(f"{min_val:0{digits}d}")

        # Connect clamping after edit
        line_edit.editingFinished.connect(clamp_text)
        return line_edit

    # Assemble input fields
    def create_time_fields():
        return [
            create_clamped_field("h"),
            create_clamped_field("m"),
            create_clamped_field("s"),
            create_clamped_field("ms")
        ]

    self.start_h, self.start_m, self.start_s, self.start_ms = create_time_fields()
    self.end_h, self.end_m, self.end_s, self.end_ms = create_time_fields()

    def add_time_row(row: int, label_text: str, fields, button):
        start_end_layout.addWidget(QLabel(label_text), row, 0)
        start_end_layout.addWidget(fields[0], row, 1)
        start_end_layout.addWidget(QLabel(":"), row, 2)
        start_end_layout.addWidget(fields[1], row, 3)
        start_end_layout.addWidget(QLabel(":"), row, 4)
        start_end_layout.addWidget(fields[2], row, 5)
        start_end_layout.addWidget(QLabel(":"), row, 6)
        start_end_layout.addWidget(fields[3], row, 7)
        start_end_layout.addWidget(button, row, 8)

    add_time_row(0, "Start time:", [self.start_h, self.start_m, self.start_s, self.start_ms], self.set_start_btn)
    add_time_row(1, "End time:", [self.end_h, self.end_m, self.end_s, self.end_ms], self.set_end_btn)

    # Optional: Adjust spacing for ":" columns
    for col in [2, 4, 6]:
        start_end_layout.setColumnMinimumWidth(col, 0)

    # Push remaining space to the right
    start_end_layout.setColumnStretch(9, 1)

    return start_end_layout
