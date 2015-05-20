# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from ui_loading import Ui_LoadingMessageDialog


class LoadingSavingDialog(QDialog, Ui_LoadingMessageDialog):
    def __init__(self, parent):
        super(LoadingSavingDialog, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(self.windowFlags() |
        #                     Qt.FramelessWindowHint |
        #                     Qt.Dialog)

        # self.setModal(True)
        # self.processingTimer = QTimer()
        # self.processingTimer.timeout.connect(QtWidgets.QApplication.processEvents)
        # self.processingTimer.start(50)
