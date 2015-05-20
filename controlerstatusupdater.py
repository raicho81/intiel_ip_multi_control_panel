# -*- coding: utf-8 -*-
import http.client, urllib.parse, re
import threading
from PyQt5.QtCore import QMutexLocker
from PyQt5.QtCore import QMutex

# import time
# import threading

import PyQt5.QtCore as QtCore


class ChannelData(object):
    def __init__(self):
        self.number = "Err!"
        self.enabled = "Off"
        self.input = "Err!"
        self.measurment = "Err!"
        self.trigger = "Err!"
        self.outputOn = "0"


class ControlerState(object):
    def __init__(self):
        self.channelsData = []
        self.date = "Err!"
        self.time = "Err!:Err!, Err!"
        self.controlerMode = "Err!"
        self.error = None
        self.setupMode = "Regular"


class ControlerStatusUpdater(QtCore.QThread):

    data_ready = QtCore.pyqtSignal(object)

    def __init__(self,  updaterSleep=1000, host=None):
        super(ControlerStatusUpdater, self).__init__()
        self.req_count = 0
        self.mutex = QMutex()
        self.mutexLocker = QMutexLocker(self.mutex)

        self.state = "Running" # Running, Paused, Stopped
        self.host = host
        self.sleep = updaterSleep

    def run(self):
        while 1:
            self.req_count += 1

            # with self.lock:
            self.mutexLocker.relock()
            if self.state == "Stopped":
                self.mutexLocker.unlock()
                break
            self.mutexLocker.unlock()

            self.mutexLocker.relock()
            # with self.lock:
            while self.state == "Paused":
                self.mutexLocker.unlock()
                self.msleep(50)
                self.mutexLocker.relock()
            self.mutexLocker.unlock()

            # Set the headers and the body and make a HTTP connection object
            params = urllib.parse.urlencode({'PSW': 'Info'})
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}

            state = ControlerState()

            # Try to make a request to the controller
            try:
                conn = http.client.HTTPConnection(self.host, timeout=10)
                conn.request("POST", "", params, headers)
                response = conn.getresponse()

                # print(response.status, response.reason)
                # print("Before response read Thread with id = " +
                #       str(int(QtCore.QThread.currentThreadId())))

                data = response.read()

                # print("After response read Thread with id = " +
                #       str(int(QtCore.QThread.currentThreadId())))

                data = str(data, encoding='ascii')

                data = data.split("\r\n")


                data = [re.sub("\\n|\\r|<br />|\s", "", line) for line in data]

                # Fill the state structure and send it to the ControllerMonitor for update
                state.controlerMode = data[10]
                state.setupMode = re.sub("mode:", "" , data[2])
                state.time = data[11]
                state.date = data[13]

                for i in range(14, 24):
                    line = data[i]
                    splited = line.split(",")
                    channelData = ChannelData()

                    channelData.number = splited[0]
                    channelData.outputOn = splited[1]
                    channelData.input = splited[2]
                    channelData.measurment = str(round(float(splited[3]), 1))
                    channelData.trigger = splited[4]
                    channelData.enabled = splited[5]

                    state.channelsData.append(channelData)


            except Exception as err:
                state.error = err
                state.channelsData = [ChannelData() for _ in range(10)]
                # print("Exception in " + str(threading.current_thread()))
                # print("Exception in Thread with id = " +
                #       str(int(QtCore.QThread.currentThreadId())))
                # print(err)
                # print("Exception Info: " + str(err))

            # print(str(threading.current_thread()) + " working.")
            # print("Thread id = " + str(int(QtCore.QThread.currentThreadId())) +
            #       " working. Made {} requests so far".format(self.req_count))
            # print()
            conn.close()

            # w.updateState(state)
            self.data_ready.emit(state)
            self.msleep(self.sleep)

    def stop(self):
        # with self.lock:
        self.mutexLocker.relock()
        self.state = "Stopped"
        self.mutexLocker.unlock()

    def pause(self):
        # with self.lock:
        self.mutexLocker.relock()
        self.state = "Paused"
        self.mutexLocker.unlock()

    def resume(self):
        # with self.lock:
        self.mutexLocker.relock()
        self.state = "Running"
        self.mutexLocker.unlock()
