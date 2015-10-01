#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide.QtCore import *
from PySide.QtGui import *

from ..resources_rc import *
from toolboxTreeWidgetItem import ToolBoxTreeWidgetItem
from toolboxStandardItem import ToolboxStandardItem


class ToolBoxesWidget(QWidget):
    def __init__(self, parent = None):
        super(ToolBoxesWidget, self).__init__(parent)

        self._current_item = None

        layout = QVBoxLayout()
        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setObjectName("Toolbox-Tree")
        layout.addWidget(self.tree)
        self.setLayout(layout)

        self.tree.clicked.connect(self.click_item)

    currentItemClicked = Signal()
    currentItemSelected = Signal()

    def init_tree(self, data):

        model = QStandardItemModel()
        root = model.invisibleRootItem()

        for key in data.keys():
            item = QStandardItem(key)
            item.setIcon(QIcon(":/toolbox-icon.png"))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            root.appendRow(item)

            for child in data[key]:
                item_child = ToolboxStandardItem()
                item_child.setText(child)
                print child
                d = data[key][child]
                item_child.setEnabled(int(d['enabled']))
                item_child.setMetadata(d)
                item.appendRow(item_child)

        self.tree.setModel(model)

        self.connect(self.tree.selectionModel(), SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.select_item)


    def get_current_item(self):
        if self._current_item:
            return self._current_item

    def click_item(self, index):
        self._current_item = index.model().itemFromIndex(index)
        if isinstance(self._current_item, ToolboxStandardItem):
            if self._current_item.isEnabled():
                self.currentItemClicked.emit()

    def select_item(self, new_item, _):
        items = new_item.indexes()
        if len(items)!=0:
            index = new_item.indexes()[0]
            #self.click_item(index)
            self._current_item = index.model().itemFromIndex(index)
            if isinstance(self._current_item, ToolboxStandardItem):
                if self._current_item.isEnabled():
                    self.currentItemSelected.emit()







