"""
Template MainWindowBase.py
"""
#Author: Miguel Molero <miguel.molero@gmail.com>


import sys
import os
os.environ['QT_API'] = 'pyside'

from PySide.QtCore import *
from PySide.QtGui import *
import markdown2
import yaml
import pprint

#own components
import resources_rc
from graphics.QVTKWidget import QVTKWidget

from AppObject import AppObject
from pcloudpy.gui.utils.qhelpers import *

from components.ViewWidget import ViewWidget
from components.TabViewWidget import TabViewWidget
from components.ToolboxesWidget import ToolBoxesWidget
from components.DatasetsWidget import DatasetsWidget
from components.ObjectInspectorWidget import ObjectInspectorWidget
from components.FilterWidget import FilterWidget

#from shell.PythonConsole import PythonConsole
from shell.IPythonConsole import IPythonConsole
from shell.CodeEdit import CodeEdit

NAME = "pcloudpy"


class Info(object):
    version = "0.10"
    date = "05-08-2015"

class MainWindowBase(QMainWindow):
    """
    Base Class for the MainWindow Object. This class should inherit its attributes and methods to a MainWindow Class
    """
    def __init__(self, parent = None):
        super(MainWindowBase, self).__init__(parent)

        self.setLocale((QLocale(QLocale.English, QLocale.UnitedStates)))

        self._software_name = NAME

        self.App = AppObject()

        self.init()
        self.create_menus()
        self.create_toolbars()
        self.setup_docks()
        self.setup_graphicsview()
        self.setup_statusbar()
        self.setup_connections()
        self.init_settings()

        self.init_toolboxes()

        QTimer.singleShot(0,self.load_initial_file)

    @property
    def software_name(self):
        return self._software_name

    @software_name.setter
    def software_name(self, name):
        self._software_name = name

    def init(self):

        self.Info = Info()

        self.dirty = False
        self.reset = False
        self.filename = None
        self.recent_files = []
        self.dir_path = os.getcwd()

        self.setGeometry(100,100,900,600)
        self.setMinimumSize(400,400)
        self.setMaximumSize(2000,1500)
        self.setWindowFlags(self.windowFlags())
        self.setWindowTitle(self.software_name)

        #Put here your init code

    def set_title(self, fname=None):
        title = os.path.basename(fname)
        self.setWindowTitle("%s:%s"%(self.softwareName,title))

    def load_initial_file(self):
        settings = QSettings()
        fname = unicode(settings.value("LastFile"))
        if fname and QFile.exists(fname):
            self.load_file(fname)

    def load_file(self, fname=None):

        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = unicode(action.data())
                if not self.ok_to_Continue():
                    return
            else:
                return

        if fname:
            self.filename = None
            self.add_recent_file(fname)
            self.filename = fname
            self.dirty = False
            self.set_title(fname)

            #Add More actions
            #
            #

    def add_recent_file(self, fname):

        if fname is None:
            return
        if not self.recentFiles.count(fname):
            self.recentFiles.insert(0,fname)
            while len(self.recentFiles)>9:
                self.recentFiles.pop()

    def create_menus(self):

        self.menubar = self.menuBar()

        file_menu = self.menubar.addMenu(self.tr('&File'))
        help_menu = self.menubar.addMenu(self.tr("&Help"))

        file_open_action = createAction(self, "&Open Dataset[s]", self.file_open)
        file_open_action.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        help_about_action = createAction(self, "&About %s"%self._software_name, self.help_about, icon="pcloudpy.png")

        addActions(file_menu, (file_open_action,))
        addActions(help_menu, (help_about_action,))

    def setup_connections(self):

        #Main Window
        self.workspaceLineEdit.textEdited.connect(self.editWorkSpace)

        self.code_edit.codeRequested.connect(self.console_widget.execute_code)

    def setup_docks(self):

        #Toolboxes
        self.toolboxes_widget = ToolBoxesWidget()
        self.toolboxes_dockwidget = QDockWidget(self.tr("Toolboxes"))
        self.toolboxes_dockwidget.setObjectName("Toolboxes-Dock")
        self.toolboxes_dockwidget.setWidget(self.toolboxes_widget)
        self.toolboxes_dockwidget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.toolboxes_dockwidget)

        #Datasets
        self.datasets_widget = DatasetsWidget()
        self.datasets_dockwidget = QDockWidget(self.tr("Datasets"))
        self.datasets_dockwidget.setObjectName("Datasets-Dock")
        self.datasets_dockwidget.setWidget(self.datasets_widget)
        self.datasets_dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.datasets_dockwidget)

        #Object Inspector
        self.object_inspector_widget = ObjectInspectorWidget()
        self.object_inspector_dockwidget = QDockWidget(self.tr("Object Inspector"))
        self.object_inspector_dockwidget.setObjectName("Object-Inspector-Dock")
        self.object_inspector_dockwidget.setWidget(self.object_inspector_widget)
        self.object_inspector_dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.object_inspector_dockwidget)

        #Filter Widget
        self.filter_widget = FilterWidget()
        self.filter_widget_dockwidget = QDockWidget(self.tr("Filter Setup"))
        self.filter_widget_dockwidget.setObjectName("Filter-Setup-Dock")
        self.filter_widget_dockwidget.setWidget(self.filter_widget)
        self.filter_widget_dockwidget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filter_widget_dockwidget)

        #Console
        self.tab_console = QTabWidget()
        self.console_widget = IPythonConsole(self, self.App)
        self.code_edit = CodeEdit()

        self.tab_console.addTab(self.console_widget, "Console")
        self.tab_console.addTab(self.code_edit, "Editor")

        self.console_widget_dockwidget = QDockWidget(self.tr("IPython"))
        self.console_widget_dockwidget.setObjectName("Console-Dock")
        self.console_widget_dockwidget.setWidget(self.tab_console)
        self.console_widget_dockwidget.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_widget_dockwidget)


    def create_toolbars(self):

        self.actionOpen_WorkSpace = createAction(self,"Set Workspace", self.setWorkSpace)
        self.actionOpen_WorkSpace.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))

        self.first_toolbar = QToolBar(self)
        self.first_toolbar.setObjectName("Workspace Toolbar")
        self.first_toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)

        self.workspaceLineEdit = QLineEdit()
        self.workspaceLineEdit.setMinimumWidth(200)

        self.first_toolbar.addWidget(QLabel("Workspace Dir"))
        self.first_toolbar.addWidget(self.workspaceLineEdit)
        self.first_toolbar.addAction(self.actionOpen_WorkSpace)

        self.addToolBar(self.first_toolbar)

        if self.dir_path is None:
            self.dir_path = os.getcwd()
        self.workspaceLineEdit.setText(self.dir_path)
        self.addToolBarBreak()

    def setup_graphicsview(self):

        self.tab_view = TabViewWidget(self)
        view = ViewWidget()
        self.tab_view.addTab(view, "Layout #1")
        self.setCentralWidget(self.tab_view)
        #
        self.datasets_widget.init_tree(view.model)

    def setup_statusbar(self):
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)

        #Add more action

    def setWorkSpace(self):
        dir = QFileDialog.getExistingDirectory(None, self.tr("Set Workspace directory"), self.dir_path, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if dir:
            self.dir_path = dir
            self.workspaceLineEdit.setText(self.dir_path)

    def editWorkSpace(self):
        if os.path.isdir(self.workspaceLineEdit.text()):
            self.dir_path = self.workspaceLineEdit.text()

    def init_settings(self):

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles")
        size = settings.value("MainWindow/Size",QSize(900,600))
        position = settings.value("MainWindow/Position",QPoint(50,50))
        self.restoreState(settings.value("MainWindow/State"))
        self.dir_path = settings.value("DirPath")
        #Retrives more options

        if self.recentFiles is None:
            self.recentFiles = []

        self.resize(size)
        self.move(position)

        #Add more actions
        self.workspaceLineEdit.setText(self.dir_path)

    def reset_settings(self):

        settings = QSettings()
        settings.clear()
        self.reset = True
        self.close()

    def init_toolboxes(self):

        if hasattr(sys, 'frozen'):
            #http://stackoverflow.com/questions/14750997/load-txt-file-from-resources-in-python
            fd = QFile(":/config_toolboxes.yaml")
            if fd.open(QIODevice.ReadOnly | QFile.Text):
                text = QTextStream(fd).readAll()
                fd.close()
            data = yaml.load(text)
        else:
            path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(path,'resources\conf\config_toolboxes.yaml'), 'r') as f:
                # use safe_load instead load
                data = yaml.safe_load(f)

        #pp = pprint.PrettyPrinter()
        #pp.pprint(data)
        self.toolboxes_widget.init_tree(data)


    def ok_to_continue(self):

        if self.dirty:
            reply = QMessageBox.question(self,
                                        "%s - Unsaved Changes"%self.softwareName,
                                        "Save unsaved changes?",
                                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)

            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.file_save()

        return True

    def file_new(self):
        pass

    def file_open(self):
        pass

    def file_saveAs(self):
        pass

    def file_save(self):
        pass

    def help_about(self):

        message = read_file(":/about.md").format(self.Info.version, self.Info.date)
        html = markdown2.markdown(str(message))

        QMessageBox.about(self, "About %s"%NAME, html)

    def closeEvent(self, event):

        if self.reset:
            return

        if self.ok_to_continue():
            settings = QSettings()
            filename = self.filename if self.filename is not None else None
            settings.setValue("LastFile", filename)
            recentFiles = self.recentFiles if self.recentFiles else None
            settings.setValue("RecentFiles", recentFiles)
            settings.setValue("MainWindow/Size",	 self.size())
            settings.setValue("MainWindow/Position", self.pos())
            settings.setValue("MainWindow/State",	 self.saveState())
            settings.setValue("DirPath", self.dir_path)
            #Set more options

        else:
            event.ignore()




if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindowBase()
    win.show()
    app.exec_()


