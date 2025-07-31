from PyQt6.QtWidgets import QPushButton, QStyle
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QTimer
from core.time_utils import parse_manual_time

class VideoControlMixin:
    def setup_media_player(self):
        from PyQt6.QtMultimedia import QAudioOutput
        from PyQt6.QtMultimediaWidgets import QVideoWidget
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QSlider, QLabel, QCheckBox, QSizePolicy

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0)
        self.media_player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget()
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.video_widget.setMinimumSize(640, 360)
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.media_player.setVideoOutput(self.video_widget)

        self.video_slider = QSlider(Qt.Orientation.Horizontal)
        self.video_timer_label = QLabel("00:00:00.000")
        self.loop_checkbox = QCheckBox("Loop GIF Area")
        self.loop_checkbox.setChecked(True)

        self.media_player.positionChanged.connect(self.handle_position_changed)
        self.media_player.durationChanged.connect(self.set_default_end_time)
        self.media_player.durationChanged.connect(self.video_slider.setMaximum)
        self.video_slider.sliderMoved.connect(lambda pos: self.media_player.setPosition(pos))

    def setup_buttons(self):
        
        self.play_pause_button = QPushButton()
        self.update_play_pause_icon()
        self.play_pause_button.clicked.connect(self.toggle_play_pause)

        self.step_forward_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward), "33ms")
        self.step_forward_button.clicked.connect(lambda: self.media_player.setPosition(self.media_player.position() + 33))

        self.step_back_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward), "33ms")
        self.step_back_button.clicked.connect(lambda: self.media_player.setPosition(max(0, self.media_player.position() - 33)))

        self.step_forward_1s_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward), "1s")
        self.step_forward_1s_button.clicked.connect(lambda: self.media_player.setPosition(self.media_player.position() + 1000))

        self.step_back_1s_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward), "1s")
        self.step_back_1s_button.clicked.connect(lambda: self.media_player.setPosition(max(0, self.media_player.position() - 1000)))

        self.to_video_start = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward), "Video")
        self.to_video_start.clicked.connect(lambda: self.media_player.setPosition(0))

        self.to_video_end = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward), "Video")
        self.to_video_end.clicked.connect(lambda: self.media_player.setPosition(self.media_player.duration()))

        self.to_gif_start = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward), "Gif")
        self.to_gif_start.clicked.connect(lambda: self.media_player.setPosition(
            int(self.get_gif_start_time() * 1000)
        ))

        self.to_gif_end = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward), "Gif")
        self.to_gif_end.clicked.connect(lambda: self.media_player.setPosition(
            int(self.get_gif_end_time() * 1000)
        ))

        self.set_start_btn = QPushButton("Set Start Time")
        self.set_start_btn.clicked.connect(self.set_start_from_position)

        self.set_end_btn = QPushButton("Set End Time")
        self.set_end_btn.clicked.connect(self.set_end_from_position)

        self.convert_button = QPushButton("Convert to GIF")
        self.convert_button.clicked.connect(self.convert_to_gif)

    def toggle_play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
        self.update_play_pause_icon()

    def update_play_pause_icon(self):
        icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPause if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
            else QStyle.StandardPixmap.SP_MediaPlay
        )
        self.play_pause_button.setIcon(icon)
        self.play_pause_button.setText("Pause" if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState else "Play")

    def setup_replay_timer(self):
        self.replay_timer = QTimer()
        self.replay_timer.setInterval(100)
        self.replay_timer.timeout.connect(lambda: self.handle_position_changed(self.media_player.position()))
        self.replay_timer.start()

    def set_default_end_time(self, duration):
        from PyQt6.QtCore import QTime
        t = QTime(0, 0, 0).addMSecs(duration)
        self.end_h.setText(f"{t.hour():02}")
        self.end_m.setText(f"{t.minute():02}")
        self.end_s.setText(f"{t.second():02}")
        self.end_ms.setText(f"{t.msec():03}")

    def handle_position_changed(self, pos):
        from core.time_utils import format_time
        self.video_slider.setValue(pos)
        self.video_timer_label.setText(format_time(pos / 1000))

        if self.loop_checkbox.isChecked():
            end = self.get_gif_end_time()
            if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                if pos >= int(end * 1000):
                    self.media_player.setPosition(int(self.get_gif_start_time() * 1000))

    def get_gif_start_time(self):
        return parse_manual_time(self.start_h.text(), self.start_m.text(), self.start_s.text(), self.start_ms.text())

    def get_gif_end_time(self):
        return parse_manual_time(self.end_h.text(), self.end_m.text(), self.end_s.text(), self.end_ms.text())

    def set_start_from_position(self):
        from PyQt6.QtCore import QTime
        t = QTime(0, 0, 0).addMSecs(self.media_player.position())
        self.start_h.setText(f"{t.hour():02}")
        self.start_m.setText(f"{t.minute():02}")
        self.start_s.setText(f"{t.second():02}")
        self.start_ms.setText(f"{t.msec():03}")

    def set_end_from_position(self):
        from PyQt6.QtCore import QTime
        t = QTime(0, 0, 0).addMSecs(self.media_player.position())
        self.end_h.setText(f"{t.hour():02}")
        self.end_m.setText(f"{t.minute():02}")
        self.end_s.setText(f"{t.second():02}")
        self.end_ms.setText(f"{t.msec():03}")
