# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog

from ui_error_saving_settings import Ui_Dialog


class ErrorDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(ErrorDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)