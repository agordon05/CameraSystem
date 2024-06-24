from PySide6 import QtWidgets, QtGui, QtCore
import cv2
import numpy as np
from obj.Camera import Camera
from ui import ui_settings


class Camera_Widget(QtWidgets.QWidget):
    def __init__(self, source: str):
        super().__init__()
        self.setMinimumSize(640, 480)  # Set a minimum size for the widget
        self.camera_frame = None
        self.camera_aspect_ratio = 4 / 3  # Adjust as per your camera's aspect ratio
        self.camera = Camera(source)
        self.camera_thread = QtCore.QThread()

        self.camera_label = QtWidgets.QLabel("No camera connected")
        ui_settings.format_label_center(self.camera_label)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.camera_label)
        self.setLayout(layout)

        # Connect camera frame_ready signal to update_camera_frame slot
        self.camera.frame_ready.connect(self.update_camera_frame)

        # Move camera operations to camera_thread
        self.camera.moveToThread(self.camera_thread)
        self.camera_thread.started.connect(self.camera.start_camera)
        self.camera_thread.start()

    @QtCore.Slot(np.ndarray)
    def update_camera_frame(self, frame):
        self.camera_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = self.camera_frame.shape
        bytesPerLine = 3 * width
        image = QtGui.QImage(self.camera_frame.data, width, height, bytesPerLine, QtGui.QImage.Format.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.camera_label.setPixmap(pixmap.scaled(self.camera_label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop_camera()
            self.camera_thread.quit()
            self.camera_thread.wait()
            self.camera.deleteLater()

        event.accept()
