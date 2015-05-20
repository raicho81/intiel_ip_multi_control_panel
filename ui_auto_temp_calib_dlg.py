# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auto_temp_calib_dlg.ui'
#
# Created: Mon Feb  2 21:05:51 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AutoTempCalibDlg(object):
    def setupUi(self, AutoTempCalibDlg):
        AutoTempCalibDlg.setObjectName("AutoTempCalibDlg")
        AutoTempCalibDlg.resize(680, 171)
        AutoTempCalibDlg.setMinimumSize(QtCore.QSize(680, 171))
        AutoTempCalibDlg.setMaximumSize(QtCore.QSize(680, 171))
        self.frame = QtWidgets.QFrame(AutoTempCalibDlg)
        self.frame.setGeometry(QtCore.QRect(10, 10, 661, 81))
        self.frame.setStyleSheet("border-width:1px;border-style: solid;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.labelInstructions = QtWidgets.QLabel(self.frame)
        self.labelInstructions.setGeometry(QtCore.QRect(10, 10, 641, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelInstructions.setFont(font)
        self.labelInstructions.setStyleSheet("border-style : none;")
        self.labelInstructions.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelInstructions.setWordWrap(True)
        self.labelInstructions.setObjectName("labelInstructions")
        self.btnStep1 = QtWidgets.QPushButton(AutoTempCalibDlg)
        self.btnStep1.setGeometry(QtCore.QRect(120, 120, 93, 28))
        self.btnStep1.setObjectName("btnStep1")
        self.btnStep2 = QtWidgets.QPushButton(AutoTempCalibDlg)
        self.btnStep2.setGeometry(QtCore.QRect(240, 120, 93, 28))
        self.btnStep2.setObjectName("btnStep2")
        self.btnSave = QtWidgets.QPushButton(AutoTempCalibDlg)
        self.btnSave.setGeometry(QtCore.QRect(360, 120, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.btnClose = QtWidgets.QPushButton(AutoTempCalibDlg)
        self.btnClose.setGeometry(QtCore.QRect(480, 120, 93, 28))
        self.btnClose.setObjectName("btnClose")

        self.retranslateUi(AutoTempCalibDlg)
        self.btnClose.clicked.connect(AutoTempCalibDlg.close)
        QtCore.QMetaObject.connectSlotsByName(AutoTempCalibDlg)

    def retranslateUi(self, AutoTempCalibDlg):
        _translate = QtCore.QCoreApplication.translate
        AutoTempCalibDlg.setWindowTitle(_translate("AutoTempCalibDlg", "Автоматична калибрация на температурни входове."))
        self.labelInstructions.setText(_translate("AutoTempCalibDlg", "TextLabelb ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffsssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"))
        self.btnStep1.setText(_translate("AutoTempCalibDlg", "Стъпка 1"))
        self.btnStep2.setText(_translate("AutoTempCalibDlg", "Стъпка 2"))
        self.btnSave.setText(_translate("AutoTempCalibDlg", "Калибрация"))
        self.btnClose.setText(_translate("AutoTempCalibDlg", "Затваряне"))

