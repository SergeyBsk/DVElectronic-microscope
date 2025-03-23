import cv2

class VideoCapture:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)  # Инициализация камеры
        self.selected_camera = None
        self.contrast = 1.0  # Параметр контраста
        self.sharpness = 1.0  # Параметр резкости
        self.zoom_level = 1.0  # Уровень цифрового зума (1.0 = без зума)

    def get_available_cameras(self):
        # Проверяем доступные камеры
        available_cameras = []
        for i in range(10):  # Перебираем первые 10 индексов камер [[1]]
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append((i, f"Камера {i}"))
                cap.release()
        return available_cameras

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Применяем цифровой зум
            frame = self.apply_zoom(frame)
            # Применяем обработку кадра (например, контраст и резкость)
            frame = self.apply_contrast(frame)
            frame = self.apply_sharpness(frame)
            return frame
        return None

    def apply_contrast(self, frame):
        # Применяем контраст
        return cv2.convertScaleAbs(frame, alpha=self.contrast, beta=0)

    def apply_sharpness(self, frame):
        # Применяем резкость
        kernel = cv2.getGaussianKernel(5, self.sharpness)
        return cv2.filter2D(frame, -1, kernel)

    def apply_zoom(self, frame):
        # Применяем цифровой зум
        if self.zoom_level <= 1.0:
            return frame  # Без зума
        h, w = frame.shape[:2]
        new_h, new_w = int(h / self.zoom_level), int(w / self.zoom_level)
        start_x = (w - new_w) // 2
        start_y = (h - new_h) // 2
        cropped_frame = frame[start_y:start_y + new_h, start_x:start_x + new_w]
        return cv2.resize(cropped_frame, (w, h))  # Масштабируем обратно до исходного размера

    def select_camera(self, camera_id):
        # Выбор камеры по ID
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(camera_id)
        self.selected_camera = camera_id

    def set_contrast(self, value):
        self.contrast = value

    def set_sharpness(self, value):
        self.sharpness = value

    def set_zoom(self, value):
        self.zoom_level = value  # Установка уровня зума

    def release(self):
        self.cap.release()