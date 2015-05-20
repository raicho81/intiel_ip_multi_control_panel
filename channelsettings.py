import urllib.parse
import http.client
import re
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from controlersettingsloader import ControllerSettings


class ChannelSetter(QThread):
    data_ready = pyqtSignal()
    error = pyqtSignal(object)

    def __init__(self, host, chanNum=0, controllerSetting = ControllerSettings(), password='12345678',
                 parent=None):
        super(ChannelSetter, self).__init__(parent)
        self.chanNum = chanNum
        self.controllerSettings = controllerSetting
        self.host = host
        self.password = password

    def run(self):
        # Set the headers and the body and make a HTTP connection object
        paramsSetup = urllib.parse.urlencode({'PSW': '{}'.format(self.password)})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        channelZones = self.controllerSettings.channelsZones[self.chanNum]

        #make setup string for the zones
        setupString = ""
        for i in range(4):
            tmp = str(channelZones.timeZonesH[i])
            if len(tmp) > 1:
                setupString += tmp
            else:
                setupString += "0" + tmp

            tmp = str(channelZones.timeZonesM[i])
            if len(tmp) > 1:
                setupString += tmp
            else:
                setupString += "0" + tmp

        paramsZones = urllib.parse.urlencode({'PSW': setupString + "Ch{}".format(self.chanNum)})

        #make setup string for zones triggers

        setupStrTrig = ""
        for x in channelZones.timeZonesTrig:
            tmp = str(x)
            sign = tmp[0]
            if sign == '-':
                tmp = tmp[1:]
                while len(tmp) < 2:
                    tmp = '0' + tmp
                tmp = sign + tmp
            else:
                while len(tmp) < 3:
                    tmp = "0" + tmp
            setupStrTrig += tmp

        setupStrTrig += "Ch{}".format(self.chanNum)

        paramszonesTrig = urllib.parse.urlencode({'PSW': setupStrTrig})

        # make setup string for channel histeresis
        setupStrChanHist = ""
        for x in self.controllerSettings.channelsHisteresis:
            setupStrChanHist += str(x)

        setupStrChanHist += "H"
        # print(setupStrChanHist)
        paramsChanHist = urllib.parse.urlencode({'PSW': setupStrChanHist})

        # make channels on/off params
        paramsDaysOnOff = []
        for day, v in self.controllerSettings.channelsOnOff.items():
            cmd = ''
            for _ in range(10):
                cmd += str(v[_])

            cmd += day[0:2]
            paramsDaysOnOff.append(urllib.parse.urlencode({'PSW': cmd}))

        # # make TMin params
        # tmin = str(self.controllerSettings.channelsTMin[self.chanNum])
        #
        # if len(tmin) < 4:
        #     padding = 4 - len(tmin)
        #     sign = tmin[0]
        #     tmin = tmin[1:]
        #
        #     for _ in range(padding):
        #         tmin = '0' + tmin
        #     tmin = sign + tmin
        #
        # cmd = '{}n{}'.format(tmin, self.chanNum)
        #
        # paramsTMin = urllib.parse.urlencode({'PSW': cmd})
        #
        # tmax = str(self.controllerSettings.channelsTMax[self.chanNum])
        #
        # # make TMax params
        # if len(tmax) < 3:
        #     padding = 4 - len(tmax)
        #
        #     for _ in range(padding):
        #         tmax = '0' + tmax
        #
        # cmd = '{}x{}'.format(tmax, self.chanNum)
        #
        # paramsTMax = urllib.parse.urlencode({'PSW': cmd})

        # make save setup params
        paramsSave = urllib.parse.urlencode({'PSW': 'Save'})

        # make exit setup params
        paramsExit = urllib.parse.urlencode({'PSW': 'Exit'})

        # Try to make some requests to the controller
        try:
            #
            # Enter setup mode
            #
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsSetup, headers)
            response = conn.getresponse()

            # print(response.status, response.reason)
            # print("Before response read Thread with id = " +
            #       str(int(QtCore.QThread.currentThreadId())))

            data = response.read()
            # print(data, "Setup")

            # # save channel TMin
            # conn = http.client.HTTPConnection(self.host, timeout=10)
            # conn.request("POST", "", paramsTMin, headers)
            # response = conn.getresponse()
            # data = response.read()
            #
            # # save channel TMax
            # conn = http.client.HTTPConnection(self.host, timeout=10)
            # conn.request("POST", "", paramsTMax, headers)
            # response = conn.getresponse()
            # data = response.read()

            #
            # Save channel zones
            #
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsZones, headers)
            response = conn.getresponse()

            data = response.read()
            # print(paramsZones)
            # print(data, "Zones")

            # print(response.status, response.reason)
            # print("Before response read Thread with id = " +
            #       str(int(QtCore.QThread.currentThreadId())))

            # data = response.read()
            #
            # data = str(data, encoding='ascii')
            #
            # data = data.split("\r\n")
            #
            #
            # data = [re.sub("\\n|\\r|<br />>", "", line) for line in data]

            # save zones triggers
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramszonesTrig, headers)
            response = conn.getresponse()
            data = response.read()
            # print(data, "Triggers")

            #TODO: error checking

            # save channels histeresis
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsChanHist, headers)
            response = conn.getresponse()
            data = response.read()
            # print(paramsChanHist, "Histeresis")

            # save weekdays channels on/off
            for _ in paramsDaysOnOff:
                conn = http.client.HTTPConnection(self.host, timeout=10)
                conn.request("POST", "", _, headers)
                response = conn.getresponse()
                data = response.read()

            #TODO: error checking

            # Save and Exit setup mode
            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsSave, headers)
            response = conn.getresponse()
            data = response.read()
            # print(data, "Save")

            conn = http.client.HTTPConnection(self.host, timeout=10)
            conn.request("POST", "", paramsExit, headers)
            response = conn.getresponse()
            data = response.read()
            # print(data, "Exit")

            #TODO: error checking
        except Exception as e:
            self.error.emit(str(e))
        else:
            self.data_ready.emit()
