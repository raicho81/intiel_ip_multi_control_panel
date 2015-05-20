# -*- coding: utf-8 -*-
import http.client, urllib.parse, re

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


class ChannelZones(object):
    def __init__(self):
        self.timeZonesH = []
        self.timeZonesM = []
        self.timeZonesTrig = []


class ControllerSettings(object):
    def __init__(self):
        self.id_ = 1
        self.indexInOut = [] # T(in) to Channels(Ch0-Ch9)
        self.channelsZones = []
        self.mode_cool_heat = 0 # 1 - cool, 0 - heat
        self.ipaddress = []
        self.lanPort = 88
        self.channelsHisteresis = [] # 2 * 0.5 = 1 degree Celsius
        self.password = "12345678"
        self.tMin = 0
        self.tMax = 0
        self.negPosIdx = 0 # 0 - negative(-), 1 - positive (+)
        self.turnOnOff = 1 # 1 - turn on, 0 - turn off
        self.channelsOnOff = {
            'Mon': [],
            'Tue': [],
            'Wed': [],
            'Thu': [],
            'Fri': [],
            'Sat': [],
            'Sun': [],
        }
        self.dataLogLow = 5
        self.dataLogHigh = 0
        self.startSopDataLogStatus = 1 # 0 - stop, 1 - start
        self.date = ""
        self.time = ""
        self.channelsTMinSign = []
        self.channelsTMin = []
        self.channelsTMax = []
        self.triggerZonesIndex = []

