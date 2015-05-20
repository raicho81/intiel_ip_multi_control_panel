# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_saving_settings.ui'
#
# Created: Sun Sep 14 15:50:56 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(581, 112)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 561, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.btnClose = QtWidgets.QPushButton(Dialog)
        self.btnClose.setGeometry(QtCore.QRect(240, 70, 93, 28))
        self.btnClose.setObjectName("btnClose")

        self.retranslateUi(Dialog)
        self.btnClose.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Грешка при записване на настройките"))
        self.label.setText(_translate("Dialog", "Възникна грешка при записването моля проверете настройките и опитайте пак."))
        self.btnClose.setText(_translate("Dialog", "Затваряне"))

