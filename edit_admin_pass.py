# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

import ui_edit_admin_pass


class EditAdminPass(QtWidgets.QDialog, ui_edit_admin_pass.Ui_Dialog):
    def __init__(self, parent, db_conn):
        super(EditAdminPass, self).__init__(parent)
        self.db_conn = db_conn
        self.setupUi(self)
        self.setModal(True)

        self.pushSavePass.clicked.connect(self.savePass)

    def savePass(self):
        # Some validation
        c = self.db_conn.cursor()
        c.execute("SELECT password FROM users WHERE name='Admin'")
        row = c.fetchone()

        if row[0] != self.lineCurrentPass.text():
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка',
                'Грешка. Текущата парола не съвпада.'
            )
            return

        if self.lineNewPass.text() == '':
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка',
                'Грешка. Паролата не може да е празна.'
            )
            return

        if self.lineNewPass.text() != self.lineNewPassRepeat.text():
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка',
                'Грешка. Паролите не съвпадат..'
            )
            return

        c = self.db_conn.cursor()
        c.execute(
            "UPDATE users SET password='{}' WHERE name='Admin'".
            format(
                self.lineNewPass.text()
            )
        )

        self.db_conn.commit()
        self.close()