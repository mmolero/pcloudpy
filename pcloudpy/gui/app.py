#Author: Miguel Molero <miguel.molero@gmail.com>

import sys
from PySide.QtGui import *
from PySide.QtCore import *
from matplotlib import rcParams
rcParams['backend.qt4']='PySide'
import time
import resources_rc

def run():
    app = QApplication(sys.argv)
    app.setOrganizationName("pcloudpy")
    app.setApplicationName("pcloudpy")
    app.setWindowIcon(QIcon(":/pcloudpy.png"))

    splash_pix = QPixmap(":/pcloudpy-name.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    from MainWindow import MainWindow
    app.processEvents()

    win = MainWindow()
    win.show()
    splash.finish(win)
    app.exec_()


if __name__ == "__main__":
    run()