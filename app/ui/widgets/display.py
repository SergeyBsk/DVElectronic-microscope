import cv2
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

class VideoDisplayWidget(QWidget):
    def __init__(self, video_capture, parent=None):
        super().__init__(parent)
        self.video_capture = video_capture
        self.init_ui()

    def init_ui(self):
        # Создаем QLabel для отображения видео
        self.label = QLabel(self)
        self.label.setText("Загрузка видео...")
        self.label.setStyleSheet("background-color: black; color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(True)  # Масштабирование содержимого под размер QLabel [[1]]

        # Размещаем QLabel в компоновщик
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Инициализация таймера для обновления кадров
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Обновление каждые 30 мс (около 33 FPS)

    def update_frame(self):
        frame = self.video_capture.get_frame()
        if frame is not None:
            # Конвертация кадра в RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

                        # Масштабируем изображение под размер виджета
            scaled_image = convert_to_qt_format.scaled(self.label.width(), self.label.height(), Qt.AspectRatioMode.KeepAspectRatio)
            self.label.setPixmap(QPixmap.fromImage(scaled_image))  # Отображение кадра
