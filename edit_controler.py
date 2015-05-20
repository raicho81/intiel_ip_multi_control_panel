# -*- coding: utf-8 -*-

import re
import sqlite3

from PyQt5 import QtWidgets

import ui_edit_controler
import controllersettingsthread
import re

import loading_dialog
import error_dialog


class EditControler(QtWidgets.QDialog, ui_edit_controler.Ui_Dialog):
    def __init__(self, parent, db_conn, _id):
        super(EditControler, self).__init__(parent)
        self.db_conn = db_conn
        self._id = _id
        self.setupUi(self)
        self.setModal(True)

        self.loadControlerData()

        self.btnSaveNameAddrPort.clicked.connect(
            self.saveControlerNameAddressPort
        )

        self.btnSavePassword.clicked.connect(self.changePassword)
        self.btnSaveLocalIPAddress.clicked.connect(self.saveControlerLocalAddress)
        self.btnSaveLocalPort.clicked.connect(self.saveControlerLocalPort)
        self.btnReset.clicked.connect(self.reset)
        self.savingDlg = None
        self.errorDlg = None
        self.passwordChange = False

    def showSavingDlg(self):
        self.savingDlg = loading_dialog.LoadingSavingDialog(
            self
        )
        self.savingDlg.setWindowTitle('Записване на настройки.')
        self.savingDlg.label.setText(
            'Записване на настройки в контролера ...'
        )
        self.savingDlg.show()

    def onError(self, err):
        self.passwordChange = False
        self.savingDlg.close()
        self.errorDlg = error_dialog.ErrorDialog(self)
        self.errorDlg.setWindowTitle(
            'Грешка при записване на настроки в контролера.'
        )
        self.errorDlg.label.setText(str(err))
        self.errorDlg.show()

    def onReady(self):
        if self.passwordChange:
            self.passwordChange = False
            c = self.db_conn.cursor()
            c.execute(
                "UPDATE controlers set password='{}' WHERE id='{}'".\
                format(
                    self.lineNewPassword.text(),
                    self._id
                )
            )
            self.db_conn.commit()
        self.savingDlg.close()

    def changePassword(self):
        # validate password
        c = self.db_conn.cursor()
        c.execute("SELECT * FROM controlers WHERE id = '{}'".format(
                self._id
            )
        )

        row = c.fetchone()

        if not self.lineCurrentPassword.text() == row[4]:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Грешна текуща парола.'
            )
            return

        rePass = '([a-z]|[A-Z]|\d){1,8}'

        if not re.match(rePass, self.lineNewPassword.text()):
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Паролата може да съдържа само букви и цифри '
                'и да е с дължина 8 символа.'
            )
            return

        if not self.lineNewPassword.text() ==\
            self.lineNewPasswordRepeat.text():
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Паролите не съвпадат.'
            )
            return

        c = self.db_conn.cursor()
        c.execute(
            "SELECT * FROM controlers WHERE id = '{}'".format(self._id)
        )
        row = c.fetchone()

        commands = []
        commands.append('{}P'.format(self.lineNewPassword.text()))

        controlerSettingsThread = controllersettingsthread.ControlerCommandSender(
            self,
            '{}:{}'.format(row[2], row[3]),
            row[4],
            commands
        )

        controlerSettingsThread.data_ready.connect(self.onReady)
        controlerSettingsThread.error.connect(self.onError)

        self.showSavingDlg()
        self.passwordChange = True

        controlerSettingsThread.start()

    def loadControlerData(self):
        c = self.db_conn.cursor()
        try:
            c.execute('SELECT * FROM controlers where id={}'.
                      format(self._id))
        except sqlite3.OperationalError as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка при четене от БД.',
                'Грешка при четене от БД. Грешка: {}'.format(str(e))
            )
            self.btnSaveLocalIPAddress.setEnabled(False)
            self.btnSaveLocalPort.setEnabled(False)
            self.btnSaveNameAddrPort.setEnabled(False)
            self.btnSavePassword.setEnabled(False)
        else:
            row = c.fetchone()

            # Set he data from the DB
            self.lineName.setText(row[1])
            self.lineIPAddress.setText(row[2])
            self.linePort.setText(row[3])

    def saveControlerNameAddressPort(self):
        # Validate input
        if len(self.lineName.text()) == 0:
            QtWidgets.QMessageBox.critical(self,
                                           'Грешка.',
                                           'Невалидно име. Името не може'
                                           ' да е празно.')
            return

        reIp = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if not re.match(reIp, self.lineIPAddress.text()):
            QtWidgets.QMessageBox.critical(self,
                                           'Грешка.',
                                           'Невалиден IP адрес')
            return

        rePort = '\d{1,3}'
        if not re.match(rePort, self.linePort.text()):
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Невалиден порт')
            return

        if int(self.linePort.text()) < 81 or\
                int(self.linePort.text()) > 255:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Невалиден порт. Валидните стойности на порт са между 81 '
                'и 255.')
            return

        # save
        c = self.db_conn.cursor()

        try:
            sql =   "UPDATE controlers SET name='{}', address='{}', port='{}'"\
                    " WHERE id='{}'".format(
                        self.lineName.text(),
                        self.lineIPAddress.text(),
                        self.linePort.text(),
                        self._id
                    )
            c.execute(
                sql
            )
            self.db_conn.commit()

        except sqlite3.OperationalError as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Грешка при запис в БД. Грешка: {}'.format(str(e))
            )

    def saveControlerLocalAddress(self):
        # validate address
        reAddress = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

        if not re.match(reAddress, self.lineLocalIPAddress.text()):
            QtWidgets.QMessageBox.critical(
                self,
                "Грешка.",
                'Невалиден IP адрес.'
            )
            return

        if not self.lineLocalIPAddress.text() == \
            self.lineLocalIPAddressRepeat.text():
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Адресите не съвпадат.'
            )
            return

        c = self.db_conn.cursor()
        c.execute(
            "SELECT * FROM controlers WHERE id = '{}'".format(self._id)
        )
        row = c.fetchone()

        commands = []

        addressText = self.lineLocalIPAddress.text()
        addressSplit = addressText.split('.')

        cmd = ''
        for x in addressSplit:
            if len(x) < 3:
                while len(x) < 3:
                    x = '0' + x
            cmd += x

        cmd += 'A'

        commands.append(cmd)

        controlerSettingsThread = controllersettingsthread.ControlerCommandSender(
            self,
            '{}:{}'.format(row[2], row[3]),
            row[4],
            commands
        )

        controlerSettingsThread.data_ready.connect(self.onReady)
        controlerSettingsThread.error.connect(self.onError)

        self.showSavingDlg()
        controlerSettingsThread.start()

    def saveControlerLocalPort(self):
        # Validate port

        portRe = '\d{1,3}'
        if not re.match(portRe, self.lineLocalPort.text()):
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                "Невалиден порт."
            )
            return

        if int(self.lineLocalPort.text()) < 81 or int(self.lineLocalPort.text()) > 255:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                "Невалидна стойност на порт. Валидни са стойности от 81 до 255."
            )
            return

        if self.lineLocalPort.text() != self.lineLocalPort_2.text():
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Портовете не съвпадат.'
            )
            return

        c = self.db_conn.cursor()
        c.execute(
            "SELECT * FROM controlers WHERE id = '{}'".format(self._id)
        )
        row = c.fetchone()

        port = self.lineLocalPort.text()

        while len(port) < 3:
            port = '0' + port

        commands = ['{}Pt'.format(port)]

        controlerSettingsThread = controllersettingsthread.ControlerCommandSender(
            self,
            '{}:{}'.format(row[2], row[3]),
            row[4],
            commands
        )

        controlerSettingsThread.data_ready.connect(self.onReady)
        controlerSettingsThread.error.connect(self.onError)

        self.showSavingDlg()
        controlerSettingsThread.start()

    def reset(self):
        commands = []

        c = self.db_conn.cursor()
        c.execute(
            "SELECT * FROM controlers WHERE id = '{}'".format(self._id)
        )
        row = c.fetchone()

        cmd = 'reset'

        commands.append(cmd)

        controlerSettingsThread = controllersettingsthread.ControlerCommandSender(
            self,
            '{}:{}'.format(
                row[2],
                row[3]
            ),
            row[4],
            commands
        )

        controlerSettingsThread.data_ready.connect(self.onReady)
        controlerSettingsThread.error.connect(self.onError)

        self.showSavingDlg()
        controlerSettingsThread.start()
