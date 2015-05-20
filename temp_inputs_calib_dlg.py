# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import controlersettingsloader
import controllersettingsthread
import loading_dialog
import tmintmaxwidget
import error_dialog

class TempInputsCalibDlg(QtWidgets.QDialog):

    def __init__(self, parent, host, password, controllerName="Мултитермостат 1"):
        super(TempInputsCalibDlg, self).__init__(parent)
        self.setWindowTitle("{}. Ръчна калибрация на температурни входове.".format(controllerName))
        self.tmin_tmax_widgets = []
        self.host = host
        self.password = password

        # Init the settings loader
        self.controllerSettingsLoader = \
            controlersettingsloader.ControllerSettingsLoader(self.host, self.password, self)
        self.controllerSettingsLoader.data_ready.connect(self.onDataReady)
        self.controllerSettingsLoader.error.connect(self.onErrorLoadingData)

        self.resize(970, 300)
        self.setMinimumSize(QtCore.QSize(970, 300))
        self.setMaximumSize(QtCore.QSize(970, 300))

        self.setModal(True)

        self.make_ui()
        self.btnClose = QtWidgets.QPushButton(self)
        self.btnClose.setText('Затваряне')
        self.btnClose.clicked.connect(self.close)
        self.btnClose.move((self.width() - self.btnClose.width())/2, 250)

        # Loading Dialog
        self.loadingDialog = loading_dialog.LoadingSavingDialog(self)
        self.loadingDialog.show()
        self.controllerSettingsLoader.start()
        self.disableSaveButtons()

        self.savingDialog = None
        self.controllerCommandsSender = None

    def make_ui(self):
        for i in range(10):
            self.tmin_tmax_widgets.append(tmintmaxwidget.TminTmaxWidget(self))

            if i < 5:
                self.tmin_tmax_widgets[-1].move(10 + i*(self.tmin_tmax_widgets[-1].width() + 10), 10)
            else:
                self.tmin_tmax_widgets[-1].move(10 + (i - 5)*(self.tmin_tmax_widgets[-1].width() + 10),
                                                10 + self.tmin_tmax_widgets[-1].height() + 10)

            self.tmin_tmax_widgets[-1].setTitle('T({}) T Min и T Max ºC'.format(i))

            self.tmin_tmax_widgets[-1].getSaveBtn().clicked.connect(self.makeSaveHandler(i, self))

    def onDataReady(self, data=controlersettingsloader.ControllerSettings):
        for i in range(10):
            tminSign = data.channelsTMinSign[i]

            tmin = data.channelsTMin[i] if tminSign else -data.channelsTMin[i]
            self.tmin_tmax_widgets[i].setTmin(tmin)
            self.tmin_tmax_widgets[i].setTmax(data.channelsTMax[i])

        self.loadingDialog.close()
        self.enableSaveButtons()

    def onErrorLoadingData(self, error):
        self.loadingDialog.close()
        errorDialog = error_dialog.ErrorDialog(self)
        errorDialog.setWindowTitle('Грешка при зареждане на настройки.')
        errorDialog.label.setText('Възникна грешка при зареждането на настройки от контролера.'
                                  ' Моля опитайте пак. Грешка : {}'.format(error))
        errorDialog.show()

    def disableSaveButtons(self):
        for w in self.tmin_tmax_widgets:
            w.getSaveBtn().setEnabled(False)

    def enableSaveButtons(self):
        for w in self.tmin_tmax_widgets:
            w.getSaveBtn().setEnabled(True)

    def makeSaveHandler(self, index, parent):

        def handler():
            self.savingDialog = loading_dialog.LoadingSavingDialog(self)
            self.savingDialog.setWindowTitle('Записване на настройки.')
            self.savingDialog.label.setText('Записване на настройки в контролера ...')
            self.savingDialog.show()

            tmin = str(self.tmin_tmax_widgets[index].spinTmin.value())

            sign = tmin[0]
            if sign == '-':
                tmin = tmin[1:]

            if len(tmin) < 3:
                padding = 3 - len(tmin)
                for _ in range(padding):
                    tmin = '0' + tmin

            if sign =='-':
                cmdTmin = sign + tmin + 'n{}'.format(index)
            else:
                cmdTmin = '0' + tmin + 'n{}'.format(index)

            tmax = str(self.tmin_tmax_widgets[index].spinTmax.value())

            if len(tmax) < 3:
                padding = 3 - len(tmax)
                for _ in range(padding):
                    tmax = '0' + tmax

            cmdTmax = tmax + 'x{}'.format(index)

            commands = [cmdTmin, cmdTmax]

            self.controllerCommandsSender = \
            controllersettingsthread.ControlerCommandSender(
                self, self.host, self.password, commands)

            parent.controllerCommandsSender.data_ready.connect(parent.onSaveDone)
            parent.controllerCommandsSender.error.connect(parent.onErrorSave)

            parent.disableSaveButtons()
            parent.controllerCommandsSender.start()

        return handler

    def onSaveDone(self, responses):
        self.savingDialog.close()
        self.enableSaveButtons()

    def onErrorSave(self, error):
        self.enableSaveButtons()
        self.savingDialog.close()
        errorDialog = error_dialog.ErrorDialog(self)
        errorDialog.setWindowTitle('Грешка при записване на настройки.')
        errorDialog.label.setText(
            'Възникна грешка при записването на настройки в контролера.'
            ' Моля опитайте пак. Грешка : {}'.format(error))
        errorDialog.show()