#Author: Miguel Molero <miguel.molero@gmail.com>

from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal as Signal

from pcloudpy.gui.utils.qhelpers import *


class StandardItem(QStandardItem):
    def __init__(self, *args, **kwargs):
        super(StandardItem, self).__init__(*args, **kwargs)

        self._current_view = None
        self._layer = None

    def set_current_view(self, view):
        self._current_view = view

    def get_current_view(self):
        return self._current_view

    def set_layer(self, layer):
        self._layer = layer

    def get_layer(self):
        return self._layer

class DatasetsWidget(QWidget):
    def __init__(self, parent = None):
        super(DatasetsWidget, self).__init__(parent)

        self._index = None
        self._enable_filter = False
        self.current_item = None
        layout = QVBoxLayout()
        self.tree = QTreeView()

        self.tree.setStyleSheet("""
            QTreeView::indicator:unchecked {image: url(:/pqEyeballd16.png);}
            QTreeView::indicator:checked {image: url(:/pqEyeball16.png);}""")

        self.tree.setHeaderHidden(True)

        layout.addWidget(self.tree)
        self.setLayout(layout)

        self.tree.clicked.connect(self.clickedItem)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.treeContextMenu)

        self.clone_dataset_action = QAction(QIcon(":/clone.png"), "Clone Dataset", self)
        self.clone_dataset_action.setStatusTip("Clone Dataset")
        self.clone_dataset_action.setToolTip("Clone Dataset")
        self.clone_dataset_action.triggered.connect(self.clone_dataset)

        self.delete_dataset_action = QAction(QIcon(":/trash_24.png"), "Delete Dataset", self)
        self.delete_dataset_action.setStatusTip("Delete Dataset")
        self.delete_dataset_action.setToolTip("Delete Dataset")
        self.delete_dataset_action.triggered.connect( self.delete_dataset)

        self.apply_filter_action = QAction("Apply Filter to Dataset", self)
        self.apply_filter_action.setStatusTip("Apply Filter to Dataset")
        self.apply_filter_action.setToolTip("Apply Filter to Dataset")
        self.apply_filter_action.triggered.connect(self.apply_filter)

    #Own Signals
    currentItemChanged = Signal(int)
    itemDeleted = Signal(int)
    itemCloneRequested = Signal(int)
    filterRequested = Signal(int)

    def init_tree(self, model):
        self.tree.setModel(model)

    def set_enable_filter(self):
        self._enable_filter = True

    def treeContextMenu(self, pos):
        self._index = self.tree.indexAt(pos)
        if self._index.row()>0:
            menu = QMenu()
            addActions(menu, self.delete_dataset_action)
            addActions(menu, self.clone_dataset_action)
            menu.addSeparator()
            if self._enable_filter:
                addActions(menu, self.apply_filter_action)
            menu.exec_(self.tree.mapToGlobal(pos))

    def clickedItem(self, index):
        if index.row()>0:
            self.current_item = index.model().itemFromIndex(index)
            self.currentItemChanged.emit(index.row()-1)

    def add_dataset(self, layer, view):

        model = self.tree.model()
        root = model.invisibleRootItem()

        item = StandardItem(layer.get_name())
        item.setIcon(QIcon(":/Toolbox-50.png"))

        item.set_current_view(view)
        item.set_layer(layer=layer)

        item.setCheckable(True)
        item.setCheckState(Qt.Checked)
        root.appendRow(item)

    def delete_dataset(self):
        if self._index.row()>0:
            self.current_item = self._index.model().itemFromIndex(self._index)
            model = self.tree.model()
            model.removeRow(self._index.row(), self._index.parent())
            self.itemDeleted.emit(self._index.row()-1)

    def clone_dataset(self):
        if self._index.row()>0:
            self.current_item = self._index.model().itemFromIndex(self._index)
            self.itemCloneRequested.emit(self._index.row()-1)

    def apply_filter(self):
         if self._index.row()>0:
            self.current_item = self._index.model().itemFromIndex(self._index)
            self.filterRequested.emit(self._index.row()-1)