class ControllerSettingsLoader(QThread):

    data_ready = pyqtSignal(object)
    error = pyqtSignal(object)

    def __init__(self, host, password, parent):
        super(ControllerSettingsLoader, self).__init__(parent)
        self.controllerSettings = ControllerSettings()
        self.host = host
        self.password = password

    def run(self):
        # Set the headers and the body and make a HTTP connection object
        paramsInfo = urllib.parse.urlencode({'PSW': 'Info'})
        paramsSetup = urllib.parse.urlencode({'PSW': '{}'.format(self.password)})
        paramsSettings = urllib.parse.urlencode({'PSW': 'ConfigExplore'})
        paramsExit = urllib.parse.urlencode({'PSW': 'Exit'})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        # Try to make some requests to the controller
        try:

            #
            # TODO: stupid hack to load the date and time, which has to be fixed
            # ./in the controller FW
            #
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsInfo, headers)
            response = conn.getresponse()

            data = response.read()

            # print("After response read Thread with id = " +
            #       str(int(QtCore.QThread.currentThreadId())))

            data = str(data, encoding='ascii')

            data = data.split("\r\n")


            data = [re.sub("\\n|\\r|<br />|\s", "", line) for line in data]

            # Fill the fieldss for date and time in the ControlerSettings class
            self.controllerSettings.time = data[11]
            self.controllerSettings.date = data[13]

            #
            # Enter setup mode
            #
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsSetup, headers)
            response = conn.getresponse()

            # Check if password is correct
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("GET", "", "")
            response = conn.getresponse()

            setupResponse = response.read()
            setupResponse = str(setupResponse, encoding='ascii')

            data = setupResponse.split('\r\n')

            if data[2] != 'mode:Setup':
                self.error.emit('Грешна парола')
                return

            # print(response.status, response.reason)

            data = response.read()

            #
            # Read setup.cfg
            #
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsSettings, headers)
            response = conn.getresponse()

            # print(response.status, response.reason)
            # print("Before response read Thread with id = " +
            #       str(int(QtCore.QThread.currentThreadId())))

            data = response.read()

            data = str(data, encoding='ascii')

            data = data.split("\r\n")

            data = [re.sub("\\n|\\r|<br />>", "", line) for line in data]

            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsExit, headers)
            response = conn.getresponse()

        except Exception as e:
            self.error.emit(str(e))
        else:
            self.parseData(data)

    def parseData(self, data):
        try:
            configString = data[6]
            configList = configString.split(" ")
            configList.pop()
            configList.pop()

            # print(configList[53], configList[55])

            configList = [int(x, base=16) for x in configList]

            # Set index tp 0 and read ip cnofig
            index = 0               # byte 0

            for _ in range(index+4):
                self.controllerSettings.ipaddress.append(configList[_])

            # advance to index in out and read data for the in-out mapping
            index += 4 # byte 4

            for _ in range(index, index+10):
                self.controllerSettings.indexInOut.append(configList[_])


            # advance to cool/heat byte
            index += 10 # byte 14
            self.controllerSettings.mode_cool_heat = configList[index]

            # advance to current sensor trigger: not used for settings
            index += 1 # byte 15

            # advance to Port(Out) to Channels(Ch0-Ch9): not used for settingd, just for service
            index += 10 # byte 25

            # advance to Histeresis Channels(Ch0-Ch9) value
            index += 10 # byte 35

            for _ in range(index, index+10):
                self.controllerSettings.channelsHisteresis.append(configList[_])

            # advance to password in ascii code
            index += 10 # byte 45
            self.controllerSettings.password = [chr(configList[i]) for i in range(index, index+8)]

            # advance to Tmin value
            index += 8 # byte 53
            self.controllerSettings.tMin = configList[index]

            # advance to positive or negative index: 0 - negative(-) , 1 - positive(+)
            index += 1 # 54
            self.controllerSettings.negPosIdx = configList[index]

            # This is very stupid but negPosIdx is the sign of tMin
            # 1 - positive(+), 0 - negative (-) and we have to change the sign
            # of tMin if necessary
            if self.controllerSettings.negPosIdx == 0:
                self.controllerSettings.tMin = - self.controllerSettings.tMin


            # advance to Tmax value
            index += 1      # byte 55
            self.controllerSettings.tMax = configList[index]

            # advance to 1 byte - TurnOn or TurnOff: 1 - TurnOn, 0 - TurnOff
            index +=1       # byte 56
            self.controllerSettings.turnOnOff = configList[index]

            #advance to 1 byte – LAN Port: range 00 - 255
            index += 1      # byte 57
            self.controllerSettings.lanPort = configList[index]

            # advance to 7 bytes - EEPROM reserved cells: Not used
            index += 1      # byte 58

            # advance to 4 bytes - Ch0 - time_zone: hour1, hour2, hour3, hour4
            index += 7      #byte 65

            for _ in range(0, 12):
                self.controllerSettings.channelsZones.append(ChannelZones())

                # append time zones H
                for i in range(4):
                    self.controllerSettings.channelsZones[_].timeZonesH.append(configList[index + i])

                # advance to the time zone m
                index += 4

                # append time zones M
                for i in range(4):
                    self.controllerSettings.channelsZones[_].timeZonesM.append(configList[index + i])

                # advance to the time zone triggers
                index += 4

                for i in range(4):
                    self.controllerSettings.channelsZones[_].timeZonesTrig.append(configList[index + i])

                # advance to next channel time zone or 10 bytes Weekdays Channels On/Off
                index +=4

                # print(self.controllerSettings.channelsZones[_].timeZonesH)

            # byte 199
            # Read channels on-off weekday settings
            for day in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'):
                for _ in range(index, index + 10):
                    self.controllerSettings.channelsOnOff[day].append(configList[_])
                index += 10

            # advanced to 1 byte – LOW byte of Datalog interval word
            # byte 269
            self.controllerSettings.dataLogLow = configList[index]

            # advance to 1 byte – HIGH byte of Datalog interval word
            # byte 270
            index += 1
            self.controllerSettings.dataLogHigh = configList[index]

            # advance to 1 byte – StartStopLog status: 0 –stop/end datalog.txt, 1 –start/write to datalog.txt
            # byte 271
            index += 1
            self.controllerSettings.startSopDataLogStatus = configList[index]

            # advance to 10 bytes Channels tmin index
            # byte 281
            index += 1

            for chan in range(10):
                self.controllerSettings.channelsTMinSign.append(configList[index+chan])

            # advance to 10 bytes channels tmin
            # byte 291
            index += 10

            for chan in range(10):
                self.controllerSettings.channelsTMin.append(configList[index+chan])

            # advance to 10 bytes channels tmax
            # byte 301
            index += 10

            for chan in range(10):
                self.controllerSettings.channelsTMax.append(configList[index+chan])

            self.data_ready.emit(self.controllerSettings)

            # advance 10 bytes to TriggerZones indexes
            index += 10

            for chan in range(10):
                tmpIndexes = []
                for i in range(4):
                    tmpIndexes.append(configList[index+i])
                self.controllerSettings.triggerZonesIndex.append(tmpIndexes)
                index += 4

        except Exception as e:
            self.error.emit(str(e))
