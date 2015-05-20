# -*- coding: utf-8 -*-

import sqlite3
import os
import re

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
import PyQt5.Qt as Qt

from controlermonitor import ControlerMonitor
from general_thermostat_settings import GeneralThermostatSettingsDialog
import loading_dialog
import temp_inputs_calib_dlg
import auto_temp_calib_dlg
import edit_controlers_dlg
from error_dialog import ErrorDialog
from controllersettingsthread import ControlerCommandSender
import edit_user_pass
import edit_admin_pass


class MainWindow(QMainWindow):

    def __init__(self, parent=None, user_type=None, user_id=None):
        super(MainWindow, self).__init__(parent)
        self.user_type = user_type
        self.user_id = user_id

        self.setBaseSize(900, 700)
        self.controllerMonitors = []
        self.setWindowTitle("INTIEL MultiThermostat Control Panel")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(900, 700))

        #---------
        # Toolbar
        #---------
        # self.mainToolBar = QToolBar(self)
        # self.mainToolBar.setObjectName("mainToolBar")
        # self.addToolBar(Qt.TopToolBarArea, self.mainToolBar)

        #--------
        # Menu
        #--------

        self.menu = self.menuBar().addMenu("Файл")

        self.menuSettings = self.menuBar().addMenu("Настройки")

        self.actionGeneralSettings =\
            self.menuSettings.addAction("Общи за контролера")
        self.actionTempChannelsCalibSettings =\
            self.menuSettings.addAction("Ръчна калибрация на температурни входове")
        self.actionAutoTempChannelsCalibSettings =\
            self.menuSettings.addAction("Автоматична калибрация на температурни входове")
        self.menuSettings.addSeparator()

        self.actionEditControllers =\
            self.menuSettings.addAction("Редакция контролери")

        # Change passwords actions
        self.actionChangeAdminPass =\
            self.menuSettings.addAction("Промяна на Admin парола")
        self.actionChangeUserPass =\
            self.menuSettings.addAction("Промяна на User парола")

        self.menuOther = self.menuBar().addMenu('Други')
        self.actionSaveDatalog =\
            self.menuOther.addAction('Сваляне на datalog.txt')
        self.actionSaveConfig =\
            self.menuOther.addAction('Сваляне на config.txt')
        self.actionSaveCalib =\
            self.menuOther.addAction('Сваляне на calibr.txt')

        self.actionExit = self.menu.addAction("Изход")

        # Connect actions
        self.actionExit.triggered.connect(self.close)

        self.actionGeneralSettings.triggered.connect(self.showGeneralSettings)

        self.actionTempChannelsCalibSettings.triggered.connect(self.showTempInputsCalibDlg)
        self.actionAutoTempChannelsCalibSettings.triggered.connect(self.showAutoTempInputsCalibDlg)

        self.actionEditControllers.triggered.connect(self.showControlersEditor)

        self.actionSaveDatalog.triggered.connect(self.showSavingDatalogDlg)
        self.actionSaveConfig.triggered.connect(self.showSavingConfigDlg)
        self.actionSaveCalib.triggered.connect(self.showSavingCalibDlg)

        self.actionChangeUserPass.triggered.connect(self.showChangeUserPass)
        self.actionChangeAdminPass.triggered.connect(self.showChangeAdminPass)
        #---------

        #----------------
        # Central widget
        #----------------
        centralWidget = QWidget(self)
        centralWidgetLayout = QVBoxLayout(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)

        # sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sizePolicy1.setHorizontalStretch(0)
        # sizePolicy1.setVerticalStretch(0)
        # sizePolicy1.setHeightForWidth(centralWidget.sizePolicy().hasHeightForWidth())
        # centralWidget.setSizePolicy(sizePolicy1)
        centralWidget.setContextMenuPolicy(Qt.Qt.NoContextMenu)

        self.tabContainer = QTabWidget(centralWidget)

        centralWidgetLayout.addWidget(self.tabContainer)

        self.setCentralWidget(centralWidget)

        self.dbConn = None
        self.initDbConn()

        self.updateControlerMonitors()

        self.savingDlg = loading_dialog.LoadingSavingDialog(self)
        self.errorDlg = ErrorDialog(self)

        self.datalogFileName = None
        self.configFileName = None
        self.calibFileName = None

    def showChangeUserPass(self):
        changeUserPass = edit_user_pass.EditUserPass(
            self,
            self.dbConn
        )
        changeUserPass.show()

    def showChangeAdminPass(self):
        changeAdminPass = edit_admin_pass.EditAdminPass(
            self,
            self.dbConn
        )
        changeAdminPass.show()

    def updateControlerMonitors(self):
        self.tabContainer.clear()
        self.controllerMonitors.clear()

        cursor = self.dbConn.cursor()
        cursor.execute("SELECT COUNT(*) FROM controlers")
        rowcount = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM controlers")

        for row in cursor:
            self.controllerMonitors.append(ControlerMonitor(self, 2000, '{}:{}'.format(
                row[2], row[3]), row[4], row[0], self.dbConn, row[1]))
            tab = self.controllerMonitors[-1]

            self.tabContainer.addTab(tab, row[1])

        # Enable/Disable editing of controlers and other menu actions
        # which also depends on the user rights
        if self.user_type == "Admin" or self.user_type == "Service":
            self.actionEditControllers.setEnabled(True)
            self.actionChangeUserPass.setEnabled(True)
            self.actionChangeAdminPass.setEnabled(True)
        else:
            self.actionEditControllers.setEnabled(False)
            self.actionChangeUserPass.setEnabled(False)
            self.actionChangeAdminPass.setEnabled(False)

        if rowcount > 0:
            self.tabContainer.setCurrentIndex(0)
            if self.user_type == "Admin" or self.user_type == "Service":
                self.actionGeneralSettings.setEnabled(True)

                if self.user_type == "Service":
                    self.actionTempChannelsCalibSettings.setEnabled(True)
                    self.actionAutoTempChannelsCalibSettings.setEnabled(True)
                else:
                    self.actionTempChannelsCalibSettings.setEnabled(False)
                    self.actionAutoTempChannelsCalibSettings.setEnabled(False)

                self.actionSaveConfig.setEnabled(True)
                self.actionSaveDatalog.setEnabled(True)
                self.actionSaveCalib.setEnabled(True)
            else:
                self.actionGeneralSettings.setEnabled(False)
                self.actionTempChannelsCalibSettings.setEnabled(False)
                self.actionAutoTempChannelsCalibSettings.setEnabled(False)
                self.actionSaveConfig.setEnabled(False)
                self.actionSaveDatalog.setEnabled(False)
                self.actionSaveCalib.setEnabled(False)
        else:
            self.actionGeneralSettings.setEnabled(False)
            self.actionTempChannelsCalibSettings.setEnabled(False)
            self.actionAutoTempChannelsCalibSettings.setEnabled(False)
            self.actionSaveConfig.setEnabled(False)
            self.actionSaveDatalog.setEnabled(False)
            self.actionSaveCalib.setEnabled(False)

            QMessageBox.information(self, 'Няма добавени контролери.',
                             'Моля добавете контролер(и) от меню Настройки.')

    def initDbConn(self):
        try:
            self.dbConn = sqlite3.connect("controlers.db")
        except Exception as e:
            QMessageBox.critical(self, "Системна грешка.", 'Възникна грешка'
                ' при опит за връзка с БД. Грешка: {}'.format(str(e)))

    def closeDbConn(self):
        self.dbConn.close()

    def pauseUpdate(self):
        for cm in self.controllerMonitors:
            cm.pauseUpdate()

    def resumeUpdate(self):
        for cm in self.controllerMonitors:
            cm.resumeUpdate()

    def stopUpdate(self):
        for cm in self.controllerMonitors:
            cm.stopUpdate()

    def showGeneralSettings(self):
        self.pauseUpdate()

        controlerMonitor = self.controllerMonitors[self.tabContainer.currentIndex()]

        settingsDlg = GeneralThermostatSettingsDialog(
            controlerMonitor.getHost(),
            "Общи настройки на {}".format(controlerMonitor.getName()),
            controlerMonitor.getPassword(),
            controlerMonitor.getId(),
            self.dbConn
        )
        settingsDlg.finished.connect(self.resumeUpdate)
        settingsDlg.show()

    def showTempInputsCalibDlg(self):
        self.pauseUpdate()
        controlerMonitor = self.controllerMonitors[self.tabContainer.currentIndex()]

        tempCalibDlg = temp_inputs_calib_dlg.TempInputsCalibDlg(self,
            controlerMonitor.getHost(),
            controlerMonitor.getPassword(),
            controlerMonitor.getName()
        )

        tempCalibDlg.finished.connect(self.resumeUpdate)

        tempCalibDlg.show()

    def showAutoTempInputsCalibDlg(self):
        self.pauseUpdate()
        controlerMonitor = self.controllerMonitors[self.tabContainer.currentIndex()]

        autoTempCalibDlg = auto_temp_calib_dlg.AutoTempCalibDlg(self,
            controlerMonitor.getHost(),
            controlerMonitor.getPassword(),
            controlerMonitor.getName()
        )

        autoTempCalibDlg.finished.connect(self.resumeUpdate)

        autoTempCalibDlg.show()

    def showControlersEditor(self):
        self.stopUpdate()
        editControlersDlg = edit_controlers_dlg.EditControlersDlg(self, self.dbConn)
        editControlersDlg.finished.connect(self.updateControlerMonitors)

        editControlersDlg.show()

    def showSavingDatalogDlg(self):
        self.pauseUpdate()
        controlerMonitor = self.controllerMonitors[self.tabContainer.currentIndex()]
        self.datalogFileName = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Запис на datalog.txt",
            os.curdir,
            "Text files (*.txt)"
        )

        if self.datalogFileName == ('', ''):
            self.resumeUpdate()
            return

        self.savingDlg = loading_dialog.LoadingSavingDialog(self)
        self.savingDlg.setWindowTitle('Записване на datalog.txt')
        self.savingDlg.label.setText(
            'Четене на настройки от контролера и запис'
            ' във файл.'
        )
        self.savingDlg.show()

        controlerSttings = ControlerCommandSender(
            self,
            controlerMonitor.getHost(),
            controlerMonitor.getPassword(),
            ['datalogExplore'],
            timeout=20
        )

        controlerSttings.data_ready.connect(self.onReadyDatalogData)
        controlerSttings.error.connect(self.onErrorSavingDatalog)
        controlerSttings.start()

    def onReadyDatalogData(self, responses):
        outputFile = open(
            self.datalogFileName[0],
            'w+'
        )
        response = str(responses[0], encoding='ascii')
        response = response.split('\r\n')

        response = response[13:-2]
        response = [re.sub('<br />', '\n', line) for line in response]

        outputFile.writelines(response)
        outputFile.close()
        self.savingDlg.close()
        QtWidgets.QMessageBox.information(
            self,
            'Успешен запис на datalog.txt',
            'Успешен запис на datalog.txt във файл {}'.format(
                self.datalogFileName[0]
            )
        )
        self.resumeUpdate()

    def onErrorSavingDatalog(self, err):
        self.savingDlg.close()
        QtWidgets.QMessageBox.critical(
            self,
            'Грешка.',
            'Грешка при записване на datalog.txt. Грешка: {}'.format(str(err))
        )
        self.resumeUpdate()

    def showSavingConfigDlg(self):
        self.pauseUpdate()
        controlerMonitor = self.controllerMonitors[self.tabContainer.currentIndex()]
        self.configFileName = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Запис на config.txt",
            os.curdir,
            "Text files (*.txt)"
        )
        if self.configFileName == ('', ''):
            self.resumeUpdate()
            return

        self.savingDlg = loading_dialog.LoadingSavingDialog(self)
        self.savingDlg.setWindowTitle('Записване на config.txt')
        self.savingDlg.label.setText(
            'Четене на настройки от контролера и запис'
            ' във файл.'
        )
        self.savingDlg.show()

        controlerSttings = ControlerCommandSender(
            self,
            controlerMonitor.getHost(),
            controlerMonitor.getPassword(),
            ['List'],
            timeout=25
        )

        controlerSttings.data_ready.connect(self.onReadyConfigData)
        controlerSttings.error.connect(self.onErrorSavingConfig)
        controlerSttings.start()

    def onReadyConfigData(self, responses):
        outputFile = open(
            self.configFileName[0],
            'w+'
        )
        response = str(responses[0], encoding='ascii')
        response = response.split('\r\n')

        response = response[6:-2]
        response = [re.sub('<br />', '\n', line) for line in response]

        outputFile.writelines(response)
        outputFile.close()
        self.savingDlg.close()
        QtWidgets.QMessageBox.information(
            self,
            'Успешен запис на config.txt',
            'Успешен запис на config.txt във файл {}'.format(
                self.configFileName[0]
            )
        )
        self.resumeUpdate()

    def onErrorSavingConfig(self, err):
        self.savingDlg.close()
        QtWidgets.QMessageBox.critical(
            self,
            'Грешка.',
            'Грешка при записване на config.txt. Грешка: {}'.format(str(err))
        )
        self.resumeUpdate()

    def showSavingCalibDlg(self):
        self.pauseUpdate()
        controlerMonitor = self.controllerMonitors[self.tabContainer.currentIndex()]
        self.calibFileName = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Запис на calibr.txt",
            os.curdir,
            "Text files (*.txt)"
        )

        if self.calibFileName == ('', ''):
            self.resumeUpdate()
            return

        self.savingDlg = loading_dialog.LoadingSavingDialog(self)
        self.savingDlg.setWindowTitle('Записване на calibr.txt')
        self.savingDlg.label.setText(
            'Четене на настройки от контролера и запис'
            ' във файл.'
        )
        self.savingDlg.show()

        controlerSttings = ControlerCommandSender(
            self,
            controlerMonitor.getHost(),
            controlerMonitor.getPassword(),
            ['CalibrExplore'],
            timeout=20
        )

        controlerSttings.data_ready.connect(self.onReadyCalibData)
        controlerSttings.error.connect(self.onErrorSavingCalibData)
        controlerSttings.start()

    def onReadyCalibData(self, responses):
        outputFile = open(
            self.calibFileName[0],
            'w+'
        )
        response = str(responses[0], encoding='ascii')
        response = response.split('\r\n')

        response = response[6:-2]
        response = [re.sub('<br />', '\n', line) for line in response]
        # response = [re.sub('<br />', '\n', line) for line in response]

        outputFile.writelines(response)
        outputFile.close()
        self.savingDlg.close()
        QtWidgets.QMessageBox.information(
            self,
            'Успешен запис на calibr.txt',
            'Успешен запис на calibr.txt във файл {}'.format(
                self.calibFileName[0]
            )
        )
        self.resumeUpdate()

    def onErrorSavingCalibData(self, err):
        self.savingDlg.close()
        QtWidgets.QMessageBox.critical(
            self,
            'Грешка.',
            'Грешка при записване на calib.txt. Грешка: {}'.format(str(err))
        )
        self.resumeUpdate()
