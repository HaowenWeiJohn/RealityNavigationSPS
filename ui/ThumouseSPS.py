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

from utils.ui_utils import stream_stylesheet
from utils.data_utils import RNStream
from utils.ui_utils import dialog_popup
import pyqtgraph as pg

class ThumouseSPS(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.ui = uic.loadUi("ui/ThumouseSPS.ui", self)



