import cv2
from PySide6 import QtCore
import numpy as np


class Camera(QtCore.QObject):
    frame_ready = QtCore.Signal(np.ndarray)

    def __init__(self, source=None):
        super().__init__()
        self.source = source
        self.capture = None
        self.running = False

    def start_camera(self):
        if not self.source:
            print("Error: No camera source specified.")
            return

        self.capture = cv2.VideoCapture(self.source)
        if not self.capture.isOpened():
            print(f"Error: Cannot open camera source {self.source}")
            return

        self.running = True
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                self.frame_ready.emit(frame)
            else:
                print("Error: Failed to capture frame.")
                break

        self.capture.release()

    def stop_camera(self):
        self.running = False
        if self.capture and self.capture.isOpened():
            self.capture.release()

    def __del__(self):
        self.stop_camera()
        print("Camera object deleted.")
