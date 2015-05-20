# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

import ui_auto_temp_calib_dlg

import controllersettingsthread
import loading_dialog
import error_dialog


class AutoTempCalibDlg(QtWidgets.QDialog, ui_auto_temp_calib_dlg.Ui_AutoTempCalibDlg):

    def __init__(self, parent, host, password, name):
        super(AutoTempCalibDlg, self).__init__(parent)

        self.host = host
        self.password = password

        self.setupUi(self)
        self.setModal(True)

        self.setWindowTitle(
            "{}. Автоматична калибрация на температурни входове.".\
            format(name)
        )

        # Disable step 2 and Save
        self.btnStep2.setEnabled(False)
        self.btnSave.setEnabled(False)

        # set initial text
        self.msg_step1 =\
            """
                Моля поставете резистори от 1000 Ohm на всички температурни входове
                и натиснете 'Стъпка 1' за да продължите.
            """

        self.labelInstructions.setWordWrap(True)
        self.labelInstructions.setText(
            self.msg_step1
        )

        # connect button actions
        self.btnStep1.clicked.connect(self.on_btn_step1)
        self.btnStep2.clicked.connect(self.on_btn_step2)
        self.btnSave.clicked.connect(self.on_btn_save)

        # saving/error dlgs
        self.error_dlg = None
        self.saving_dlg = None

        # command sender
        self.command_sender = None

    # Step 1 methods
    def on_btn_step1(self):
        self.saving_dlg = loading_dialog.LoadingSavingDialog(self)
        self.saving_dlg.setWindowTitle('Записване на настройки.')
        self.saving_dlg.label.setText('Изпращане на команда към устройството.')
        self.saving_dlg.show()

        # command sender init and start
        commands = ['CalibrPass1']
        self.command_sender = controllersettingsthread.ControlerCommandSender(
            self, self.host, self.password, commands
        )

        self.command_sender.data_ready.connect(self.on_step1_ready)
        self.command_sender.error.connect(self.on_save_error)

        self.command_sender.start()

    def on_step1_ready(self, responses):
        self.saving_dlg.close()
        self.btnStep1.setEnabled(False)
        self.btnStep2.setEnabled(True)
        self.labelInstructions.setText(
            """
                Моля поставете резистори от 1385 Ohm на всички температурни входове
                и натиснете 'Стъпка 2' за да продължите.
            """
        )

    # Step 2 methods
    def on_btn_step2(self):
        self.saving_dlg = loading_dialog.LoadingSavingDialog(self)
        self.saving_dlg.setWindowTitle('Записване на настройки.')
        self.saving_dlg.label.setText('Изпращане на команда към устройството.')
        self.saving_dlg.show()

        # command sender init and start
        commands = ['CalibrPass2']
        self.command_sender = controllersettingsthread.ControlerCommandSender(
            self, self.host, self.password, commands
        )

        self.command_sender.data_ready.connect(self.on_step2_ready)
        self.command_sender.error.connect(self.on_save_error)

        self.command_sender.start()

    def on_step2_ready(self, responses):
        self.saving_dlg.close()
        self.btnStep2.setEnabled(False)
        self.btnSave.setEnabled(True)
        self.labelInstructions.setText(
            """
                Моля натиснете 'Калибрация' за да запишете настройките за калибрацията.
            """
        )

    # Step Save methods
    def on_btn_save(self):
        self.saving_dlg = loading_dialog.LoadingSavingDialog(self)
        self.saving_dlg.setWindowTitle('Записване на настройки.')
        self.saving_dlg.label.setText('Изпращане на команда към устройството.')
        self.saving_dlg.show()

        # command sender init and start
        commands = ['Calibration']
        self.command_sender = controllersettingsthread.ControlerCommandSender(
            self, self.host, self.password, commands
        )

        self.command_sender.data_ready.connect(self.on_save_ready)
        self.command_sender.error.connect(self.on_save_error)

        self.command_sender.start()

    def on_save_ready(self, responses):
        self.saving_dlg.close()
        self.btnSave.setEnabled(False)
        self.btnStep1.setEnabled(True)
        self.labelInstructions.setText(
            self.msg_step1
        )

    def on_save_error(self, error):
        self.saving_dlg.close()
        self.error_dlg = error_dialog.ErrorDialog(self)
        self.error_dlg.setWindowTitle("Грешка при изпращане на команда.")
        self.error_dlg.label.setText(
            """
                Възникна грешка при изпращане на команда към устройството. Грешка: {}
            """.format(str(error))
        )
        self.error_dlg.show()
