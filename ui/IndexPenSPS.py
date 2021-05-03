# This Python file uses the following encoding: utf-8
import os
import pickle
import sys
import time

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, uic, sip

import numpy as np
from datetime import datetime

from PyQt5.QtCore import QTimer, QFile, QTextStream
from PyQt5.QtWidgets import QFileDialog

from config import config_ui

from utils.ui_utils import init_slider_bar_box
from utils.ui_utils import *
from utils.data_utils import RNStream
from utils.ui_utils import dialog_popup
import pyqtgraph as pg
from config import config_path


class IndexPenSPS(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.experiment_running = False



        # load panel
        self.ui = uic.loadUi("ui/IndexPenSPS.ui", self)

        # indexpen_markerinfo_verticalLayout & indexpen_presentation_verticalLayout
        # indexpen marker info
        self.indexpen_markercontrolpanel_container, self.indexpen_markercontrolpanel_layout = init_container \
            (parent=self.indexpen_markercontrol_vertical_layout, vertical=True, label='IndexPen Marker Control Panel')

        # label duration
        self.time_interval_block, self.time_interval_slider_view = init_slider_bar_box(
            self.indexpen_markercontrolpanel_layout,
            label="Interval lasts(sec)",
            vertical=False,
            label_bold=True,
            min_value=1,
            max_value=4)
        # repeat time slider
        self.repeat_num_block, self.repeat_num_slider_view = init_slider_bar_box(
            self.indexpen_markercontrolpanel_layout,
            label="Repeats(Times)",
            vertical=False,
            label_bold=True,
            min_value=1,
            max_value=10)
        # Randomized order check box
        self.random_checkbox_layout, self.random_checkbox = init_checkBox(
            parent=self.indexpen_markercontrolpanel_layout, label='Randomized Order : ', default_checked=False)

        # label list
        self.label_list_layout, self.label_list_input = init_inputBox(parent=self.indexpen_markercontrolpanel_layout,
                                                                      label='Task Label List:')

        # LSL stream Name
        self.LSL_stream_name_layout, self.LSL_stream_name_input = init_inputBox(
            parent=self.indexpen_markercontrolpanel_layout, label='LSL outlet stream name:')

        self.LSL_error_stream_name_layout, self.LSL_error_stream_name_input = init_inputBox(
            parent=self.indexpen_markercontrolpanel_layout, label='LSL error marker outlet stream name:')

        self.indexpen_markercontrol_btns_container, self.indexpen_markercontrol_btns_layout = init_container \
            (parent=self.indexpen_markercontrolpanel_layout, vertical=False, label='IndexPen Marker control')

        self.interrupt_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Interrupt')
        self.start_testing_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Start testing')
        self.start_experiment_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Start Recording')
        self.error_capture_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Error Signal')

        ##################Instruction block########################
        self.indexpen_instruction_container, self.indexpen_instruction_layout = init_container \
            (parent=self.indexpen_presentation_vertical_layout, vertical=True, label='IndexPen Instruction')

        self.pop_instruction_window_btn = init_button(parent=self.indexpen_instruction_layout, label='Pop instruction')

        self.currentLabel = QLabel(text='Write')
        self.nextLabel = QLabel(text='Next to Write:')
        self.indexpen_instruction_layout.addWidget(self.currentLabel)
        self.indexpen_instruction_layout.addWidget(self.nextLabel)
        self.currentLabel.adjustSize()
        self.nextLabel.adjustSize()

        # test init image
        self.image_label_dict = init_label_img_dict(config_path.indexpen_gesture_image_dir)
        self.currentLabel.setPixmap(self.image_label_dict['A' + '.PNG'])

        #function connection
        self.start_testing_btn.clicked.connect(self.start_testing_btn_clicked)

        # marker on tick
        # self.marker_timer = QTimer()
        # self.marker_timer.timeout.connect(self.marker_tick)
        # self.timer.setInterval(config.REFRESH_INTERVAL)  # for 1000 Hz refresh rate

        # self.timer.start()

    def marker_info(self):
        #interval
        # #repeats
        # #randomized
        # tasklabel list
        # #LSL outlet name
        # Error Stream name

        task_interval = self.time_interval_slider_view.slider.value()
        task_repeats = self.repeat_num_slider_view.slider.value()
        randomized_order = self.random_checkbox.isChecked()
        task_label_list = self.label_list_input.text()
        lsl_marker_stream_name = self.LSL_stream_name_input.text()
        lsl_error_stream_name = self.LSL_error_stream_name_input.text()

        return task_interval, task_repeats, randomized_order, task_label_list, lsl_marker_stream_name, lsl_error_stream_name

    def start_testing_btn_clicked(self):
        if self.experiment_running:
            return

        task_interval, task_repeats, randomized_order, task_label_list, lsl_marker_stream_name, lsl_error_stream_name = self.marker_info()

        print('John')
