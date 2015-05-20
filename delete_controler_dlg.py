# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtCore

import ui_delete_controler


class DeleteControlerDlg(QtWidgets.QDialog, ui_delete_controler.Ui_Dialog):
    deletedControler = QtCore.pyqtSignal()

    def __init__(self, parent, _id, dbConn):
        super(DeleteControlerDlg, self).__init__(parent)
        self.setupUi(self)
        self.dbConn = dbConn
        self._id = _id
        self.btnCancel.clicked.connect(self.close)
        self.btnYes.clicked.connect(self.deleteControler)

    def deleteControler(self):
        c = self.dbConn.cursor()

        c.execute(
            "DELETE FROM controler_channels WHERE controler_id='{}'".
            format(self._id)
        )

        c.execute(
            "DELETE FROM controlers WHERE id = '{}'".format(self._id)
        )

        self.dbConn.commit()
        self.deletedControler.emit()
        self.close()