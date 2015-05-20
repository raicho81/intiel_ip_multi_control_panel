# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tmintmaxwidget.ui'
#
# Created: Wed Feb  4 20:28:37 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(182, 101)
        self.tminTmaxFrame = QtWidgets.QGroupBox(Form)
        self.tminTmaxFrame.setGeometry(QtCore.QRect(0, 0, 181, 101))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tminTmaxFrame.setFont(font)
        self.tminTmaxFrame.setStyleSheet("QGroupBox {border-color: rgb(0, 0, 0);border-style: solid; border-width: 1px;}")
        self.tminTmaxFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.tminTmaxFrame.setObjectName("tminTmaxFrame")
        self.spinTmin = QtWidgets.QSpinBox(self.tminTmaxFrame)
        self.spinTmin.setGeometry(QtCore.QRect(30, 30, 51, 22))
        self.spinTmin.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.spinTmin.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinTmin.setMinimum(-255)
        self.spinTmin.setMaximum(255)
        self.spinTmin.setObjectName("spinTmin")
        self.btnSaveTmin = QtWidgets.QPushButton(self.tminTmaxFrame)
        self.btnSaveTmin.setGeometry(QtCore.QRect(50, 60, 81, 28))
        self.btnSaveTmin.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnSaveTmin.setObjectName("btnSaveTmin")
        self.spinTmax = QtWidgets.QSpinBox(self.tminTmaxFrame)
        self.spinTmax.setGeometry(QtCore.QRect(100, 30, 51, 22))
        self.spinTmax.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.spinTmax.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinTmax.setMinimum(-255)
        self.spinTmax.setMaximum(255)
        self.spinTmax.setObjectName("spinTmax")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tminTmaxFrame.setTitle(_translate("Form", "T(0) T Min и T Max ºC"))
        self.btnSaveTmin.setText(_translate("Form", "Запис"))

