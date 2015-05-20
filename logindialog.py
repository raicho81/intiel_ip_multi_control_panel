# -*- coding: utf-8 -*-

import sqlite3

from  PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

import ui_login
import mainwindow


class LoginDialog(QtWidgets.QDialog, ui_login.Ui_Dialog):
    start = pyqtSignal(object)

    def __init__(self, parent=None, main=None):
        super(LoginDialog, self).__init__(parent)
        self.main = main
        self.setupUi(self)

        self.btnLogin.clicked.connect(self.login)
        self.mainwindow = None

        self.comboUser.addItem('Admin')
        self.comboUser.addItem('User')
        self.comboUser.addItem('Service')

    def login(self):
        conn = sqlite3.connect('controlers.db')
        c = conn.cursor()
        c.execute(
            "select * from users where name='{}' and password='{}' limit 1".
            format(
                self.comboUser.currentText(),
                self.linePass.text()
            )
        )
        row = c.fetchone()
        conn.close()

        if row is not None:
            self.main = mainwindow.MainWindow(
                None,
                row[3],
                row[0]
            )
            # QtWidgets.QApplication.lastWindowClosed.connect(self.close)

            self.hide()

            self.main.show()
        else:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешна парола.',
                'Грешна парола. Моля опитайте пак.'
            )
