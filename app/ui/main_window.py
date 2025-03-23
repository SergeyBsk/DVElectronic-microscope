''' app/ui/main_window.py '''
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication
from ..utils.config import AppConfig
from ..utils.video import VideoCapture
from .widgets.settings import SettingsPanelWidget
from .widgets.display import VideoDisplayWidget

class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow (QMainWindow): Inheritance
    """

    def __init__(self) -> None:
        """
        Initialize the Main-Window.
        """
        super().__init__()
        # Window-Settings
        self.setWindowTitle(AppConfig.APP_NAME)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setFixedWidth(QApplication.primaryScreen().availableGeometry().width())
        self.setFixedHeight(QApplication.primaryScreen().availableGeometry().height())

        layout = QHBoxLayout(central_widget)
        central_widget.setLayout(layout)

        self.video_capture = VideoCapture()

        self.videodisplay = self.create_videodisplay()
        self.settings_panel = self.create_settings_panel()


        layout.addWidget(self.videodisplay, stretch=3)
        layout.addWidget(self.settings_panel, stretch=1)

    def create_settings_panel(self):
        """
        Creates and adds the Settings Panel widget to the main window.
        """
        return SettingsPanelWidget(self.video_capture)

    def create_videodisplay(self) -> VideoDisplayWidget:
        """
        Creates and adds the VideoDisplay widget to the main window.
        """
        return VideoDisplayWidget(self.video_capture)