from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QLineEdit,
    QLabel,
    QMainWindow,
    QApplication,
    QFileDialog,
)
from time import gmtime
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from os import getcwd


class Window(QMainWindow):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.width = 436
        self.height = 277
        self.setGeometry(0, 0, self.width, self.height)
        self.setup_ui()

        self.alarm_filename = "resources/alarm.mp3"
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(self.alarm_filename))
        self.audio_output.setVolume(0.15)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.setInterval(1000)
        self.time = 0

        self.app_is_running = False
        self.timer_is_paused = False
        self.timer_is_started = False

    def setup_ui(self):
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint)
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet("background-color: #2f2f2f;")
        self.setProperty("_q_windowsizegrip", False)
        self.setProperty("_q_wndradius", 10)

        self.center()

        self.onlyInt = QtGui.QIntValidator()
        self.onlyInt.setRange(0, 99)

        self.label = QLabel("Timer", self)
        self.hours_label = QLabel("Hours", self)
        self.minutes_label = QLabel("Minutes", self)
        self.seconds_label = QLabel("Seconds", self)
        self.hours_button = QLineEdit("00", self)
        self.minutes_button = QLineEdit("00", self)
        self.seconds_button = QLineEdit("00", self)
        self.start_button = QPushButton("Start", self)
        self.reset_button = QPushButton("Reset", self)
        self.close_button = QPushButton("", self)
        self.upload_button = QPushButton("", self)

        self.label.setGeometry(175, 20, 87, 41)
        self.hours_label.setGeometry(58, 88, 34, 15)
        self.minutes_label.setGeometry(173, 88, 45, 15)
        self.seconds_label.setGeometry(288, 88, 49, 15)
        self.hours_button.setGeometry(53, 105, 100, 85)
        self.minutes_button.setGeometry(168, 105, 100, 85)
        self.seconds_button.setGeometry(283, 105, 100, 85)
        self.start_button.setGeometry(113, 222, 100, 30)
        self.reset_button.setGeometry(223, 222, 100, 30)
        self.close_button.setGeometry(77, 229, 16, 16)
        self.upload_button.setGeometry(345, 229, 12, 16)

        self.label.setStyleSheet(
            "font-size: 32px;"
            "color: #ffffff;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.hours_label.setStyleSheet(
            "font-size: 12px;"
            "color: #ffffff;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.minutes_label.setStyleSheet(
            "font-size: 12px;"
            "color: #ffffff;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.seconds_label.setStyleSheet(
            "font-size: 12px;"
            "color: #ffffff;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.hours_button.setStyleSheet(
            "background-color: #181818;"
            "color: #ffffff;"
            "border-style: outset;"
            "border-radius: 4px;"
            "font-size: 50px;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.minutes_button.setStyleSheet(
            "background-color: #181818;"
            "color: #ffffff;"
            "border-style: outset;"
            "border-radius: 4px;"
            "font-size: 50px;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.seconds_button.setStyleSheet(
            "background-color: #181818;"
            "color: #ffffff;"
            "border-style: outset;"
            "border-radius: 4px;"
            "font-size: 50px;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.start_button.setStyleSheet(
            "background-color: #004807;"
            "font-size: 14px;"
            "color: #ffffff;"
            "border-style: outset;"
            "border-radius: 4px;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.reset_button.setStyleSheet(
            "background-color: #181818;"
            "font-size: 14px;"
            "color: #ffffff;"
            "border-style: outset;"
            "border-radius: 4px;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.close_button.setStyleSheet("border-style: outset;")
        self.upload_button.setStyleSheet("border-style: outset;")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hours_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.minutes_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.seconds_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.hours_button.setValidator(self.onlyInt)
        self.minutes_button.setValidator(self.onlyInt)
        self.seconds_button.setValidator(self.onlyInt)

        self.start_button.clicked.connect(self.start)
        self.reset_button.clicked.connect(self.reset)
        self.close_button.clicked.connect(self.close_)
        self.upload_button.clicked.connect(self.set_alarm_filename)

        self.close_button.setIcon(QtGui.QIcon("resources/close.png"))
        self.upload_button.setIcon(QtGui.QIcon("resources/upload.png"))

        self.close_button.setIconSize(QtCore.QSize(16, 16))
        self.upload_button.setIconSize(QtCore.QSize(12, 16))

        self.hours_button.editingFinished.connect(
            self.hours_on_editing_finished
        )
        self.minutes_button.editingFinished.connect(
            self.minutes_on_editing_finished
        )
        self.seconds_button.editingFinished.connect(
            self.seconds_on_editing_finished
        )


    def start(self):
        if self.timer_is_started:
            self.pause()
            self.timer_is_started = False
            self.start_button.setStyleSheet(
                "background-color: #004807;"
                "font-size: 14px;"
                "color: #ffffff;"
                "border-style: outset;"
                "border-radius: 4px;"
                "font-family: 'LensGrotesk-Medium';"
            )
            self.start_button.setText("Continue")
        elif not self.app_is_running or self.timer_is_paused:
            try:
                self.player.stop()
                hours = int(self.hours_button.text())
                minutes = int(self.minutes_button.text())
                seconds = int(self.seconds_button.text())
                self.time = hours * 3600 + minutes * 60 + seconds
                self.timer.start()
                self.update_display()
                self.app_is_running = True
                self.start_button.setText("Pause")
                self.start_button.setStyleSheet(
                    "background-color: #484100;"
                    "font-size: 14px;"
                    "color: #ffffff;"
                    "border-style: outset;"
                    "border-radius: 4px;"
                    "font-family: 'LensGrotesk-Medium';"
                )
                self.timer_is_started = True
                if self.timer_is_paused:
                    self.timer_is_paused = False
                if self.timer_is_started:
                    self.block_edit(True)
            except ValueError:
                self.time = 0

    def pause(self):
        if self.app_is_running and not self.timer_is_paused:
            self.timer.stop()
            self.timer_is_paused = True

    def reset(self):
        self.timer.stop()
        self.time = 0

        self.app_is_running = False
        self.timer_is_paused = False
        self.timer_is_started = False

        self.block_edit(False)

        self.start_button.setStyleSheet(
            "background-color: #004807;"
            "font-size: 14px;"
            "color: #ffffff;"
            "border-style: outset;"
            "border-radius: 4px;"
            "font-family: 'LensGrotesk-Medium';"
        )
        self.start_button.setText("Start")

        self.update_display()

    def close_(self):
        self.close()

    def play_alarm(self):
        if self.timer_is_started and not self.time > 0:
            self.player.play()

    def set_alarm_filename(self):
        if not self.timer_is_started:
            filename = self.get_alarm_filename()
            self.player.setSource(QUrl.fromLocalFile(filename))

    def get_alarm_filename(self):
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a media file",
            directory=f"{getcwd()}/resources/",
            filter="Media file (*.mp3)",
            initialFilter="Media file (*.mp3)",
        )
        return response[0]

    def hours_on_editing_finished(self):
        text = self.hours_button.text()
        if len(text) == 1:
            self.hours_button.setText("0" + text)
        elif len(text) == 0:
            self.minutes_button.setText("00")

    def minutes_on_editing_finished(self):
        text = self.minutes_button.text()
        if len(text) == 1:
            self.minutes_button.setText("0" + text)
        elif len(text) == 3:
            self.minutes_button.setText("0" + str(int(text)))
        elif len(text) == 4:
            self.minutes_button.setText(str(int(text)))
        elif len(text) == 0:
            self.minutes_button.setText("00")
        elif int(text) > 59:
            self.minutes_button.setText("59")

    def seconds_on_editing_finished(self):
        text = self.seconds_button.text()
        if len(text) == 1:
            self.seconds_button.setText("0" + text)
        elif len(text) == 3:
            self.seconds_button.setText("0" + str(int(text)))
        elif len(text) == 4:
            self.seconds_button.setText(str(int(text)))
        elif len(text) == 0:
            self.minutes_button.setText("00")
        elif int(text) > 59:
            self.seconds_button.setText("59")

    def update_time(self):
        if self.time > 0:
            self.time -= 1
            self.update_display()
        else:
            self.play_alarm()
            self.reset()

    def update_display(self):
        hours = gmtime(self.time).tm_hour
        minutes = gmtime(self.time).tm_min
        seconds = gmtime(self.time).tm_sec

        self.hours_button.setText(str(hours))
        self.minutes_button.setText(str(minutes))
        self.seconds_button.setText(str(seconds))

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def block_edit(self, flag):
        if flag:
            self.hours_button.setReadOnly(True)
            self.minutes_button.setReadOnly(True)
            self.seconds_button.setReadOnly(True)
            self.upload_button.setEnabled(True)
        else:
            self.hours_button.setReadOnly(False)
            self.minutes_button.setReadOnly(False)
            self.seconds_button.setReadOnly(False)
            self.upload_button.setEnabled(False)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (
            self.offset is not None
            and event.buttons() == QtCore.Qt.MouseButton.LeftButton
        ):
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()

    app.exec()
