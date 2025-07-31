from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout
)
from ui.framerate import framerate
from ui.color_palette import color_palette
from ui.resolution import resolution
from ui.open_video_button import open_video_button

def right_layout(self: QWidget) -> QVBoxLayout:
    
    right_layout = QVBoxLayout()
    
    # Open file button
    right_layout.addLayout(open_video_button(self))
    right_layout.addSpacing(10)

    # Resolution
    right_layout.addLayout(resolution(self))
    right_layout.addSpacing(10)

    # Framerate
    right_layout.addLayout(framerate(self))
    right_layout.addSpacing(10)

    # Color palette
    right_layout.addLayout(color_palette(self))
    right_layout.addSpacing(10)
    
    # Convert to GIF button
    right_layout.addWidget(self.convert_button)
    right_layout.addStretch()

    return right_layout