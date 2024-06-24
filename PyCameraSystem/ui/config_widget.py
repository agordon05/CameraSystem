import cv2
import numpy as np
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton

from obj.Camera import Camera
from ui import ui_settings


class Config_Widget(QtWidgets.QWidget):

    def __init__(self, source):
        super().__init__()
        self.setLayout(QVBoxLayout())

        # Top layout - page name and config button
        self.page_name = QLabel("Camera")
        ui_settings.format_page_name(self.page_name)

        self.config_button = QPushButton("Config")
        ui_settings.format_button(self.config_button)

        self.create_top_layout()
        # Center layout - camera feed (initially "No camera connected" label)
        self.camera_label = QLabel(f"No camera connected: {source}")
        # self.layout().addWidget(self.camera_label)
        self.create_camera_layout()



        # Bottom layout - buttons (to be added)
        # Start camera worker in a separate thread
        self.thread = QtCore.QThread()
        self.worker = Camera(source)
        self.worker.moveToThread(self.thread)
        self.worker.frame_ready.connect(self.update_camera_label)
        self.thread.started.connect(self.worker.start_camera)
        self.thread.start()

    def create_top_layout(self):
        widget = ui_settings.align_horizontal([self.config_button],
                                              stretch_beginning=True)
        self.layout().addWidget(widget)

        widget = ui_settings.align_horizontal([self.page_name],
                                              stretch_beginning=True, stretch_end=True)
        self.layout().addWidget(widget)

    def create_camera_layout(self):
        camera_widget = ui_settings.align_horizontal([self.camera_label], stretch_beginning=True, stretch_end=True)
        self.layout().addWidget(camera_widget)
        self.layout().addStretch()

    def update_camera_label(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert frame to QImage
        height, width, channel = frame.shape
        bytes_per_line = width * channel
        image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

        pixmap = QPixmap.fromImage(image)
        self.camera_label.setPixmap(pixmap)


