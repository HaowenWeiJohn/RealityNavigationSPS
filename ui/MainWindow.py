import time

import pyqtgraph as pg
from PyQt5 import QtWidgets, sip, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QMessageBox
from scipy.signal import decimate
from ui.SettingsTab import SettingsTab

import config

# from ui.SettingsTab import SettingsTab


from utils.data_utils import window_slice

from utils.ui_utils import init_sensor_or_lsl_widget, init_add_widget, CustomDialog, init_button, dialog_popup, \
    get_distinct_colors, init_camera_widget, convert_cv_qt, AnotherWindow
import numpy as np


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi("ui/mainwindow.ui", self)
        self.setWindowTitle('Reality Navigation SPS')
        self.app = app

        #Thumouse Tab



        #IndexPen Tab




        #fNirsTab




        #SetingTab
        self.settingTab = SettingsTab(self)
        self.settings_tab_vertical_layout.addWidget(self.settingTab)



        #signal
        lsl_marker_thread = {}





        # create sensor threads, worker threads for different sensors

        # timer

        # self.timer = QTimer()
        # self.timer.setInterval(config.REFRESH_INTERVAL)  # for 1000 Hz refresh rate
        # self.timer.timeout.connect(self.ticks)
        # self.timer.start()
        #
        # # visualization timer
        # self.v_timer = QTimer()
        # self.v_timer.setInterval(config.VISUALIZATION_REFRESH_INTERVAL)  # for 15 Hz refresh rate
        # self.v_timer.timeout.connect(self.visualize_LSLStream_data)
        # self.v_timer.start()
        #
        # # camera/screen capture timer
        # self.c_timer = QTimer()
        # self.c_timer.setInterval(config.CAMERA_SCREENCAPTURE_REFRESH_INTERVAL)  # for 15 Hz refresh rate
        # self.c_timer.timeout.connect(self.camera_screen_capture_tick)
        # self.c_timer.start()
        #
        # self.settingTab = SettingsTab(self)
        # self.settings_tab_vertical_layout.addWidget(self.settingTab)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Exit Application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.app.quit()
        else:
            event.ignore()
