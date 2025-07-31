from PyQt6.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QUrl
from PyQt6 import QtGui
from core.gif_converter import convert_video_to_gif
from core.time_utils import parse_manual_time
from core.media_probe import probe_video_properties, parse_fps
from ui.video_controls import VideoControlMixin
from ui.build_main_layout import build_main_layout

class GifTrimmerApp(QWidget, VideoControlMixin):  
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./assets/Logo.ico'))
        self.setWindowTitle("Gifsauce  -  A simple video to gif converter")
        self.setMinimumSize(1000, 600)

        # Setup inherited functionality
        self.setup_media_player()
        self.setup_buttons()

        # Connect play/pause updates
        self.media_player.playbackStateChanged.connect(lambda _: self.update_play_pause_icon())
        self.setup_replay_timer()

        # Call for the layouts
        self.setLayout(build_main_layout(self))

    def convert_to_gif(self):
        try:
            if not hasattr(self, 'video_path'):
                return

            width = int(self.width_input.text())
            height = int(self.height_input.text())
            
            if self.custom_fps_checkbox.isChecked():
                fps = self.fps_input.value()
            else:
                _, _, fps_str = probe_video_properties(self.video_path)
                parsed = parse_fps(fps_str)
                if parsed:
                    fps = parsed

            max_colors = self.palette_size_input.value()+1 if self.auto_palette_checkbox.isChecked() else 256

            start = parse_manual_time(self.start_h.text(), self.start_m.text(), self.start_s.text(), self.start_ms.text())
            end = parse_manual_time(self.end_h.text(), self.end_m.text(), self.end_s.text(), self.end_ms.text())

            if end <= start:
                QMessageBox.warning(self, "Trim Error", "End time must be after start time.")
                return

            output_file, _ = QFileDialog.getSaveFileName(self, "Save GIF As", self.video_path.rsplit('.', 1)[0] + ".gif")
            if output_file:
                convert_video_to_gif(self.video_path, output_file, width, height, start, end, fps, max_colors)
                QMessageBox.information(self, "Success", f"GIF saved to {output_file}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
