# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delete_controler.ui'
#
# Created: Mon Feb  2 20:14:13 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(477, 92)
        self.btnYes = QtWidgets.QPushButton(Dialog)
        self.btnYes.setGeometry(QtCore.QRect(160, 60, 75, 23))
        self.btnYes.setObjectName("btnYes")
        self.btnCancel = QtWidgets.QPushButton(Dialog)
        self.btnCancel.setGeometry(QtCore.QRect(250, 60, 75, 23))
        self.btnCancel.setObjectName("btnCancel")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 20, 471, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.btnCancel.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Премахване на контролер."))
        self.btnYes.setText(_translate("Dialog", "Да"))
        self.btnCancel.setText(_translate("Dialog", "Отказ"))
        self.label.setText(_translate("Dialog", "Сигурни ли сте, че желаете да изтриете избрания контролер?"))

