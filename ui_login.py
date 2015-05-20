# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sat Nov 15 01:52:33 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(322, 131)
        self.linePass = QtWidgets.QLineEdit(Dialog)
        self.linePass.setGeometry(QtCore.QRect(90, 60, 221, 22))
        self.linePass.setMaxLength(100)
        self.linePass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.linePass.setObjectName("linePass")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 60, 53, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label_2.setObjectName("label_2")
        self.btnLogin = QtWidgets.QPushButton(Dialog)
        self.btnLogin.setGeometry(QtCore.QRect(60, 97, 93, 21))
        self.btnLogin.setObjectName("btnLogin")
        self.btnCancel = QtWidgets.QPushButton(Dialog)
        self.btnCancel.setGeometry(QtCore.QRect(170, 97, 93, 21))
        self.btnCancel.setObjectName("btnCancel")
        self.comboUser = QtWidgets.QComboBox(Dialog)
        self.comboUser.setGeometry(QtCore.QRect(90, 20, 221, 22))
        self.comboUser.setObjectName("comboUser")

        self.retranslateUi(Dialog)
        self.btnCancel.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Моля въведете потребител и парола"))
        self.label.setText(_translate("Dialog", "Парола"))
        self.label_2.setText(_translate("Dialog", "Потребител"))
        self.btnLogin.setText(_translate("Dialog", "Вход"))
        self.btnCancel.setText(_translate("Dialog", "Отказ"))

