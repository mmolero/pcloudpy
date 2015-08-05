#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide.QtCore import *
from PySide.QtGui import *

class ToolboxStandardItem(QStandardItem):
    def __init__(self, *args, **kwargs):
        super(ToolboxStandardItem, self).__init__(*args, **kwargs)

        self._metadata = None
        self.setFlags(self.flags() & ~Qt.ItemIsEditable)
        self.setIcon(QIcon(":/Toolbox-50.png"))
        self._objectName = None
        self._metadata = None

    def setText(self, text):
        super(ToolboxStandardItem, self).setText(text)
        self.setObjectName(text.replace(" ","-"))

    def setMetadata(self, metadata):
        self._metadata = metadata

    def metadata(self):
        return self._metadata

    def setObjectName(self, name):
        self._objectName = name

    def objectName(self):
        return self._objectName

