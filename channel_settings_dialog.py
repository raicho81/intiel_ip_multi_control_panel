# -*- coding: utf-8 -*-
import sqlite3

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from ui_channel_settings import Ui_Dialog
import controlersettingsloader
import error_dialog, loading_dialog
from channelsettings import ChannelSetter


class ChannelSettingsDialog(QDialog, Ui_Dialog):
    load_data = pyqtSignal()
    nameChanged = pyqtSignal(bool)

    def __init__(self, parent, chanNum, host, password, db_conn, id):
        super(ChannelSettingsDialog, self).__init__(parent)
        self.chanNum = chanNum
        self.host = host
        self.password = password
        self.db_conn = db_conn
        self._id = id

        # Set up the user interface from Designer.
        self.setupUi(self)

        # Read name
        self.readName()

        self.buttonSave.setEnabled(False)

        self.controlerSettingsLoader = controlersettingsloader.ControllerSettingsLoader(self.host,
                                                                                  self.password, self)
        self.controlerSettingsLoader.data_ready.connect(self.onDataReadyLoading)
        self.controlerSettingsLoader.error.connect(self.onErrorLoading)
        self.controlerSettingsLoader.start()
        self.loadingSavingDlg = loading_dialog.LoadingSavingDialog(self)

        self.channelSetter = None
        self.controlerSettings = controlersettingsloader.ControllerSettings()

        self.comboDays.addItem("Mon")
        self.comboDays.addItem("Tue")
        self.comboDays.addItem("Wed")
        self.comboDays.addItem("Thu")
        self.comboDays.addItem("Fri")
        self.comboDays.addItem("Sat")
        self.comboDays.addItem("Sun")

        self.comboDays.currentIndexChanged.connect(self.comboDaysHandler)
        self.comboDays.setEnabled(False)
        self.checkEnabled.clicked.connect(self.checkEnabledHandler)
        self.checkEnabled.setEnabled(False)

        self.load_data.connect(self.loadSettings)
        self.load_data.emit()
        self.buttonSaveName.clicked.connect(self.saveName)

    def readName(self):
        c = self.db_conn.cursor()
        try:
            c.execute(
                "SELECT name from controler_channels WHERE id='{}'".format(
                    self._id
                )
            )
        except sqlite3.OperationalError as e:
            QtWidgets.QMessageBox.critical(
                self,
                'Грешка.',
                'Грешка при четене от БД. Грешка: {}'.format(str(e))
            )
        else:
            name = c.fetchone()[0]
            self.setWindowTitle(name)
            self.lineName.setText(name)


    def comboDaysHandler(self):
        day = self.comboDays.currentText()
        self.checkEnabled.setChecked(self.controlerSettings.channelsOnOff[day][self.chanNum])

    def checkEnabledHandler(self):
        checked = self.checkEnabled.isChecked()
        day = self.comboDays.currentText()

        self.controlerSettings.channelsOnOff[day][self.chanNum] = int(checked)

    def loadSettings(self):
        self.loadingSavingDlg.show()
        self.loadingSavingDlg.setModal(True)
        self.loadingSavingDlg.setFocus(True)

    def save(self):
        self.buttonSave.setEnabled(False)
        self.checkEnabled.setEnabled(False)
        self.comboDays.setEnabled(False)

        channelZones = self.controlerSettings.channelsZones[self.chanNum]

        # zones hours
        channelZones.timeZonesH[0] = self.spinStartHour.value()
        channelZones.timeZonesH[1] = self.spinStartHour_2.value()
        channelZones.timeZonesH[2] = self.spinStartHour_3.value()
        channelZones.timeZonesH[3] = self.spinStartHour_4.value()

        # zones minutes
        channelZones.timeZonesM[0] = self.spinStartMin.value()
        channelZones.timeZonesM[1] = self.spinStartMin_2.value()
        channelZones.timeZonesM[2] = self.spinStartMin_3.value()
        channelZones.timeZonesM[3] = self.spinStartMin_4.value()

        # zones triggers
        channelZones.timeZonesTrig[0] = self.spinTemp.value()
        channelZones.timeZonesTrig[1] = self.spinTemp_2.value()
        channelZones.timeZonesTrig[2] = self.spinTemp_3.value()
        channelZones.timeZonesTrig[3] = self.spinTemp_4.value()

        # channels histeresis
        self.controlerSettings.channelsHisteresis[self.chanNum] = int(round(self.spinHisteresis.value()*2))

        # Run the settings thread
        self.channelSetter = ChannelSetter(self.host, self.chanNum, self.controlerSettings,
                                           self.password, self)
        self.channelSetter.data_ready.connect(self.onReadySaving)
        self.channelSetter.error.connect(self.onErrorSaving)

        self.loadingSavingDlg = loading_dialog.LoadingSavingDialog(self)
        self.loadingSavingDlg.setWindowTitle("Записване на настройките в контролера")
        self.loadingSavingDlg.label.setText("Записване на настройките в контролера ...")
        self.loadingSavingDlg.show()
        self.loadingSavingDlg.setFocus(True)

        self.channelSetter.start()


    def onDataReadyLoading(self, controlerSettings=controlersettingsloader.ControllerSettings()):
        self.controlerSettings = controlerSettings
        self.loadingSavingDlg.close()

        # start zones

        # read hours
        self.spinStartHour.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[0])
        self.spinEndHour.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[1])


        self.spinStartHour_2.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[1])
        self.spinEndHour_2.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[2])

        self.spinStartHour_3.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[2])
        self.spinEndHour_3.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[3])

        self.spinStartHour_4.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[3])
        self.spinEndHour_4.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesH[0])

        # read minutes
        self.spinStartMin.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[0])
        self.spinEndMin.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[1])


        self.spinStartMin_2.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[1])
        self.spinEndMin_2.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[2])

        self.spinStartMin_3.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[2])
        self.spinEndMin_3.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[3])

        self.spinStartMin_4.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[3])
        self.spinEndMin_4.setValue(controlerSettings.channelsZones[self.chanNum].timeZonesM[0])


        # read trigger temp
        temp = controlerSettings.channelsZones[self.chanNum].timeZonesTrig[0]
        if controlerSettings.triggerZonesIndex[self.chanNum][0] == 0:
            temp = -temp
        self.spinTemp.setValue(temp)
        self.spinTemp.setMinimum(controlerSettings.tMin)
        self.spinTemp.setMaximum(controlerSettings.tMax)

        temp2 = controlerSettings.channelsZones[self.chanNum].timeZonesTrig[1]
        if controlerSettings.triggerZonesIndex[self.chanNum][1] == 0:
            temp2 = -temp2
        self.spinTemp_2.setValue(temp2)
        self.spinTemp_2.setMinimum(controlerSettings.tMin)
        self.spinTemp_2.setMaximum(controlerSettings.tMax)

        temp3 = controlerSettings.channelsZones[self.chanNum].timeZonesTrig[2]
        if controlerSettings.triggerZonesIndex[self.chanNum][2] == 0:
            temp3 = -temp3
        self.spinTemp_3.setValue(temp3)
        self.spinTemp_3.setMinimum(controlerSettings.tMin)
        self.spinTemp_3.setMaximum(controlerSettings.tMax)

        temp4 = controlerSettings.channelsZones[self.chanNum].timeZonesTrig[3]
        if controlerSettings.triggerZonesIndex[self.chanNum][3] == 0:
            temp4 = -temp4
        self.spinTemp_4.setValue(temp4)
        self.spinTemp_4.setMinimum(controlerSettings.tMin)
        self.spinTemp_4.setMaximum(controlerSettings.tMax)

        # end zones

        # set histeresis
        self.spinHisteresis.setValue(float(controlerSettings.channelsHisteresis[self.chanNum])/2)


        # # Tmin and Tmax
        # tminSign = self.controlerSettings.channelsTMinSign[self.chanNum]
        #
        # if tminSign == 0:
        #     tmin = - self.controlerSettings.channelsTMin[self.chanNum]
        # else:
        #     tmin = self.controlerSettings.channelsTMin[self.chanNum]
        #
        # self.spinTMin.setValue(tmin)
        #
        # tmax = self.controlerSettings.channelsTMax[self.chanNum]
        #
        # self.spinTMax.setValue(tmax)

        self.buttonSave.setEnabled(True)
        self.checkEnabled.setEnabled(True)
        self.comboDays.setEnabled(True)

        # refresh enabled
        self.comboDaysHandler()

    def onErrorLoading(self, error):
        self.loadingSavingDlg.close()

        self.errorDlg = error_dialog.ErrorDialog(self)
        self.errorDlg.setWindowTitle('Грешка при четене на настройки.')
        self.errorDlg.label.setText("Възникна грешка при четенето на настойките от "
                                    "устройството моля опитайте пак. Грешка: {}.".format(error))
        self.errorDlg.show()

    def onReadySaving(self):
        self.buttonSave.setEnabled(True)
        self.checkEnabled.setEnabled(True)
        self.comboDays.setEnabled(True)

        self.loadingSavingDlg.close()

    def onErrorSaving(self, error):
        self.buttonSave.setEnabled(True)
        self.checkEnabled.setEnabled(True)
        self.comboDays.setEnabled(True)

        self.loadingSavingDlg.close()
        self.errorDlg = error_dialog.ErrorDialog(self)
        self.errorDlg.setWindowTitle('Грешка при записване на настройки.')
        self.errorDlg.label.setText("Възникна грешка при записване на настойките в устройството."
                                    " Моля опитайте пак. Грешка: {}".format(error))
        self.errorDlg.show()

    def saveName(self):
        cursor = self.db_conn.cursor()

        try:
            cursor.execute("UPDATE controler_channels set name='{}' WHERE id={}".
                format(
                    self.lineName.text(),
                    self._id
                )
            )
            self.db_conn.commit()
            self.nameChanged.emit(False)
            self.setWindowTitle(self.lineName.text())
        except Exception as e:
            QMessageBox.critical(self, 'Системна хрешка.',
                'Грешка при запис в БД. Грешка: {}'.format(str(e))
            )