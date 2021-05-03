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
from PyQt5.QtWidgets import QFileDialog, QProgressBar

from config import config_ui

from utils.ui_utils import init_slider_bar_box
from utils.ui_utils import *
from utils.data_utils import RNStream
from utils.ui_utils import dialog_popup
import pyqtgraph as pg
from config import config_path
from utils.data_utils import generate_task_label_array
from utils.sound import *


class IndexPenSPS(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()

        self.experiment_state = 'idle'

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

        self.start_testing_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Start testing')
        self.interrupt_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Interrupt')
        self.error_capture_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Error Signal')
        self.interrupt_btn.setDisabled(True)
        self.error_capture_btn.setDisabled(True)
        # self.start_experiment_btn = init_button(parent=self.indexpen_markercontrol_btns_layout, label='Start Recording')

        ##################Instruction block########################
        self.indexpen_instruction_container, self.indexpen_instruction_layout = init_container \
            (parent=self.indexpen_presentation_vertical_layout, vertical=True, label='IndexPen Instruction')

        ##################Pop Window Btn########################
        self.pop_instruction_window_btn = init_button(parent=self.indexpen_instruction_layout, label='Pop instruction')
        ########## progress bar ############
        self.progress_bar = QProgressBar()
        self.indexpen_instruction_layout.addWidget(self.progress_bar)

        # Instruction Label
        self.currentLabel = QLabel(text='Write')
        self.nextLabel = QLabel(text='Next to Write:')
        self.indexpen_instruction_layout.addWidget(self.currentLabel)
        self.indexpen_instruction_layout.addWidget(self.nextLabel)
        self.currentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentLabel.adjustSize()
        self.nextLabel.adjustSize()

        # test init image
        self.image_label_dict = init_label_img_dict(config_path.indexpen_gesture_image_dir)
        self.currentLabel.setPixmap(self.image_label_dict['Nois' + '.PNG'])

        # function connection
        self.start_testing_btn.clicked.connect(self.start_testing_btn_clicked)

        # marker on tick
        self.marker_timer = QTimer()
        self.marker_timer.timeout.connect(self.marker_tick)
        # self.timer.setInterval(config.REFRESH_INTERVAL)  # for 1000 Hz refresh rate
        # self.timer.start()

    def marker_info(self):
        # interval
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
        if self.experiment_state != 'idle':
            return

        task_interval, task_repeats, randomized_order, task_label_list, lsl_marker_stream_name, lsl_error_stream_name = self.marker_info()

        if ' ' in lsl_marker_stream_name or ' ' in lsl_error_stream_name:
            dialog_popup(msg='LSL stream name cannot have space')
            return
        # TODO: init lsl marker thread

        # TODO: init lsl error marker thread

        # create task list
        self.task_label_array = generate_task_label_array(task_label_str=task_label_list, repeats=task_repeats,
                                                          randomized=randomized_order)

        self.marker_timer.setInterval(1000 * task_interval)  # for 1000 Hz refresh rate

        self.prepare_experiment()

    def prepare_experiment(self):
        self.currentLabel.setText('Press G to Continue')
        self.experiment_state = 'waiting'  # press Enter to continue

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_G and self.experiment_state == 'waiting':
            self.start_experinment()
        if event.key() == Qt.Key_S and self.experiment_state != 'idle':
            self.interrupt_experinment()

    def start_experinment(self):
        print('switch to running state')
        # start self.marker_timer
        self.marker_timer.start()
        # send start marker

        self.experiment_state = 'running'

    def interrupt_experinment(self):
        print('switch to idle state with interrupt')
        #  TODO: send interrupt marker

        self.stop_experiment_reset()

    def finish_experinment(self):
        print('switch to idle state with normal exit')
        #  TODO: send finishing marker

        self.stop_experiment_reset()

    def marker_tick(self):
        if self.task_label_array.size == 0:
            self.finish_experinment()
            return
        # remove first element, return first element
        current_task = self.task_label_array[0]
        self.task_label_array = np.delete(self.task_label_array, 0)
        # switch current image
        self.currentLabel.setPixmap(self.image_label_dict[current_task + '.PNG'])
        # Label Next to Write

        if self.task_label_array.size>0:
            self.nextLabel.setText('Next to Write: ' + self.task_label_array[0])
        else:
            self.nextLabel.setText('No next')
        # TODO: send encoder marker

        print('Current task: '+ current_task)

        # sound
        dah()

    def stop_experiment_reset(self):
        self.marker_timer.stop()
        self.currentLabel.setPixmap(self.image_label_dict['Nois' + '.PNG'])
        self.nextLabel.setText('Next to Write')
        self.experiment_state = 'idle'
