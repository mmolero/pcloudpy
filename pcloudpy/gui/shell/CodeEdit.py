"""
A basic example that show you how to create a basic python code editor widget,
from scratch.

Editor features:
    - syntax highlighting
    - code completion (using jedi)
    - code folding
    - auto indentation
    - auto complete
    - comments mode (ctrl+/)
    - calltips mode
    - linters (pyflakes and pep8) modes + display panel
    - line number panel
    - builtin search and replace panel
"""
import logging
logging.basicConfig()

import sys
from pyqode.qt import QtWidgets
from pyqode.python.backend import server
from pyqode.core import api, modes, panels
from pyqode.python import modes as pymodes, panels as pypanels, widgets

from PySide.QtGui import *
from PySide.QtCore import *

from .. import resources_rc
from ..utils.qhelpers import *


class CodeEdit(QWidget):
    def __init__(self, parent=None, dir_path=None):
        super(CodeEdit, self).__init__(parent)

        self.dir_path = dir_path

        layout = QVBoxLayout()

        self.toolbar = QToolBar()
        file_open_action = createAction(self, "&Open Script (.py)", self.file_open)
        file_open_action.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))

        file_save_action = createAction(self, "&Save Script (.py)", self.file_save)
        file_save_action.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))

        file_run_action = createAction(self, "&Run Script (.py)", self.file_run)
        file_run_action.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))

        self.toolbar.addAction(file_open_action)
        self.toolbar.addAction(file_save_action)
        self.toolbar.addAction(file_run_action)

        self.python_editor = MyPythonCodeEdit()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.python_editor)

        self.setLayout(layout)

    codeRequested = Signal(str)

    def file_run(self):
        pass
        #self.codeRequested.emit(self.python_editor.document().toPlainText())


    def file_open(self):
        filters = "*.py"
        filename, _ = QFileDialog.getOpenFileName(self, "Open Script (.py)", self.dir_path, filters)
        if filename:
            self.python_editor.file.open(filename)

    def file_save(self):
        filters = "*.py"
        filename, _ = QFileDialog.getSaveFileName(self, "Save Script (.py)", self.dir_path, filters)
        if filename:
            self.python_editor.file.save(filename)




class MyPythonCodeEdit(widgets.PyCodeEditBase):
    def __init__(self):
        super(MyPythonCodeEdit, self).__init__()

        # starts the default pyqode.python server (which enable the jedi code
        # completion worker).
        #Now it does not work,  why?????
        if hasattr(sys, 'frozen'):
            self.backend.start(server.__file__, interpreter="python")
        else:
            self.backend.start(server.__file__)


        # some other modes/panels require the analyser mode, the best is to
        # install it first
        #self.modes.append(pymodes.DocumentAnalyserMode())

        #--- core panels
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        # add a context menu separator between editor's
        # builtin action and the python specific actions
        self.add_separator()

        #--- python specific panels
        self.panels.append(pypanels.QuickDocPanel(), api.Panel.Position.BOTTOM)

        #--- core modes
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.ExtendedSelectionMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.SmartBackSpaceMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.ZoomMode())

        #---  python specific modes
        self.modes.append(pymodes.CommentsMode())
        self.modes.append(pymodes.CalltipsMode())
        self.modes.append(pymodes.FrostedCheckerMode())
        self.modes.append(pymodes.PEP8CheckerMode())
        self.modes.append(pymodes.PyAutoCompleteMode())
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.PyIndenterMode())


"""
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
editor = MyPythonCodeEdit()
editor.file.open(__file__)
window.setCentralWidget(editor)
window.show()
app.exec_()
"""