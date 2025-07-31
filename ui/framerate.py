from PyQt6.QtWidgets import (
    QVBoxLayout, QCheckBox, QSpinBox, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QFont

def framerate(self):
    bold_font = QFont()
    bold_font.setBold(True)
    
    # Container for the full framerate section
    framerateLayout = QVBoxLayout()    
    
    framerate_label_row = QHBoxLayout()
    framerate_label = QLabel("Framerate:")
    framerate_label.setFont(bold_font)
    
    self.custom_fps_checkbox = QCheckBox("Custom framerate")
    self.custom_fps_checkbox.setChecked(False)
    self.custom_fps_label = QLabel("      ")
    
    framerate_label_row.addWidget(framerate_label)
    framerate_label_row.addWidget(self.custom_fps_label)
    
    # SpinBox for FPS input
    self.fps_input = QSpinBox()
    self.fps_input.setRange(1, 50)
    self.fps_input.setValue(15)
    self.fps_input.setMaximumWidth(70)
    self.fps_input.setDisabled(True)  # Start disabled
    
    # Function to handle checkbox state changes
    def toggle_fps_input(checked: bool):
        self.fps_input.setEnabled(checked)
    
    # Connect checkbox state change to enabling/disabling the spinbox
    self.custom_fps_checkbox.toggled.connect(toggle_fps_input)
    
    # Second row: checkbox, spacer, "FPS:" label, and input
    fps_row = QHBoxLayout()
    fps_row.addWidget(self.custom_fps_checkbox)
    fps_row.addStretch()
    fps_row.addWidget(QLabel("FPS:"))
    fps_row.addWidget(self.fps_input)
    
    # Add both layout rows to main layout
    framerateLayout.addLayout(framerate_label_row)
    framerateLayout.addLayout(fps_row)
    
    return framerateLayout
