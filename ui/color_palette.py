from PyQt6.QtWidgets import (
    QVBoxLayout, QCheckBox, QSpinBox, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QFont

def color_palette(self):
    bold_font = QFont()
    bold_font.setBold(True)
    
    # Color palette    
    # Container for the full framerate section
    color_palette_layout = QVBoxLayout()    
    
    palette_label = QLabel("Color Palette:")
    palette_label.setFont(bold_font)
    
    self.auto_palette_checkbox = QCheckBox("Custom palette size")
    self.auto_palette_checkbox.setChecked(False)
    
    # SpinBox for palette input
    self.palette_size_input = QSpinBox()
    self.palette_size_input.setRange(2, 255)
    self.palette_size_input.setValue(255)
    self.palette_size_input.setMaximumWidth(70)
    self.palette_size_input.setDisabled(True)  # Start disabled
    
    # Function to handle checkbox state changes
    def toggle_palette_size_input(checked: bool):
        self.palette_size_input.setEnabled(checked)
    
    # Connect checkbox state change to enabling/disabling the spinbox
    self.auto_palette_checkbox.toggled.connect(toggle_palette_size_input)
    
    # Second row
    palette_row = QHBoxLayout()
    palette_row.addWidget(self.auto_palette_checkbox)
    palette_row.addStretch()
    palette_row.addWidget(QLabel("Max colors:"))
    palette_row.addWidget(self.palette_size_input)
    
    # Add both layout rows to main layout    
    color_palette_layout.addWidget(palette_label)
    color_palette_layout.addLayout(palette_row)
    
    return color_palette_layout