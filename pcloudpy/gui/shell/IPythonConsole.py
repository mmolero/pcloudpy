from PySide import QtGui, QtCore

def new_load_qt(api_options):
    from PySide import QtCore, QtGui, QtSvg
    return QtCore, QtGui, QtSvg, 'pyside'

from IPython.external import  qt_loaders
qt_loaders.load_qt = new_load_qt


from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
from IPython.qt.inprocess import QtInProcessKernelManager
from IPython.lib import guisupport


class EmbedIPython(RichIPythonWidget):
    """
    Based on:
    http://stackoverflow.com/questions/11513132/embedding-ipython-qt-console-in-a-pyqt-application
    """

    def __init__(self, **kwarg):
        super(RichIPythonWidget, self).__init__()
        self.app = app = guisupport.get_app_qt4()
        self.kernel_manager = QtInProcessKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel = self.kernel_manager.kernel
        self.kernel.gui = 'qt4'
        self.kernel.shell.push(kwarg)
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

    def get_kernel_shell(self):
        return self.kernel_manager.kernel.shell

    def get_kernel_shell_user(self):
        return self.kernel_manager.kernel.shell.user_ns


class IPythonConsole(QtGui.QMainWindow):

    def __init__(self, parent=None, App=None):
        super(IPythonConsole, self).__init__(parent)
        self.App = App
        self.console = EmbedIPython(App=self.App)
        self.console.kernel.shell.run_cell('%pylab qt')
        self.console.kernel.shell.run_cell("import numpy as np")
        self.console.kernel.shell.run_cell("from matplotlib import rcParams")
        self.console.kernel.shell.run_cell("rcParams['backend.qt4']='PySide'")
        self.console.kernel.shell.run_cell("import matplotlib.pyplot as plt")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.console)

        b = QtGui.QWidget()
        b.setLayout(vbox)
        self.setCentralWidget(b)

    def execute_code(self, text):
        self.console.execute(text)
        #self.console.kernel.shell.run_cell(text)

