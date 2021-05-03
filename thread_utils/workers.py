import time

import cv2
import pyqtgraph as pg
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from pylsl import local_clock

from config import config_ui

from utils.sim import sim_openBCI_eeg, sim_unityLSL, sim_inference

import pyautogui

import numpy as np

from utils.ui_utils import dialog_popup
# class LSLOutletWorker(QObject)：