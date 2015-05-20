# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_controlers.ui'
#
# Created: Tue Nov  4 22:27:43 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditControllersDialog(object):
    def setupUi(self, EditControllersDialog):
        EditControllersDialog.setObjectName("EditControllersDialog")
        EditControllersDialog.resize(818, 393)
        EditControllersDialog.setMinimumSize(QtCore.QSize(818, 393))
        EditControllersDialog.setMaximumSize(QtCore.QSize(818, 393))
        self.groupBox = QtWidgets.QGroupBox(EditControllersDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 581, 371))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox {border-color: rgb(0, 0, 0);border-style: solid; border-width: 1px;}")
        self.groupBox.setObjectName("groupBox")
        self.controlersTableView = QtWidgets.QTableView(self.groupBox)
        self.controlersTableView.setGeometry(QtCore.QRect(10, 20, 561, 341))
        self.controlersTableView.setAlternatingRowColors(True)
        self.controlersTableView.setSortingEnabled(False)
        self.controlersTableView.setObjectName("controlersTableView")
        self.btnEdit = QtWidgets.QPushButton(EditControllersDialog)
        self.btnEdit.setGeometry(QtCore.QRect(630, 30, 161, 28))
        self.btnEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnEdit.setObjectName("btnEdit")
        self.btnAdd = QtWidgets.QPushButton(EditControllersDialog)
        self.btnAdd.setGeometry(QtCore.QRect(630, 100, 161, 28))
        self.btnAdd.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnAdd.setObjectName("btnAdd")
        self.btnRemove = QtWidgets.QPushButton(EditControllersDialog)
        self.btnRemove.setGeometry(QtCore.QRect(630, 170, 161, 28))
        self.btnRemove.setObjectName("btnRemove")
        self.btnClose = QtWidgets.QPushButton(EditControllersDialog)
        self.btnClose.setGeometry(QtCore.QRect(630, 240, 161, 28))
        self.btnClose.setObjectName("btnClose")

        self.retranslateUi(EditControllersDialog)
        self.btnClose.clicked.connect(EditControllersDialog.close)
        QtCore.QMetaObject.connectSlotsByName(EditControllersDialog)

    def retranslateUi(self, EditControllersDialog):
        _translate = QtCore.QCoreApplication.translate
        EditControllersDialog.setWindowTitle(_translate("EditControllersDialog", "Редакция на контролери"))
        self.groupBox.setTitle(_translate("EditControllersDialog", "Списък с контролери"))
        self.btnEdit.setText(_translate("EditControllersDialog", "Редакция"))
        self.btnAdd.setText(_translate("EditControllersDialog", "Добавяне на нов"))
        self.btnRemove.setText(_translate("EditControllersDialog", "Премахване"))
        self.btnClose.setText(_translate("EditControllersDialog", "Затваряне"))

