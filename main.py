# -*- coding: UTF-8 -*-
__author__ = 'YMM'

import sys
from ui import *

class Main(object):
    def main(self):
        app = QtGui.QApplication(sys.argv)
        mainWindow = QtGui.QMainWindow()
        ui = Ui_Form()
        ui.setupUi(mainWindow)
        mainWindow.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    obj = Main()
    obj.main()