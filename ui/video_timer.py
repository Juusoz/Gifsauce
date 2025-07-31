from PyQt6.QtWidgets import (
    QHBoxLayout
)

def video_timer(self):
        
    # Timer row
    timer_row = QHBoxLayout()
    timer_row.addWidget(self.video_timer_label)
    
    return timer_row
    