import cv2
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QSlider, QComboBox, QMessageBox


class SettingsPanelWidget(QWidget):
    def __init__(self, video_capture, parent=None):
        super().__init__(parent)
        self.video_capture = video_capture
        self.init_ui()

    def init_ui(self):
        # Создаем простую панель настроек
        layout = QVBoxLayout()

        # Кнопка для увеличения контраста
        contrast_button = QPushButton("Увеличить контраст")
        contrast_button.clicked.connect(lambda: self.video_capture.set_contrast(self.video_capture.contrast + 0.1))
        layout.addWidget(contrast_button)

        # Кнопка для уменьшения контраста
        contrast_down_button = QPushButton("Уменьшить контраст")
        contrast_down_button.clicked.connect(lambda: self.video_capture.set_contrast(self.video_capture.contrast - 0.1))
        layout.addWidget(contrast_down_button)

        # Кнопка для увеличения резкости
        sharpness_button = QPushButton("Увеличить резкость")
        sharpness_button.clicked.connect(lambda: self.video_capture.set_sharpness(self.video_capture.sharpness + 0.1))
        layout.addWidget(sharpness_button)

        # Кнопка для уменьшения резкости
        sharpness_down_button = QPushButton("Уменьшить резкость")
        sharpness_down_button.clicked.connect(lambda: self.video_capture.set_sharpness(self.video_capture.sharpness - 0.1))
        layout.addWidget(sharpness_down_button)

                # Слайдер для управления цифровым зумом
        zoom_label = QLabel("Цифровой зум:")
        layout.addWidget(zoom_label)
        zoom_slider = QSlider(Qt.Orientation.Horizontal)
        zoom_slider.setMinimum(1)  # Минимальный уровень зума (1x)
        zoom_slider.setMaximum(4)  # Максимальный уровень зума (4x)
        zoom_slider.setValue(1)    # Начальный уровень зума
        zoom_slider.valueChanged.connect(lambda value: self.video_capture.set_zoom(value))
        layout.addWidget(zoom_slider)

        # Выпадающий список для выбора камеры
        self.camera_combo = QComboBox()
        self.available_cameras = self.video_capture.get_available_cameras()
        if self.available_cameras:
            for cam_id, cam_name in self.available_cameras:
                self.camera_combo.addItem(cam_name, userData=cam_id)
            self.camera_combo.currentIndexChanged.connect(self.on_camera_selected)
        else:
            self.camera_combo.addItem("Камеры не обнаружены")
        layout.addWidget(self.camera_combo)

        self.setLayout(layout)

    def on_camera_selected(self, index):
        if self.available_cameras:
            selected_camera_id = self.camera_combo.itemData(index)
            self.video_capture.select_camera(selected_camera_id)
        else:
            QMessageBox.warning(self, "Ошибка", "Камеры не обнаружены. Проверьте подключение.") [[4]]

