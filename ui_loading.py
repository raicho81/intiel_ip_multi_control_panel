# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading.ui'
#
# Created: Thu Nov  6 00:04:27 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoadingMessageDialog(object):
    def setupUi(self, LoadingMessageDialog):
        LoadingMessageDialog.setObjectName("LoadingMessageDialog")
        LoadingMessageDialog.setWindowModality(QtCore.Qt.NonModal)
        LoadingMessageDialog.setEnabled(True)
        LoadingMessageDialog.resize(571, 101)
        LoadingMessageDialog.setModal(True)
        self.frame = QtWidgets.QFrame(LoadingMessageDialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 571, 101))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 20, 531, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label.setStyleSheet("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(LoadingMessageDialog)
        QtCore.QMetaObject.connectSlotsByName(LoadingMessageDialog)

    def retranslateUi(self, LoadingMessageDialog):
        _translate = QtCore.QCoreApplication.translate
        LoadingMessageDialog.setWindowTitle(_translate("LoadingMessageDialog", "Зареждане на настройки"))
        self.label.setText(_translate("LoadingMessageDialog", "Зареждане на настройки от контролера ..."))

