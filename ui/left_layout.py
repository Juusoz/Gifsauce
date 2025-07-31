from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QWidget, QLineEdit
)
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtCore import Qt
from ui.start_end_times import start_end_times
from ui.video_timer import video_timer

def left_layout(self: QWidget) -> QVBoxLayout:
    left_layout = QVBoxLayout()
    left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    left_layout.addWidget(self.video_widget)
    

    row1 = QHBoxLayout()
    row1.addLayout(video_timer(self))
    
    row1.addStretch()
    row1.addWidget(self.loop_checkbox)
    
    # Row 1
    left_layout.addLayout(row1)

    # Video slider
    left_layout.addWidget(self.video_slider)

    # Playback controls
    control_row = QHBoxLayout()
    for btn in [
        self.to_video_start, self.to_gif_start, self.step_back_1s_button,
        self.step_back_button, self.play_pause_button, self.step_forward_button,
        self.step_forward_1s_button, self.to_gif_end, self.to_video_end
    ]:
        control_row.addWidget(btn)
        
    left_layout.addLayout(control_row)  
    # Start and end times
    left_layout.addLayout(start_end_times(self))

    return left_layout