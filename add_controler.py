# -*- coding: utf-8 -*-

import re
import sqlite3

from PyQt5 import QtWidgets

import ui_add_controler


class AddControlerDlg(QtWidgets.QDialog, ui_add_controler.Ui_Dialog):
    def __init__(self, parent, db_conn):
        super(AddControlerDlg, self).__init__(parent)
        self.db_conn = db_conn
        self.setupUi(self)
        self.setModal(True)
        self.btnSave.clicked.connect(self.addController)

    def addController(self):
        # validate input
        if len(self.lineName.text()) == 0:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Името не може да е празно.'
            )
            return

        reIp = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if not re.match(reIp, self.lineIPAddress.text()):
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Невалиден IP адрес'
            )

            return

        rePort = '\d{1,3}'
        if not re.match(rePort, self.linePort.text()):
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Невалиден порт'
            )
            return

        if int(self.linePort.text()) < 81 or\
            int(self.linePort.text()) > 255:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Невалиден порт. Валидните стойности на порт са между 81 '
                'и 255.'
            )
            return

        rePass = '([a-z]|[A-Z]|\d){1,8}'
        if not re.match(rePass, self.lineNewPassword.text()):
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Паролата може да е само букви и цифри с дължина до 8.'
            )
            return

        if self.lineNewPassword.text() !=\
            self.lineNewPasswordRepeat.text():
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка',
                'Паролите се различават.'
            )

            return

        c = self.db_conn.cursor()

        try:
            c.execute(
                "INSERT INTO controlers SELECT NULL,'{}', "
                "'{}', '{}' , '{}'".\
                format(
                    self.lineName.text(),
                    self.lineIPAddress.text(),
                    self.linePort.text(),
                    self.lineNewPassword.text()
                )
            )

            c.execute('SELECT last_insert_rowid()')
            row = c.fetchone()

            for i in range(10):
                c.execute("INSERT INTO controler_channels SELECT"
                          " NULL, '{}', '{}'".
                          format(row[0], 'Термостат {}'.format(i))
                )

            self.db_conn.commit()
        except sqlite3.OperationalError as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Грешка при запис в БД. Грешка: {}'.\
                format(str(e))
            )
        else:
            self.close()
