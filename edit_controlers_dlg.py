# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import ui_edit_controlers
import edit_controler
import add_controler
import delete_controler_dlg


class EditControlersDlg(QtWidgets.QDialog,
                        ui_edit_controlers.Ui_EditControllersDialog):
    def __init__(self, parent, db_conn):
        super(EditControlersDlg, self).__init__(parent)
        self.db_conn = db_conn
        self.setupUi(self)
        self.tableModel = None
        self.setModal(True)
        self.createTable()
        self.btnEdit.clicked.connect(self.showEditControlerDlg)
        self.btnAdd.clicked.connect(self.showAddControlerDlg)
        self.btnRemove.clicked.connect(self.showRemoveControler)

    def showRemoveControler(self):
        indexes = self.controlersTableView.selectedIndexes()
        controler_id = self.controlersTableView.model().data(indexes[0], 0)
        controler_id = controler_id.value()

        deleteControlerDlg = delete_controler_dlg.DeleteControlerDlg(
            self,
            controler_id,
            self.db_conn
        )

        deleteControlerDlg.finished.connect(self.updateTableModel)
        deleteControlerDlg.show()

    def createTable(self):
        # create the view
        tv = self.controlersTableView

        # set the table model
        header = ['ID', 'Име', 'Адрес', 'Порт']

        self.tableModel = ControlersTableModel(self, self.db_conn,
                                               header)
        tm = self.tableModel
        tv.setModel(tm)

        tv.setSelectionMode(tv.SingleSelection)
        tv.setSelectionBehavior(tv.SelectRows)

        # set the minimum size
        self.setMinimumSize(400, 300)

        # hide grid
        tv.setShowGrid(False)

        # set the font
        font = QtGui.QFont("Courier New", 8)
        tv.setFont(font)

        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        tv.resizeColumnsToContents()

        # set row height
        nrows = tm.rowCount(None)
        for row in range(nrows):
            tv.setRowHeight(row, 18)

        if nrows > 0:
            tv.selectRow(0)
        else:
            self.btnRemove.setEnabled(False)
            self.btnEdit.setEnabled(False)

        # enable sorting
        # this doesn't work
        #tv.setSortingEnabled(True)

        return tv

    def updateTableModel(self):
        self.tableModel.loadData()
        if self.tableModel.rowCount(None) > 0:
            self.btnEdit.setEnabled(True)
            self.btnRemove.setEnabled(True)
            self.controlersTableView.selectRow(0)
        else:
            self.btnEdit.setEnabled(False)
            self.btnRemove.setEnabled(False)

    def showEditControlerDlg(self):
        indexes = self.controlersTableView.selectedIndexes()
        controler_id = self.controlersTableView.model().data(indexes[0], 0)
        controler_id = controler_id.value()

        editControlerDlg = edit_controler.EditControler(
            self, self.db_conn, controler_id
        )
        editControlerDlg.finished.connect(self.updateTableModel)
        editControlerDlg.show()

    def showAddControlerDlg(self):
        addControlerDlg = add_controler.AddControlerDlg(self, self.db_conn)

        addControlerDlg.finished.connect(self.updateTableModel)
        addControlerDlg.show()

class ControlersTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, db_conn, headerdata, *args):
        super(ControlersTableModel, self).__init__(parent, *args)
        self.parent = parent
        self.arraydata = None
        self.headerdata = headerdata
        self.db_conn = db_conn
        self.loadData()

    def loadData(self):
        c = self.db_conn.cursor()

        c.execute('SELECT id, name, address, port FROM controlers')
        self.arraydata = c.fetchall()
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.headerdata)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()
