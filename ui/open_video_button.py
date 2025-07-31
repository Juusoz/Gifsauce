from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtCore import QUrl
from core.media_probe import probe_video_properties, parse_fps

def open_video_button(self):
    open_button_layout = QVBoxLayout()

    open_button = QPushButton("Open video file")
    open_button.clicked.connect(lambda: open_video_file(self))

    open_button_layout.addWidget(open_button)
    return open_button_layout

def open_video_file(self):
    file, _ = QFileDialog.getOpenFileName(self, "Open video file")
    if file:
        self.video_path = file
        self.media_player.setSource(QUrl.fromLocalFile(file))
        self.media_player.setPosition(0)
        self.media_player.play()

        w, h, fps_str = probe_video_properties(file)
        self.width_input.setText(str(w))
        self.height_input.setText(str(h))
        self.aspect_ratio = w / h if h else 1.0

        parsed_fps = parse_fps(fps_str)
        self.custom_fps_label.setText(f"({parsed_fps if parsed_fps else fps_str} fps)")

        self.width_input.setEnabled(True)
        self.height_input.setEnabled(True)

        if hasattr(self, "update_aspect_ratio_from_inputs"):
            self.update_aspect_ratio_from_inputs()
