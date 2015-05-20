import urllib.parse
import http.client

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


class ControlerCommandSender(QThread):
    data_ready = pyqtSignal(object)
    error = pyqtSignal(object)

    def __init__(self, parent=None, host='', password='12345678', commands=[],
                 timeout=10):
        super(ControlerCommandSender, self).__init__(parent)
        self.host = host
        self.password = password
        self.commands = commands
        self.responses = []
        self.timeout = timeout

    def run(self):
        # Set the headers and the body and make a HTTP connection object
        paramsSetup = urllib.parse.urlencode({'PSW': '{}'.format(self.password)})

        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        # make exit setup params
        # paramsSave = urllib.parse.urlencode({'PSW': 'Save'})

        # make exit setup params
        paramsExit = urllib.parse.urlencode({'PSW': 'Exit'})

        # Try to make request to the controller
        try:
            #
            # Enter setup mode
            #
            conn = http.client.HTTPConnection(self.host, timeout=self.timeout)
            conn.request("POST", "", paramsSetup, headers)
            response = conn.getresponse()
            data = response.read()

            #
            # Check if password is correct
            #
            conn = http.client.HTTPConnection(self.host, timeout=self.timeout)
            conn.request("GET", "", "")
            response = conn.getresponse()

            setupResponse = response.read()
            setupResponse = str(setupResponse, encoding='ascii')

            data = setupResponse.split('\r\n')

            if data[2] != 'mode:Setup':
                self.error.emit('Грешна парола')
                return

            #
            # Execute the commands and read the response
            #
            for command in self.commands:
                params = urllib.parse.urlencode({'PSW': '{}'.format(command)})
                # print(command)
                conn = http.client.HTTPConnection(self.host, timeout=self.timeout)
                conn.request("POST", "", params, headers)
                response = conn.getresponse()

                data = response.read()
                self.responses.append(data)

            # Save setup params
            paramsSave = urllib.parse.urlencode({'PSW': 'Save'})
            conn = http.client.HTTPConnection(self.host, timeout=self.timeout)
            conn.request("POST", "", paramsSave, headers)
            response = conn.getresponse()
            data = response.read()

            # Exit setup mode
            conn = http.client.HTTPConnection(self.host, timeout=self.timeout)
            conn.request("POST", "", paramsExit, headers)
            response = conn.getresponse()
            data = response.read()
            # print(data, "Exit")

            #TODO: error checking
        except Exception as e:
            self.error.emit(str(e))
        else:
            self.data_ready.emit(self.responses)

