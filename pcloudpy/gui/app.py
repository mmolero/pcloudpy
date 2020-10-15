#Author: Miguel Molero <miguel.molero@gmail.com>

import sys
from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import time
from pcloudpy.gui.resources_rc import *

sys.setrecursionlimit(140000)

def run():
    app = QApplication(sys.argv)
    app.setOrganizationName("pcloudpy")
    app.setApplicationName("pcloudpy")
    app.setWindowIcon(QIcon(":/pcloudpy.png"))

    splash_pix = QPixmap(":/pcloudpy-name.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    from pcloudpy.gui.MainWindow import MainWindow
    app.processEvents()

    win = MainWindow()
    win.show()
    splash.finish(win)
    app.exec_()


if __name__ == "__main__":
    run()