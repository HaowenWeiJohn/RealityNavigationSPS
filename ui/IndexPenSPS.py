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
from pylsl import StreamInfo, StreamOutlet

from config import config_ui, config_signal

from utils.ui_utils import init_slider_bar_box
from utils.ui_utils import *
from utils.data_utils import RNStream
from utils.ui_utils import dialog_popup
import pyqtgraph as pg
from config import config_path
from utils.data_utils import generate_task_label_array
from utils.sound import *


class IndexPenSPS(QtWidgets.QWidget):
    def __init__(self, parent, exp_presets_dict):
        super().__init__()

        self.experiment_state = 'idle'

        # load panel
        self.ui = uic.loadUi("ui/IndexPenSPS.ui", self)

        self.indexpen_exp_preset_dict = exp_presets_dict['IndexPen_2021_Summer']

        self.create_lsl(name=self.indexpen_exp_preset_dict['ExpLSLStreamName'], type='Gestur_Exp_Marker',
                        nominal_srate=3, channel_format='float32',
                        source_id='indexpen')

        # indexpen_markerinfo_verticalLayout & indexpen_presentation_verticalLayout
        # indexpen marker info
        self.indexpen_markercontrolpanel_container, self.indexpen_markercontrolpanel_layout = init_container \
            (parent=self.indexpen_markercontrol_vertical_layout, vertical=True, label='IndexPen Marker Control Panel')

        # label duration
        self.time_interval_block, self.time_interval_slider_view = init_slider_bar_box(
            self.indexpen_markercontrolpanel_layout,
            label="Interval lasts(Sec)",
            vertical=False,
            label_bold=True,
            min_value=1,
            max_value=config_ui.indexpen_interval_default_max)
        self.time_interval_slider_view.slider.setValue(config_ui.indexpen_interval_time_default)
        # repeat time slider
        self.repeat_num_block, self.repeat_num_slider_view = init_slider_bar_box(
            self.indexpen_markercontrolpanel_layout,
            label="Repeats(Times)",
            vertical=False,
            label_bold=True,
            min_value=1,
            max_value=config_ui.indexpen_repeats_default_max)
        self.repeat_num_slider_view.slider.setValue(config_ui.indexpen_repeats_num_default)

        # Randomized order check box
        self.random_checkbox_layout, self.random_checkbox = init_checkBox(
            parent=self.indexpen_markercontrolpanel_layout, label='Randomized Order : ', default_checked=False)

        # label list
        self.task_dict = generate_sentence_task()
        self.task_dict.insert(0, config_ui.indexPen_classes_default)
        self.task_dict_combbox = self.task_dict.copy()
        for i in range(0, len(self.task_dict_combbox)):
            self.task_dict_combbox[i] = ''.join((str(i), '. ', self.task_dict_combbox[i]))

        self.label_list_layout, self.label_list_input = init_inputBox(parent=self.indexpen_markercontrolpanel_layout,
                                                                      label='Task Label List:',
                                                                      default_input=self.task_dict[0])

        self.task_combo_box = init_combo_box(parent=self.indexpen_markercontrolpanel_layout, label=None,
                                             item_list=self.task_dict_combbox)
        self.task_combo_box.currentIndexChanged.connect(self.task_combo_box_index_changed)

        # # LSL stream Name
        # self.LSL_stream_name_layout, self.LSL_stream_name_input = init_inputBox(
        #     parent=self.indexpen_markercontrolpanel_layout, label='LSL outlet stream name:',
        #     default_input=config_ui.marker_lsl_outlet_name_default)
        #
        # self.LSL_error_stream_name_layout, self.LSL_error_stream_name_input = init_inputBox(
        #     parent=self.indexpen_markercontrolpanel_layout, label='LSL error marker outlet stream name:',
        #     default_input=config_ui.error_marker_lsl_outlet_name_default)

        self.indexpen_markercontrol_btns_container, self.indexpen_markercontrol_btns_layout = init_container \
            (parent=self.indexpen_markercontrolpanel_layout, vertical=False, label='IndexPen Marker control')

        self.currentIndexLabel = QLabel(text='Current Label Index: ')
        self.indexpen_markercontrolpanel_layout.addWidget(self.currentIndexLabel)
        self.currentIndexLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.currentIndexLabel.adjustSize()
        self.currentLabelIndex = 0

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

        ################# Text Input Box ######################
        self.indexpeninference_text_layout, self.indexpeninference_text_input = init_textEditInputBox(
            parent=self.indexpen_instruction_layout,
            min_h=80,
            max_h=80,
            label='Index Input Box',
            default_input=config_ui.indexPen_text_input_default,
            vertical=True)


        ########## progress bar ############
        self.task_progress_bar = QProgressBar()
        self.indexpen_instruction_layout.addWidget(self.task_progress_bar)

        # Instruction Label
        self.currentLabel = QLabel(text='Write')
        self.currentLabel.setMinimumSize(500,600)
        self.nextLabel = QLabel(text='Next to Write:')
        self.indexpen_instruction_layout.addWidget(self.currentLabel)
        self.indexpen_instruction_layout.addWidget(self.nextLabel)
        self.currentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentLabel.adjustSize()
        self.nextLabel.adjustSize()

        # test init image
        self.image_label_dict = init_label_img_dict(config_path.indexpen_gesture_image_dir)
        self.currentLabel.setPixmap(self.image_label_dict['Ready' + '.PNG'])

        # btn function connection
        self.start_testing_btn.clicked.connect(self.start_testing_btn_clicked)
        self.interrupt_btn.clicked.connect(self.interrupt_experiment)
        self.error_capture_btn.clicked.connect(self.error_signal)
        ##########################Timer connect#####################################
        # marker on tick
        self.marker_timer = QTimer()
        self.marker_timer.timeout.connect(self.marker_tick)

        self.progress_bar_update_timer = QTimer()
        self.progress_bar_update_timer.timeout.connect(self.updata_progress_bar)
        self.progress_bar_update_timer.setInterval(config_ui.progress_bar_updat_freq)

        self.internal_marker_timer = QTimer()
        self.internal_marker_timer.timeout.connect(self.internal_marker_tick)
        self.internal_marker_timer.setInterval(config_signal.internal_marker_tick_period)

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

        # lsl_marker_stream_name = self.LSL_stream_name_input.text()
        # lsl_error_stream_name = self.LSL_error_stream_name_input.text()
        return task_interval, task_repeats, randomized_order, task_label_list

    def start_testing_btn_clicked(self):
        if self.experiment_state != 'idle':
            return

        # send exprenment ID
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpID']])

        task_interval, task_repeats, randomized_order, task_label_list = self.marker_info()

        # TODO: init lsl marker thread

        # create task list
        self.task_label_array = generate_task_label_array(task_label_str=task_label_list, repeats=task_repeats,
                                                          randomized=randomized_order)
        self.time_interval_ms = 1000 * task_interval
        self.marker_timer.setInterval(self.time_interval_ms)  # for 1000 Hz refresh rate

        self.prepare_experiment()

        self.interrupt_btn.setDisabled(False)
        self.error_capture_btn.setDisabled(False)
        self.start_testing_btn.setDisabled(True)

    def prepare_experiment(self):
        self.currentLabel.setText('Press G to Continue')
        self.nextLabel.setText('Next to Write: ' + self.task_label_array[0])
        self.experiment_state = 'waiting'  # press Enter to continue

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_G and self.experiment_state == 'waiting':
            self.start_experiment()
        if event.key() == Qt.Key_S and self.experiment_state != 'idle':
            self.interrupt_experiment()

    def start_experiment(self):
        print('switch to running state')

        # send start marker
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpStartMarker']])

        # start self.marker_timer
        self.marker_timer.start()
        self.progress_bar_update_timer.start()
        # send start marker

        self.experiment_state = 'running'

    def interrupt_experiment(self):
        print('switch to idle state with interrupt, send interrupt&end marker')
        #  TODO: send interrupt marker
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpInterruptMarker']])
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpEndMarker']])
        self.stop_experiment_reset()

    def end_experiment(self):
        print('switch to idle state with normal exit(end), send ending marker')
        #  TODO: send ending marker
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpEndMarker']])

        self.stop_experiment_reset()

    def marker_tick(self):
        if self.task_label_array.size == 0:
            self.end_experiment()
            return
        self.currentIndexLabel.setText('Current Label Index: ' + str(self.currentLabelIndex))
        self.currentLabelIndex += 1
        # remove first element, return first element
        current_task = self.task_label_array[0]
        self.task_label_array = np.delete(self.task_label_array, 0)

        # switch current image
        self.currentLabel.setPixmap(self.image_label_dict[current_task + '.PNG'])
        # Label Next to Write
        if self.task_label_array.size > 0:
            self.nextLabel.setText('Next to Write: ' + self.task_label_array[0])
        else:
            self.nextLabel.setText('No next')
        # TODO: send encoder marker
        marker = self.indexpen_exp_preset_dict['ExpLabelMarker'][current_task]
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpLabelMarker'][current_task]])
        # start internal dilidilidili timer
        self.internal_marker_timer.start()

        print('time.time(): ', time.time())

        # printInfo
        print('Current task: ' + current_task)
        print('Send Encoded Marker: ' + str(marker))
        print('Task Remaining Time: ' + str(self.marker_timer.remainingTime()))
        # sound bilibilibilibili
        dah()

    def internal_marker_tick(self):
        dih()
        self.internal_marker_timer.stop()

    def stop_experiment_reset(self):
        self.marker_timer.stop()
        self.progress_bar_update_timer.stop()
        self.task_progress_bar.setValue(0)
        self.currentLabel.setPixmap(self.image_label_dict['Ready' + '.PNG'])
        self.nextLabel.setText('Next to Write: ')
        self.experiment_state = 'idle'

        self.interrupt_btn.setDisabled(True)
        self.error_capture_btn.setDisabled(True)
        self.start_testing_btn.setDisabled(False)
        self.currentIndexLabel.setText('Current Label Index: ')
        self.currentLabelIndex = 0

    def error_signal(self):
        self.outlet_stream.push_sample([self.indexpen_exp_preset_dict['ExpErrorMarker']])

    def updata_progress_bar(self):
        bar_value = int((self.time_interval_ms - self.marker_timer.remainingTime()) / self.time_interval_ms * 100)
        self.task_progress_bar.setValue(bar_value)
        # if bar_value<25:
        #     self.task_progress_bar.setStyleSheet("QProgressBar::chunk "
        #                                          "{"
        #                                          "background-color: red;"
        #                                          "}")
        # else:
        #     self.task_progress_bar.setStyleSheet("QProgressBar::chunk "
        #                                          "{"
        #                                          "background-color: green;"
        #                                          "}")

    def create_lsl(self, name='IndexPen_30', type='Gestur_Exp_Marker',
                   nominal_srate=3, channel_format='float32',
                   source_id='indexPen'):
        channel_count = 1
        # + \
        # config_signal.range_bins

        self.info_stream = StreamInfo(name=name, type=type, channel_count=channel_count,
                                      nominal_srate=nominal_srate, channel_format=channel_format,
                                      source_id=source_id)

        self.outlet_stream = StreamOutlet(self.info_stream)

        print("--------------------------------------\n" + \
              str(name) + \
              "LSL Configuration: \n" + \
              "  Stream 1: \n" + \
              "      Name: " + name + " \n" + \
              "      Type: " + type + " \n" + \
              "      Channel Count: " + str(channel_count) + "\n" + \
              "      Sampling Rate: " + str(nominal_srate) + "\n" + \
              "      Channel Format: " + channel_format + " \n" + \
              "      Source Id: " + source_id + " \n")

    def task_combo_box_index_changed(self):
        combo_box_index = self.task_combo_box.currentIndex()
        self.label_list_input.setText(
            self.task_dict[combo_box_index]
        )
        print('Current Selected Sentence: ', combo_box_index)
