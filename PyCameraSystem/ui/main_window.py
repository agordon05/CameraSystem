from PySide6 import QtWidgets, QtGui


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.accept()
