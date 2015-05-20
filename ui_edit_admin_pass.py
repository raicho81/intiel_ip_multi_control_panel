# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_admin_pass.ui'
#
# Created: Sat Nov 15 19:16:07 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(361, 180)
        Dialog.setMinimumSize(QtCore.QSize(361, 180))
        Dialog.setMaximumSize(QtCore.QSize(361, 180))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 111, 16))
        self.label.setObjectName("label")
        self.lineCurrentPass = QtWidgets.QLineEdit(Dialog)
        self.lineCurrentPass.setGeometry(QtCore.QRect(130, 20, 211, 20))
        self.lineCurrentPass.setMaxLength(100)
        self.lineCurrentPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineCurrentPass.setObjectName("lineCurrentPass")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 111, 16))
        self.label_2.setObjectName("label_2")
        self.lineNewPass = QtWidgets.QLineEdit(Dialog)
        self.lineNewPass.setGeometry(QtCore.QRect(130, 60, 211, 20))
        self.lineNewPass.setMaxLength(100)
        self.lineNewPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineNewPass.setObjectName("lineNewPass")
        self.lineNewPassRepeat = QtWidgets.QLineEdit(Dialog)
        self.lineNewPassRepeat.setGeometry(QtCore.QRect(130, 100, 211, 20))
        self.lineNewPassRepeat.setMaxLength(100)
        self.lineNewPassRepeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineNewPassRepeat.setObjectName("lineNewPassRepeat")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 111, 16))
        self.label_3.setObjectName("label_3")
        self.pushSavePass = QtWidgets.QPushButton(Dialog)
        self.pushSavePass.setGeometry(QtCore.QRect(140, 140, 81, 21))
        self.pushSavePass.setObjectName("pushSavePass")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Смяна на Admin парола"))
        self.label.setText(_translate("Dialog", "Текуща парола"))
        self.label_2.setText(_translate("Dialog", "Нова парола"))
        self.label_3.setText(_translate("Dialog", "Повторете парола"))
        self.pushSavePass.setText(_translate("Dialog", "Запис"))

