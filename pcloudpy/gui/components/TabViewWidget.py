

from PyQt5.QtCore import  *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal as Signal


class TabBarPlus(QTabBar):
    """Tab bar that has a plus button floating to the right of the tabs."""

    plusClicked = Signal()

    def __init__(self):
        super(TabBarPlus, self).__init__()

        # Plus Button
        self.plusButton = QPushButton("+")
        self.plusButton.setParent(self)
        self.plusButton.setMaximumSize(30, 25) # Small Fixed size
        self.plusButton.setMinimumSize(30, 25) # Small Fixed size
        self.plusButton.clicked.connect(self.plusClicked.emit)
        self.movePlusButton() # Move to the correct location

    def sizeHint(self):
        """Return the size of the TabBar with increased width for the plus button."""
        sizeHint = QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QSize(width+30, height)

    def resizeEvent(self, event):
        """Resize the widget and make sure the plus button is in the correct location."""
        super(TabBarPlus, self).resizeEvent(event)
        self.movePlusButton()

    def tabLayoutChange(self):
        """This virtual handler is called whenever the tab layout changes.
        If anything changes make sure the plus button is in the correct location.
        """
        super(TabBarPlus, self).tabLayoutChange()

        self.movePlusButton()
    # end tabLayoutChange

    def movePlusButton(self):
        """Move the plus button to the correct location."""
        # Find the width of all of the tabs
        size = 0
        for i in range(self.count()):
            size += self.tabRect(i).width()

        # Set the plus button location in a visible area
        h = self.geometry().top()
        w = self.width()
        if size > w: # Show just to the left of the scroll buttons
            self.plusButton.move(w-54, h)
        else:
            self.plusButton.move(size, h)

class TabViewWidget(QTabWidget):

    def __init__(self, parent = None):
        super(TabViewWidget, self).__init__(parent)

        # Tab Bar
        self.tab = TabBarPlus()
        self.setTabBar(self.tab)

        # Properties
        self.setMovable(True)
        self.setTabsClosable(True)

        self.tabCloseRequested.connect(self.remove_tab)

    tabDeleted = Signal(int)

    def remove_tab(self, index):
        if index !=0:
            widget = self.widget(index)
            super(TabViewWidget, self).removeTab(index)
            del widget


