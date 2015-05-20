# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QApplication

from channelmonitor import ChannelMonitor
from controlerstatusupdater import ControlerStatusUpdater
from channel_settings_dialog import ChannelSettingsDialog


class ControlerMonitor(QWidget):

    # looper = Looper()


    def __init__(self,
                 parent=None,
                 updaterSleep=10000,
                 host="83.228.50.143:88",
                 password="12345678",
                 _id=None, dbConn=None, name=None):
        super(ControlerMonitor, self).__init__(parent)
        self.name = name
        self.updaterSleep = updaterSleep
        self.controlerLayout = QVBoxLayout(self)
        self._id = _id
        self.host = host
        self.password = password
        self.dbConn = dbConn
        # Timer
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.looper.process)
        # self.timer.start(50)

        #
        #Header
        #
        self.header = QWidget(self)
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(10, 0, 10, 0)
        self.labelMode = QLabel(self.header)
        self.labelMode.setText("Текущ Режим: Oхлаждане")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelMode.setFont(font)
        self.header.setStyleSheet("background-color: rgb(78, 66, 255);"
                                     "color: rgb(255, 255, 255);")
        self.headerLayout.addWidget(self.labelMode)

        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.headerLayout.addItem(self.spacer1)

        self.labelDateTime = QLabel(self.header)
        self.labelDateTime.setText("Текущи Дата и час: 6.9.2014, 22:22")
        self.labelDateTime.setFont(font)

        self.headerLayout.addWidget(self.labelDateTime)

        self.controlerLayout.addWidget(self.header)

        #
        #Scroll area
        #

        # self.scrollArea = QScrollArea(self)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollWidget = QWidget(self)
        # self.scrollLayout = QVBoxLayout(self.scrollWidget)
        #
        # self.controlerLayout.addWidget(self.scrollArea)
        # self.scrollArea.setWidget(self.scrollWidget)

        #
        #Add the channels and start monitoring
        #

        self.channelMonitors = []
        self.updateChannelMonitors()

        self.updater = ControlerStatusUpdater(self.updaterSleep, self.host)
        self.updater.data_ready.connect(self.updateState)
        self.updater.start()

        QApplication.instance().lastWindowClosed.connect(self.updater.stop)

    def updateChannelMonitors(self, addNew=True):
        cursor = self.dbConn.cursor()

        cursor.execute('SELECT * FROM controler_channels WHERE '
                       'controler_channels.controler_id={} ORDER BY id ASC'.format(self._id))

        if addNew:
            i = 0
            for _ in cursor.fetchall():
                self.channelMonitors.append(
                    ChannelMonitor(self,
                    _[2]
                    )
                )

                self.controlerLayout.addWidget(self.channelMonitors[-1])
                self.channelMonitors[-1].buttonChanSettings.clicked.connect(
                    self.make_settings_handler(
                        i,
                        self.host,
                        _[0]
                    )
                )
                i += 1
        else:
            i = 0
            for _ in cursor.fetchall():
                self.channelMonitors[i].setTitle(_[2])
                i += 1

    def getName(self):
        return self.name

    def getHost(self):
        return self.host

    def getPassword(self):
        return self.password

    def getId(self):
        return self._id

    def stopUpdate(self):
        self.updater.stop()

    def pauseUpdate(self):
        self.updater.pause()

    def resumeUpdate(self):
        self.updater.resume()

    def showSettingsDialog(self, chanNum, host, id):
        self.pauseUpdate()
        chanSettingsDlg = ChannelSettingsDialog(self, chanNum, host, self.password, self.dbConn, id)
        chanSettingsDlg.finished.connect(self.resumeUpdate)
        chanSettingsDlg.nameChanged.connect(self.updateChannelMonitors)

        chanSettingsDlg.setModal(True)
        chanSettingsDlg.show()

    def make_settings_handler(self, chanNum, host, id):

        def inner():
            self.showSettingsDialog(chanNum, host, id)

        return inner

    # @looper.run_in_ui
    def updateState(self, controlerState):
        if controlerState.controlerMode == "HEAT":
            self.labelMode.setText("Текущ Режим: Отопление")
        else:
            self.labelMode.setText("Текущ Режим: Охлаждане")

        time_split = controlerState.time.split(":")

        if len(time_split[0]) == 1:
            time_split[0] = "0" + time_split[0]

        minDaySplit = time_split[1].split(",")

        if len(minDaySplit[0]) == 1:
            minDaySplit[0] = "0" + minDaySplit[0]

        # Reusing a variable is a bad idea ...

        time_split[1] = minDaySplit[0] + ", " + minDaySplit[1]

        joinedTime = ":".join(time_split)

        self.labelDateTime.setText("Текущи Дата и час: " +  controlerState.date + ", " + joinedTime)

        for i in range(10):
            channelMonitor = self.channelMonitors[i]
            channelMonitor.setValues(controlerState.channelsData[i])

    def getId(self):
        return self._id
