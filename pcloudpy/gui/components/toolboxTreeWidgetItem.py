#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide.QtCore import *
from PySide.QtGui import *

class ToolBoxTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None,  type=QTreeWidgetItem.UserType + 2):
        super(ToolBoxTreeWidgetItem, self).__init__(parent, type)

        self.setIcon(0,QIcon(":/Toolbox-50.png"))
        self._objectName = None
        self._metadata = None

    def setText(self, column, text):
        super(ToolBoxTreeWidgetItem, self).setText(column, text)
        self.setObjectName(text.replace(" ","-"))

    def setMetadata(self, metadata):
        self._metadata = metadata

    def metadata(self):
        return self._metadata


    def setObjectName(self, name):
        self._objectName = name

    def objectName(self):
        return self._objectName
