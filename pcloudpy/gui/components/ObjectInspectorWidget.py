#Author: Miguel Molero <miguel.molero@gmail.com>

from PySide.QtCore import *
from PySide.QtGui import *

class ObjectInspectorWidget(QWidget):
    def __init__(self, parent = None):
        super(ObjectInspectorWidget, self).__init__(parent)

        layout = QVBoxLayout()

        self.tab = QTabWidget()
        self.properties_tree = QTreeWidget()
        self.properties_tree.setHeaderLabels(["",""])
        self.properties_tree.setAlternatingRowColors(True)
        self.properties_tree.setColumnCount(2)
        self.properties_tree.header().resizeSection(0, 200)

        self.tab.addTab(self.properties_tree, "Properties")

        layout.addWidget(self.tab)
        self.setLayout(layout)

        self.setGeometry(0,0,100, 400)

    def update(self, props):

        self.properties_tree.clear()
        data_tree = QTreeWidgetItem(self.properties_tree)
        data_tree.setText(0,"Data")
        #data_tree.setFont(0,QFont(c.FONT_NAME, c.FONT_SIZE_1, QFont.Bold))

        labels = props.keys()
        values = props.values()
        self.populateTree(data_tree, labels, values)

    def populateTree(self, parent,labels,values):
        for i,j in zip(labels,values):
            if j is  None:
                continue
            item = QTreeWidgetItem(parent)
            item.setText(0,i)
            #item.setFont(0,QFont(c.FONT_NAME, c.FONT_SIZE_2, QFont.Normal))
            if isinstance(j,bool):
                if j is True:
                    item.setText(1, c.MARK)
                else:
                    item.setText(1, c.CROSS)
            else:
                item.setText(1,str(j))

            #item.setFont(1,QFont(c.FONT_NAME, c.FONT_SIZE_3, QFont.Normal))
        self.properties_tree.expandItem(parent)