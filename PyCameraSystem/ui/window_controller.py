import sys
from PySide6 import QtWidgets

from ui import ui_settings
from ui.widgets.camera_widget import Camera_Widget
from ui.main_window import Main_Window


app = QtWidgets.QApplication()
widget: QtWidgets = None
window: Main_Window = Main_Window()
# secondary_window: QtWidgets = second_window()
# table_widget: Table_Widget.table_widget = Table_Widget.table_widget(ui_settings.exchange_table)
# log_window: dialog_window = dialog_window()


def switch_ui(temp_widget: QtWidgets):
    global widget
    widget = temp_widget
    window.setCentralWidget(widget)


# def set_camera(source: str):
#     print("Window Controller adding camera")
#     cam = Camera(source)
#     return widget.set_camera(cam)


# def seperate_window(temp_widget: QtWidgets):
#     global secondary_window
#     secondary_window = temp_widget
#     secondary_window.resize(400, 400)
#     secondary_window.show()

# def create_dialog(widget_dialog: QtWidgets.QWidget):
#     global log_window, window
#     log_window = dialog_window(widget=widget_dialog, parent=window)
#     log_window.setWindowTitle(ui_settings.window_title)
#     log_window.setModal(True)  # Make it a modal dialog
#
#     center_x: int = int(window.geometry().center().x() - ui_settings.dialog_width // 2)
#     if isinstance(widget_dialog, new_bot_widget):
#         center_y: int = int(window.geometry().center().y() - ui_settings.dialog_new_bot_height // 2)
#     else:
#         center_y: int = int(window.geometry().center().y() - ui_settings.dialog_height // 2)
#     log_window.setGeometry(center_x, center_y, ui_settings.dialog_width, ui_settings.dialog_height)
#     log_window.show()
#     print(f"height: {log_window.height()}")


# def switch_dialog(widget_dialog: QtWidgets.QWidget):
#     global log_window, window
#     log_window.clear_widgets()
#     log_window.set_widget(widget_dialog)

#
# def close_dialog():
#     global log_window
#     log_window.accept()


def run_ui():
    global widget
    # Set up the main window
    window.setWindowTitle(ui_settings.window_title)
    # window.resize(800, 600)
    # window.setCentralWidget(widget)

    # Set camera source and start camera
    camera_source = "rtsp://admin:12345@10.0.0.30/Streaming/channels/2/picture"
    # camera = Camera(camera_source)
    # widget.set_camera(camera)
    widget = Camera_Widget(camera_source)
    window.setCentralWidget(widget)

    # Show the main window
    window.showFullScreen()

    # Execute the application
    sys.exit(app.exec())
