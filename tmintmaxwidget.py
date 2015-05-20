# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

import ui_tmintmaxwidget


class TminTmaxWidget(QtWidgets.QWidget, ui_tmintmaxwidget.Ui_Form):

    def __init__(self, parent):
        super(TminTmaxWidget, self).__init__(parent)
        self.setupUi(self)

    def getSaveBtn(self):
        return self.btnSaveTmin

    def getTmin(self):
        return self.spinTmin.value()

    def getTmax(self):
        return self.spinTmax.value()

    def setTmin(self, value):
        self.spinTmin.setValue(value)

    def setTmax(self, value):
        self.spinTmax.setValue(value)

    def setTitle(self, title):
        self.tminTmaxFrame.setTitle(title)