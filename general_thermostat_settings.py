# -*- coding: utf-8 -*-

import sqlite3

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QRect, QDate, QTime
from PyQt5 import QtWidgets

from ui_general_thermostat_settings import Ui_GeneralSettingsDialog
import controlersettingsloader
import controllersettingsthread
import loading_dialog
import error_dialog


class GeneralThermostatSettingsDialog(QDialog, Ui_GeneralSettingsDialog):

    def __init__(self, host, name, password, _id, dbConn, parent=None):
        super(GeneralThermostatSettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self._id = _id
        self.dbConn = dbConn
        self.channelCombos = []
        self.saveButtons = [
            self.btnSaveOnOff, self.btnSaveDateTime,
            self.btnSaveLogInterval, self.btnSaveMode,
            self.btnSaveRouting, self.btnSaveTminTmax,
            self.btnSaveDatalogOnOff
        ]

        self.controlerSettings = controlersettingsloader.ControllerSettings()

        ####
        self.addCombos()
        self.setWindowTitle(name)
        self.host = host
        self.password = password

        self.setModal(True)

        self.controlerSettingsLoader = controlersettingsloader.ControllerSettingsLoader(
            host, self.password, self)
        self.controlerSettingsLoader.data_ready.connect(self.onDataReadyLoading)
        self.controlerSettingsLoader.error.connect(self.onErrorLoading)
        self.controlerSettingsLoader.start()
        self.loadingSavingDlg = loading_dialog.LoadingSavingDialog(self)

        self.controlerCommandSender = None

        # Connect Save buttons
        self.btnSaveTminTmax.clicked.connect(self.saveTminTmax)
        self.btnSaveMode.clicked.connect(self.saveMode)
        self.btnSaveRouting.clicked.connect(self.saveRouting)
        self.btnSaveOnOff.clicked.connect(self.saveOnOff)
        self.btnSaveLogInterval.clicked.connect(self.saveLogInterval)
        self.btnSaveDateTime.clicked.connect(self.saveDateTime)
        self.btnSaveDatalogOnOff.clicked.connect(self.saveLogOnOff)

        self.loadSettings()

    def addCombos(self):
        c = self.dbConn.cursor()
        try:
            c.execute("SELECT * FROM controler_channels WHERE controler_id='{}'".
                      format(self._id)
            )
            rows = c.fetchall()
        except sqlite3.OperationalError as e:
            QtWidgets.QMessageBox(
                self,
                'Грешка.',
                'Грешка при четене на имената на изходните '
                'канали от контролера. Грешка: {}'.format(str(e))
            )
        else:
            # add the channels mapping combos
            for i in range(10):
                label = QLabel(self.groupInOutMap)
                label.setText(rows[i][2])

                if i < 5:
                    label.setGeometry(QRect(17+122*i, 22, 112, 22))
                else:
                    label.setGeometry(QRect(17+122*(i-5), 78, 112, 22))

                label.setStyleSheet("border-style:none;font: bold;")

                combo = QComboBox(self.groupInOutMap)

                if i < 5:
                    combo.setGeometry(QRect(17+122*i, 47, 112, 22))
                else:
                    combo.setGeometry(QRect(17+122*(i-5), 103, 112, 22))

                for _ in range(10):
                    combo.addItem("Вход T({})".format(_))
                    combo.setCurrentIndex(0)

                self.channelCombos.append(combo)
                combo.currentIndexChanged.connect(self.make_combo_changed_hadler(i))


    def make_combo_changed_hadler(self, chanNum):

        def valueChanger():
            self.controlerSettings.indexInOut[chanNum] =\
                self.channelCombos[chanNum].currentIndex

        return valueChanger

    def loadSettings(self):
        [btn.setEnabled(False) for btn in self.saveButtons]
        self.loadingSavingDlg.show()

    def onDataReadyLoading(self, controlerSettings=controlersettingsloader.ControllerSettings()):
        self.controlerSettings = controlerSettings

        #
        # Input to output channels mapping
        #
        for i in range(10):
            self.channelCombos[i].setCurrentIndex(controlerSettings.indexInOut[i])

        #
        # Date and time
        #
        timeUnsplit = self.controlerSettings.time.split(",")[0]
        timeSplit = timeUnsplit.split(":")

        self.dateTimeEdit.setTime(QTime(int(timeSplit[0]), int(timeSplit[1])))

        date = self.controlerSettings.date.split("/")
        self.dateTimeEdit.setDate(QDate(int(date[2]), int(date[1]), int(date[0])))

        #
        # Cool / heat
        #

        if self.controlerSettings.mode_cool_heat == 0: # 0 - heat
            self.radioHeat.setChecked(True)
        else: # 1 - cool
            self.radioCool.setChecked(True)

        #
        # Tmin and Tmax
        #

        self.spinTmin.setValue(self.controlerSettings.tMin)
        self.spinTmax.setValue(self.controlerSettings.tMax)

        #
        # On/Off
        #
        if self.controlerSettings.turnOnOff:
            self.radioOn.setChecked(True)
        else:
            self.radioOff.setChecked(True)

        #
        # Log interval
        #
        high = self.controlerSettings.dataLogHigh
        high <<= 8
        low = self.controlerSettings.dataLogLow

        data_log_interval = high | low

        self.spinLogInterval.setValue(data_log_interval)

        #
        # Log start/stop
        #
        if self.controlerSettings.startSopDataLogStatus:
            self.radioDatalogOn.setChecked(True)
        else:
            self.radioDatalogOff.setChecked(True)

        # Close the loading dialog
        self.loadingSavingDlg.close()

        self.setFocus()

        # Enable buttons
        [btn.setEnabled(True) for btn in self.saveButtons]

    def onErrorLoading(self, error):
        # [btn.setEnabled(True) for btn in self.saveButtons]
        self.loadingSavingDlg.close()

        self.errorDlg = error_dialog.ErrorDialog(self)
        self.errorDlg.setWindowTitle('Грешка при четенето на настройките от контролера.')
        self.errorDlg.label.setText(
            "Възникна грешка при четенето на настойките от устройството моля опитайте пак. Грешка: {}".format(error))
        self.errorDlg.show()

    def saveRouting(self):
        [btn.setEnabled(False) for btn in self.saveButtons]
        cmd = ''

        for _ in self.channelCombos:
            cmd += str(_.currentIndex())
        cmd += 'I'

        self.controlerCommandSender = controllersettingsthread.ControlerCommandSender(self, self.host,
            self.password, [cmd])

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()
        self.showSavingDlg()

    def saveDateTime(self):
        [btn.setEnabled(False) for btn in self.saveButtons]
        cmd = '' # hhmmssddmmyyyyT

        thedate = self.dateTimeEdit.date()
        time = self.dateTimeEdit.time()

        day = str(thedate.day())
        month = str(thedate.month())
        year = str(thedate.year())

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        hours = str(time.hour())
        if len(hours) == 1:
            hours = '0' + hours

        minutes = str(time.minute())
        if len(minutes) == 1:
            minutes = '0' + minutes

        cmd = hours + minutes + '00' + day + month + year + 'T'

        self.controlerCommandSender = controllersettingsthread.ControlerCommandSender(self, self.host,
            self.password, [cmd])

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()

        self.showSavingDlg()

    def saveMode(self):
        [btn.setEnabled(False) for btn in self.saveButtons]

        cmd = ''
        if self.radioCool.isChecked():
            cmd = 'cool'
        else:
            cmd = 'heat'

        self.controlerCommandSender = controllersettingsthread.ControlerCommandSender(self, self.host,
            self.password, [cmd])

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()

        self.showSavingDlg()

    def saveTminTmax(self):
        [btn.setEnabled(False) for btn in self.saveButtons]

        tmin = str(self.spinTmin.value())

        sign = tmin[0]
        if sign == '-':
            tmin = tmin[1:]

        if len(tmin) < 3:
            padding = 3 - len(tmin)
            for _ in range(padding):
                tmin = '0' + tmin

        if sign =='-':
            cmdTmin = sign + tmin + 'N'
        else:
            cmdTmin = '0' + tmin + 'N'

        tmax = str(self.spinTmax.value())

        if len(tmax) < 3:
            padding = 3 - len(tmax)
            for _ in range(padding):
                tmax = '0' + tmax

        cmdTmax = tmax + 'X'

        # Init the commands sending thread
        self.controlerCommandSender = controllersettingsthread.ControlerCommandSender(self, self.host,
            self.password, [cmdTmin, cmdTmax])

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()

        self.showSavingDlg()

    def saveOnOff(self):
        [btn.setEnabled(False) for btn in self.saveButtons]

        cmd = ''

        if self.radioOff.isChecked():
            cmd = 'turnOf'
        else:
            cmd = 'turnOn'

        self.controlerCommandSender = controllersettingsthread.ControlerCommandSender(self, self.host,
            self.password, [cmd])

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()

        self.showSavingDlg()

    def saveLogInterval(self):
        [btn.setEnabled(False) for btn in self.saveButtons]

        cmd = str(self.spinLogInterval.value())

        if len(cmd) < 4:
            padding = 4 - len(cmd)

            for _ in range(padding):
                cmd = '0' + cmd

        cmd += 'L'

        self.controlerCommandSender = controllersettingsthread.ControlerCommandSender(self, self.host,
            self.password, [cmd])

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()

        self.showSavingDlg()

    def saveLogOnOff(self):
        [btn.setEnabled(False) for btn in self.saveButtons]

        if self.radioDatalogOn.isChecked():
            cmd = 'datalogStart'
        else:
            cmd = 'datalogStop'

        self.controlerCommandSender =\
            controllersettingsthread.ControlerCommandSender(
                self, self.host,
                self.password, [cmd]
            )

        # Connect on ready and error signals
        self.controlerCommandSender.data_ready.connect(self.onSaveDone)
        self.controlerCommandSender.error.connect(self.onErrorSave)

        self.controlerCommandSender.start()

        self.showSavingDlg()

    def showSavingDlg(self):
        self.loadingSavingDlg = loading_dialog.LoadingSavingDialog(self)
        self.loadingSavingDlg.label.setText("Записване на настройките в контролера ...")
        self.loadingSavingDlg.setWindowTitle('Записване на настройки.')
        self.loadingSavingDlg.show()
        self.loadingSavingDlg.setFocus(True)

    def onSaveDone(self):
        [btn.setEnabled(True) for btn in self.saveButtons]
        self.loadingSavingDlg.close()

    def onErrorSave(self, err):
        [btn.setEnabled(True) for btn in self.saveButtons]
        self.loadingSavingDlg.close()
        self.errorDlg = error_dialog.ErrorDialog(self)
        self.errorDlg.label.setText(
            "Възникна грешка при записването на настойките в устройството моля опитайте пак. Грешка: {}".format(err))
        self.errorDlg.show()
