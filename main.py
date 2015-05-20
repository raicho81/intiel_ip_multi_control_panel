# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow
from logindialog import LoginDialog


def main(argv):
    app = QApplication(argv)

    loginDlg = LoginDialog()
    loginDlg.show()

    # w = MainWindow(None, 'Admin')
    # w.show()

    # t = test()
    # t.setModal(True)
    # t.show()

    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)
    # params = urllib.parse.urlencode({'PSW': 'Exit'})
    # headers = {"Content-type": "application/x-www-form-urlencoded",
    #            "Accept": "text/plain"}
    #
    # # Try to make a request to the controller
    # conn = http.client.HTTPConnection('83.228.50.143:88', timeout=10)
    # conn.request("POST", "", params, headers)
    # response = conn.getresponse()
    #
    # # print(response.status, response.reason)
    # # print("Before response read Thread with id = " +
    # #       str(int(QtCore.QThread.currentThreadId())))
    #
    # data = response.read()
    # pprint(data)