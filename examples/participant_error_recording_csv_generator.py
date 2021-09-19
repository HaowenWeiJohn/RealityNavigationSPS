# This Python file uses the following encoding: utf-8
import os
import pickle
import sys
import time

import numpy as np
from datetime import datetime

from config import config_ui, config_signal

from utils.ui_utils import init_slider_bar_box
from utils.ui_utils import *
import pandas as pd

tasks = generate_sentence_task('../resources/pangram/40sentences.txt')

tasks_len = len(tasks)
for b in range (0,len(tasks)):
    tasks.insert(b*2+1,'')

for index in range(0, len(tasks)):
    tasks[index] = tasks[index].split(' ')
error_recording_form = pd.DataFrame(tasks)

row_name = []
for index in range(1,tasks_len+1):
    row_name.append(index)
    row_name.append(str(index)+'_error')

error_recording_form.index = row_name

print(error_recording_form.index)
error_recording_form.to_csv('error_recording_form.csv')


