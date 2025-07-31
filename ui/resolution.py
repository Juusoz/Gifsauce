from PyQt6.QtWidgets import (
    QGridLayout, QLineEdit, QCheckBox, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

def resolution(self):
    # -- Setup --
    bold_font = QFont()
    bold_font.setBold(True)

    layout = QGridLayout()
    layout.setColumnStretch(2, 1)  # Stretch right side
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Prevent centering

    # -- Label --
    resolution_label = QLabel("Resolution:")
    resolution_label.setFont(bold_font)
    layout.addWidget(resolution_label, 0, 0, 1, 2)

    # -- Internal state --
    self.aspect_ratio = None
    self._resolution_updating = False

    # -- Width Row --
    layout.addWidget(QLabel("Width:"), 1, 0)
    self.width_input = QLineEdit()
    self.width_input.setMaximumWidth(60)
    self.width_input.setEnabled(False)

    width_container = QHBoxLayout()
    width_container.addWidget(self.width_input)
    width_container.setAlignment(Qt.AlignmentFlag.AlignLeft)
    layout.addLayout(width_container, 1, 1)

    # -- Height Row --
    layout.addWidget(QLabel("Height:"), 2, 0)
    self.height_input = QLineEdit()
    self.height_input.setMaximumWidth(60)
    self.height_input.setEnabled(False)

    height_container = QHBoxLayout()
    height_container.addWidget(self.height_input)
    height_container.setAlignment(Qt.AlignmentFlag.AlignLeft)
    layout.addLayout(height_container, 2, 1)

    # -- Lock Checkbox --
    self.lock_aspect_checkbox = QCheckBox("Lock aspect ratio")
    self.lock_aspect_checkbox.setChecked(True)
    layout.addWidget(self.lock_aspect_checkbox, 3, 0, 1, 2)

    # --- Aspect Ratio Logic ---
    def update_aspect_ratio():
        try:
            width = int(self.width_input.text())
            height = int(self.height_input.text())
            if width > 0 and height > 0:
                self.aspect_ratio = width / height
        except ValueError:
            pass

    def on_width_changed(text):
        if self._resolution_updating or not self.lock_aspect_checkbox.isChecked():
            return
        try:
            width = int(text)
            if width > 0 and self.aspect_ratio:
                height = round(width / self.aspect_ratio)
                self._resolution_updating = True
                self.height_input.setText(str(height))
        except ValueError:
            pass
        finally:
            self._resolution_updating = False

    def on_height_changed(text):
        if self._resolution_updating or not self.lock_aspect_checkbox.isChecked():
            return
        try:
            height = int(text)
            if height > 0 and self.aspect_ratio:
                width = round(height * self.aspect_ratio)
                self._resolution_updating = True
                self.width_input.setText(str(width))
        except ValueError:
            pass
        finally:
            self._resolution_updating = False

    self.width_input.textChanged.connect(on_width_changed)
    self.height_input.textChanged.connect(on_height_changed)
    self.update_aspect_ratio_from_inputs = update_aspect_ratio

    return layout
