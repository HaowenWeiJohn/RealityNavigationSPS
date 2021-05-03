import time

import cv2
import pyqtgraph as pg
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from pylsl import local_clock

import config_ui
from interfaces.InferenceInterface import InferenceInterface
from interfaces.LSLInletInterface import LSLInletInterface
from utils.sim import sim_openBCI_eeg, sim_unityLSL, sim_inference

import pyautogui

import numpy as np

from utils.ui_utils import dialog_popup
class LSLOutletWorker(QObject)：